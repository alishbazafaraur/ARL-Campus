# app.py

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define some dummy data for demonstration
projects = [
    {"id": 1, "name": "ARL Campus", "status": "Ongoing"},
    {"id": 2, "name": "Data Analytics", "status": "To Do"},
    {"id": 3, "name": "Content Generation", "status": "Done"},
]

tasks = [
    {"id": 1, "project_id": 1, "name": "Task 1", "priority": "High", "status": "To Do", "assigned_to": "AI Interns"},
    {"id": 2, "project_id": 1, "name": "Task 2", "priority": "Medium", "status": "In Progress", "assigned_to": " AI Interns"},
    {"id": 3, "project_id": 2, "name": "Task 3", "priority": "Low", "status": "Done", "assigned_to": "AI Interns"},
]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project(project_id):
    project_tasks = [task for task in tasks if task['project_id'] == project_id]
    project_info = next((project for project in projects if project['id'] == project_id), None)
    if project_info:
        return render_template('project.html', project_info=project_info, tasks=project_tasks)
    else:
        return "Project not found"

@app.route('/create_project', methods=['POST'])
def create_project():
    name = request.form['name']
    status = request.form['status']
    
    new_project = {
        "id": len(projects) + 1,
        "name": name,
        "status": status
    }
    projects.append(new_project)
    
    return redirect(url_for('index'))

@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    name = request.form['name']
    priority = request.form['priority']
    status = request.form['status']
    assigned_to = request.form['assigned_to']
    
    new_task = {
        "id": len(tasks) + 1,
        "project_id": project_id,
        "name": name,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to
    }
    tasks.append(new_task)
    
    return redirect(url_for('project', project_id=project_id))

if __name__ == '__main__':
    app.run(debug=True)
