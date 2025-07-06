from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Todo(title=title, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# Create tables on app startup regardless of run method
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
