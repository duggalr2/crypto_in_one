import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


FILEPATH = '/Users/Rahul/Desktop/Side_projects/crypto_in_one/uci_news.csv'

# >>> import pickle
# >>> s = pickle.dumps(clf)
# >>> clf2 = pickle.loads(s)

def read_dataset(filename):
    news_df = pd.read_csv(filename)
    X = news_df.TITLE  # pre-hardcoded in..
    y = news_df.CATEGORY
    return X, y


def create_training_set(filename):
    X, y = read_dataset(filename)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    return X_train, X_test, y_train, y_test


def vectorize_dataset(X, y):
    vect = CountVectorizer()
    X_train_dtm = vect.fit_transform(X)
    X_test_dtm = vect.transform(y)
    return vect, X_train_dtm, X_test_dtm


def train_test(X_train, X_test, y_train, y_test):
    """Uses the training set to test the model"""
    vect = CountVectorizer()
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)
    print('General Accuracy:', metrics.accuracy_score(y_test, y_pred_class))


def train_model_save(X, y):
    vect, X_train_dtm, y_vect = vectorize_dataset(X, y)
    nb = MultinomialNB()
    nb.fit(X_train_dtm, y)
    s = pickle.dumps(nb)
    return s, vect


def classify(X, y, title, model, vect):
    nb = pickle.loads(model)
    X_test_dtm = vect.transform([title,])
    prediction = nb.predict(X_test_dtm)
    return prediction[0]

# if __name__ == '__main__':
#     X, y = read_dataset(FILEPATH)
#     m, v = train_model_save(X, y)
#     print(classify(X, y, 'Web Development Top 10 Articles for the Past Month (v.Feb 2018)', m, v))


# conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/crypto_in_one/db.sqlite3', check_same_thread=False)
# c = conn.cursor()
# c.execute('SELECT title FROM crypto_feeddetail')
# feed_list = [title[0] for title in c.fetchall()]
#
# filename = 'uci_news.csv'
# news_df = pd.read_csv(filename)
# X = news_df.TITLE
# y = news_df.CATEGORY
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# vect = CountVectorizer()
#
# X_train_dtm = vect.fit_transform(X_train)
# X_test_dtm = vect.transform(X_test)
#
# nb = MultinomialNB()
# nb.fit(X_train_dtm, y_train)
# y_pred_class = nb.predict(X_test_dtm)
#
# print('General Accuracy:', metrics.accuracy_score(y_test, y_pred_class))
#
# X_train_dtm = vect.fit_transform(X)
# nb = MultinomialNB()
# nb.fit(X_train_dtm, y)
# X_test_dtm = vect.transform(feed_list)
# y_pred_class = nb.predict(X_test_dtm)
#
# c.execute('SELECT MIN(id) FROM crypto_feeddetail')
# min_primary_key = c.fetchone()
# min_primary_key = min_primary_key[0]
# c.execute('SELECT MAX(id) FROM crypto_feeddetail')
# max_primary_key = c.fetchone()
# max_primary_key = max_primary_key[0]
# for i in range(min_primary_key, max_primary_key+1):
#     c.execute("INSERT INTO crypto_feeddetail (id, category) VALUES (?, ?)",
#               (i, y_pred_class[i]))
#     conn.commit()



# vect = CountVectorizer()
# X_train_dtm = vect.fit_transform(X)
# nb = MultinomialNB()
# nb.fit(X_train_dtm, y)
# X_test_dtm = vect.transform([title,])
# y_pred_class = nb.predict(X_test_dtm)
# return y_pred_class[0]
