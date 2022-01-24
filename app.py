from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db_session

import cryptocode

senha_padrao = 'opa'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_clientes_mentorstec.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class InsertDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    pw_cliente = db.Column(db.String(100))

@app.route('/')
def home():
    users = InsertDB.query.all()
    return render_template("gc.html", users=users)  

@app.route("/add", methods=["POST"])
def add():
    id_cliente = request.form.get("id_cliente")
    user_name = request.form.get("user_name")
    pw_cliente = request.form.get("pw_cliente")
    senha_cript = cryptocode.encrypt(pw_cliente, senha_padrao) 
    new_cliente = InsertDB(id_cliente=id_cliente, user_name=user_name, pw_cliente=senha_cript)
    db.session.add(new_cliente)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:id>", methods =['GET', 'POST'])
def edit(id):
    cliente = InsertDB.query.filter_by(id=id).first()
    if request.method == 'POST':
        cliente.id_cliente = request.form['id_cliente']
        cliente.user_name = request.form['user_name']
        senha_antiga = request.form['pw_cliente']
        cliente.pw_cliente = cryptocode.encrypt(senha_antiga, senha_padrao)  
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", users=cliente)


@app.route("/delete/<int:id_cliente>")
def delete(id_cliente):
    cliente = InsertDB.query.filter_by(id=id_cliente).first()
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for("home"))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    def decode(senha):
        return cryptocode.decrypt(senha, senha_padrao)

    CORS(app)
    app.jinja_env.globals.update(decode=decode)
    db.create_all()
    app.run(debug=True, host='0.0.0.0')