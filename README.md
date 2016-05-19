# RateBeer.com data collection and modeling

## What's this project about?

- Web crawler for RateBeer.com
- Task of aspect prediction from review data
- Task of experience level prediction from review data

### Web crawler for RateBeer.com

Code included in the `data_collection` dir provides basic web scraping functionality. We collect:

- dim 1
- dim 2 ...

The data collected in this project includes novel user-level dimensions, compared to previous studies using RateBeer.com data (see Leskovec). In particular, we collect:

- user total number of reviews
- user total number of styles
- user total number of places rated ...

### Aspect ratings prediction task

We examine 3 different models with varying feature fns to predict ratings for 

- Overall
- Taste
- Aroma
- Palate
- Appearance

Models examined

- Linear Regression
- Lasso
- Random Forest
- Gradient Boosting method

#### Experience classification task

We examine two methods for 