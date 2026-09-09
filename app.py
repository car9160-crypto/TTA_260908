import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_url = os.environ.get('POSTGRES_URL', 'sqlite:///todo.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo_task = request.form.get('todo')
    if todo_task:
        new_todo = Todo(task=todo_task)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = db.session.get(Todo, todo_id)
    if todo:
        todo.done = not todo.done
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.session.get(Todo, todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
