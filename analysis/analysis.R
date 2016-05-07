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

#####
##### Prelim summary stats
#####
print_review_summary(d.raw)
print_ids_summary(good_ids)
review_summary_plots(d.raw)
review_aspect_correlations(d.raw)
missing_data_summary(d.raw)

#####
##### Cleaned data - remove missing reviews
#####
d.clean <- d.raw %>%
  filter(!is.na(review_blob),
         !is.na(review_palate_score),
         !is.na(review_aroma_score),
         !is.na(review_taste_score),
         !is.na(review_appearance_score),
         !is.na(review_overall_score))
# write.csv(d.clean, "data/clean_data.csv")

## beer ABV plot
beer_abv_plot(d.raw)

## beer styles
length(unique(d.raw$beer_style))
d.raw %>%
  group_by(beer_style) %>%
  summarise(count = n()) %>%
  arrange(-count)

## individual beers
length(unique(d.raw$beer_name))

## Number of users with over n reviews
d.raw %>%
  mutate(expert = user_num_ratings >= 50) %>%
  group_by(expert) %>%
  summarise(count = n())

## How does the number of review predict your predictability
d.raw %>%
  filter(user_num_ratings >= 50) %>%
  group_by(user_id) %>%
  mutate(review_overall_score = review_overall_score / 4,
         review_taste_score = review_taste_score / 2,
         review_aroma_score = review_aroma_score / 2) %>%
  summarise(avgOverallScore = mean(review_overall_score),
            varOverallScore = var(review_overall_score),
            avgTasteScore = mean(review_taste_score),
            varTasteScore = var(review_taste_score),
            avgAromaScore = mean(review_aroma_score),
            varAromaScore = var(review_aroma_score),
            avgAppearanceScore = mean(review_appearance_score),
            varAppearanceScore = var(review_appearance_score),
            avgPalateScore = mean(review_palate_score),
            varPalateScore = var(review_palate_score),
            numReviews = unique(user_num_ratings),
            overall_distance = abs(abs(avgTasteScore - avgAromaScore) - abs(avgAppearanceScore - avgPalateScore))) %>%
  gather(type, value, c(varTasteScore, varAromaScore, varAppearanceScore, varPalateScore)) %>%
  ggplot(aes(x = log(numReviews), y = value, col = type)) +
    geom_point(alpha = 0.5) +
    facet_wrap(~type)+
    geom_smooth(method = "lm")








### Quick work to take care of missing overall scores (20pt scores)
urls <- d.raw[which(is.na(d.raw$beer_num_calories)), ]$user_url
pattern <- '([0-9]{3,6})'
missing_overall_score_ids <- unique(sapply(urls, function(url) {
  str_match(url, pattern)[, 2]  
}))
d.raw[which(is.na(d.raw$beer_num_calories)),][2,]
# write.csv(missing_overall_score_ids, file = "missingOverallScores.csv")




