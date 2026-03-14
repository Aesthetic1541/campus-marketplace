from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from database import (
    insert_user,
    get_user_by_email,
    create_users_table,
    insert_product,
    create_products_table,
    get_all_products,
    get_product_by_id,
    get_all_users,
    delete_product,
    delete_user,
    get_pending_products,
    get_connection,
    get_approved_products
)

app = Flask(__name__)
app.secret_key = "campusmart-secret-key"


# =========================================
# DATABASE INITIALIZATION
# =========================================

create_users_table()
create_products_table()


# =========================================
# LOGIN REQUIRED DECORATOR
# =========================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login first.")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)

        if not user or not check_password_hash(user["password"], password):
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["role"] = user["role"]

        flash("Login successful.")

        return redirect(url_for("marketplace"))

    return render_template("login.html")


# =========================================
# REGISTER
# =========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        if not email.endswith("@gkv.ac.in"):
            flash("Only @gkv.ac.in email IDs allowed.")
            return redirect(url_for("register"))

        existing_user = get_user_by_email(email)

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        insert_user(
            name,
            email,
            hashed_password
        )

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# =========================================
# MARKETPLACE
# =========================================

@app.route("/marketplace")
@login_required
def marketplace():

    products = get_approved_products()

    return render_template(
        "marketplace.html",
        products=products
    )


# =========================================
# PRODUCT DETAILS
# =========================================

@app.route("/product/<int:product_id>")
def product_detail(product_id):

    product = get_product_by_id(product_id)

    if not product:
        return "Product not found", 404

    return render_template(
        "product_detail.html",
        product=product
    )


# =========================================
# ADD PRODUCT
# =========================================

@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        title = request.form.get("title")
        price_str = request.form.get("price")
        category = request.form.get("category")
        description = request.form.get("description")
        condition = request.form.get("condition")

        try:
            price = float(price_str)

            if price < 0:
                flash("Price cannot be negative.")
                return redirect(url_for("add_product"))

        except:
            flash("Invalid price format.")
            return redirect(url_for("add_product"))

        image_file = request.files.get("image")
        image_filename = None

        if image_file and image_file.filename != "":

            image_filename = secure_filename(image_file.filename)

            upload_folder = os.path.join(app.root_path, "static/uploads")
            os.makedirs(upload_folder, exist_ok=True)

            image_path = os.path.join(upload_folder, image_filename)

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


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("login"))


# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route("/admin")
@login_required
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect(url_for("login"))

    products = get_all_products()
    users = get_all_users()
    pending_products = get_pending_products()

    return render_template(
        "admin.html",
        products=products,
        users=users,
        pending_products=pending_products
    )


# =========================================
# ADMIN DELETE PRODUCT
# =========================================

@app.route("/delete_product/<int:id>")
@login_required
def delete_product_route(id):

    if session.get("role") != "admin":
        return "Unauthorized"

    delete_product(id)

    return redirect(url_for("admin_dashboard"))


# =========================================
# ADMIN DELETE USER
# =========================================

@app.route("/delete_user/<int:id>")
@login_required
def delete_user_route(id):

    if session.get("role") != "admin":
        return "Unauthorized"

    delete_user(id)

    return redirect(url_for("admin_dashboard"))


# =========================================
# ADMIN APPROVE PRODUCT
# =========================================

@app.route("/approve_product/<int:id>")
@login_required
def approve_product_route(id):

    if session.get("role") != "admin":
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET status = 'approved'
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)