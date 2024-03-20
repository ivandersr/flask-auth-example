from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:1234@localhost:3306/flask_auth"

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"}), 200


    return jsonify({"message": "Credenciais Inválidas"}), 401


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"}), 200

@app.route("/user", methods=["POST"])
@login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        existing_user = User.query.filter_by(username=username)
        if existing_user:
            return jsonify({"message": "Nome de usuário não disponível"}), 400
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuário criado com sucesso"}), 200
    
    return jsonify({"message": "Dados inválidos"}), 400


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)