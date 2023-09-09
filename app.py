from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"


db = SQLAlchemy(app)

migrate = Migrate(app, db)


class ToDo(db.Model):
      sno = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(200), nullable=False)
      des = db.Column(db.String(500), nullable=False)
      current_date = datetime.now()
      date = db.Column(db.String, default=current_date.date())
      
      def __repr__(self) -> str:
            return f"{self.sno}-{self.title}"
      
 
@app.route("/", methods=["GET", "POST"])
def home():
      if request.method == "POST":
            title = request.form["title"]
            des = request.form["des"]
            todo = ToDo(title=title,des=des)
            db.session.add(todo)
            db.session.commit()
      todos = ToDo.query.all() 
      return render_template("index.html",todos=todos)
      
@app.route("/delete/<int:sno>")
def delete(sno):
      todo = ToDo.query.filter_by(sno=sno).first()
      db.session.delete(todo)
      db.session.commit()
      
      return redirect("/")
     
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
      if request.method == 'POST':
            title = request.form["title"]
            des = request.form["des"]
            todo = ToDo.query.filter_by(sno=sno).first()
            todo.title = title
            todo.des = des
            db.session.add(todo)
            db.session.commit()
            
            return redirect("/")
      todo = ToDo.query.filter_by(sno=sno).first()
      return render_template("update.html", todo=todo)

if __name__ == "__main__":
      with app.app_context():
            db.create_all()
      app.run(debug=True, port=6969)