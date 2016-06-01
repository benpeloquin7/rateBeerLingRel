#############
#############
############# Scikit-learn helpers
#############
#############
import pdb
import pandas as pd
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer

def build_data_set(data, vectorizer = None, aspect_str = "OVERALL"):
    """
    Aspect ratings cols:
        (7)  review_palate_score      -- score_normalizer = 1
        (8)  review_taste_score       -- score_normalizer = 2
        (11) review_aroma_score       -- score_normalizer = 2
        (14) review_avg_score         -- score_normalizer = 1
        (18) review_overall_score     -- score_normalizer = 4
        (20) review_appearance_score  -- score_normalizer = 1
        
    predict_col :: column for aspect we're predicting, current default is column 18 (OVERALL)
    
    """
    
    ## RateBeer scrape data locations
    ## ------------------------------
    REVIEW_BLOB = 24
    ASPECTS = {
        "PALATE"           : [7, 1],
        "TASTE"            : [8, 2],
        "AROMA"            : [11, 2],
        "AVERAGE"          : [14, 1],
        "OVERALL"          : [18, 4],
        "APPEARANCE"       : [20, 1],
        "user_experience"  : [32, None],
        "user_num_ratings" : [10, None]
    }
    assert(aspect_str in ASPECTS)
        
    aspect_column = ASPECTS[aspect_str][0]      ## Get aspect rating column
    aspect_normalizer = ASPECTS[aspect_str][1]  ## Get aspect normalizer
    labels = []                                 ## Ratings
    feat_dicts = []                             ## Features
    raw_examples = []                           ## Review strings
    data_values = data.values                   ## Data from pandas df
    for row in data.values:
        review, score = row[REVIEW_BLOB], row[aspect_column]

        score = float(score) / aspect_normalizer if aspect_str != "user_experience" else score
        score = np.log10(score) if aspect_str != "user_num_ratings" else score

        ## Safety check
        if not isinstance(review, basestring):
            print 'weird review:\t', review
            
        labels.append(score)
        raw_examples.append(review)
        
    # In training, we want a new vectorizer:
    if vectorizer == None:
        vectorizer = DictVectorizer(sparse=True)
        feat_matrix = vectorizer.fit_transform(feat_dicts)
    # In assessment, we featurize using the existing vectorizer:
    else:
        feat_matrix = vectorizer.fit_transform(raw_examples)

    return {'X'            : feat_matrix, 
            'y'            : labels, 
            'vectorizer'   : vectorizer, 
            'raw_examples' : raw_examples,
            'feature_names' : vectorizer.get_feature_names()}