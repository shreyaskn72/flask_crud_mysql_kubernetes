Below is **a clean Flask CRUD API** (GET, POST, PUT, DELETE) using **MySQL**, **SQLAlchemy**, **Docker**, and a **Kubernetes deployment strategy** that is production-ready.

You will get:

1. Full Flask CRUD API
2. MySQL integration
3. Dockerfile
4. Kubernetes strategy (best practice for MySQL + app)
5. Deployment architecture explanation

---

# ✅ 1. Flask CRUD API (MySQL + SQLAlchemy)

### **Project structure**

```
flask-crud/
├── app.py
├── models.py
├── db.py
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    ├── mysql-deployment.yaml
    ├── mysql-service.yaml
```

---

# ✅ 2. Flask API Code

### **db.py**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

### **models.py**

```python
from db import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
```

---

### **app.py**

```python
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
    app.run(host="0.0.0.0", port=5000)
```

---

# ✅ 3. requirements.txt

```
Flask
Flask-SQLAlchemy
Flask-Migrate
PyMySQL
gunicorn
```

---

# ✅ 4. Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2"]
```

Build image:

```bash
docker build -t flask-crud-api:latest .
```

---

# ⭐ 5. Kubernetes Deployment Strategy

This is **VERY IMPORTANT** — MySQL and the API are deployed differently.

---

# 🎯 Strategy Summary

| Component      | Deployment Strategy                    | Notes                             |
| -------------- | -------------------------------------- | --------------------------------- |
| **MySQL**      | StatefulSet + PersistentVolume         | Databases need persistent storage |
| **Flask App**  | Deployment + Service                   | Stateless API                     |
| **Connection** | Service DNS (`mysql`)                  | Kubernetes resolves automatically |
| **Secrets**    | Store DB password in Kubernetes Secret | Never hardcode                    |

---

# 🧱 Why This Strategy?

### ✔ Microservice principle → API should be stateless

### ✔ Use **MySQL StatefulSet**, not Deployment

StatefulSet provides:

* stable hostnames (mysql-0, mysql-1)
* persistent storage (PVC)
* recovery after restart

### ✔ Use **PersistentVolumeClaim** for MySQL data

Otherwise you lose your DB each restart.

### ✔ Use **Kubernetes Secrets** for DB password

Never store password in config files.

---

# 📦 6. Kubernetes Files

---

## 6.1 MySQL Secret (password)

`k8s/mysql-secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: cGFzc3dvcmQ=   # base64("password")
```

---

## 6.2 MySQL StatefulSet

`k8s/mysql-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  serviceName: mysql
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: MYSQL_ROOT_PASSWORD
            - name: MYSQL_DATABASE
              value: itemsdb
          ports:
            - containerPort: 3306
          volumeMounts:
            - name: mysql-storage
              mountPath: /var/lib/mysql
  volumeClaimTemplates:
    - metadata:
        name: mysql-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

---

## 6.3 MySQL Service

`k8s/mysql-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
    - port: 3306
  selector:
    app: mysql
  clusterIP: None   # headless for StatefulSet
```

---

## 6.4 Flask API Deployment

`k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
        - name: flask-api
          image: flask-crud-api:latest
          imagePullPolicy: Never
          env:
            - name: DATABASE_URL
              value: "mysql+pymysql://root:password@mysql:3306/itemsdb"
          ports:
            - containerPort: 5000
```

---

## 6.5 Flask API Service

`k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-api-service
spec:
  type: NodePort
  selector:
    app: flask-api
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30008
```

---

# 🚀 7. Deploy to Kubernetes

Run in order:

```bash
kubectl apply -f k8s/mysql-secret.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check pods:

```bash
kubectl get pods
```

Check services:

```bash
kubectl get svc
```

---

# 🌐 8. Access API

```
http://localhost:30008/items
```

---

# ✅ Ensure the DB exists

Exec into the mysql pod:

```bash
kubectl exec -it mysql-0 -- bash
```

Login:

```bash
mysql -u root -p
# password: password  (same as your secret)
```

Check DB:

```sql
SHOW DATABASES;
```

If `itemsdb` is missing, create it manually:

```sql
CREATE DATABASE itemsdb;
```

---


# 🔧 **Alternative Quick Fix — Create the table directly in MySQL**

```
use itemsdb;
```



Then:

```sql
CREATE TABLE item (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100)
);
```

But using SQLAlchemy to create the table is cleaner.

# 🎉 You Now Have:

✔ Full CRUD Flask API
✔ MySQL database backend
✔ Dockerized application
✔ Proper Kubernetes strategy
✔ Stateful MySQL + Stateless Flask app

---

# 👉 Want Next?

In the next section we can generate

✅ A **Helm Chart**

✅ A **Copier template**

✅ GitHub Actions CI/CD to build/push Docker image

✅ Ingress + TLS

✅ A production-optimized version (non-root user, slim image)


