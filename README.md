# SpamShield AI - Email Spam Classifier

## Overview

SpamShield AI is a machine learning-based email spam detection system. It classifies emails as spam or not spam using natural language processing and an ensemble (voting) model.

The project includes model training, evaluation, and a web interface built with Streamlit for real-time predictions.

---

## Features

* Text preprocessing and cleaning
* TF-IDF vectorization
* Voting Classifier (SVM, Naive Bayes, Random Forest)
* High precision and balanced performance
* Simple Streamlit web app for user input

---

## Tech Stack

* Python
* Scikit-learn
* Pandas, NumPy
* Streamlit

---

## Model Details

* Vectorization: TF-IDF (with max features)
* Models used:

  * Support Vector Machine (SVM)
  * Multinomial Naive Bayes
  * Random Forest
* Final Model: Voting Classifier (soft voting)

---

## Project Structure

```
spamshield-ai/
│── app.py
│── model.pkl
│── vectorizer.pkl
│── requirements.txt
│── README.md
```

---

## How to Run Locally

1. Clone the repository

```
git clone https://github.com/your-username/spamshield-ai.git
cd spamshield-ai
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the app

```
streamlit run app.py
```

---

## Usage

* Enter email text in the input box
* Click on "Check Spam"
* The model predicts whether the email is spam or not

---

## Results

* Accuracy: ~97%
* High precision with low false positives
* Balanced F1-score using ensemble model

---

## Future Improvements

* Hyperparameter tuning
* Adding more data for training
* Deploying on cloud platforms

---

## Author

Rajesh Kumar
