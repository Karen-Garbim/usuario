from flask import Flask, make_response, render_template, request, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost:3306/usuario"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column("usuario_id", db.Integer, primary_key=True)
    nome = db.Column("usuario_nome",db.String(256))
    email = db.Column("usuario_email",db.String(256))
    senha = db.Column("usuario_senha",db.String(256))
    endereco = db.Column("usuario_endereco",db.String(256))

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco


@app.route("/")
def index():
    return render_template("index.html", titulo='Usuário')

@app.route("/cadastro/usuario")
def usuario():
    return render_template("usuario.html", titulo='Usuário')

@app.route("/usuario/novo", methods=["POST"])
def novousuario():
    usuario = Usuario(request.form.get("nome"), request.form.get("email"), request.form.get("senha"), request.form.get("endereco"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('relUsuario'))

@app.route("/usuario/detalhes/<int:id>")
def buscausuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods = ['GET', 'POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('senha')
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('relUsuario'))
    return render_template("editusuario.html", usuario = usuario, titulo=" Usuário")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('relUsuario'))

@app.route("/relatorio/usuarios")
def relUsuario():
    return render_template("relusuario.html", usuarios = Usuario.query.all(), titulo="Usuários")

if __name__ == 'app':
    db.create_all()


#servidor do heroku - publicação
