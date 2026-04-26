import pandas as pd
from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import utils
import sys

# --- Application Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_strong_and_unique_secret_key'

# --- Database Connection Management ---
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['internship_matching_db']

students_col = db['students']
employers_col = db['employers']

# --- Function to Export DB to CSV ---
def export_db_to_csv():
    print("Exporting database to CSV files...")
    students_data = list(students_col.find({}))
    employers_data = list(employers_col.find({}))

    students_df = pd.DataFrame(students_data)
    employers_df = pd.DataFrame(employers_data)

    if not students_df.empty:
        students_df['_id'] = students_df['_id'].astype(str)
    if not employers_df.empty:
        employers_df['_id'] = employers_df['_id'].astype(str)

    students_df.to_csv('students.csv', index=False)
    employers_df.to_csv('employers.csv', index=False)
    print("Export complete.")
    return students_df, employers_df

# --- Access Control Decorators ---
def student_login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'student_id' not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('student_login'))
        return view(**kwargs)
    return wrapped_view

def employer_login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'employer_id' not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('employer_login'))
        return view(**kwargs)
    return wrapped_view

# --- General Routes ---
@app.route('/')
def index():
    return redirect(url_for('student_signup'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# --- Student Routes ---
@app.route('/student/signup', methods=('GET', 'POST'))
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        # FIX: Clean the email input
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        error = None
        if not all([name, email, password]):
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif students_col.find_one({'email': email}):
            error = f"Email {email} is already registered."

        if error is None:
            students_col.insert_one({'name': name, 'email': email, 'password': password})
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('student_login'))
            
        flash(error, 'danger')
    return render_template('student_signup.html')

@app.route('/student/login', methods=('GET', 'POST'))
def student_login():
    if request.method == 'POST':
        # FIX: Clean the email input
        email = request.form['email'].strip().lower()
        password = request.form['password']
        
        student = students_col.find_one({'email': email, 'password': password})

        if student is None:
            flash('Incorrect email or password.', 'danger')
        else:
            session.clear()
            session['student_id'] = str(student['_id'])
            return redirect(url_for('student_profile'))

    return render_template('student_login.html')

@app.route('/student/profile', methods=('GET', 'POST'))
@student_login_required
def student_profile():
    student_id = session['student_id']
    
    if request.method == 'POST':
        profile_data = request.form.to_dict()
        
        update_data = {
            'phone': profile_data.get('phone'),
            'location': profile_data.get('location'),
            'skills': profile_data.get('skills'),
            'interests': profile_data.get('interests'),
            'aspirations': profile_data.get('aspirations'),
            'academic_background': profile_data.get('academic_background')
        }
        
        students_col.update_one({'_id': ObjectId(student_id)}, {'$set': update_data})
        flash('Profile updated successfully! Generating your matches...', 'success')

        print("--- Starting Recommendation Pipeline ---")
        students_df, employers_df = export_db_to_csv()
        student_embeds, employer_embeds, stud_df_proc, emp_df_proc = utils.create_and_save_embeddings(students_df, employers_df)
        session['matches'] = utils.find_top_matches(student_id, stud_df_proc, emp_df_proc, student_embeds, employer_embeds)

        return redirect(url_for('student_matches'))

    profile_data = students_col.find_one({'_id': ObjectId(student_id)})
    return render_template('student_profile.html', profile=profile_data)

@app.route('/student/matches')
@student_login_required
def student_matches():
    matches = session.get('matches', [])
    return render_template('student_matches.html', matches=matches)

@app.route('/student/delete', methods=['POST'])
@student_login_required
def delete_student_account():
    student_id = session['student_id']
    students_col.delete_one({'_id': ObjectId(student_id)})
    session.clear()
    flash('Your account and profile have been permanently deleted.', 'info')
    return redirect(url_for('index'))

# --- Employer Routes ---
@app.route('/employer/signup', methods=('GET', 'POST'))
def employer_signup():
    if request.method == 'POST':
        company_name = request.form['company_name']
        # FIX: Clean the email input
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        error = None
        if not all([company_name, email, password]):
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif employers_col.find_one({'email': email}):
            error = f"Email {email} is already registered."

        if error is None:
            employers_col.insert_one({'company_name': company_name, 'email': email, 'password': password})
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('employer_login'))
            
        flash(error, 'danger')
    return render_template('employer_signup.html')

@app.route('/employer/login', methods=('GET', 'POST'))
def employer_login():
    if request.method == 'POST':
        # FIX: Clean the email input
        email = request.form['email'].strip().lower()
        password = request.form['password']
        
        employer = employers_col.find_one({'email': email, 'password': password})
        
        if employer is None:
            flash('Incorrect email or password.', 'danger')
        else:
            session.clear()
            session['employer_id'] = str(employer['_id'])
            return redirect(url_for('employer_profile'))
            
    return render_template('employer_login.html')

@app.route('/employer/profile', methods=('GET', 'POST'))
@employer_login_required
def employer_profile():
    employer_id = session['employer_id']
    
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        update_data = {
            'company_name': form_data.get('company_name'),
            'position_offered': form_data.get('position_offered'),
            'description': form_data.get('description'),
            'required_skills': form_data.get('required_skills'),
            'location_of_work': form_data.get('location_of_work'),
            'stipend': form_data.get('stipend')
        }
        
        employers_col.update_one({'_id': ObjectId(employer_id)}, {'$set': update_data})
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employer_profile'))
        
    employer_data = employers_col.find_one({'_id': ObjectId(employer_id)})
    return render_template('employer_profile.html', employer=employer_data)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'initdb':
        print("Initializing the database (dropping existing collections)...")
        db.drop_collection('students')
        db.drop_collection('employers')
        print("Collections cleared. MongoDB will auto-create them on the first insertion.")
    else:
        app.run(debug=True)