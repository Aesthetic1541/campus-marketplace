import sqlite3

DB_NAME = "campusmart.db"


# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# USERS TABLE
# =====================================================

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT USER ----------------
def insert_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, 'user')
    """, (name, email, password))

    conn.commit()
    conn.close()


# ---------------- GET USER BY EMAIL ----------------
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()
    return user


# ---------------- GET ALL USERS ----------------
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()
    return users


# ---------------- DELETE USER ----------------
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


# ---------------- PROMOTE USER TO ADMIN ----------------
# def make_admin(email):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         UPDATE users
#         SET role = 'admin'
#         WHERE email = ?
#     """, (email,))

#     conn.commit()
#     conn.close()


# =====================================================
# PRODUCTS TABLE
# =====================================================

def create_products_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            condition TEXT,
            image TEXT,
            status TEXT DEFAULT 'approved',
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT PRODUCT ----------------
def insert_product(title, price, category, description, condition, image, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products
        (title, price, category, description, condition, image, status, user_id)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (title, price, category, description, condition, image, user_id))

    conn.commit()
    conn.close()


# ---------------- GET ALL PRODUCTS ----------------
def get_all_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        ORDER BY id DESC
    """)

    products = cursor.fetchall()

    conn.close()
    return products

# ---------------- GET ALL PENDING PRODUCTS ----------------
def get_pending_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM products
        WHERE status = 'pending'
        ORDER BY id DESC
    """)

    products = cursor.fetchall()

    conn.close()
    return products


# ---------------- GET ALL APPROVED PRODUCTS ----------------
def get_approved_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE status='approved'
        ORDER BY id DESC
    """)

    products = cursor.fetchall()

    conn.close()
    return products

# ---------------- GET PRODUCT BY ID ----------------
def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()
    return product

# ---------------- APPROVE PRODUCT ----------------
def approve_product(product_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET status='approved'
        WHERE id=?
    """, (product_id,))

    conn.commit()
    conn.close()


# ---------------- DELETE PRODUCT ----------------
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()