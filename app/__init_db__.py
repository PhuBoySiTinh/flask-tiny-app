from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["flask-tiny-app"]
users = db["users"]

# Danh sách tài khoản mẫu
user_data = [
    {"username": "admin", "password": generate_password_hash("admin123"), "role": "admin"},
    {"username": "user1", "password": generate_password_hash("user123"), "role": "user"},
    {"username": "user2", "password": generate_password_hash("user123"), "role": "user"}
]

# Chèn vào MongoDB
users.insert_many(user_data)
print("Đã thêm user và admin thành công!")
