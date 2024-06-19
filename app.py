from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, send_from_directory
from pymongo import MongoClient
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Connecting to MongoDB
db = client['Db']  # Selecting database
users_collection = db['users']  # Selecting collection for users
register_collection = db['register']  # Selecting collection for registrations
recommended_jobs_collection = db['recommended_jobs']  # New collection for recommended jobs

# Load job descriptions from CSV into a dictionary
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, 'job_descriptions.csv')
job_descriptions = {}

try:
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Job Title']
            job_descriptions[title] = {
                'role': row['Role'],
                'salary': row['Salary Range'],
                'skills': row['skills'],
                'location': row['location'],
                'qualification': row['Qualifications'],
                'experience': row['Experience'],
                'company': row['Company']
            }
except FileNotFoundError:
    print("Error: CSV file not found. Ensure the 'job_descriptions.csv' file exists.")

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'message': 'All fields are required'}), 400

        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return jsonify({'message': 'Username already exists'}), 400

        # Add the new user to the collection
        users_collection.insert_one({'username': username, 'password': password})

        # Automatically log the user in
        session['username'] = username

        return redirect(url_for('home'))  # Redirect to home page after successful signup
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Find the user in the database
    user = users_collection.find_one({'username': username, 'password': password})

    if user:
        session['username'] = username
        return redirect(url_for('home'))
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    
    username = session['username']  # Get the logged-in user's name

    # Determine whether to show the pop-up message
    show_popup = not session.get('popup_shown', False)

    return render_template('home.html', username=username, show_popup=show_popup)  # Pass 'show_popup' to the template

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        degree = request.form.get('degree')
        stream = request.form.get('stream')
        cgpa = request.form.get('cgpa')
        jobtitle = request.form.get('jobtitle')
        experience = request.form.get('experience')

        if not all([degree, stream, cgpa, jobtitle, experience]):
            return jsonify({'message': 'All fields are required'}), 400

        register_data = {
            'username': session['username'],  # Associate registration with logged-in user
            'degree': degree,
            'stream': stream,
            'cgpa': cgpa,
            'jobtitle': jobtitle,
            'experience': experience,
        }
        register_collection.insert_one(register_data)

        # Flash a success message
        flash("Successfully registered!", "success")

        # Set a session variable to indicate the pop-up has been shown
        session['popup_shown'] = True

        # Redirect to the home page
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/recommendation')
def recommendation():
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    
    username = session['username']  # Get the logged-in user's name
    
    # Retrieve user's registered job title
    user_data = register_collection.find_one({'username': username})
    if user_data:
        user_job_title = user_data.get('jobtitle', '')
    else:
        return jsonify({'message': 'User data not found'}), 404
    
    # Retrieve recommended jobs for the user
    recommended_jobs_data = recommended_jobs_collection.find_one({'username': username})
    if recommended_jobs_data:
        recommended_jobs = recommended_jobs_data.get('recommended_jobs', [])
    else:
        return jsonify({'message': 'Recommended jobs not found'}), 404
    
    # Filter recommended jobs that match the user's registered job title
    matched_jobs = [job for job in recommended_jobs if job['info']['jobtitle'] == user_job_title]
    
    return render_template('recommendation.html', username=username, matched_jobs=matched_jobs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/jobss')
def jobs():
    return render_template('jobs.html')

@app.route('/course1')
def course1():
    return render_template('course1.html')

@app.route('/course2')
def course2():
    return render_template('course2.html')

@app.route('/course3')
def course3():
    return render_template('course3.html')

@app.route('/course4')
def course4():
    return render_template('course4.html')

@app.route('/course5')
def course5():
    return render_template('course5.html')

@app.route('/course6')
def course6():
    return render_template('course6.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session to log out
    return redirect(url_for('index'))  # Redirect to the login page

@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        results = {title: info for title, info in job_descriptions.items() if query.lower() in title.lower()}
    else:
        results = {}
    return render_template('search_results.html', query=query, results=results)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
