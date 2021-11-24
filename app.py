from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from werkzeug.utils import redirect
app = Flask(__name__)

db = SQLAlchemy(app);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/notas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Notas(db.Model):
    '''Clase Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self, tituloNota, cuerpoNota):
        
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    objeto = {"nombre": "Gerardo",
              "apellido": "Toscano"
    }
    nombre = "Gerardo"
    lista_nombre = ["Gerardo", "Diego", "Irving", "Jair" ]
    return render_template("index.html", variable = lista_nombre)
        
@app.route("/about")
def about():
    return render_template("about.html")  

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    notaNueva = Notas(tituloNota = campotitulo, cuerpoNota = campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()

    return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo)
    #return "Nota creada" + campotitulo + " " + campocuerpo
    
@app.route("/leernotas")
def leernotas():
    consulta_notas= Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        print(nota.tituloNota)
        print(nota.cuerpoNota)

    #return "Notas consultadas"
    return render_template("index.html", consulta = consulta_notas)

    

@app.route("/eliminarnota/<ID>")
def eliminar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).delete()
    print(nota)
    db.session.commit()
    return render_template("index.html")



@app.route("/modificar", methods=['POST'])
def modificarnota():
    idnota = request.form['idnota']
    ntitulo = request.form['campotitulo']
    ncuerpo = request.form['campocuerpo']
    nota = Notas.query.filter_by(idNota = int(idnota)).first()
    nota.tituloNota = ntitulo
    nota.cuerpoNota = ncuerpo
    db.session.commit()
    return redirect("/leernotas")

@app.route("/editarnota/<ID>")
def editar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    
    return render_template("modificar.html", nota = nota)

if __name__ == "__main__":
    db.create_all()
    app.run()
    