from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) #intialisng db 

# creation of a model
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable=False) #dont want task to be blank
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])

def index():
    if request.method=="POST":                  # to put things into db
        task_content = request.form['content']  # references the content id in the index.html file 
        new_task = Todo(content=task_content)   #creates the content of the task

        try:
            db.session.add(new_task)            
            db.session.commit()
            return redirect('/')                # returns a redirect to the homepage
        except:
            return "There is an issue adding the task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #order by date created and return all entries
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was a problem deleting the task"


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id) #getting task from the id
    if request.method=="POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return redirect('/')

    else:
        return render_template('update.html',task=task)


if __name__ == "__main__":
    app.run(debug=True)
