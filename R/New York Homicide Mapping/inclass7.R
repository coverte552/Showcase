# Clear memory
rm(list = ls())
gc()

## Load necessary packages
#install.packages("readr")    # For reading CSV files
#install.packages("dplyr")    # For data manipulation
#install.packages("leaflet")  # For interactive maps
#install.packages("lubridate")  # For date handling

library(readr)
library(dplyr)
library(leaflet)
library(lubridate)

# Read and clean Buffalo data
buffalo_df <- read_csv("Buffalo_Homicide_Data.csv", col_types = cols()) %>%
  select(`Case Number`, `Incident Datetime`, City, Latitude, Longitude, neighborhood) %>%
  rename(Neighborhood = neighborhood) %>%
  mutate(
    Latitude = as.numeric(Latitude),
    Longitude = as.numeric(Longitude),
    Year = as.character(year(mdy_hms(`Incident Datetime`)))  # Extract Year for reference
  )

# Read and clean Rochester data
rochester_df <- read_csv("RPD_Homicide_Data.csv", col_types = cols()) %>%
  select(CaseNumber, OccurredDate, Latitude, Longitude, Section) %>%
  rename(`Case Number` = CaseNumber,
         `Incident Datetime` = OccurredDate,
         Neighborhood = Section) %>%
  mutate(
    City = "Rochester",
    Latitude = as.numeric(Latitude),
    Longitude = as.numeric(Longitude),
    Year = as.character(year(mdy_hms(`Incident Datetime`)))  # Extract Year for reference
  )

# Combine datasets
city_data <- bind_rows(buffalo_df, rochester_df)

# Create Leaflet map (No Filtering, Just Clustering)
leaflet(city_data) %>%
  addTiles() %>%
  addCircleMarkers(
    ~Longitude, ~Latitude,
    popup = ~paste0("<b>Case:</b> ", `Case Number`, "<br>",
                    "<b>Date:</b> ", `Incident Datetime`, "<br>",
                    "<b>City:</b> ", City, "<br>",
                    "<b>Neighborhood:</b> ", Neighborhood),
    radius = 4,
    color = "blue",
    fillOpacity = 0.6,
    clusterOptions = markerClusterOptions()  # Enable proper clustering
  )
