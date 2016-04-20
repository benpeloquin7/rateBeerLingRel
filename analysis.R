setwd("/Users/benpeloquin/Desktop/Spring2016/CS224U/rateBeerLingRel")

#### Number of scrape
timeNeededInSeconds <- function(nIDs, pauseTime, pauseValue) {
  nBreaks <- nIDs / pauseValue
  breakSeconds <- nBreaks * pauseTime
  nonBreakSeconds <- (nIDs - nBreaks) * 5
  breakSeconds + nonBreakSeconds
}
timeNeededInSeconds(5000, 50, 30) / 60 / 60 ## These are good settings


d <- read.csv("data/good.csv")
names(d) <- c("userID", "n")
sum(d$n)
nrow(d)
