
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing courses

with sqlite3.connect('courses.db') as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS courses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title TEXT, 
                     description TEXT, 
                     instructor TEXT, 
                     duration INTEGER)''')

@app.route('/')
def home():
    # Fetch all courses from the database
    with sqlite3.connect('courses.db') as conn:
        courses = conn.execute('SELECT * FROM courses').fetchall()
    return render_template('course.html', courses=courses)

@app.route('/add', methods=['POST'])
def add_course():
    title = request.form['title']
    description = request.form['description']
    instructor = request.form['instructor']
    duration = int(request.form['duration'])
    with sqlite3.connect('courses.db') as conn:
        conn.execute('INSERT INTO courses (title, description, instructor, duration) VALUES (?,?,?,?)', (title, description, instructor, duration))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_course():
    course_id = int(request.form['id'])
    title = request.form['title']
    description = request.form['description']
    instructor = request.form['instructor']
    duration = int(request.form['duration'])
    with sqlite3.connect('courses.db') as conn:
        conn.execute('UPDATE courses SET title =?, description =?, instructor =?, duration =? WHERE id =?', (title, description, instructor, duration, course_id))
    return 'Course updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_course():
    course_id = int(request.form['id'])
    with sqlite3.connect('courses.db') as conn:
        conn.execute('DELETE FROM courses WHERE id =?', (course_id,))
    return 'Course deleted successfully!'

@app.route('/search', methods=['GET'])
def search_courses():
    search_query = request.args.get('query', '')
    with sqlite3.connect('courses.db') as conn:
        results = conn.execute('SELECT * FROM courses WHERE title LIKE? OR description LIKE?', (f'%{search_query}%', f'%{search_query}%')).fetchall()
    return jsonify(results)

