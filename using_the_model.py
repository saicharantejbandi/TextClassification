import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
import csv
from nltk.stem import WordNetLemmatizer
stemmer = WordNetLemmatizer()


X=[]
documents = []
name="human_mod_cmts"

with open(str(name)+'.csv', 'r', errors="ignore") as csv_file:
    csv_reader= csv.reader(csv_file)
    for line in csv_reader:
        X.append(line[-1])
    


print("lemmatize start")


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

#print(documents)

print("lemmatize done")
print(".")
print(".")
print(".")


print("extracting features")

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=437, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()
print("features extracted")

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()


print("Predicting Now!")


with open('text_classifier_LG', 'rb') as training_model:
    model = pickle.load(training_model)
    y_pred2 = model.predict(X)

with open('text_classifier_RF', 'rb') as training_model:
    model = pickle.load(training_model)
    y_pred3 = model.predict(X)

print("ready to load the predicted results into csv")
with open(str(name)+'.csv', 'r', errors="ignore") as csv_file:

    csv_reader= csv.reader(csv_file)
    m=0
    with open(str(name)+"_with_pred"+'.csv', 'w') as new_file:
        csv_writer=csv.writer(new_file)
        for line in csv_reader:
            line.append(y_pred2[m])
            line.append(y_pred3[m])
            m=m+1
            csv_writer.writerow(line)


    
