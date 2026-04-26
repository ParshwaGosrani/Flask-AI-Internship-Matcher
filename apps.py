# from flask import Flask, jsonify, request
# import pandas as pd
# from inference import find_top_matches
# from embed import load_embeddings, STUDENT_EMBEDDINGS_FILE, EMPLOYER_EMBEDDINGS_FILE
#
# app = Flask(__name__)
#
# # --- Load all data into memory on startup ---
# print("Loading data for Flask app...")
# try:
#     STUDENTS_DF = pd.read_csv('students_processed.csv')
#     EMPLOYERS_DF = pd.read_csv('employers_processed.csv')
#     STUDENT_EMBEDDINGS = load_embeddings(STUDENT_EMBEDDINGS_FILE)
#     EMPLOYER_EMBEDDINGS = load_embeddings(EMPLOYER_EMBEDDINGS_FILE)
#
#     if any(data is None for data in [STUDENTS_DF, EMPLOYERS_DF, STUDENT_EMBEDDINGS, EMPLOYER_EMBEDDINGS]):
#         raise FileNotFoundError
#
#     print("Data loaded successfully.")
#     DATA_LOADED = True
# except FileNotFoundError:
#     print("Could not load necessary data files. Make sure you have run preprocess.py and embed.py")
#     DATA_LOADED = False
#
#
# @app.route("/")
# def index():
#     return "Welcome to the Internship Recommendation API! Use /recommend/&lt;student_id&gt; to get matches."
#
#
# @app.route("/recommend/<int:student_id>")
# def recommend(student_id):
#     """
#     API endpoint to get recommendations for a specific student.
#     """
#     if not DATA_LOADED:
#         return jsonify({"error": "Server is not ready. Data files are missing."}), 500
#
#     # Find the top 5 matches for the given student ID
#     result = find_top_matches(
#         student_id=student_id,
#         students_df=STUDENTS_DF,
#         employers_df=EMPLOYERS_DF,
#         student_embeddings=STUDENT_EMBEDDINGS,
#         employer_embeddings=EMPLOYER_EMBEDDINGS,
#         top_n=5
#     )
#
#     if "error" in result:
#         return jsonify(result), 404  # Not Found
#
#     return jsonify(result)
#
#
# if __name__ == '__main__':
#     # To run the app: `flask --app app run` in your terminal
#     # Or simply: `python app.py`
#     app.run(debug=True, port=5001)