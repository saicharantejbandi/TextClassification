import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from xgboost import XGBClassifier

movie_data = load_files(r"C:\Master Docs\ASU\Sem 2\Emily\Moderation\txt_sentoken")
X, y = movie_data.data, movie_data.target


documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(0, len(X)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(X[sen]))
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    
    documents.append(document)

    
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=437, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()
p=X
from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

classifier_RF = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier_LG = linear_model.SGDClassifier(max_iter=1000,tol=1e-5,loss='log',class_weight='balanced')
classifier_RF.fit(X_train, y_train) 
classifier_LG.fit(X_train, y_train) 

y_pred = classifier_RF.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))
with open('text_classifier_RF', 'wb') as picklefile:
    pickle.dump(classifier_RF,picklefile)

with open('text_classifier_LG', 'wb') as picklefile:
    pickle.dump(classifier_LG,picklefile)