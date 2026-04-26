# AI Internship Matcher 🚀

## What it does
The **AI Internship Matcher** is a smart, full-stack web application designed to connect students with their ideal internships. 

Unlike traditional job boards that rely on flawed, basic keyword-matching (which often results in unqualified candidates matching with senior roles due to buzzwords), this platform utilizes a **Semantic Search Engine**. By leveraging a state-of-the-art Natural Language Processing (NLP) machine learning model, the backend reads and *understands* the context of a student's profile and an employer's job description. 

It calculates a highly accurate **70/30 weighted compatibility score** (prioritizing Hard Skills at 70% and Soft Interests/Culture Fit at 30%), ensuring students are recommended for roles they are genuinely qualified for. The application also features complete, secure CRUD (Create, Read, Update, Delete) functionality for all users.

## Tech Stack
* **Backend:** Python, Flask
* **Database:** MongoDB (PyMongo) for flexible NoSQL document storage
* **Machine Learning / AI:** * `sentence-transformers` (`all-mpnet-base-v2` model) for deep-semantic text vectorization
  * `scikit-learn` for Cosine Similarity mathematical calculations
  * `pandas` for high-speed data extraction and preprocessing
* **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2 Templating

---

## How to Run It

### 1. Prerequisites
Before you begin, ensure you have the following installed on your machine:
* **Python 3.8+**
* **MongoDB** (running locally on port `27017` or configured via a MongoDB Atlas URI)

### 2. Install Dependencies
Open your terminal and install the required Python libraries:
```bash
pip install flask pymongo pandas sentence-transformers scikit-learn
