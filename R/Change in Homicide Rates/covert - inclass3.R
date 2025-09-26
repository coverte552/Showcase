# Clear the environment
rm(list = ls())

# Install required packages if not already installed
#install.packages(c("usmap", "usmapdata", "ggplot2", "tidyverse", "sf", "gridExtra"))

# Load necessary libraries
library(usmap)       # U.S. map visualization
library(usmapdata)   # State centroid labels
library(ggplot2)     # Data visualization
library(tidyverse)   # Data manipulation
library(sf)          # Handling spatial data
library(gridExtra)   # For arranging plots and tables together

# Load the dataset
data <- read_csv("homicide_rates.csv")

# Convert 'RATE' to numeric, replacing NAs with 0
data$RATE <- as.numeric(data$RATE)
data$RATE[is.na(data$RATE)] <- 0

# Calculate the average RATE from 2019 to 2021
avg_rate <- data %>%
  filter(YEAR >= 2019 & YEAR <= 2021) %>%
  group_by(STATE) %>%
  summarise(AVG_RATE_2019_2021 = mean(RATE, na.rm = TRUE))

# Extract 2022 rates
rate_2022 <- data %>%
  filter(YEAR == 2022) %>%
  select(STATE, RATE_2022 = RATE)

# Merge the data frames and calculate the difference
final_data <- merge(avg_rate, rate_2022, by = "STATE", all = TRUE)
final_data$RATE_DIFF <- final_data$RATE_2022 - final_data$AVG_RATE_2019_2021

# Replace any remaining NA values with 0
final_data[is.na(final_data)] <- 0

# Categorize rate changes into discrete tiers with arrows
final_data <- final_data %>%
  mutate(
    ARROW = case_when(
      RATE_DIFF == 0 ~ "-",
      RATE_DIFF > 0 & RATE_DIFF <= 1 ~ "↑",
      RATE_DIFF > 1 & RATE_DIFF <= 2 ~ "↑↑",
      RATE_DIFF > 2 ~ "↑↑↑",
      RATE_DIFF < 0 & RATE_DIFF >= -1 ~ "↓",
      RATE_DIFF < -1 & RATE_DIFF >= -2 ~ "↓↓",
      RATE_DIFF < -2 ~ "↓↓↓"
    ),
    LABEL = paste(STATE, ARROW)  # Combine state abbreviation with arrows
  )

# List of small states that have their own table (added Hawaii)
small_states <- c("VT", "NH", "CT", "RI", "NJ", "DE", "MD", "MA", "ME", "HI")

# Create a table of small states with their labels
small_states_table <- final_data %>%
  filter(STATE %in% small_states) %>%
  select(STATE, ARROW) %>%
  arrange(STATE)

# Remove small states from the map dataset (but keep their colors)
final_data <- final_data %>%
  mutate(LABEL = ifelse(STATE %in% small_states, "", LABEL))  # Remove labels for small states

# Convert state abbreviations to full state names for mapping
final_data <- final_data %>%
  mutate(STATE_FULL = state.name[match(STATE, state.abb)])

# Remove any NA values (from mismatches)
final_data <- na.omit(final_data)

# Get centroid coordinates for states
centroid_labels <- usmapdata::centroid_labels("states")

# Extract numeric coordinates from `geom` column
centroid_labels$x <- st_coordinates(centroid_labels$geom)[,1]  # Longitude
centroid_labels$y <- st_coordinates(centroid_labels$geom)[,2]  # Latitude

# Convert state names to lowercase for merging
final_data <- final_data %>%
  mutate(STATE_FULL = tolower(STATE_FULL))

centroid_labels <- centroid_labels %>%
  mutate(STATE_FULL = tolower(full))

# Merge homicide data with centroid coordinates
final_data <- final_data %>%
  inner_join(centroid_labels, by = "STATE_FULL")

# Create a legend manually with both numbers and arrows
legend_labels <- c("-3 ↓↓↓", "-2 ↓↓", "-1 ↓", " 0 -", " 1 ↑", " 2 ↑↑", " 3 ↑↑↑")

# Create the US Map plot with colors for all states
map_plot <- plot_usmap(data = final_data, values = "RATE_DIFF", regions = "states") +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0, 
                       name = "Rate Change", breaks = c(-3, -2, -1, 0, 1, 2, 3),
                       labels = legend_labels) +
  labs(title = "Change in Homicide Rates (2022 vs. 2019-2021 Avg)",
       subtitle = "Red = Increase, Blue = Decrease. Arrows indicate magnitude.") +
  theme(legend.position = "right") +  # Keeps the legend on the right
  
  # Add state abbreviation + categorized arrows at centroids (excluding small states)
  geom_text(data = final_data, aes(x = x, y = y, label = LABEL), 
            size = 3.5, color = "black", fontface = "bold")  # Proper centroid alignment

# Create a table of small states without rate difference
table_plot <- tableGrob(small_states_table, rows = NULL)

# Arrange map and table side by side
grid.arrange(map_plot, table_plot, ncol = 2, widths = c(3, 1))
