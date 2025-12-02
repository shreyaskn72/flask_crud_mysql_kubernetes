from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import Item
import os

app = Flask(__name__)

# MySQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@mysql:3306/itemsdb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    item = Item(name=data["name"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item created", "id": item.id})

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    item = Item.query.get_or_404(item_id)
    item.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Item updated"})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
