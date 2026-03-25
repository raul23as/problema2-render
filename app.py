import os
import psycopg2
from flask import Flask, render_template, request, redirect

# FORZAMOS A FLASK A BUSCAR LA CARPETA CON T MAYÚSCULA
app = Flask(__name__, template_folder='Templates')

# URL Directa de tu base de datos en Render
DATABASE_URL = "postgresql://usuariosdb_czmv_user:LSbluidIePcSYm2qUQlITfSNp5fWZfiV@dpg-d720l76a2pns738cora0-a.virginia-postgres.render.com/usuariosdb_czmv"

def get_db():
    # En Render es obligatorio sslmode='require'
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    """Crea la tabla si no existe"""
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
        print("Base de datos conectada con éxito")
    except Exception as e:
        print(f"Error de conexión: {e}")

# Inicializamos la DB
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
        return f"Error en el servidor: {e}", 500

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
    # Comando para correr local si lo necesitaras, pero Render usa Gunicorn
    app.run(host="0.0.0.0", port=10000)