# Studying the impact of domain expertise on language use

How does the amount we know about a topic impact the language we use to describe it? And, given the way someone talks about a topic, can we recover the amount they know about it? Previous studies indicate that the accumulation of domain specific experiences can influence the way we talk about those experiences. Those previous studies, however, employed different operational definitions of `expertise` or `experience-level`. In the current study, we use a dataset of over 50 thousand reviews from RateBeer.com, operationalizing `experience-level` via number of reviews written. We find that specific language features differ based on a reviewer's experience-level and also that we can predict a user's experience-level based on language data alone.

## Part I: Data collection

- Scraped 50K reviews from the site RateBeer.com using user-centric sampling (generating random user-id's and constraining the number of reviews from individual users to 50 max).
- See scraping code (https://github.com/benpeloquin7/rateBeerLingRel/tree/master/data_collection).

## Part II: Statistical language analysis
- We assessed 7 hypotheses direcly or indirectly indicated by previous work. See paper for citations (https://github.com/benpeloquin7/rateBeerLingRel/blob/master/paper/domain_expt_lang_use.pdf).
- Statistical analysis markdown (https://github.com/benpeloquin7/rateBeerLingRel/blob/master/analysis/expertise_linguistic_analysis.Rmd).

## Part III: Classifying user experience-level
- Compared two standard machine learning classifiers (Naive Bayes, Random Forest) and two language model (LM) based classifiers (unigram Laplace, trigram Stupid-backoff, which are trained on sub-group data and make classifications based on LM's perplexity) to a baseline model.
