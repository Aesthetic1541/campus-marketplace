from flask import Flask, render_template, request, redirect, url_for, flash, session

from database import insert_user, get_user_by_email, create_users_table, insert_product, create_products_table

from functools import wraps

app = Flask(__name__)
app.secret_key = "campusmart-secret-key"  # Needed for flash messages

create_users_table()
create_products_table()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("LOGIN_REQUIRED CHECK RUNNING")  # 👈 DEBUG LINE
        if "user_id" not in session:
            print("USER NOT LOGGED IN")
            flash("Please login first.")
            return redirect(url_for("login"))
        print("USER LOGGED IN")
        return f(*args, **kwargs)
    return decorated_function

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")







# ---------------- AUTH ----------------

# ----------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)

        # If user does not exist or password is wrong
        if not user or user["password"] != password:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        # Login successful
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        flash("Login successful.")
        return redirect(url_for("marketplace"))

    return render_template("login.html")



# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # 1. College email validation
        if not email.endswith("@gkv.ac.in"):
            flash("Only @gkv.ac.in email IDs are allowed to register.")
            return redirect(url_for("register"))

        # 2. Check if email already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("This email is already registered.")
            return redirect(url_for("register"))

        # 3. Insert user into database
        insert_user(name, email, password)

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")






# ---------------- MARKETPLACE ----------------
@app.route("/marketplace")
@login_required
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
@login_required
def add_product():
    if "user_id" not in session:
        flash("Please login to add a product.")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        category = request.form.get("category")
        description = request.form.get("description")
        condition = request.form.get("condition")

        insert_product(
            title=title,
            price=price,
            category=category,
            description=description,
            condition=condition,
            user_id=session["user_id"]
        )

        flash("Product submitted for approval.")
        return redirect(url_for("marketplace"))

    return render_template("add_product.html")


# ---Logout route ----
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))







@app.route("/force-logout")
def force_logout():
    session.clear()
    return "SESSION CLEARED"



# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)



