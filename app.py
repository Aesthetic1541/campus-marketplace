from flask import session, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, flash, session

from database import insert_user, get_user_by_email, create_users_table, insert_product, create_products_table
from database import get_all_products, get_product_by_id
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "campusmart-secret-key"  # Needed for flash messages

create_users_table()
create_products_table()


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
        confirm_password = request.form.get("confirm_password")

        # 🔹 1. Check passwords match
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        # 🔹 2. College email validation
        if not email.endswith("@gkv.ac.in"):
            flash("Only @gkv.ac.in email IDs are allowed.")
            return redirect(url_for("register"))

        # 🔹 3. Check existing user
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("This email is already registered.")
            return redirect(url_for("register"))

        # 🔹 4. Insert user
        insert_user(name, email, password)

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- MARKETPLACE ----------------
@app.route("/marketplace")
@login_required
def marketplace():
    products = get_all_products()
    return render_template("marketplace.html", products=products)


# ---------------- PRODUCT DETAILS ----------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product_by_id(product_id)

    if not product:
        return "Product not found", 404

    return render_template("product_detail.html", product=product)


# ---------------- ADD PRODUCT ----------------
@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        title = request.form.get("title")
        price_str = request.form.get("price")
        category = request.form.get("category")
        description = request.form.get("description")
        condition = request.form.get("condition")

        # --- NEW VALIDATION CONDITION ---
        try:
            price = float(price_str)
            if price < 0:
                flash("Price cannot be negative. Please enter a valid amount.")
                return redirect(url_for("add_product"))
        except (ValueError, TypeError):
            flash("Invalid price format. Please enter a number.")
            return redirect(url_for("add_product"))
        # --------------------------------

        image_file = request.files.get("image")

        image_filename = None

        if image_file and image_file.filename != "":
            image_filename = secure_filename(image_file.filename)
            os.makedirs("static/uploads", exist_ok=True)
            image_path = os.path.join("static/uploads", image_filename)
            image_file.save(image_path)

        insert_product(
            title=title,
            price=price,
            category=category,
            description=description,
            condition=condition,
            image=image_filename,
            user_id=session["user_id"]
        )

        flash("Product submitted successfully.")
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
