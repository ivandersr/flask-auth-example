from flask import Flask, request
from models.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:1234@localhost:3306/flask_auth"

db.init_app(app)

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)