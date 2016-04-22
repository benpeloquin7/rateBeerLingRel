rm(list = ls())

library(ggplot2)
library(tidyr)
library(dplyr)
setwd("/Users/benpeloquin/Desktop/Spring2016/CS224U/rateBeerLingRel")

#### Number of scrape
timeNeededInSeconds <- function(nIDs, pauseTime, pauseValue) {
  nBreaks <- nIDs / pauseValue
  breakSeconds <- nBreaks * pauseTime
  nonBreakSeconds <- (nIDs - nBreaks) * 5
  breakSeconds + nonBreakSeconds
}
timeNeededInSeconds(5000, 50, 15) / 60 / 60 ## These are good settings

## Data
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


