rm(list = ls())

library(ggplot2)
library(tidyr)
library(dplyr)
library(stringr)
setwd("/Users/benpeloquin/Desktop/Spring2016/CS224U/rateBeerLingRel")

####
#### Number of scrape
####
timeNeededInSeconds <- function(nIDs, pauseTime, pauseValue) {
  nBreaks <- nIDs / pauseValue
  breakSeconds <- nBreaks * pauseTime
  nonBreakSeconds <- (nIDs - nBreaks) * 5
  breakSeconds + nonBreakSeconds
}
timeNeededInSeconds(5000, 40, 20) / 60 / 60 ## These are good settings

####
#### Sample Ids
####
print_ids_summary <- function() {
  d <- read.csv("data/good.csv")
  names(d) <- c("userID", "n")
  numReviews <- sum(d$n)
  numReviewers <- nrow(d)
  avgReviewsPer <- numReviews / numReviewers
  
  cat(paste("numReviews:", numReviews, sep = "\t"), "\n")
  cat(paste("numReviewers:", numReviewers, sep = "\t"), "\n")
  cat(paste("avgReviewsPer:", avgReviewsPer, sep = "\t"), "\n")
  cat(paste("one review reviewers:", d %>%
              filter(n == 1) %>% nrow(), sep = "\t"), "\n")
  cat(paste("50+ review reviewers:", d %>%
              filter(n == 50) %>% nrow(), sep = "\t"))
  d %>%
    group_by(n) %>%
    summarise(counts = n()) %>%
    ggplot(aes(x = n, y = counts)) +
    geom_bar(stat = "identity")
}
print_ids_summary()


####
#### run sampling
####
path <- "data/reviews_store/"
files <- list.files(path)
d.raw <- data.frame()
for (f in files){
  d <- read.csv(paste0(path, f))
  d.raw <- rbind(d.raw, d)
}
print_review_summary <- function(d.raw) {
  
  n_users <- length(unique(d.raw$user_id))
  cat(paste0("Number of unique users: ", n_users), "\n")
  n_reviews <- nrow(d.raw)
  cat(paste0("Number of reviews: ", n_reviews))
  
  d.raw[match(unique(d.raw$user_id), d.raw$user_id),] %>%
    select(user_id, user_num_ratings) %>%
    group_by(user_num_ratings) %>%
    summarise(count = n()) %>%
    ggplot(aes(x = log(user_num_ratings), y = count)) +
      geom_point(alpha = 0.5)
      # geom_bar(stat = "identity")
}
print_review_summary(d.raw)

review_summary_plots <- function(d.raw) {
  d.raw %>%
    gather(type, score,
           c(review_palate_score,
             review_taste_score,
             review_aroma_score,
             review_avg_score,
             review_appearance_score)) %>%
    ggplot(aes(score)) +
    geom_bar() +
    facet_wrap(~type, scales = "free")
}
review_summary_plots(d.raw)

## Review aspect correlations
d.raw %>%
  select(review_palate_score,
         review_taste_score,
         review_aroma_score,
         review_avg_score,
         review_appearance_score) %>%
  as.matrix() %>%
  cor(use = "pairwise.complete.obs")


missing_data_summary <- function(d.raw) {
  cat(paste0("-------------- REVIEW ----------------"), "\n")
  cat(paste0("===================================="), "\n")
  
  miss_rev_text <- nrow(d.raw[which(is.na(d.raw$review_blob)), ])
  cat(paste0("Missing review text: ", miss_rev_text), "\n")
  
  miss_rev_overall_score <- nrow(d.raw[which(is.na(d.raw$review_overall_score)), ])
  cat(paste0("Missing review overall score: ", miss_rev_overall_score), "\n")
  
  miss_rev_avg_score <- nrow(d.raw[which(is.na(d.raw$review_blob)), ])
  cat(paste0("Missing review avg score: ", miss_avg_score), "\n")
  
  miss_rev_taste_score <- nrow(d.raw[which(is.na(d.raw$review_taste_score)), ])
  cat(paste0("Missing review taste score: ", miss_rev_taste_score), "\n")
  
  miss_rev_aroma_score <- nrow(d.raw[which(is.na(d.raw$review_aroma_score)), ])
  cat(paste0("Missing review aroma score: ", miss_rev_aroma_score), "\n")
  
  miss_rev_palate_score <- nrow(d.raw[which(is.na(d.raw$review_palate_score)), ])
  cat(paste0("Missing review palate score: ", miss_rev_palate_score), "\n")
  
  miss_rev_appearance_score <- nrow(d.raw[which(is.na(d.raw$review_appearance_score)), ])
  cat(paste0("Missing review appearance score: ", miss_rev_appearance_score), "\n")
  
  
  cat(paste0("-------------- BEER ----------------"), "\n")
  cat(paste0("===================================="), "\n")
  
  miss_beer_weighted_avg_score <- nrow(d.raw[which(is.na(d.raw$beer_weighted_avg_score)), ])
  cat(paste0("Missing beer weighted avg score: ", miss_beer_weighted_avg_score), "\n")
  
  miss_beer_num_ratings <- nrow(d.raw[which(is.na(d.raw$beer_num_ratings)), ])
  cat(paste0("Missing beer num ratings: ", miss_beer_num_ratings), "\n")
  
  miss_beer_global_score <- nrow(d.raw[which(is.na(d.raw$beer_global_score)), ])
  cat(paste0("Missing beer global score: ", miss_beer_global_score), "\n")
  
  miss_beer_global_style_score <- nrow(d.raw[which(is.na(d.raw$beer_global_style_score)), ])
  cat(paste0("Missing beer global style score: ", miss_beer_global_style_score), "\n")
  
  miss_beer_ABV <- nrow(d.raw[which(is.na(d.raw$beer_ABV)), ])
  cat(paste0("Missing beer ABV: ", miss_beer_ABV), "\n")
  
  miss_beer_style <- nrow(d.raw[which(is.na(d.raw$beer_style)), ])
  cat(paste0("Missing beer style: ", miss_beer_style), "\n")
  
  miss_beer_location <- nrow(d.raw[which(is.na(d.raw$beer_location)), ])
  cat(paste0("Missing beer location: ", miss_beer_location), "\n")
  
  miss_beer_num_calories <- nrow(d.raw[which(is.na(d.raw$beer_num_calories)), ])
  cat(paste0("Missing beer num calories: ", miss_beer_num_calories), "\n")
  
  miss_beer_brewer_name <- nrow(d.raw[which(is.na(d.raw$beer_brewer_name)), ])
  cat(paste0("Missing beer brewer name: ", miss_beer_brewer_name), "\n")
  
  cat(paste0("-------------- USER ----------------"), "\n")
  cat(paste0("===================================="), "\n")
  
  miss_user_num_ratings <- nrow(d.raw[which(is.na(d.raw$user_num_ratings)), ])
  cat(paste0("Missing user num ratings: ", miss_user_num_ratings), "\n")
  
  miss_user_num_places_rated <- nrow(d.raw[which(is.na(d.raw$user_num_places_rated)), ])
  cat(paste0("Missing user num places rated: ", miss_user_num_places_rated), "\n")
  
  miss_user_location <- nrow(d.raw[which(is.na(d.raw$user_location)), ])
  cat(paste0("Missing user location: ", miss_user_location), "\n")
  
  miss_user_num_friends <- nrow(d.raw[which(is.na(d.raw$user_num_friends)), ])
  cat(paste0("Missing user num countries rated: ", miss_user_num_friends), "\n")
  
  miss_user_num_following <- nrow(d.raw[which(is.na(d.raw$user_num_following)), ])
  cat(paste0("Missing user num following: ", miss_user_num_following), "\n")
  
  miss_user_name <- nrow(d.raw[which(is.na(d.raw$user_name)), ])
  cat(paste0("Missing user name: ", miss_user_name), "\n")
  
  miss_user_num_breweries_rated <- nrow(d.raw[which(is.na(d.raw$user_num_breweries_rated)), ])
  cat(paste0("Missing user num breweries rated: ", miss_user_num_breweries_rated), "\n")
  
  miss_user_num_countries_rated <- nrow(d.raw[which(is.na(d.raw$user_num_countries_rated)), ])
  cat(paste0("Missing user num countries rated: ", miss_user_num_countries_rated), "\n")
}
missing_data_summary(d.raw)



### Quick work to take care of missing overall scores (20pt scores)
urls <- d.raw[which(is.na(d.raw$review_overall_score)), ]$user_url
pattern <- '([0-9]{3,6})'
missing_overall_score_ids <- unique(sapply(urls, function(url) {
  str_match(url, pattern)[, 2]  
}))

# write.csv(missing_overall_score_ids, file = "missingOverallScores.csv")

