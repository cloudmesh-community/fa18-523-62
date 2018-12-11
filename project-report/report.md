# Predict EPL results using Tweets :smiley: fa18-523-62 fa18-523-69

| Manek Bahl, Sohan Udupi Rai
| mbahl@iu.edu, surai@iu.edu
| Indiana University
| hid: fa18-523-62, fa18-523-69
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-523-62/blob/master/project-report/report.md)
| code: [:cloud:](https://github.com/cloudmesh-community/fa18-523-62/tree/master/project-code)

---

**:mortar_board: Learning Objectives**

* Learn about extracting Tweets and storing them on MongoDB
* Run Machine Learning and NLP algorithms on the data to predict soccer results

---

Keywords: Twitter API, MongoDB, Machine Learning, NLP

## Abstract

There are a lot of factors that influence the outcome of a football game. Team
statistics such as recent form, win-loss ratio, goals scored, goals conceded etc
have been proven to be useful in dictating the results of a game. These
statistics can be directly obtained from the Official EPL website, however,
there are certain other factors such as injuries, general mood of the fanbase
and sentiment of the fanbase, preparation by the team etc. which aren't
documented in the official website. Analysis of Twitter data could prove useful
in extracting these undocumented features, using NLP models. In this paper, we
analyze the usefulness of Tweets in predicting the outcomes of games in the
English Premier League. We create three different models to predict the
outcomes, the first using the statistics available from the EPL website, the
second using only the twitter data and the third with combination of both. If
the model improves with the addition of features obtained from the twitter data,
we would be able to prove that Twitter data does increase the predictive power
of the model.

## Introduction

The English Premier League is one of the most famous and competitive football
leagues in the world. The season begins in August and ends in May in which 20
teams compete for the championship. Each team plays each of the other teams
exactly twice, Home and Away, over the course of the season. A win awards the
team with 3 points while a draw earns 1 point and a loss gives 0 points. At the
end of the season, the team with the maximum points is crowned as the champion.

Twitter is a social media website where people express their opinions about a
wide range of topics such as Politics, Sports, Religion, Entertainment etc. It
was launched in 2006 and currently has 335 Million users worldwide. Due to the
large number of users, Twitter has proven to be a reliable source of the general
opinion of the public regarding any matter. When it comes to tweets regarding
the Premier League, Twitter is being used not only by the public, but also by
the players and the club officials. Therefore, we think that tweets could
contain valuable information which could be used to improve the prediction
models.

We are choosing the English Premier League due to its globally widespread
fanbase which is active on Twitter. This provides us with a rich corpus of data
regarding the team which could be used to analyze and interpret the overall fan
sentiment for a team and other factors such as player unavailability, current
coaching style etc. which are subjective and hence not obtainable from any other
statistical sources.

For each team playing in the upcoming weekend fixtures, we are using Twitter
scraping API in Python called Selenium, to monitor and extract all tweets over 
the course of the entire week. This is repeated for first 12 gameweeks, to build 
the corpus of tweets. These tweets are fed to Natural Language Processing tool to
create a feature which serve as the predictor in the dataset. The corresponding
results of the matches will serve as the class labels. With dataset with the 
statistics and tweet feature combined we run machine learning predictive 
algorithms to predict the results of the 13th gameweek.

## Related Work

There were a few papers in which an attempt has been made to predict soccer 
results using machine learning techniques but just using the statistical data. 
However, owing to the intense competition in the English Premier league and the 
unpredictable nature of soccer results a great accuracy was never achieved. In
Timmaraju et al. they used game statistics such as number of goals, shots on 
target, corners etc [@fa-523-62-stanford-timmaraju]. They added another feature 
which was based on the recent form of the team in the last 5 matches. They were 
able to achieve the maximum accuracy of 66%. 

We however, didn't find any other paper which included external feature such as 
tweet sentiment. We are not too concerned about the accuracy of the models, but we 
tried to leverage the usability of tweet data and check if it improves our model 
in any way.

## Implementation

### Data

The tweets were extracted using web scraping tool with Python called Selenium
and were stored in MongoDB over the course of almost 3 months from September 2018
to November 2018. We were able to collect more than 100,000 tweets combined for 
20 premier league teams using the team specific hashtags. Examples of hastags 
used are: #AFCB for Bournemouth, #Arsenalfc and #Gunners for Arsenal, #MANU and 
#RedDevils for Manchester United etc. In total we had 50 hashtags overall for 
different teams. 

The statistical football data for this season was taken from English Football 
Data Website [@fa-523-62-football-data]. The data contains all individual match 
results for this season with number of goals scored by each  team, number of shots, 
number of shots on target, corners etc. The data also  contained win-loss odd 
prediction for each time according to various betting websites. The results were 
given as Home team Win, Away Team Win or Draw.

The above 2 datasets are seperately imported by our main code and the following 
processing is done to get them into the required format:

The tweet text imported from the database (or the CSV file in the case of this 
demo) are fed to the TextBlob method from the python library 'textblob' and the 
'polarity' attribute of the 'sentiment' attribute is extracted to get the overall 
sentiment of each tweet. These individual tweet sentiment scores are then grouped 
and averaged for each team into weekly batches from saturday through friday. We 
now have the average sentiment of tweets for each team leading upto each of 
weekend fixtures. This is added as one of the 'predictors' for the dataset to be 
fed to the machine learning algorithms.

Next, the statstical dataset (along with the outcomes of each match) is manipulated
 using for loops and dictionaries in Python so that the goals, shots, shots on target, 
fouls, corners, yellow cards and red cards are converted to their coresponding 
per match averages prior to the game. The odds data obtained are kept as obtained. 
These per game average values generated along with the odds data serve as the other 
'predictors' in the dataset. 

The outcome of each of the game labelled as 'w' for a win, 'd' for a draw and 'l' 
for a loss act as the 'class label' for the prediction algorithm in the dataset. The 
rows for data corresponding to gameweek 13 is seperated and stripped off the class 
label column, this acts as the test dataset. The rest of he data (including the 
'result' column) acts as the train dataset for the prediction algorithms.

### MongoDB

Developed by MongoDB Inc., MongoDB is a NoSQL Database system which stores data
as documents. The documents are stored in JSON format which means that various
documents can have their own different format and data structure. The structure
of the existing documents as well can be changed later in time. Another
advantage that this structure provides is that, it makes mapping of different
objects in the application code much easier. High availability and horizontal
scaling are in built features of MongoDB due to it being a distributed database.
It was written in C, C++ and Javascript and can be used on various operating
systems such as Windows, iOS, Linux and Solaris. 

However, owing to default security configuration, MongoDB has been rendered to 
a lot of data thefts as it allows full database access to all
[@fa-523-62-wikipedia-mongoDB].  

#### Local Installation

We used the MongoDB Community Edition on Windows and MacOS systems. The below 
steps were followed for MacOS using Homebrew:

Updated the HomeBrew's version by the following shell command
```bash
brew update
```
Then use the below command to install the mongodb binary files
```bash
brew install mongodb
```
To run MongoDB the below command was used
```bash
<path to the binary files>mongod
```
Once MongoDB is up and running we should be able to see the following line in 
the shell or terminal window [@fa-523-62-docs-mongoDB].
```bash
[initandlisten] waiting for connections on port 27017
```

### Tweet Extraction

#### Tweepy and its challenges

Twitter provides dedicated API for developers and researchers to be able to
extract tweets for any given hashtag or for a particular username and perform
various kinds of analysis. For various use cases, Twitter provides different
types of access levels with the business version being called the Enterprise API
which large scale business use for their analysis. To obtain the developers
access, one must own a twitter account and apply for a developer's API access.
The form usually consists of basic user information and justifying the purpose
of obtaining a developer's access for the API. This information is then reviewed
by Twitter and assigns 4 unique keys for each user which are needed to use the
API. The keys consist of consumer key, consumer secret, access token key and
access token secret. Once these are obtained a dedicated python version of
Twitter API called Tweepy can be used.

Tweepy is an easily installable python package which leverages the Twitter API
using Python. Tweepy can be easily installed as other python packages using pip
command in the command line.     
```bash
pip install tweepy
```
The package can then be imported in python IDE and authentication between python
and Twitter API can then be established using the keys obtained earlier.

Tweepy though can be used only to extract tweets only for 7 days. For tweets
before 7 days, Tweepy cannot be used. However, for our project we need tweets
starting from August 10, so using Tweepy is not feasible for our project.

#### Selenium

Since the data we needed from Twitter could not be extracted using official
twitter API due to the 7-day restriction, we had to try another approach. We
scraped data from Twitter using the selenium package in python. Selenium
essentially is a package which is used to automate the interaction of python
with a web browser of our choice.

To use selenium, we needed to install a WebDriver for the specific web browser,
Firefox in our case. The below shell script can be used to install the WebDriver
for Firefox.

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodrive
r-v0.19.1-linux64.tar.gz tar xvfz geckodriver-v0.19.1-linux64.tar.gz mv
geckodriver ~/.local/bin
```

Once the WebDriver is installed, we can install Selenium package just as
installing any other python package.

```bash
pip install selenium
```

Then in the python code, we can just point to the location of the WebDriver to
successfully run selenium and scrape data [@fa-523-62-www-realpython].

```bash
from selenium import webdriver browser = webdriver.Chrome(r'<location of the
WebDriver>)
```

### Natural Language Processing

Natural Language Processing is an integral part of this project as we need to
extract the general sentiment of the team's fans from the tweets they have
posted. There are various tools available that can be integrated with Python
which can be used to provide the overall sentiment of a sentence. One such tool
is TextBlob. It is a python specific library which is built on the existing NLTK
but has a much simpler interface to use and is much faster.

```bash
pip install -U textblob python -m textblob.download_corpora
```

It is adept in performing a lot of NLP tasks such as POS tagging, word
tokenization, Noun Phrase extraction, spelling correction and obviously
sentiment analysis which we are interested in.  Sentiment analysis is the
process of extracting the attitude, mood or the emotion of the writer and
judging whether the sentence written is overall positive, negative or neutral.
The sentiment function gives us the overall sentiment of the sentence in the
range [1,-1], where 1 is the positive sentiment and -1 is the negative
sentiment.

```bash
#Example: 
from textblob import TextBlob 
text = 'Big Data is exciting.' 
blob = TextBlob(text) 
print(blob.sentiment.polarity) 
>> 0.15
```

We use TextBlob on all the tweets captured for all teams and create a new
feature vector which is the averaged sentiment score of all tweets for a team
for a given week [@fa-523-62-www-analyticsvidhya].

### Machine Learning Approaches

Once our data is ready, we needed to feed this data to various machine learning
prediction algorithms to predict the outcome of each match in the test dataset.
Built-in python package Scikit-Learn was used to run these algorithms.

#### Random Forest Classifier

In Random forests, multiple random decision trees are created using only a small
random subset of the features. Samples of the training dataset are taken with
replacement, but the trees are constructed in a way that reduces the correlation
between individual classifiers. Specifically, rather than greedily choosing the
best split point in the construction of the tree, only a random subset of
features is considered for each split. Using Random Forests also removes the
necessity of pruning trees which would otherwise be required to prevent over-
fitting of the model to the training dataset.

There were few parameters that we had to set to achieve best results which are
shown in the snippet below.

```bash
model_RF = RandomForestClassifier(n_estimators=num_trees, max_features=max_features,max_depth=max_depth,class_weight="balanced")
model_RF.fit(X,Y)
y_pred_RF=model_RF.predict(Xtest)
```


#### Logistic Regression

Logistic regression is a classification algorithm used to assign observations to
a discrete set of classes. Unlike linear regression which outputs continuous
numeric values, logistic regression transforms its output using the logistic
sigmoid function. The function maps any real value into another value between 0
and 1. Since this is a 3-class problem, we need to use the multinomial logistic
regression.

#### XGBoost

Boosting is a sequential technique which works on the principle of ensemble. It
combines a set of weak learners and delivers improved prediction accuracy. At
any instant t, the model outcomes are weighed based on the outcomes of previous
instant t-1. The outcomes predicted correctly are given a lower weight and the
ones miss-classified are weighted higher. This technique is followed for a
classification problem while a similar technique is used for regression. 
XGBoost(eXtreme Gradient Boosting) is an advanced implementation of gradient 
boosting algorithm. XGBoost is well known because of the in-built cross-validation 
and regularization feature that helps reduce overfitting. It also deals with 
missing values in a very effective way.

Below snippet was used to run XGBoost with the parameters that were defined by
us:

```bash
model_xgb = XGBClassifier(max_depth= 3)
model_xgb.fit(X2, Y)
y_pred_XGB = model_xgb.predict(Xtest2)
```


## Results

We ran our three machine learning algorithms with dataset with and without the 
feature extracted from twitter sentiments. We can see the accuracy of each of 
the algorithms in the table below. 
  
|                   |   With Tweets  | Without Tweets  |
|-------------------|----------------|-----------------|
|Random Forest      |       60%      |      50%        |
|XGboost            |       40%      |      40%        |
|Logistic Regression|       50%      |      50%        |

We can see that there is no definite impact created by adding the feature containing 
the tweet sentiments. In some of the cases it it improves the prediction accuracy 
but in other cases it doesn't. However, considering all factors Random Forest gives 
us the best prediction accuracy of 60% with tweets.

## Conclusion and future work

Based on the above results, there is no evident increase in the accuracy by adding 
the tweet sentiments. This might have been due to the quality of tweets that were 
extracted. So as part of future work we need to plan to somehow be able to remove 
unwanted tweets and keep only meaningful ones. 

## Acknowledgement

We would like to thank Professor Gregor von Laszweski for all his support in this
project and his material which helped us install MongoDB. We would also like to 
acknowledge the TAs for their extended support and guidance thoughout.

## Work Breakdown

Sohan and Manek worked on this report equally on this report. The tweet extraction part
was divided equally between the two of us on our respective MongoDB localhost. 
The responsibility of data manipulation and the NLP was handled by Sohan and Manek 
completed the machine learning part of the project.
