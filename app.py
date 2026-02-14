from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "campusmart-secret-key"  # Needed for flash messages

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
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # College email validation
        if not email.endswith("@gkv.ac.in"):
            flash("Only @gkv.ac.in email IDs are allowed to register.")
            return redirect(url_for("register"))

        # TEMPORARY: no database yet
        flash("Registration successful. You can now login.")
        return redirect(url_for("login"))

    return render_template("register.html")






# ---------------- MARKETPLACE ----------------
@app.route("/marketplace")
def marketplace():
    # TODO: fetch products from database
    products = []  # placeholder
    return render_template("marketplace.html", products=products)







# ---------------- PRODUCT DETAILS ----------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):

    # Temporary dummy data (FAKE DATABASE)
    products = {
        1: {
            "name": "Data Structures Book",
            "price": 250,
            "category": "Books",
            "description": "Well-maintained book, useful for exams.",
            "seller": "Aditya"
        },
        2: {
            "name": "Scientific Calculator",
            "price": 400,
            "category": "Electronics",
            "description": "Casio calculator in good condition.",
            "seller": "Rahul"
        }
    }

    product = products.get(product_id)

    if not product:
        return "Product not found", 404

    return render_template("product_detail.html", product=product)








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
