from database import db


class Libro(db.Model):
    isbn=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    autor = db.Column(db.String(100))
    year = db.Column(db.Integer)
#Retornar un string
def __str__(self):
        return (
            f'ISBN: {self.isbn} , '
            f'Nombre: {self.nombre}, '
            f'Autor: {self.autor}, '
            f'Año: {self.year}'
        )


