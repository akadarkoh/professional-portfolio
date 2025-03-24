# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import os
# import json
# from datetime import datetime

# app = Flask(__name__, static_folder='.', static_url_path='')

# # Store projects data in a JSON file
# PROJECTS_FILE = 'projects/projects.json'

# def get_projects():
#     if os.path.exists(PROJECTS_FILE):
#         with open(PROJECTS_FILE, 'r') as f:
#             return json.load(f)
#     return []

# @app.route('/')
# def home():
#     projects = get_projects()
#     return render_template('index.html', projects=projects)

# @app.route('/api/projects')
# def api_projects():
#     return jsonify(get_projects())

# @app.route('/api/contact', methods=['POST'])
# def contact():
#     data = request.form.to_dict()
    
#     # Add timestamp
#     data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # In a real application, you would:
#     # 1. Validate the data
#     # 2. Store it in a database
#     # 3. Send an email notification
    
#     # For now, just print it
#     print(f"Contact form submission: {data}")
    
#     # Save to a file as an example
#     with open('contact_submissions.json', 'a') as f:
#         f.write(json.dumps(data) + '\n')
    
#     return jsonify({"success": True, "message": "Thank you for your message!"})

# # Admin routes for managing projects (would need authentication in production)
# @app.route('/admin/projects', methods=['GET', 'POST'])
# def admin_projects():
#     if request.method == 'POST':
#         projects = get_projects()
#         new_project = {
#             "id": len(projects) + 1,
#             "title": request.form.get('title'),
#             "description": request.form.get('description'),
#             "tags": request.form.get('tags').split(','),
#             "image": request.form.get('image', ''),
#             "github": request.form.get('github', ''),
#             "live": request.form.get('live', '')
#         }
        
#         projects.append(new_project)
        
#         with open(PROJECTS_FILE, 'w') as f:
#             json.dump(projects, f, indent=2)
            
#         return redirect(url_for('admin_projects'))
    
#     return render_template('admin/projects.html', projects=get_projects())

# if __name__ == '__main__':
#     # Make sure the projects directory exists
#     os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
    
#     # Create an empty projects file if it doesn't exist
#     if not os.path.exists(PROJECTS_FILE):
#         with open(PROJECTS_FILE, 'w') as f:
#             json.dump([], f)
    
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
from functools import wraps
import secrets

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = secrets.token_hex(16)  # Generate secure secret key

# Database setup (MongoDB)
app.config["MONGO_URI"] = "mongodb://localhost:27017/portfolio"
mongo = PyMongo(app)

# Fallback to file system if database is not available
PROJECTS_FILE = 'projects/projects.json'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_projects():
    try:
        # Try to get projects from MongoDB
        projects = list(mongo.db.projects.find())
        # Convert ObjectId to string for JSON serialization
        for project in projects:
            if '_id' in project:
                project['_id'] = str(project['_id'])
        return projects
    except Exception as e:
        # Fallback to file system
        print(f"Database error: {e}, falling back to file system")
        if os.path.exists(PROJECTS_FILE):
            with open(PROJECTS_FILE, 'r') as f:
                return json.load(f)
        return []

@app.route('/')
def home():
    projects = get_projects()
    return render_template('index.html', projects=projects)

@app.route('/api/projects')
def api_projects():
    return jsonify(get_projects())

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.form.to_dict() if request.form else request.get_json()
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Store in MongoDB
        mongo.db.messages.insert_one(data)
    except Exception as e:
        print(f"Database error: {e}, falling back to file system")
        # Fallback to file system
        with open('contact_submissions.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    return jsonify({"success": True, "message": "Thank you for your message!"})

# Auth routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials (in production, get from database)
        # For demo, hardcoded admin/admin123
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'projects_count': len(get_projects()),
        'messages_count': mongo.db.messages.count_documents({}) if mongo else 0
    }
    return render_template('admin/dashboard.html', stats=stats)

# Admin routes for managing projects
@app.route('/admin/projects', methods=['GET', 'POST'])
@login_required
def admin_projects():
    if request.method == 'POST':
        new_project = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "tags": request.form.get('tags').split(','),
            "image": request.form.get('image', ''),
            "github": request.form.get('github', ''),
            "live": request.form.get('live', ''),
            "created_at": datetime.now()
        }
        
        try:
            # Store in MongoDB
            mongo.db.projects.insert_one(new_project)
        except Exception as e:
            print(f"Database error: {e}, falling back to file system")
            # Fallback to file system
            projects = get_projects()
            new_project["id"] = len(projects) + 1
            projects.append(new_project)
            
            with open(PROJECTS_FILE, 'w') as f:
                json.dump(projects, f, indent=2)
            
        flash('Project added successfully', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/projects.html', projects=get_projects())

@app.route('/admin/projects/delete/<project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    try:
        # Delete from MongoDB
        mongo.db.projects.delete_one({"_id": project_id})
    except Exception as e:
        print(f"Database error: {e}, falling back to file system")
        # Fallback to file system
        projects = get_projects()
        projects = [p for p in projects if str(p.get('id')) != project_id]
        
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(projects, f, indent=2)
    
    flash('Project deleted successfully', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/messages')
@login_required
def admin_messages():
    try:
        messages = list(mongo.db.messages.find().sort('timestamp', -1))
        for message in messages:
            message['_id'] = str(message['_id'])
    except Exception as e:
        print(f"Database error: {e}, falling back to file system")
        # Fallback to file system
        messages = []
        if os.path.exists('contact_submissions.json'):
            with open('contact_submissions.json', 'r') as f:
                for line in f:
                    try:
                        messages.append(json.loads(line))
                    except:
                        pass
    
    return render_template('admin/messages.html', messages=messages)

if __name__ == '__main__':
    # Make sure the projects directory exists
    os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
    
    # Create an empty projects file if it doesn't exist
    if not os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'w') as f:
            json.dump([], f)
    
    app.run(debug=True)