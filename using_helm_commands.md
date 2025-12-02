Here is a **clean, ready-to-copy document** that explains **Install, Upgrade, Delete, Debug, and Manage Helm Releases** for your Flask-CRUD Helm chart.

You can paste this into your README.md or internal docs.

---

# 📘 **Helm Commands Cheat Sheet — Flask CRUD Application**

This document provides the complete set of Helm commands required to **install, upgrade, delete, debug, and manage** your Helm chart for the Flask CRUD + MySQL application.

---

# 🚀 **1. Install the Helm Chart**

### **Basic install**

Go to folder where Chart.yaml exist.

in this case its /flask_crud_mysql_kubernetes/flask-crud/flask-crud-chart


```bash
helm install flask-crud-release .
```

### **Install with required MySQL password**

(You MUST provide it if your chart uses `required`)

```bash
helm install flask-crud-release . \
  --set mysqlSecret.mysqlRootPassword=password
```

### Verify installation

```bash
helm status flask-crud-release
kubectl get pods
kubectl get svc
```

---

# 🔄 **2. Upgrade / Update Your Release**

Use this when:

* You modified your templates
* You changed `values.yaml`
* You want to update passwords, image tags, environment variables, etc.

### **Basic upgrade**

```bash
helm upgrade flask-crud-release .
```

### **Upgrade with updated values**

```bash
helm upgrade flask-crud-release . \
  --set mysqlSecret.mysqlRootPassword=newpassword
```

### Check status after upgrade

```bash
helm status flask-crud-release
```

---

# 🛑 **3. Uninstall / Delete the Helm Release**

This removes:

✔ Deployments
✔ Services
✔ Secrets
✔ ConfigMaps
✔ ReplicaSets
✔ Pods

❌ PVCs (Persistent Volumes) are NOT deleted unless you delete manually.

### Delete release:

```bash
helm uninstall flask-crud-release
```

Check:

```bash
kubectl get all
```

---

# 🧹 **4. (Optional) Delete PersistentVolumes / PVCs**

MySQL PVC remains even after uninstall.
To list:

```bash
kubectl get pvc
```

To delete:

```bash
kubectl delete pvc <pvc-name>
```

Example:

```bash
kubectl delete pvc data-flask-crud-release-mysql-0
```

To delete all PVCs (dangerous in dev only):

```bash
kubectl delete pvc --all
```

---

# 🔍 **5. Debugging Commands**

### **Dry-run (preview without deploying)**

```bash
helm install flask-crud-release . --dry-run --debug
```

### **Render all YAML (helpful for troubleshooting)**

```bash
helm template flask-crud-release .
```

### **Check logs of pods**

```bash
kubectl logs -l app.kubernetes.io/instance=flask-crud-release
```

### **Describe resources**

```bash
kubectl describe pod <pod-name>
kubectl describe deployment <deployment-name>
kubectl describe svc <service-name>
```

---

# 🔄 **6. Reinstall (Clean Deployment)**

### Remove old release

```bash
helm uninstall flask-crud-release
```

### (optional) clean PVCs

```bash
kubectl delete pvc --all
```

### Reinstall fresh

```bash
helm install flask-crud-release . \
  --set mysqlSecret.mysqlRootPassword=password
```

---

# 📦 **7. Check What’s Running**

```bash
kubectl get pods
kubectl get svc
kubectl get deploy
kubectl get pvc
```

---

# 🌐 **8. Accessing the Flask API**

If your service is NodePort:

```bash
kubectl get svc
```

Example:

```
flask-crud-release   NodePort   5000:32000/TCP
```

Access via:

```
http://localhost:32000
```

For minikube:

```bash
minikube service flask-crud-release
```

---

# 🎉 You’re Ready!

This document now covers:

✔ Install
✔ Upgrade
✔ Delete
✔ Uninstall
✔ Reinstall
✔ PVC cleanup
✔ Debug
✔ Accessing your Flask API

