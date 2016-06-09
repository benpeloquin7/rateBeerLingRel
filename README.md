# RateBeer.com data collection and modeling

## Studying the impact of domain expertise on language use

How does the amount we know about a topic impact the language we use to describe it? And, given the way we someone talks about a topic, can we recover the amount they know about it? Previous studies indicate that the accumulation of domain specific experiences can influence the way we talk about those experiences. Those previous studies, however, employed different operational definitinos of 'expertise' or 'experience level'. In the current study, we use a data set of over 50 thousand reviews from RateBeer.com, operationalizing 'experience level' via number of reviews written. We find that specific language features differ based on a reviewers experience level and also that we can predict a users' level of experience based on language data alone.

## Part I: Data collection

- Scraped 50K reviews from the site RateBeer.com using a user-centric sampling (generating random user-id's and constraining the number of reviews from individual users to 50 max).
- See scraping code (https://github.com/benpeloquin7/rateBeerLingRel/tree/master/data_collection)

## Part II: Statistical language analysis
- We assessed 7 hypothese direcly or indirectly indicated by previous work.
- See analysis () 

## Part III: Classifying user experience level

- Compared 2 standard ML classifiers (Naive Bayes, Random Forest) and 2 language model based classifiers (unigram Laplace, trigram Stupid-backoff) to a baseline
