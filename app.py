import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

# --- Resources Loading ---
@st.cache_resource
def load_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
    return tfidf, model

tfidf, model = load_resources()
ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = [ps.stem(i) for i in text if i.isalnum() and i not in stopwords.words('english') and i not in string.punctuation]
    return " ".join(y)

def extra_scam_checks(text):
    text = text.lower()
    
    # 1. Check for "Check + Equipment" pattern
    if re.search(r'check.*(buy|purchase).*equipment', text):
        return "🚨 Scam Alert: This 'Check for Equipment' pattern is a known fraud."
    
    # 2. Check for Telegram/WhatsApp for interviews
    if "telegram" in text or "whatsapp" in text:
        if "interview" in text or "shortlisted" in text:
            return "⚠️ Caution: Professional interviews rarely happen on Telegram/WhatsApp."
            
    return None

def safety_check(text):
    text = text.lower()
    # Pattern 1: Internship + Money
    if 'internship' in text and ('fee' in text or 'pay' in text or '£' in text or '₹' in text):
        return "⚠️ Scam Alert: Genuine internships don't ask for fees."
    
    # Pattern 2: Job + Equipment Check
    if 'check' in text and 'equipment' in text:
        return "🚨 Fraud Alert: This 'Check for Equipment' is a famous scam."
    
    return None

# --- Sidebar Section ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/561/561127.png", width=80)
    st.title("🛡️ SpamShield AI")
    st.info("""
    **About this Project:**
    This AI tool helps identify if an email or SMS is Spam or Safe.
    
    **Model Info:**
    - Algorithm: Voting Classifier
    - Base Models: SVM, NB, RF
    """)
    
    st.divider()
    st.warning("""
    **⚠️ Pro Tip:**
    If an email asks for **Money** or **OTP**, it's a scam even if the model says Safe!
    """)

# --- Main UI ---
st.title("📧 Email/SMS Spam Classifier")
st.markdown("---")

# User Input
input_sms = st.text_area("Paste your message here", height=180, placeholder="Example: Congratulations! You've won a prize...")

# Column Buttons
col1, col2 = st.columns([1, 4])
with col1:
    predict_btn = st.button("Analyze")
with col2:
    if st.button("Clear"):
        st.rerun()

# --- Prediction Logic ---
if predict_btn:
    if not input_sms.strip():
        st.toast("Please enter text first!", icon="⚠️")
    else:
        with st.spinner('Analyzing patterns...'):
            # Transformation
            transformed_sms = transform_text(input_sms)
            vector_input = tfidf.transform([transformed_sms]).toarray()
            
            # Predict
            result = model.predict(vector_input)[0]
            prob = model.predict_proba(vector_input)[0]
            confidence = max(prob) * 100

            st.subheader("Result:")
            
            # Smart Logic for "Sophie Bennett" cases (Manual Check)
            scam_keywords = ['fee', 'payment', 'pay', 'gbp', 'inr', 'limited seats']
            is_suspicious = any(word in input_sms.lower() for word in scam_keywords)

            if result == 1:
                st.error(f"🚨 SPAM DETECTED ({confidence:.2f}%)")
            elif is_suspicious and result == 0:
                st.warning(f"🟡 CAUTION ({confidence:.2f}%)")
                st.info("**Note:** Model says Safe, but we found financial keywords. Be careful!")
            else:
                st.success(f"✅ SAFE / HAM ({confidence:.2f}%)")

            # Analysis logic mein ise use karein:
            scam_warning = extra_scam_checks(input_sms)
            if scam_warning:
                st.warning(scam_warning)

# --- Footer Instruction ---
st.markdown("---")
st.caption("Instructions: Always check the sender's email address. AI can make mistakes.")