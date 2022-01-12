from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, content, quantity):
        self.content = content
        self.quantity = quantity


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        new_item = Todo(request.form["content"], request.form["quantity"])

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return "There was an issue adding your item"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    item_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that item"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Todo.query.get_or_404(id)

    if request.method == "POST":
        item.content = request.form["content"]
        item.quantity = request.form["quantity"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your item"

    else:
        return render_template("update.html", task=item)


if __name__ == "__main__":
    app.run(debug=True)
