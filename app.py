from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from flask_pymongo import PyMongo
import os
from flask_bcrypt import Bcrypt

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

bcrypt = Bcrypt(app)
# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/tiny-app")
db = client["user_database"]
users_collection = db["users"]

# Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Định nghĩa lớp User
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"username": user_id})
    return User(user_id) if user else None

# **1️⃣ API Đăng ký**
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Tên đăng nhập đã tồn tại"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({"username": username, "password": hashed_pw})

    return jsonify({"message": "Đăng ký thành công"}), 201

# **2️⃣ API Đăng nhập**
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json  # Kiểm tra nếu request có đúng định dạng JSON
        if not data:
            return jsonify({"message": "Dữ liệu không hợp lệ"}), 400

        username = data.get("username")
        password = data.get("password")

        print("Received username:", username)  # Log kiểm tra dữ liệu nhận được

        user = users_collection.find_one({"username": username})
        if not user:
            return jsonify({"message": "Sai tài khoản hoặc mật khẩu"}), 400

        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "Sai tài khoản hoặc mật khẩu"}), 400

        return jsonify({"message": "Đăng nhập thành công"}), 200

    except Exception as e:
        print("Lỗi đăng nhập:", str(e))
        return jsonify({"message": "Lỗi server"}), 500



# **3️⃣ API Đăng xuất**
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Đăng xuất thành công"}), 200

# **4️⃣ Route Giao diện**
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

