from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from models import Libro
from database import db
from WTForms import LibroForm

app= Flask(__name__)

#Configurar BD
USER_DB= 'postgres'
PASS_DB='admin'
URL_DB='localhost'
NAME_DB='CRUDLibros'
FULL_URL_DB=f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
app.config['SQLALCHEMY_DATABASE_URI']= FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SECRET_KEY']='llave-secreta'
db.init_app(app)

#configurar flask-migrate para realizar la migración
migrate=Migrate()
migrate.init_app(app,db)

@app.route('/index')
@app.route('/')
def index():
    libro=Libro.query.order_by('isbn')
    numLibros=Libro.query.count()
    app.logger.debug(f"Total de libros: {numLibros}")
    return render_template('index.html', listaLibros=libro, numLibros=numLibros)

#Consultar un libro  por su isbn
@app.route('/ver/<int:isbn>')
def ver_individual(isbn):
    #Consulta para manejar el error 404
    libro=Libro.query.get_or_404(isbn)
    return render_template('individual.html', libro=libro)

@app.route('/agregar',methods=['GET','POST'])
def agregar():
    libro=Libro()
    libroForm= LibroForm(obj=libro)
    if request.method=="POST":
        if libroForm.validate_on_submit():
            #copiar los datos de persona
            libroForm.populate_obj(libro)
            #añadir a la DB
            db.session.add(libro)
            #sube los cambios
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('agregar.html',forma=libroForm)

@app.route('/eliminar/<int:isbn>', methods=["GET", "POST"])
def eliminar (isbn):
    libro=Libro.query.get_or_404(isbn)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:isbn>', methods=["GET", "POST"])
def editar(isbn):
    libro=Libro.query.get_or_404(isbn)
    libroForm= LibroForm(obj=libro)
    if libroForm.validate_on_submit():
        libroForm.populate_obj(libro)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', forma=libroForm)