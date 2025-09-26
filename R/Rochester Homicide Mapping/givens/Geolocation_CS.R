setwd("C:/Users/kims2/OneDrive - Alfred State College/Desktop/25SR") # your R-working location

################################################################################
# Crime Mapping (When we know the latitude and longitude of homicide scene)
################################################################################
# Install necessary libraries if not already installed
install.packages(c("leaflet", "readxl"))



###############################################################################
# 2025 Homicide  Mapping (Rochester, NY)
################################################################################
# Load necessary libraries
library(leaflet)
library(readxl)

# Load the data
# data should be in your working directory
# Make sure the Excel file is not open in another application.

file_path <- "RPD Homicide 2025.xlsx" 

homicide_data <- read_excel(file_path, sheet = "Homicides in RochesterNY_0")

# Extract latitude and longitude
# y is typically the latitude (North-South)
# x is typically the longitude (East-West)

latitudes <- homicide_data$y
longitudes <- homicide_data$x

# Create the pop-up text as a character vector
# Popup will display case number, date, and status when you click map markers.
# paste() is used to concatenate text.
# <br> adds line breaks in the pop-up window.

popup_text <- paste("Case Number:", homicide_data$CaseNumber, 
                    "<br>Date:", homicide_data$OccurredDate,
                    "<br>Status:", homicide_data$CaseStatus)


# use 'leaflet' to create an interactive map:
leaflet() %>%
  addTiles() %>%
  addMarkers(lng = longitudes, lat = latitudes, 
             popup = popup_text) %>%
  setView(lng = mean(longitudes, na.rm = TRUE), 
          lat = mean(latitudes, na.rm = TRUE), 
          zoom = 12)


#====================================================================
# Minimal interactive map- 2025 Homicide (Rochester, NY)
#====================================================================

# Load necessary libraries
library(leaflet)
library(readxl)

# Load the data
# Make sure the file is in your working directory or provide the full path

file_path <- "RPD Homicide 2025.xlsx"  
homicide_data <- read_excel(file_path, sheet = "Homicides in RochesterNY_0")

# Extract latitude and longitude
latitudes <- homicide_data$y
longitudes <- homicide_data$x

# Create the pop-up text as a character vector
popup_text <- paste("Case Number:", homicide_data$CaseNumber, 
                    "<br>Date:", homicide_data$OccurredDate,
                    "<br>Status:", homicide_data$CaseStatus)

# Create the leaflet map with a Minimalist Base Map
leaflet() %>%
  addProviderTiles(providers$CartoDB.Positron) %>%  # Minimalist base map
  addMarkers(lng = longitudes, 
             lat = latitudes, 
             popup = popup_text) %>%
  setView(lng = mean(longitudes, na.rm = TRUE), 
          lat = mean(latitudes, na.rm = TRUE), 
          zoom = 12)


###############################################################################
###############################################################################
# 2024-2025 Homicide  Mapping (Rochester, NY)
################################################################################
###############################################################################

# Load necessary libraries
library(leaflet)
library(readxl)

# Load the data
file_path <- "RPD Homicide victim_2425.xlsx"
homicide_data <- read_excel(file_path, sheet = "Homicides in RochesterNY_0")

head(homicide_data)
# Extract latitude and longitude
latitudes <- homicide_data$y
longitudes <- homicide_data$x

# Assign colors based on OccurredYear
colors <- ifelse(homicide_data$OccurredYear == 2024, "red", "blue")

# Create the pop-up text as a character vector
# Add weapon info

popup_text <- paste("Case Number:", homicide_data$CaseNumber, 
                    "<br>Occured:", homicide_data$OccurredDate,
                    "<br>Status:", homicide_data$CaseStatus,
                    "<br>Weapon:",homicide_data$WeaponCategory )

# Create the leaflet map
leaflet() %>%
  addTiles() %>%
  addCircleMarkers(lng = longitudes, lat = latitudes, 
                   popup = popup_text,
                   color = colors,
                   radius = 5, 
                   fillOpacity = 0.7) %>%
  setView(lng = mean(longitudes, na.rm = TRUE), 
          lat = mean(latitudes, na.rm = TRUE), 
          zoom = 12)


##====================================================================
#  Change Base Map: minimal look
##====================================================================

# Load necessary libraries
library(leaflet)
library(readxl)

# Load the data
file_path <- "RPD Homicide victim_2425.xlsx"  # Ensure the file is in your working directory or provide the full path
homicide_data <- read_excel(file_path, sheet = "Homicides in RochesterNY_0")

# Extract latitude and longitude
latitudes <- homicide_data$y
longitudes <- homicide_data$x

# Assign colors based on OccurredYear
colors <- ifelse(homicide_data$OccurredYear == 2024, "red", "blue")

# Create the pop-up text as a character vector
# Including Case Number, Occurred Date, Status, and Weapon Category
popup_text <- paste("Case Number:", homicide_data$CaseNumber, 
                    "<br>Occurred:", homicide_data$OccurredDate,
                    "<br>Status:", homicide_data$CaseStatus,
                    "<br>Weapon:", homicide_data$WeaponCategory)

# Create the leaflet map with a Minimalist Base Map
leaflet() %>%
  addProviderTiles(providers$CartoDB.Positron) %>%  # Minimalist base map
  addCircleMarkers(lng = longitudes, 
                   lat = latitudes, 
                   popup = popup_text,
                   color = colors,
                   radius = 5, 
                   fillOpacity = 0.7) %>%
  setView(lng = mean(longitudes, na.rm = TRUE), 
          lat = mean(latitudes, na.rm = TRUE), 
          zoom = 12)


##====================================================================
#  Cluster Markers: For dense areas
##====================================================================

# Load necessary libraries
library(leaflet)
library(readxl)

# Load the data
file_path <- "RPD Homicide victim_2425.xlsx"  # Ensure the file is in your working directory or provide the full path
homicide_data <- read_excel(file_path, sheet = "Homicides in RochesterNY_0")

# Extract latitude and longitude
latitudes <- homicide_data$y
longitudes <- homicide_data$x

# Assign colors based on OccurredYear
colors <- ifelse(homicide_data$OccurredYear == 2024, "red", "blue")

# Create the pop-up text as a character vector
# Including Case Number, Occurred Date, Status, and Weapon Category
popup_text <- paste("Case Number:", homicide_data$CaseNumber, 
                    "<br>Occurred:", homicide_data$OccurredDate,
                    "<br>Status:", homicide_data$CaseStatus,
                    "<br>Weapon:", homicide_data$WeaponCategory)

# Create the leaflet map with Cluster Markers and Minimalist Base Map
leaflet() %>%
  addProviderTiles(providers$CartoDB.Positron) %>%  # Minimalist base map
  addCircleMarkers(lng = longitudes, 
                   lat = latitudes, 
                   popup = popup_text,
                   color = colors,
                   radius = 5, 
                   fillOpacity = 0.7,
                   clusterOptions = markerClusterOptions()) %>%
  setView(lng = mean(longitudes, na.rm = TRUE), 
          lat = mean(latitudes, na.rm = TRUE), 
          zoom = 12)



