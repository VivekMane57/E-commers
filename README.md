# E-commers
Django-based e-commerce platform with product catalog, cart, checkout, and Razorpay integration. 🎉 Special feature: when 2 or more friends shop together, they can split bills and unlock exclusive rewards &amp; discounts for group shopping.

# 🛍️ BuyTogether - E-Commerce Platform

BuyTogether is a full-stack Django e-commerce platform with Razorpay integration.  
It allows users to shop online, manage carts, checkout securely, and even **split bills with friends**.  
When friends shop together, they unlock **special benefits and rewards**.

---

## 🚀 Features
- 👤 User registration, login, profile, referral system  
- 🛒 Add to cart, update, remove items  
- 📦 Place orders, track orders, view order history  
- 💳 Secure payments with Razorpay (split billing option for friends)  
- 🎁 Rewards and benefits when 2+ friends shop together  
- 📧 Email notifications for account and order updates  
- 🔐 Authentication and password reset flows  

---

## ⚙️ Tech Stack
- **Backend:** Django, SQLite (dev)  
- **Frontend:** HTML, CSS, Bootstrap, jQuery  
- **Payments:** Razorpay API  
- **Other:** Crispy Forms, Session Management, Referrals  

---

## 🖥️ Installation
```bash
# Clone the repo
git clone https://github.com/VivekMane57/E-commers.git
cd E-commers

# Create virtual environment
python -m venv env
env\Scripts\activate  # (Windows)
source env/bin/activate  # (Linux/Mac)

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
