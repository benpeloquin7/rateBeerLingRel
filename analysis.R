rm(list = ls())

library(ggplot2)
library(tidyr)
library(dplyr)
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
d <- read.csv("data/good.csv")
names(d) <- c("userID", "n")
numReviews <- sum(d$n)
numReviewers <- nrow(d)
avgReviewsPer <- numReviews / numReviewers
printSummary <- function() {
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
printSummary()


####
#### run sampling
####
print_review_summary <- function() {
  path <- "data/reviews_store/"
  files <- list.files(path)
  d.raw <- data.frame()
  for (f in files){
    d <- read.csv(paste0(path, f))
    d.raw <- rbind(d.raw, d)
  }
  n_users <- length(unique(d.raw$user_id))
  cat(paste0("Number of unique users: ", n_users), "\n")
  n_reviews <- nrow(d.raw)
  cat(paste0("Number of reviews: ", n_reviews))
  
  d.raw[match(unique(d.raw$user_id), d.raw$user_id),] %>%
    select(user_id, user_num_ratings) %>%
    group_by(user_num_ratings) %>%
    summarise(count = n()) %>%
    ggplot(aes(x = log(user_num_ratings), y = count)) +
    geom_bar(stat = "identity")
}
print_review_summary()
