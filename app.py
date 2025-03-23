from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# Store projects data in a JSON file
PROJECTS_FILE = 'projects/projects.json'

def get_projects():
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
    data = request.form.to_dict()
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # In a real application, you would:
    # 1. Validate the data
    # 2. Store it in a database
    # 3. Send an email notification
    
    # For now, just print it
    print(f"Contact form submission: {data}")
    
    # Save to a file as an example
    with open('contact_submissions.json', 'a') as f:
        f.write(json.dumps(data) + '\n')
    
    return jsonify({"success": True, "message": "Thank you for your message!"})

# Admin routes for managing projects (would need authentication in production)
@app.route('/admin/projects', methods=['GET', 'POST'])
def admin_projects():
    if request.method == 'POST':
        projects = get_projects()
        new_project = {
            "id": len(projects) + 1,
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "tags": request.form.get('tags').split(','),
            "image": request.form.get('image', ''),
            "github": request.form.get('github', ''),
            "live": request.form.get('live', '')
        }
        
        projects.append(new_project)
        
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(projects, f, indent=2)
            
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/projects.html', projects=get_projects())

if __name__ == '__main__':
    # Make sure the projects directory exists
    os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
    
    # Create an empty projects file if it doesn't exist
    if not os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'w') as f:
            json.dump([], f)
    
    app.run(debug=True)
