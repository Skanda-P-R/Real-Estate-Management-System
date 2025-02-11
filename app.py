from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from send_to_groq import send_to_groq
import joblib
import numpy as np

lr_clf = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "real_estate_db"
mysql = MySQL(app)

@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.id, p.title, p.description, p.price, p.location, p.status, u.name AS owner FROM properties p JOIN users u ON p.owner_id = u.id")
    properties = cur.fetchall()
    cur.close()
    return render_template("index.html", properties=properties)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        price = request.form.get("price", "").strip()
        location = request.form.get("location_search", "").strip()

        query = (
            "SELECT p.id, p.title, p.description, p.price, p.location, p.status, u.name AS owner "
            "FROM properties p "
            "JOIN users u ON p.owner_id = u.id "
            "WHERE 1=1 "
        )

        params = []

        if title:
            query += "AND p.title LIKE %s "
            params.append(f"%{title}%")

        if location:
            query += "AND p.location LIKE %s "
            params.append(f"%{location}%")

        if price:
            query += "AND p.price = %s "
            params.append(price)

        cur = mysql.connection.cursor()
        cur.execute(query, tuple(params))
        properties = cur.fetchall()
        cur.close()

        return render_template("search.html", properties=properties)

    return render_template("search.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", (name, email, password, role))
        mysql.connection.commit()
        cur.close()
        flash("Registration Successful! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["role"] = user[4]
            if user[4] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user[4] == "owner":
                return redirect(url_for("owner_dashboard"))
            elif user[4] == "customer":
                return redirect(url_for("customer_dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties")
    properties = cur.fetchall()
    cur.close()
    return render_template("admin.html", properties=properties)

@app.route("/owner_dashboard")
def owner_dashboard():
    if session.get("role") != "owner":
        return redirect(url_for("login"))

    owner_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM properties WHERE owner_id = %s", [owner_id])
    properties = cur.fetchall()

    cur.execute("""
        SELECT u.name, p.title, b.booking_date
        FROM bookings b
        JOIN users u ON b.customer_id = u.id
        JOIN properties p ON b.property_id = p.id
        WHERE p.owner_id = %s
    """, [owner_id])
    bookings = cur.fetchall()

    cur.close()

    return render_template("owner.html", properties=properties, bookings=bookings)


@app.route("/customer")
def customer_dashboard():
    if session.get("role") != "customer":
        return redirect(url_for("login"))
    
    customer_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT p.id, p.title, p.description, p.price, p.location, p.status, u.name AS owner FROM properties p JOIN users u ON p.owner_id = u.id WHERE status = 'available'")
    properties = cur.fetchall()

    cur.execute("SELECT p.id, p.title, p.description, p.price, p.location, p.status, u.name AS owner FROM properties p, users u, bookings b WHERE p.owner_id = u.id AND p.id = b.property_id AND p.status = 'booked' AND b.customer_id = %s", [customer_id])
    bookings = cur.fetchall()

    cur.close()
    return render_template("customer.html", properties=properties, bookings=bookings)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/delete_property/<int:property_id>")
def delete_property(property_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM properties WHERE id = %s", [property_id])
    cur.execute("DELETE FROM bookings WHERE property_id = %s", [property_id])
    mysql.connection.commit()
    cur.close()
    flash("Property deleted successfully", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/add_property", methods=["POST"])
def add_property():
    if session.get("role") != "owner":
        return redirect(url_for("login"))

    title = request.form["title"]
    description = request.form["description"]
    price = request.form["price"]
    location = request.form["location"]
    owner_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO properties (title, description, price, location, owner_id) VALUES (%s, %s, %s, %s, %s)",
                (title, description, price, location, owner_id))
    mysql.connection.commit()
    cur.close()

    flash("Property added successfully", "success")
    return redirect(url_for("owner_dashboard"))

@app.route("/book_property/<int:property_id>")
def book_property(property_id):
    if session.get("role") != "customer":
        return redirect(url_for("login"))

    customer_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bookings (customer_id, property_id) VALUES (%s, %s)", (customer_id, property_id))
    cur.execute("UPDATE properties SET status = 'booked' WHERE id = %s", [property_id])
    mysql.connection.commit()
    cur.close()

    flash("Property booked successfully!", "success")
    return redirect(url_for("customer_dashboard"))

@app.route("/cancel_property/<int:property_id>")
def cancel_property(property_id):
    if session.get("role") != "customer":
        return redirect(url_for("login"))

    customer_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM bookings WHERE customer_id = %s AND property_id = %s", (customer_id, property_id))
    cur.execute("UPDATE properties SET status = 'available' WHERE id = %s", [property_id])
    mysql.connection.commit()
    cur.close()

    flash("Property canceled successfully!", "success")
    return redirect(url_for("customer_dashboard"))

@app.route('/get_response', methods=['POST'])
def get_response():
    user_prompt = request.form['user_prompt']
    groq_response = send_to_groq(user_prompt)
    return jsonify({'response': groq_response})

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form['location']
    sqft = request.form['sqft']
    bath = request.form['bath']
    bhk = request.form['bhk']

    def predict_price(location,sqft,bath,bhk):
        loc_index = np.where(columns==location)[0][0]

        x = np.zeros(len(columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index>=0:
            x[loc_index] = 1

        return lr_clf.predict([x])[0]
    
    predicted_price = predict_price(location,sqft,bath,bhk)

    return jsonify({'Predicted_Price': predicted_price})

if __name__ == "__main__":
    app.run(debug=True)
