from flask import Flask, render_template, request, redirect, url_for, flash
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_mysqldb import MySQL
from flask_mysqldb import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, template_folder="templates")
# app = Flask(__name__)
app.secret_key = "\xbb\xed\x84v\x0e\x1f\xb2\xc3\x92,0\xcak\x94\x02\xfd\x05\xac\xac\x15\x13~-z"  # Replace with a unique, secure key

# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Swetha@mysql04"
app.config["MYSQL_DB"] = "see"

mysql = MySQL(app)


# routes
@app.route("/")
def index():
    return render_template("Homepage3.html")


@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/admin_home")
def admin_homepage():
    return render_template("admin_home.html")


@app.route("/sign_up_page")
def sign_up_page():
    return render_template("Signup.html")


@app.route("/admin/users")
def admin_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id, name, age, ph_no, email FROM sign_up WHERE email != 'admin@gmail.com'"
    )
    users = cursor.fetchall()
    cursor.close()
    return render_template("admin_users.html", users=users)


@app.route("/remove_user/<int:user_id>", methods=["POST"])
def remove_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM sign_up WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("admin_users"))


@app.route("/sign_up", methods=["POST"])
def sign_up():
    name = request.form["name"]
    age = request.form["age"]
    ph_no = request.form["ph_no"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO sign_up (name, age, ph_no, email, password) VALUES (%s, %s, %s, %s, %s)",
        (name, age, ph_no, email, password),
    )
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("sign_in"))


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM sign_up WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user[5], password):
            if email == "admin@gmail.com":
                return render_template(
                    "admin_home.html"
                )  # Redirect to Admin page if admin
            elif email.endswith("officer@gmail.com"):
                return render_template(
                    "officer_Home.html"
                )  # Redirect to officer's page
            else:
                return render_template(
                    "home.html"
                )  # Redirect to home page for other users
        else:
            flash(
                "Invalid email or password", "danger"
            ) 
    return render_template("Login2.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM sign_up WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], old_password):
            hashed_password = generate_password_hash(new_password)
            cursor.execute(
                "UPDATE sign_up SET password = %s WHERE email = %s",
                (hashed_password, email),
            )
            mysql.connection.commit()
            flash("Password updated successfully", "success")
            cursor.close()
            return redirect(url_for("sign_in"))
        else:
            flash("Invalid email or old password", "danger")
            cursor.close()

    return render_template("ForgotPassword.html")


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        name = request.form["name"]
        ph_no = request.form["ph_no"]
        address = request.form["address"]
        email = request.form["email"]
        food_name = request.form["food_name"]
        food_quantity = request.form["food_quantity"]
        expiry = request.form["expiry"]
        description = request.form.get("description", "")

        food_image = request.files["food_image"]
        image_filename = None
        if food_image:
            image_filename = food_image.filename
            save_path = os.path.join("static/uploads", image_filename)
            food_image.save(save_path)

        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO surplus_food (name, ph_no, address, email, food_name, food_quantity, expiry, description, food_image, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'NOT EXPIRED')
            """,
            (
                name,
                ph_no,
                address,
                email,
                food_name,
                food_quantity,
                expiry,
                description,
                image_filename,
            ),
        )
        mysql.connection.commit()
        cursor.close()

        flash("Food donation posted successfully!", "success")
        return redirect(url_for("homepage"))

    return render_template("Donate_form.html")


@app.route("/admin_donate", methods=["GET", "POST"])
def admin_donate():
    if request.method == "POST":
        name = request.form["name"]
        ph_no = request.form["ph_no"]
        address = request.form["address"]
        email = request.form["email"]
        food_name = request.form["food_name"]
        food_quantity = request.form["food_quantity"]
        expiry = request.form["expiry"]
        description = request.form.get("description", "")

        food_image = request.files["food_image"]
        image_filename = None
        if food_image:
            image_filename = food_image.filename
            save_path = os.path.join("static/uploads", image_filename)
            food_image.save(save_path)

        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO surplus_food (name, ph_no, address, email, food_name, food_quantity, expiry, description, food_image, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'NOT EXPIRED')
            """,
            (
                name,
                ph_no,
                address,
                email,
                food_name,
                food_quantity,
                expiry,
                description,
                image_filename,
            ),
        )
        mysql.connection.commit()
        cursor.close()

        flash("Food donation posted successfully!", "success")
        return redirect(url_for("admin_homepage"))

    return render_template("admin_d_form.html")


@app.route("/donations")
def donations():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        """
        UPDATE surplus_food 
        SET status = 'EXPIRED' 
        WHERE expiry < NOW() AND status = 'NOT EXPIRED'
        """
    )
    mysql.connection.commit()

    # Fetch all food items
    cursor.execute("SELECT * FROM surplus_food WHERE status = 'NOT EXPIRED' ")
    donations = cursor.fetchall()
    cursor.close()

    return render_template("donations.html", donations=donations)


@app.route("/admin_donations")
def admin_donations():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        """
        UPDATE surplus_food 
        SET status = 'EXPIRED' 
        WHERE expiry < NOW() AND status = 'NOT EXPIRED'
        """
    )
    mysql.connection.commit()

    cursor.execute("SELECT * FROM surplus_food WHERE status = 'NOT EXPIRED' ")
    donations = cursor.fetchall()
    cursor.close()

    return render_template("admin_donations.html", donations=donations)


@app.route("/remove/<int:donation_id>", methods=["POST"])
def remove_donation(donation_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("DELETE FROM surplus_food WHERE id = %s", (donation_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("admin_donations"))


@app.route("/remove2/<int:donation_id>", methods=["POST"])
def remove_donation2(donation_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("DELETE FROM surplus_food WHERE id = %s", (donation_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("admin_agri_manure"))


@app.route("/agri_manure")
def agri_manure():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM surplus_food WHERE status = 'EXPIRED' ")
    donations = cursor.fetchall()
    cursor.close()

    return render_template("donations2.html", donations=donations)


@app.route("/admin_agri_manure")
def admin_agri_manure():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM surplus_food WHERE status = 'EXPIRED' ")
    donations = cursor.fetchall()
    cursor.close()

    return render_template("admin_donations2.html", donations=donations)


@app.route("/Donate_form")
def Donate_form():
    return render_template("Donate_form.html")


@app.route("/admin_Donate_form")
def admin_Donate_form():
    return render_template("admin_d_form.html")


@app.route("/admin")
def admin():
    return render_template("Admin_Home.html")


if __name__ == "__main__":
    app.run(debug=True)
