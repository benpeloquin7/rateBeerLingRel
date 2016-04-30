rm(list = ls())

library(ggplot2)
library(tidyr)
library(dplyr)
library(stringr)
library(stringi)
library(textcat) ## for detecting lang, but doesn't work well
setwd("/Users/benpeloquin/Desktop/Spring2016/CS224U/rateBeerLingRel")
source("analysis/analysis_helpers.R")


####
#### Read in data
####
path <- "data/reviews_store/"
files <- list.files(path)
d.raw <- data.frame()
for (f in files) {
  d <- read.csv(paste0(path, f))
  d.raw <- rbind(d.raw, d)
}

#####
##### Data processing
#####

## Get ABV
ABV_pattern <- "([0-9]{1,2}(?:\\.[0-9])?)%"
stri_match_all_regex(as.character(d.raw$beer_ABV[1000]), ABV_pattern)[[1]][1,2]
d.raw <- d.raw %>%
  rowwise %>%
  mutate(beer_ABV_num = as.numeric(stri_match_all_regex(as.character(beer_ABV), ABV_pattern)[[1]][1,2]))

## ID analysis
# good_ids <- read.csv("data/good.csv")
# timeNeededInSeconds(5000, 40, 20) / 60 / 60 ## These are good settings

print_ids_summary(good_ids)
print_review_summary(d.raw)
review_summary_plots(d.raw)
review_aspect_correlations(d.raw)
missing_data_summary(d.raw)


beer_abv_plot(d.raw)
ggplot(d.raw, aes(x = beer_ABV_num, y = review_avg_score)) +
  geom_point()

## beer styles
length(unique(d.raw$beer_style))
d.raw %>%
  group_by(beer_style) %>%
  summarise(count = n()) %>%
  arrange(-count)

## individual beers
length(unique(d.raw$beer_name))
d.raw %>%
  group_by(beer_name) %>%
  summarise(count = n()) %>%
  arrange(-count)

## Number of users with over n reviews
d.raw %>%
  mutate(expert = user_num_ratings >= 50) %>%
  group_by(expert) %>%
  summarise(count = n())


### Quick work to take care of missing overall scores (20pt scores)
urls <- d.raw[which(is.na(d.raw$beer_num_calories)), ]$user_url
pattern <- '([0-9]{3,6})'
missing_overall_score_ids <- unique(sapply(urls, function(url) {
  str_match(url, pattern)[, 2]  
}))
d.raw[which(is.na(d.raw$beer_num_calories)),][2,]
# write.csv(missing_overall_score_ids, file = "missingOverallScores.csv")


df1 <- d.raw[1:100,]

df1 %>%
  mutate(lang = textcat(review_blob)) %>%
  View()



