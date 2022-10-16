from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#TOKEN DE SEGURANÇA DO SITE
app.config['SECRET_KEY'] = '496976885764c57a3b043055300cd974'

# /// = relative path, //// = absolute path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False, unique=True)
    endereco = db.Column(db.String, nullable=False)
    carros = db.relationship('Carro', backref='proprietario', lazy=True)

    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carro = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=False)
    cor = db.Column(db.String, nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    pessoa = db.relationship('Pessoa', foreign_keys=pessoa_id)

    def __init__(self, carro, modelo, cor, pessoa_id):
        self.carro = carro
        self.modelo = modelo
        self.cor = cor
        self.pessoa_id = pessoa_id

@app.route("/")
def home():
    pessoa = Pessoa.query.all()
    carro = Carro.query.all()
    return render_template("base.html", pessoa=pessoa, carro=carro)


#CRUD

#CREATE - VISUALIZAR TAREFA
@app.route("/visualizar")
def visualizar():
    pessoa = Pessoa.query.all()
    carro = Carro.query.all()
    return render_template("visualizar.html", pessoa=pessoa, carro=carro)

#CADASTRANDO CLIENTES
@app.route("/addcliente", methods=["GET", "POST"])
def addcliente():
    if request.method == "POST":
        nova_pessoa = Pessoa(request.form['nome'], request.form['cpf'], request.form['endereco'])
        db.session.add(nova_pessoa)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("addcliente.html")

#CADASTRANDO CARROS
@app.route("/addcarro", methods=["GET", "POST"])
def addcarro():
    pessoa = Pessoa.query.all()
    if request.method == "POST":
        novo_carro = Carro(request.form['carro'], request.form['modelo'], request.form['cor'], request.form['pessoa_id'])
        db.session.add(novo_carro)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("addcarro.html", pessoa=pessoa)

#UPDATE - ATUALIZAR CLIENTES
@app.route("/update/<int:pessoa_id>", methods=["GET", "POST"])
def update(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    carro = Carro.query.get(pessoa_id)
    if request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.cpf = request.form['cpf']
        pessoa.endereco = request.form['endereco']
        carro.carro = request.form['carro']
        carro.modelo = request.form['modelo']
        carro.cor = request.form['cor']
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update.html", pessoa=pessoa)

#DELETE - DELETAR CLIENTES
@app.route("/delete/<int:pessoa_id>")
def delete(pessoa_id):
    nome = Pessoa.query.filter_by(id=pessoa_id).first()
    db.session.delete(nome)
    db.session.commit()
    return redirect(url_for("home"))

with app.app_context():
    if __name__ == "__main__":
        app.run(debug=True)
        db.create_all()