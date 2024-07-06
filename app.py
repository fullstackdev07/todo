from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()
    

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        contact=request.form['contact']

        new_todo=Todo(name=name, description=description, contact=contact)
        db.session.add(new_todo) 
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.filter_by(id=id).first()
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect("/")



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo_to_update = Todo.query.filter_by(id=id).first()
    if request.method == 'POST':
        todo_to_update.name = request.form['name']
        todo_to_update.description = request.form['description']
        todo_to_update.contact = request.form['contact']

        db.session.commit()
        return redirect("/")
    return render_template('update.html', todo=todo_to_update)
   

if __name__ == '__main__':
    app.run(debug=True)