import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
data = pd.read_csv("Healthcare_Transformed.csv")

# Clean symptoms (remove commas)
data["symptoms"] = data["symptoms"].str.replace(",", "")

# Combine useful columns
data["input"] = (
    data["age"].astype(str) + " " +
    data["gender"] + " " +
    data["age_group"] + " " +
    data["symptoms"]
)

X = data["input"]
y = data["disease"]

# Text to numeric
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train Naive Bayes
model = MultinomialNB()
model.fit(X_vec, y)

#Accuracy 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


def predict_disease(age, gender, age_group, symptoms):
    symptoms = symptoms.replace(",", "")
    user_input = f"{age} {gender} {age_group} {symptoms}"

    input_vec = vectorizer.transform([user_input])
    probs = model.predict_proba(input_vec)[0]
    diseases = model.classes_

    # Combine & sort
    disease_probs = list(zip(diseases, probs))
    disease_probs.sort(key=lambda x: x[1], reverse=True)

    # Take top 3
    top_three = disease_probs[:3]

    # Sum of top 3 probabilities
    total_prob = sum(p for _, p in top_three)

    # Normalize to 100%
    high = (top_three[0][0], round((top_three[0][1] / total_prob) * 100, 2))
    medium = (top_three[1][0], round((top_three[1][1] / total_prob) * 100, 2))
    low = (top_three[2][0], round((top_three[2][1] / total_prob) * 100, 2))

    return {
        "HIGH": high,
        "MEDIUM": medium,
        "LOW": low
    }


