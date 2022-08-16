from flask import Flask, make_response, render_template, request, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost:3306/miauCommerce"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#INSTANCIAR OBJETO
miauCommerce = SQLAlchemy(app)

#PARA CADA TABELA DO BANCO CRIAR UMA CLASSE

class Usuario(miauCommerce.Model):
    id = miauCommerce.Column("usuario_id", miauCommerce.Integer, primary_key=True)
    nome = miauCommerce.Column("usuario_nome",miauCommerce.String(256))
    email = miauCommerce.Column("usuario_email",miauCommerce.String(256))
    senha = miauCommerce.Column("usuario_senha",miauCommerce.String(256))
    endereco = miauCommerce.Column("usuario_endereco",miauCommerce.String(256))

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco

class Categoria(miauCommerce.Model):
    id = miauCommerce.Column("categ_id", miauCommerce.Integer, primary_key=True)
    nome = miauCommerce.Column("categ_nome",miauCommerce.String(256))
    descricao = miauCommerce.Column("categ_descricao",miauCommerce.String(256))

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

class Anuncio(miauCommerce.Model):
    id = miauCommerce.Column("anuncio_id", miauCommerce.Integer, primary_key=True)
    nome = miauCommerce.Column("anuncio_nome",miauCommerce.String(256))
    descricao = miauCommerce.Column("anuncio_descricao",miauCommerce.String(256))
    qtde = miauCommerce.Column("anuncio_qtde",miauCommerce.Integer)
    preco = miauCommerce.Column("anuncio_preco",miauCommerce.Float)
    categ_id = miauCommerce.Column("categ_id",miauCommerce.Integer, miauCommerce.ForeignKey("categoria.categ_id"))
    usuario_id = miauCommerce.Column("usuario_id",miauCommerce.Integer, miauCommerce.ForeignKey("usuario.usuario_id"))

    def __init__(self, nome, descricao, qtde, preco, categ_id, usuario_id) :
        self.nome = nome
        self.descricao = descricao
        self.qtde = qtde
        self.preco = preco
        self.categ_id = categ_id
        self.usuario_id = usuario_id


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro/usuario")
def usuario():
    return render_template("usuario.html", usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")

@app.route("/usuario/novo", methods=["POST"])
def novousuario():
    usuario = Usuario(request.form.get("nome"), request.form.get("email"), request.form.get("senha"), request.form.get("endereco"))
    miauCommerce.session.add(usuario)
    miauCommerce.session.commit()
    return redirect(url_for('usuario'))

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
        miauCommerce.session.add(usuario)
        miauCommerce.session.commit()
        return redirect(url_for('usuario'))
    return render_template("editusuario.html", usuario = usuario, titulo=" Usuário")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    miauCommerce.session.delete(usuario)
    miauCommerce.session.commit()
    return redirect(url_for('usuario'))

@app.route("/cadastro/anuncio")
def anuncio():
    return render_template("anuncios.html", anuncios = Anuncio.query.all(), titulo="Cadastro de Anúncio")

@app.route("/anuncio/novo", methods=["POST"])
def novouanuncio():
    anuncio = Anuncio(request.form.get("nome"), request.form.get("descricao"), request.form.get("qtde"), request.form.get("preco"), request.form.get("categ_id"), request.form.get("usuario_id"))
    miauCommerce.session.add(anuncio)
    miauCommerce.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/editar/<int:id>", methods = ['GET', 'POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome = request.form.get('nome')
        anuncio.descricao = request.form.get('descricao')
        anuncio.qtde = request.form.get('qtde')
        anuncio.preco = request.form.get('preco')
        anuncio.categ_id = request.form.get('categ_id')
        anuncio.usuario_id = request.form.get('usuario_id')
        miauCommerce.session.add(anuncio)
        miauCommerce.session.commit()
        return redirect(url_for('anuncio'))
    return render_template("editanuncio.html", anuncio = anuncio, titulo=" Anuncio")

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    miauCommerce.session.delete(anuncio)
    miauCommerce.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/config/categoria")
def categoria():
    return render_template("categoria.html", categorias = Categoria.query.all(), titulo="Categoria")

@app.route("/categoria/novo", methods=["POST"])
def novacategoria():
    categoria = Categoria(request.form.get("nome"), request.form.get("descricao"))
    miauCommerce.session.add(categoria)
    miauCommerce.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods = ['GET', 'POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.descricao = request.form.get('descricao')
        miauCommerce.session.add(categoria)
        miauCommerce.session.commit()
        return redirect(url_for('categoria'))
    return render_template("editcategoria.html", categoria = categoria, titulo=" Categoria")

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    miauCommerce.session.delete(categoria)
    miauCommerce.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorio/vendas")
def relVendas():
    return render_template("relVendas.html")

@app.route("/relatorio/compras")
def relCompras():
    return render_template("relCompras.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template("pergunta.html")

@app.route("/anuncios/compra")
def compra():
    return render_template("anunciosCompra.html")

@app.route("/anuncios/favoritos")
def favoritos():
    return render_template("favoritos.html")

@app.route("/ofertas")
def ofertas():
    return render_template("ofertas.html")

@app.route("/user/<username>")
def username(username):
# escape transformou a variavel username em texto
    print("O que foi passado ", username)
    cok = make_response("<h2>cookie criado</h2")
    cok.set_cookie("username", username)
    return cok

@app.route("/user2/")
@app.route("/user2/<username>")
def username2(username=None):
# render _template é a rota para a pagina html
    cokUsername = request.cookies.get("username")
    print(cokUsername)
    return render_template("user.html",username = username, cokUsername = cokUsername)

if __name__ == 'app':
    app.run(debug=True)
    miauCommerce.create_all()


#servidor do heroku - publicação