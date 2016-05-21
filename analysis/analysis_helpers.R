library(ggplot2)
library(tidyr)
library(dplyr)
library(stringr)

#####
##### inGlobalEnv()
##### -------------
##### boolean object presence in global env
#####
inGlobalEnv <- function(item) {
  item %in% ls(envir = .GlobalEnv)
}

#####################################################################
##                 Language analysis helpers
#####################################################################
## review_similarities
## ------------------
review_similarities <- function(user_reviews) {
  ## Note dfm default params
  ## toLower = TRUE,
  ## removeNumbers = TRUE, removePunct = TRUE, removeSeparators = TRUE,
  ## removeTwitter = FALSE, stem = FALSE
  ## language = "english"
  dfm <- quanteda::dfm(user_reviews)
  mean(unlist(quanteda::similarity(dfm, margin = "documents", method = "cosine")))
}

## get_num_tokens
## --------------
get_num_tokens <- function(review) {
  quanteda::ntoken(tolower(review),
                   removeNumbers = TRUE,
                   removePunct = TRUE,
                   removeSeparators = TRUE)
}
## get_num_types
## -------------
get_num_types <- function(review) {
  quanteda::ntype(tolower(review),
                  removeNumbers = TRUE,
                  removePunct = TRUE,
                  removeSeparators = TRUE)
}
## get_num_syllables
## --------------
get_num_syllables <- function(review) {
  quanteda::syllables(tolower(review))
}
## get_num_first_person_pnouns()
## ------------------------------
get_num_first_person_pnouns <- function(review) {
  fpsp <- c("(^i(?:'m|m)?\\s|\\si(?:'m|m)?\\.?\\s|\\si(?:'m|m)?\\.?$)",
            "(^we(?:'re)?\\s|\\swe(?:'re)?\\.?\\s|\\swe(?:'re)?\\.?$)",
            "(^me\\s|\\sme\\.?\\s|\\sme\\.?$)",
            "(^us\\s|\\sus\\.?\\s|\\sus\\.?$)",
            "(^ours?\\s|\\sours?\\.?\\s|\\sours?\\.?$)",
            "(^my\\s|\\smy\\.?\\s|\\smy\\.?$)",
            "(^mine\\s|\\smine\\.?\\s|\\smine\\.?$)")
  sum(stringr::str_count(review, pattern = fpsp))
}



#####################################################################
##                     Scraping helpers
#####################################################################

####
#### Number of scrape
####
timeNeededInSeconds <- function(nIDs, pauseTime, pauseValue) {
  nBreaks <- nIDs / pauseValue
  breakSeconds <- nBreaks * pauseTime
  nonBreakSeconds <- (nIDs - nBreaks) * 5
  breakSeconds + nonBreakSeconds
}

######
###### print_ids_summary()
###### --------------------
###### print the number of ids and reviews we've scraped
######
print_ids_summary <- function(d) {
  
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

######
###### print_review_summary()
###### summary of reviews data
######
print_review_summary <- function(d.raw) {
  
  n_users <- length(unique(d.raw$user_id))
  cat(paste0("Number of unique users: ", n_users), "\n")
  n_reviews <- nrow(d.raw)
  cat(paste0("Number of reviews: ", n_reviews))
  
  d.raw[match(unique(d.raw$user_id), d.raw$user_id),] %>%
    select(user_id, user_num_ratings) %>%
    group_by(user_num_ratings) %>%
    summarise(count = n()) %>%
    ggplot(aes(x = log(count), y = log(user_num_ratings))) +
      ylab("Log count number of reviews made") +
      xlab("Log count number of users") +
      ylim(0, 10) +
      xlim(0, 10) +
      # scale_x_reverse() +
      geom_point(alpha = 0.25, size = 3, col = "blue")
      # geom_bar(stat = "identity")
}

######
###### review_summary_plots()
###### plots of review aspects
######
review_summary_plots <- function(d.raw) {
  d.raw %>%
    mutate(review_taste_score = review_taste_score / 2,
           review_aroma_score = review_aroma_score / 2,
           review_overall_score = review_overall_score / 4) %>%
    gather(type, score,
           c(review_palate_score,
             review_taste_score,
             review_aroma_score,
             review_avg_score,
             review_appearance_score,
             review_overall_score)) %>%
    ggplot(aes(score)) +
    geom_bar() +
    facet_wrap(~type, scales = "free")
  
  cat(paste0("-------------- Aspects summaries ----------------"), "\n")
  
  summary_stas <- d.raw %>%
    mutate(review_taste_score = review_taste_score / 2,
           review_aroma_score = review_aroma_score / 2,
           review_overall_score = review_overall_score / 4) %>%
    gather(type, score,
           c(review_palate_score,
             review_taste_score,
             review_aroma_score,
             review_avg_score,
             review_appearance_score,
             review_overall_score)) %>%
    group_by(type) %>%
    summarise(avg = mean(score),
              var = var(score))
    
  print(summary_stas)
}

######
###### review_aspect_correlations()
###### correlations between reviews aspects
######
review_aspect_correlations <- function(d.raw) {
  d.raw %>%
    select(review_palate_score,
           review_taste_score,
           review_aroma_score,
           review_avg_score,
           review_appearance_score) %>%
    as.matrix() %>%
    cor(use = "pairwise.complete.obs")
}

######
###### beer_summary_plots()
###### summary of beers
######
beer_abv_plot <- function(d.raw) {
  d.raw %>%
    ggplot(aes(x = beer_ABV_num)) +
      geom_histogram(binwidth = 1)
}
  
######
###### missing_data_summary()
###### summary of missing data
######
missing_data_summary <- function(d.raw) {
  cat(paste0("-------------- REVIEW ----------------"), "\n")
  cat(paste0("===================================="), "\n")
  
  miss_rev_text <- nrow(d.raw[which(is.na(d.raw$review_blob)), ])
  cat(paste0("Missing review text: ", miss_rev_text), "\n")
  
  miss_rev_overall_score <- nrow(d.raw[which(is.na(d.raw$review_overall_score)), ])
  cat(paste0("Missing review overall score: ", miss_rev_overall_score), "\n")
  
  miss_rev_avg_score <- nrow(d.raw[which(is.na(d.raw$review_blob)), ])
  cat(paste0("Missing review avg score: ", miss_rev_avg_score), "\n")
  
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