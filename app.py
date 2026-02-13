from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- AUTH ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: login logic
        return redirect(url_for("marketplace"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: registration logic
        return redirect(url_for("login"))
    return render_template("register.html")

# ---------------- MARKETPLACE ----------------
@app.route("/marketplace")
def marketplace():
    # TODO: fetch products from database
    products = []  # placeholder
    return render_template("marketplace.html", products=products)

# ---------------- ADD PRODUCT ----------------
@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        # TODO: save product to database
        return redirect(url_for("marketplace"))
    return render_template("add_product.html")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
