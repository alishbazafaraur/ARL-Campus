from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['ARL']
db2=client['leave_management']

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')
@app.route('/index')  # Decorate the index function as a route
def index():
    return render_template('index.html')

@app.route('/checkin', methods=['GET', 'POST'])
def check_in():
    if request.method == 'POST':
        emp_id = request.form['id']  # Changed from 'id' to 'emp_id'
        department = request.form['department']
        tasks = request.form['tasks'].split('.')

        # Store check-in data
        check_in_data = {
            "emp_id": emp_id,  # Changed from 'id' to 'emp_id'
            "department": department,
            "tasks": tasks,
            "check_in_time": datetime.now(),
            "check_out_time": None
        }
        db.checks.insert_one(check_in_data)
        return redirect(url_for('index'))
    return render_template('checkin.html')

@app.route('/checkout', methods=['GET', 'POST'])
def check_out():
    if request.method == 'POST':
        emp_id = request.form['id']  # Changed from 'id' to 'emp_id'

        # Check if employee already checked in
        check_in_data = db.checks.find_one({"emp_id": emp_id, "check_out_time": None})  # Changed from 'id' to 'emp_id'

        if check_in_data:
            tasks = check_in_data['tasks']
            if request.form.getlist('tasks_done'):
                tasks_done = request.form.getlist('tasks_done')
            else:
                tasks_done = []

            # Store check-out data
            db.checks.update_one({"emp_id": emp_id, "check_out_time": None}, {"$set": {"check_out_time": datetime.now(), "tasks_done": tasks_done}})
            return redirect(url_for('index'))
        else:
            return "Employee hasn't checked in. Please check in first."
    return render_template('checkout.html')

@app.route('/latearrival', methods=['GET', 'POST'])
def late_arrival():
    if request.method == 'POST':
        id = request.form['id']
        department = request.form['department']
        reason = request.form['reason']
        db.late.insert_one({'id': id, 'department': department, 'reason': reason})
        return redirect(url_for('index', message="Late arrival recorded. Have a nice day!"))
    return render_template('latearrival.html')

# Dummy data for leave tracking
leave_data = {
    'John Doe': {
        'total_leave': 20,
        'leave_taken': 5,
        'leave_remaining': 15
    },
    'Jane Smith': {
        'total_leave': 25,
        'leave_taken': 10,
        'leave_remaining': 15
    }
}

@app.route('/leavemanagment')
def leavemanagment():
    return render_template('leavemanagment.html')

# Route for leave tracking
@app.route('/remote-work', methods=['GET', 'POST'])
def remote_work():
    if request.method == 'POST':
        id = request.form['id']
        department = request.form['department']
        team_leader = request.form['team_leader']
        reason = request.form['reason']
        num_days = request.form['num_days']

        # Here you can add your logic to handle the remote work request
        return render_template('remote_work_success.html', id=id, department=department, team_leader=team_leader, reason=reason, num_days=num_days)
    return render_template('remote_work.html')

@app.route('/admin_hr', methods=['GET', 'POST'])
def admin_hr():
    return render_template('admin_hr.html')


@app.route('/Monday_Boards_Replica', methods=['GET', 'POST'])
def Monday_Boards_Replica():
    return render_template('Monday_Boards_Replica.html')

@app.route('/Leave_Management', methods=['GET', 'POST'])
def Leave_Management():
    return render_template('Leave_Management.html')


@app.route('/time_off_request', methods=['GET', 'POST'])
def time_off_request():
    if request.method == 'POST':
        id = request.form['id']
        department = request.form['department']
        team_leader = request.form['team_leader']
        reason = request.form['reason']

        # Store data in MongoDB
        db2.requests.insert_one({
            'id': id,
            'department': department,
            'team_leader': team_leader,
            'reason': reason
        })

        return redirect(url_for('index'))

    return render_template('time_off_request.html')





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
@app.route('/Team Management')
def Team_Management():
    return render_template('Team Management.html', projects=projects)

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
    
    return redirect(url_for('Team Management'))

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
    app.run(port=8080)
