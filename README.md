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


## Resources
http://download.springer.com/static/pdf/693/art%253A10.3758%252FBRM.40.4.1065.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.3758%2FBRM.40.4.1065&token2=exp=1463956414~acl=%2Fstatic%2Fpdf%2F693%2Fart%25253A10.3758%25252FBRM.40.4.1065.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.3758%252FBRM.40.4.1065*~hmac=42b31bea7214d65670c61a96a1e18bb19c927158cae8292a459e9f8f26e9d119