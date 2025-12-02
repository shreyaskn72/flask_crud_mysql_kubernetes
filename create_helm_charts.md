Here are **the exact steps** to install **Helmify inside GitHub Codespaces** (Ubuntu environment).

Codespaces runs Linux, so installation is easy.

---

# ✅ **Step 1 — Install Helm (required)**

Open the Terminal in Codespaces and run:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify:

```bash
helm version
```

---

# ✅ **Step 2 — Install Go (required for Helmify)**

Helmify is written in Go. You must install Go first.

```bash
sudo apt update
sudo apt install -y golang-go
```

Verify:

```bash
go version
```

You should see something like:
`go version go1.21 linux/amd64`

---

# ✅ **Step 3 — Install Helmify using Go**

Run:

```bash
go install github.com/arttor/helmify/cmd/helmify@latest
```

This will install the binary at:

```
/home/codespace/go/bin/helmify
```

Add it to PATH:

```bash
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

Verify the installation:

```bash
helmify --help
```

🎉 You should now see Helmify CLI instructions.

---

# ✅ **Step 4 — Use Helmify to generate chart**

Assuming your folder structure is:

```
flask-crud/
   k8s/
       deployment.yaml
       service.yaml
       configmap.yaml
       secret.yaml
```

Run:

```bash
cd flask-crud
helmify -f ./k8s flask-crud-chart
```

This will create a folder:

```
flask-crud-chart/
  Chart.yaml
  values.yaml
  templates/
```

---

