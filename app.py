import os
import psycopg2
from flask import Flask, render_template, request, redirect

# CONFIGURACIÓN BLINDADA: Busca en ambas versiones de la carpeta
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(base_dir, 'templates')
Templates_path = os.path.join(base_dir, 'Templates')

app = Flask(__name__, template_folder=templates_path)
# Si no encuentra la carpeta en minúsculas, usa la de mayúsculas
if not os.path.exists(templates_path):
    app.template_folder = Templates_path

# URL Directa
DATABASE_URL = "postgresql://usuariosdb_czmv_user:LSbluidIePcSYm2qUQlITfSNp5fWZfiV@dpg-d720l76a2pns738cora0-a.virginia-postgres.render.com/usuariosdb_czmv"

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    try:
        con = get_db()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id SERIAL PRIMARY KEY, nombre VARCHAR(100), email VARCHAR(100), telefono VARCHAR(20), rol VARCHAR(50)
            );
        """)
        con.commit()
        con.close()
    except Exception as e:
        print(f"Error DB: {e}")

init_db()

@app.route("/")
def index():
    try:
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios ORDER BY id DESC")
        users = cur.fetchall()
        con.close()
        return render_template("index.html", users=users)
    except Exception as e:
        return f"Error: {e}. Carpeta configurada: {app.template_folder}", 500

@app.route("/add", methods=["POST"])
def add():
    n, e, t, r = request.form["nombre"], request.form["email"], request.form["telefono"], request.form["rol"]
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios (nombre,email,telefono,rol) VALUES (%s,%s,%s,%s)", (n, e, t, r))
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
    app.run()