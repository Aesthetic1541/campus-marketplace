# CampusMart

CampusMart is a campus-based online marketplace where students can buy and sell used items within their college community.  
The platform allows users to list products, browse available items, and connect with other students safely using college email verification.

---

## Features

- User registration with **college email verification (OTP)**
- Secure login system with **password hashing**
- Marketplace to browse approved products
- Product listing with image upload
- Admin dashboard for managing users and products
- Product approval system before items appear in the marketplace
- Clean and responsive UI

---

## Tech Stack

### Frontend
- HTML
- CSS
- Jinja Templates

### Backend
- Python
- Flask

### Database
- SQLite

### Other Libraries
- Flask-Mail
- Werkzeug

---

## Project Structure
![alt text](image-1.png)


---

## Installation and Setup

### 1. Clone the repository
git clone https://github.com/your-username/campus-marketplace.git

cd campus-marketplace


### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the application


python app.py


### 4. Open in browser


http://127.0.0.1:5000


---

## Email OTP Configuration

To enable email verification, configure the following in `app.py`.


MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 246301012@gkv.ac.in

MAIL_PASSWORD = qxnfqiobrqipjtzo




Use a **Google App Password** instead of your Gmail password.

---

## Future Improvements

- Product search functionality
- User profile page
- Wishlist feature
- Messaging between buyers and sellers
- Payment integration

---

## Author

Aditya Singh  
B.Tech Student

---

## License

This project is created for educational and portfolio purposes.
