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
d.raw <- read.csv("data/clean_data_full2.csv", stringsAsFactors = FALSE)
if (!inGlobalEnv("d.raw")) {
  ptm <- proc.time()
  path <- "data/reviews_store/"
  files <- list.files(path)
  d.raw <- data.frame()
  for (f in files) {
    d <- read.csv(paste0(path, f))
    d.raw <- rbind(d.raw, d)
  }
  proc.time() - ptm  
}

##########
########## Append feature cols
##########

## ABV
## ---
ABV_pattern <- "([0-9]{1,2}(?:\\.[0-9])?)%"
stri_match_all_regex(as.character(d.raw$beer_ABV[1000]), ABV_pattern)[[1]][1,2]
d.raw <- d.raw %>%
  rowwise %>%
  mutate(beer_ABV_num = as.numeric(stri_match_all_regex(as.character(beer_ABV), ABV_pattern)[[1]][1,2]))

## Filter patterns 
## ---------------
must_contain_chars_pattern <- '^[^a-zA-Z]*$'

## General filtering and mutation
## -------------------------------
d.clean <- d.raw
if (!inGlobalEnv("d.clean") & inGlobalEnv("d.raw")) {
  d.clean <- d.raw %>%
    filter(review_blob != '',
           !grepl(must_contain_chars_pattern, review_blob),
           review_blob != ' ',
           !is.nan(review_blob),
           !is.na(review_blob),
           !is.na(review_palate_score),
           !is.na(review_aroma_score),
           !is.na(review_taste_score),
           !is.na(review_appearance_score),
           !is.na(review_overall_score)) %>%
    ## Append quantile column
    mutate(review_blob_lower = tolower(review_blob),
           ## User expertise quartile
           user_experience_quartile = ifelse(user_num_ratings < 18, 'Q1',
                                             ifelse(user_num_ratings >= 18 & user_num_ratings < 72, 'Q2',
                                                    ifelse(user_num_ratings >= 72 & user_num_ratings < 278, 'Q3', 'Q4'))),
           user_experience1000 = ifelse(user_num_ratings >= 1000, "Over1000", "Under999"),
           user_experience500 = ifelse(user_num_ratings >= 500, "Over500", "Under499"),
           ## Review specific features
           num_tokens = get_num_tokens(review_blob_lower),
           num_types = get_num_types(review_blob_lower),
           type_token_ratio = num_types / num_tokens,
           corrected_ttr = quanteda::lexdiv(quanteda::dfm(review_blob), measure = "CTTR"),
           num_syllables = get_num_syllables(review_blob_lower),
           readability_score = quanteda::readability(review_blob, measure = "Flesch.Kincaid"))
  d.clean <- d.clean %>%
    rowwise %>%
    mutate(num_first_person_singular_pnouns = get_num_first_person_pnouns(review_blob_lower))
  
  write.csv(d.clean, "data/clean_data_full2.csv")
}

######
###### User level analysis
######
d.user_info <- d.clean %>%
  filter(user_num_ratings >= 10) %>%
  group_by(user_name) %>%
  summarise(user_num_ratings = mean(user_num_ratings),
            review_sims = review_similarities(review_blob_lower),
            avg_num_tokens = mean(num_tokens),
            avg_num_types = mean(num_types),
            avg_lediv_type_token = mean(type_token_ratio),
            avg_num_syllables = mean(num_syllables),
            avg_cttr = mean(corrected_ttr),
            avg_readability = mean(readability_score),
            avg_fpspns = mean(num_first_person_singular_pnouns))


## Plotting first person singular pronouns
ggplot(aes(x = log(num_ratings), y = avg_fpspns)) +
  geom_point(alpha = 0.2) +
  geom_smooth(method = "lm")



d.user_info %>%
  gather(type, value, c(review_sims, avg_num_tokens, avg_num_types, avg_type_token, avg_cttr, avg_readability)) %>%
  ggplot(aes(x = log(user_num_ratings), y = value)) +
  geom_point() +
  geom_smooth(method = "lm") +
  facet_wrap(~type, scales = "free_y")

#####
##### write data
#####
#write.csv(d.clean, "data/clean_data_full.csv")

## Append quantile column
##


#####
##### Cleaned data - remove missing reviews
#####



## other filtering


d.clean <- d.raw

# which(sapply(d.clean$review_blob, FUN = function(review) !grepl(pattern, review)))


bad1 <- '                             ???????? ??????? ????, ?? ? ??????? ???????? ? ??????. ????? ???? ???? ????????? ?????'
bad2 <- '&# '
good1 <- 'ben'
good2 <- 'A%'
grepl(pattern, good2)

d.clean$review_blob[49]
#####
##### Prelim summary stats
#####
print_review_summary(d.clean)
print_ids_summary(good_ids)
review_summary_plots(d.clean)
review_aspect_correlations(d.raw)
missing_data_summary(d.raw)

########
######## Quartiles
########
stats::quantile(d.clean$user_num_ratings)
d.quantiles <- d.clean %>%
  mutate(quantile = ifelse(user_num_ratings < 18, 'first',
                           ifelse(user_num_ratings < 72, 'second',
                                  ifelse(user_num_ratings < 278, 'third', 'fourth'))))

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


# d.mini <- d.raw[1:100,]
# 
# d.mini %>%
#   group_by(user_name) %>%
#   summarise(n())
# 
# str(d.mini)
# 
# 
# user_Borr <- d.mini %>% filter(user_name == "Borr")
# reviews <- user_Borr$review_blob
# num_reviews <- length(reviews)
# curr_review_index <- sample(1:num_reviews, 1)
# other_reviews <- seq(1, num_reviews)[-curr_review_index]
# mean(sapply(other_reviews, FUN = function(index) {
#   self_similarity(reviews[curr_review_index], reviews[index])
# }))
# 
# user_7Aaron <- d.mini %>% filter(user_name == "7Aaron")
# reviews <- user_7Aaron$review_blob
# num_reviews <- length(reviews)
# curr_review_index <- sample(1:num_reviews, 1)
# other_reviews <- seq(1, num_reviews)[-curr_review_index]
# mean(sapply(other_reviews, FUN = function(index) {
#   self_similarity(reviews[curr_review_index], reviews[index])
# }))

## Analysis
## Data
d.self_sim <- d.raw %>%
  filter(user_num_ratings >= 10) %>%
  group_by(user_name) %>%
  summarise(user_num_ratings = mean(user_num_ratings),
            review_sims = review_similarities(review_blob)) %>%
  mutate(user_name = as.factor(user_name))

## Plot
ggplot(d.self_sim, aes(x = log(user_num_ratings), y = review_sims)) +
  geom_point() +
  geom_smooth(method = "lm")

## LM
lm <- lm(review_sims ~ user_num_ratings, data = d.self_sim)
summary(lm)


#####
##### First person singular pronouns
#####
d.mini <- d.clean[1:100,]

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

practice <- d.mini %>%
  rowwise %>%
  mutate(num_fppns = get_num_first_person_pnouns(review_blob_lower)) %>%
  as.data.frame()

sum(stringr::str_count(d.mini$review_blob_lower[1], pattern = fpsp))

practice$num_fppns
pract





fpsp <- c('(^i\\s|\\si\\.?\\s|\\si\\.?$)',
          '(^we\\s|\\swe\\.?\\s|\\swe\\.?$)',
          '(^me\\s|\\sme\\.?\\s|\\sme\\.?$)',
          '(^us\\s|\\sus\\.?\\s|\\sus\\.?$)',
          '(^ours?\\s|\\sours?\\.?\\s|\\sours?\\.?$)',
          '(^my\\s|\\smy\\.?\\s|\\smy\\.?$)',
          '(^mine\\s|\\smine\\.?\\s|\\smine\\.?$)')

reviews <- d.clean$review_blob[1:10]

stringr::str_count(tolower(reviews[1]), pattern = fpsp)
?stringr::str_count


