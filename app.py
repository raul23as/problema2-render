import os
import psycopg2
from flask import Flask, render_template, request, redirect

# Flask busca la carpeta 'templates' por defecto
app = Flask(__name__)

# URL Directa de tu base de datos de Render
DATABASE_URL = "postgresql://usuariosdb_czmv_user:LSbluidIePcSYm2qUQlITfSNp5fWZfiV@dpg-d720l76a2pns738cora0-a.virginia-postgres.render.com/usuariosdb_czmv"

def get_db():
    # Render requiere SSL
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    try:
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
        cur.close()
        con.close()
    except Exception as e:
        print(f"Error inicializando DB: {e}")

# Crear tabla al inicio
init_db()

@app.route("/")
def index():
    try:
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios ORDER BY id DESC")
        users = cur.fetchall()
        cur.close()
        con.close()
        return render_template("index.html", users=users)
    except Exception as e:
        return f"Error en la base de datos o plantilla: {e}", 500

@app.route("/add", methods=["POST"])
def add():
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    rol = request.form["rol"]
    
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre, email, telefono, rol) VALUES (%s, %s, %s, %s)",
        (nombre, email, telefono, rol)
    )
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run()