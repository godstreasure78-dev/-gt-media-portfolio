from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    send_from_directory
)
import sqlite3
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Used to protect login sessions
app.secret_key = "gt-media-change-this-later"

DATABASE = "gt_media.db"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Make sure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ==============================
# SERVE UPLOADED IMAGES
# ==============================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==============================
# PUBLIC HOME / PORTFOLIO
# ==============================

@app.route("/")
def home():

    connection = get_db()

    designs = connection.execute(
        "SELECT * FROM designs ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        designs=designs
    )


# ==============================
# ADMIN LOGIN
# ==============================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    # If already logged in, go straight to dashboard
    if "admin_id" in session:
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        connection = get_db()

        admin = connection.execute(
            "SELECT * FROM admins WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if admin and check_password_hash(
            admin["password"],
            password
        ):

            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]

            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin/dashboard")
def dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db()

    designs = connection.execute(
        "SELECT * FROM designs ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        designs=designs,
        admin_username=session.get("admin_username")
    )


# ==============================
# ADD DESIGN
# ==============================

@app.route("/admin/add-design", methods=["GET", "POST"])
def add_design():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["designTitle"]
        category = request.form["designCategory"]
        description = request.form["designDescription"]

        image = request.files.get("designImage")

        if image and image.filename:

            filename = image.filename

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image.save(image_path)

            connection = get_db()

            connection.execute(
                """
                INSERT INTO designs
                (title, category, description, image)
                VALUES (?, ?, ?, ?)
                """,
                (
                    title,
                    category,
                    description,
                    filename
                )
            )

            connection.commit()
            connection.close()

            return redirect(url_for("dashboard"))

    return render_template("add-design.html")


# ==============================
# DELETE DESIGN
# ==============================

@app.route(
    "/admin/delete-design/<int:design_id>",
    methods=["POST"]
)
def delete_design(design_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db()

    design = connection.execute(
        "SELECT * FROM designs WHERE id = ?",
        (design_id,)
    ).fetchone()

    if design:

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            os.path.basename(design["image"])
        )

        connection.execute(
            "DELETE FROM designs WHERE id = ?",
            (design_id,)
        )

        connection.commit()

        # Delete the image file from uploads folder
        if os.path.exists(image_path):
            os.remove(image_path)

    connection.close()

    return redirect(url_for("dashboard"))


# ==============================
# EDIT DESIGN
# ==============================

@app.route(
    "/admin/edit-design/<int:design_id>",
    methods=["GET", "POST"]
)
def edit_design(design_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_db()

    design = connection.execute(
        "SELECT * FROM designs WHERE id = ?",
        (design_id,)
    ).fetchone()

    if not design:
        connection.close()
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        title = request.form["designTitle"]
        category = request.form["designCategory"]
        description = request.form["designDescription"]

        image = request.files.get("designImage")

        # ==============================
        # NEW IMAGE SELECTED
        # ==============================

        if image and image.filename:

            old_image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                os.path.basename(design["image"])
            )

            new_filename = image.filename

            new_image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                new_filename
            )

            image.save(new_image_path)

            # Remove old image
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            connection.execute(
                """
                UPDATE designs
                SET title = ?,
                    category = ?,
                    description = ?,
                    image = ?
                WHERE id = ?
                """,
                (
                    title,
                    category,
                    description,
                    new_filename,
                    design_id
                )
            )

        # ==============================
        # NO NEW IMAGE
        # ==============================

        else:

            connection.execute(
                """
                UPDATE designs
                SET title = ?,
                    category = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    title,
                    category,
                    description,
                    design_id
                )
            )

        connection.commit()
        connection.close()

        return redirect(url_for("dashboard"))

    connection.close()

    return render_template(
        "edit-design.html",
        design=design
    )


# ==============================
# LOGOUT
# ==============================

@app.route("/admin/logout")
def logout():

    session.clear()

    return redirect(url_for("admin_login"))


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)