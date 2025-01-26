# -*- coding: utf-8 -*-
"""goit-numericalpy-hw-07-soloviova_lesia.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ScWAuO3v_Wc8bLE-dCil_5Y4KjvO52OA
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer

print("=== Крок 1: Завантаження бібліотек NLTK ===")
# Завантаження бібліотек NLTK
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Крок 2: Завантаження даних
print("\n=== Крок 2: Завантаження даних ===")
!wget -O SpamEmailClassificationDataset.zip https://github.com/goitacademy/NUMERICAL-PROGRAMMING-IN-PYTHON/blob/main/SpamEmailClassificationDataset.zip?raw=true
!unzip -o SpamEmailClassificationDataset.zip

# Крок 3: Завантаження CSV файлу
print("\n=== Крок 3: Завантаження CSV файлу ===")
df = pd.read_csv('./SpamEmailClassificationDataset/combined_data.csv')

# Крок 4: Перевірка кількості класів
print("\n=== Крок 4: Перевірка кількості класів ===")
print("Кількість записів у кожному класі:")
print(df['label'].value_counts())

# Видалення класів з недостатньою кількістю записів
df = df.groupby('label').filter(lambda x: len(x) >= 2)

# Перевірка кількості записів після фільтрації
print("\nКількість записів у кожному класі після фільтрації:")
print(df['label'].value_counts())

# Крок 5: Візуалізація розподілу класів
print("\n=== Крок 5: Візуалізація розподілу класів ===")
plt.figure(figsize=(6, 6))
sns.countplot(data=df, x='label', palette='coolwarm')
plt.title('Розподіл повідомлень за класами')
plt.xlabel('Клас')
plt.ylabel('Кількість')
plt.show()

# Крок 6: Попередня обробка тексту
print("\n=== Крок 6: Попередня обробка тексту ===")
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub("[^a-zA-Z]", " ", text).lower()  # Видалення небуквених символів
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Лематизація
    words = list(set(words))  # Видалення повторів
    return " ".join(words)

df["text"] = df["text"].apply(preprocess_text)

# Крок 7: Поділ даних на тренувальні та тестові набори
print("\n=== Крок 7: Поділ даних на тренувальні та тестові набори ===")
train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

# Крок 8: Ініціалізація векторизатора TF-IDF
print("\n=== Крок 8: Ініціалізація векторизатора TF-IDF ===")
vectorizer = TfidfVectorizer(max_features=5000)

# Крок 9: Векторизація тексту
print("\n=== Крок 9: Векторизація тексту ===")
X_train = vectorizer.fit_transform(train["text"])
X_test = vectorizer.transform(test["text"])

# Крок 10: Мітки класів
print("\n=== Крок 10: Мітки класів ===")
y_train = train["label"]
y_test = test["label"]

# Крок 11: Пошук найкращих гіперпараметрів
print("\n=== Крок 11: Пошук найкращих гіперпараметрів ===")
param_grid = {'alpha': [0.1, 0.5, 1.0, 2.0]}
grid_search = GridSearchCV(MultinomialNB(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Використання найкращих параметрів
nb_classifier = grid_search.best_estimator_

# Крок 12: Прогнозування
print("\n=== Крок 12: Прогнозування ===")
predictions = nb_classifier.predict(X_test)

# Крок 13: Оцінка моделі
print("\n=== Крок 13: Оцінка моделі ===")
accuracy = accuracy_score(y_test, predictions)
print(f"Точність класифікації: {accuracy * 100:.2f}%")

# Повний звіт
print("\nПовний звіт про класифікацію:")
print(classification_report(y_test, predictions))

# Крок 14: Матриця плутанини
print("\n=== Крок 14: Матриця плутанини ===")
cm = confusion_matrix(y_test, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=nb_classifier.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Матриця плутанини")
plt.show()

# Крок 15: Аналіз важливих слів
print("\n=== Крок 15: Аналіз важливих слів ===")
feature_names = np.array(vectorizer.get_feature_names_out())

# Топ 10 слів для спаму
top_spam_words = feature_names[np.argsort(nb_classifier.feature_log_prob_[1])[-10:]]
top_spam_probs = np.exp(nb_classifier.feature_log_prob_[1][np.argsort(nb_classifier.feature_log_prob_[1])[-10:]])
print("\nТоп 10 слів для спаму:")
for word, prob in zip(top_spam_words, top_spam_probs):
    print(f"{word}: {prob:.4f}")

# Топ 10 слів для хему
top_ham_words = feature_names[np.argsort(nb_classifier.feature_log_prob_[0])[-10:]]
top_ham_probs = np.exp(nb_classifier.feature_log_prob_[0][np.argsort(nb_classifier.feature_log_prob_[0])[-10:]])
print("\nТоп 10 слів для звичайних повідомлень:")
for word, prob in zip(top_ham_words, top_ham_probs):
    print(f"{word}: {prob:.4f}")

print("""
=== Висновки ===
1. Висока точність моделі
   Модель показала точність 94.99%, що свідчить про її ефективність у класифікації спаму та не спаму. Це дозволяє використовувати її для автоматичної фільтрації повідомлень.

2. Важливі слова для класифікації
   - Для спаму: Найважливіші слова — це 'escapenumber', 'http', 'com', що часто зустрічаються в рекламних повідомленнях.
   - Для не спаму: Найважливіші слова — це 'org', 'please', 'thanks', які характерні для звичайних листів.

3. Потенційні покращення
   Модель можна покращити, додавши обробку контексту (наприклад, n-grams) або використавши більш складні методи векторизації, такі як Word2Vec або FastText, для кращого розуміння семантики текстів.
""")