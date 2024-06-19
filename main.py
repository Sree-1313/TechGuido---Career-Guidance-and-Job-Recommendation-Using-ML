from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # Connecting to MongoDB
db = client['Db']  # Selecting database
users_collection = db['users']  # Selecting collection
register_collection = db['register']  # Selecting collection

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Register:
    def __init__(self, name, email, dob, cgpa, degree, stream, resume):
        self.name = name
        self.email = email
        self.dob = dob
        self.cgpa = cgpa
        self.degree = degree
        self.stream = stream
        self.resume = resume

# Print a message when MongoDB connection is established
if client is not None:
    print("Connected to MongoDB successfully!")

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

        # Check if username already exists in MongoDB
        if users_collection.find_one({'username': username}):
            return jsonify({'message': 'Username already exists'}), 400

        # Insert user data into MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        return redirect(url_for('register'))  # Redirect to registration page after signup
    else:
        return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        dob = request.form.get('dob')
        cgpa = request.form.get('cgpa')
        degree = request.form.get('degree')
        stream = request.form.get('stream')
        resume = request.files['resume'].read()

        if not all([name, email, dob, cgpa, degree, stream, resume]):
            return jsonify({'message': 'All fields are required'}), 400

        # Insert registration data into MongoDB
        register_data = {
            'name': name,
            'email': email,
            'dob': dob,
            'cgpa': cgpa,
            'degree': degree,
            'stream': stream,
            'resume': resume
        }
        register_collection.insert_one(register_data)
        return redirect(url_for('home'))  # Redirect to home page after registration
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Query MongoDB for the user
    user = users_collection.find_one({'username': username, 'password': password})

    if user:
        return redirect(url_for('home'))  # Redirect to home page after successful login
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    # Perform logout actions here
    # For example, clear session data
    return redirect(url_for('home')) 

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print("An error occurred:", e)
