from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


import string
import re

## KEYWORD HANDLING

def preprocessing(train_data):
    ### KEYWORDS

    # handling NaN in keyword
    train_data["keyword"] = train_data["keyword"].fillna("")

    train_data["keyword"] = train_data['keyword'].str.replace("%20", " ")

    # adding hashtags to keywords
    train_data['keyword'] = train_data["keyword"] + train_data["text"].apply(lambda x: " ".join(re.findall("#(\w+)", x)).lower())

    ### TEXT
    train_data['text'] = train_data['text'].apply(lambda x: x.lower())

    #strip data
    train_data['text'] = train_data['text'].str.strip()

    #cleaning urls
    train_data['text'] = train_data['text'].apply(lambda x: re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                                                       '', x))
    #remove emails
    train_data['text'] = train_data['text'].apply(lambda x: re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", x))

    #clean username
    train_data['text'] = train_data['text'].apply(lambda x: re.sub('@[^\s]+','', x))

    #remove digits
    train_data['text'] = train_data['text'].apply(lambda x: ''.join(i for i in x if i not in string.digits))

    #remove punctuations
    train_data['text'] = train_data['text'].apply(lambda x: ''.join(i for i in x if i not in string.punctuation))

    return train_data


def tokenize_text(df, remove_stopwords=False):

    df['Tokenized'] = df['text'].apply(word_tokenize)

    if remove_stopwords==True:
        stop= stopwords.words('english')
        df['Tokenized'].apply(lambda x: [i for i in x if i not in stop])

    return df
#testpr
