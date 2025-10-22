from sqlalchemy.orm import Session
import models

def get_editais(db: Session, uf=None, termo=None):
    query = db.query(models.Edital)
    if uf:
        query = query.filter(models.Edital.uf == uf)
    if termo:
        query = query.filter(models.Edital.titulo.ilike(f"%{termo}%"))
    return query.all()

def salvar_editais(db: Session, lista):
    for e in lista:
        edital = models.Edital(**e)
        db.merge(edital)
    db.commit()

