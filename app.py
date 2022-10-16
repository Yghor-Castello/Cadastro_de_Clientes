from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from forms import FormCadastrarCliente, FormCadastrarCarros


app = Flask(__name__)

#TOKEN DE SEGURANÇA DO SITE
app.config['SECRET_KEY'] = '496976885764c57a3b043055300cd974'

# /// = relative path, //// = absolute path

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Pessoa(db.Model):
    __tablename__ = "pessoa"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(11))
    endereco = db.Column(db.String(150))
    carros = db.relationship('Carro', backref='proprietario', lazy=True)

    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco


class Carro(db.Model):
    __tablename__ = "carro"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    carro = db.Column(db.String(30))
    modelo = db.Column(db.String(30))
    cor = db.Column(db.String(30))
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))

    pessoa = db.relationship("Pessoa", foreign_keys=pessoa_id)

    def __init__(self, pessoa_id, carro, modelo, cor):
        self.pessoa_id = pessoa_id
        self.carro = carro
        self.modelo = modelo
        self.cor = cor

@app.route("/")
def home():
    # form_cliente = FormCadastrarCliente
    # form_carro = FormCadastrarCarros
    # if form_cliente.validate_on_submit():
    #     #fez o cadastro com sucesso
    #
    # if form_carro.validate_on_submit():
    #     # fez o cadastro com sucesso
    pessoa = Pessoa.query.all()
    carro = Carro.query.all()
    # return render_template("base.html", form_cliente=form_cliente, form_carro=form_carro)
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
    if request.method == "POST":
        pessoa_id = Carro(request.form['pessoa_id'])
        novo_carro = Carro(request.form['carro'], request.form['modelo'], request.form['cor'])
        db.session.add(pessoa_id, novo_carro)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("addcarro.html")

#UPDATE - ATUALIZAR CLIENTES
@app.route("/update/<int:pessoa_id>", methods=["GET", "POST"])
def update(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    if request.method == "POST":
        pessoa.nome = request.form['nome']
        pessoa.cpf = request.form['cpf']
        pessoa.endereco = request.form['endereco']
        pessoa.carro = request.form['carro']
        pessoa.modelo = request.form['modelo']
        pessoa.cor = request.form['cor']
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
        db.create_all()
        app.run(debug=True) #responsavel por atualizar o site em toda modificação


