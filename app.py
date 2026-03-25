from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

# Si no existe (modo local) usa tu postgres local
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:1234@localhost:5432/usuariosdb"


def get_db():
    # Si es Render usa SSL
    if "render.com" in DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        return psycopg2.connect(DATABASE_URL)


def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        email VARCHAR(100),
        telefono VARCHAR(20),
        rol VARCHAR(50)
    );
    """)
    con.commit()
    con.close()

init_db()


@app.route("/")
def index():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios ORDER BY id DESC")
    users = cur.fetchall()
    con.close()
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add():
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    rol = request.form["rol"]

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre,email,telefono,rol) VALUES (%s,%s,%s,%s)",
        (nombre, email, telefono, rol)
    )
    con.commit()
    con.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    con.commit()
    con.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)