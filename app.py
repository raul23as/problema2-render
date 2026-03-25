import os
import psycopg2
from flask import Flask, render_template, request, redirect

# Configuramos Flask para que busque en 'templates' (minúsculas) o 'Templates' (mayúsculas)
# Para asegurar éxito en el laboratorio, intentamos registrar la ruta absoluta
template_dir = os.path.abspath('Templates')
if not os.path.exists(template_dir):
    template_dir = os.path.abspath('templates')

app = Flask(__name__, template_folder=template_dir)

# URL Directa de tu base de datos de Render
DATABASE_URL = "postgresql://usuariosdb_czmv_user:LSbluidIePcSYm2qUQlITfSNp5fWZfiV@dpg-d720l76a2pns738cora0-a.virginia-postgres.render.com/usuariosdb_czmv"

def get_db():
    # Render requiere SSL activo
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    """Crea la tabla si no existe al arrancar"""
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
        print("--- Conexión a Base de Datos: EXITOSA ---")
    except Exception as e:
        print(f"--- ERROR DE CONEXIÓN: {e} ---")

# Inicializar tabla
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
        # Si falla el HTML, esto nos dirá qué carpeta está buscando Flask
        return f"Error: {e}. Flask buscando en: {app.template_folder}", 500

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
    # Render usa Gunicorn, pero esto sirve para local
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)