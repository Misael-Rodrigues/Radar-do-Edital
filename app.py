from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from database import SessionLocal, engine
import models, crud, auth, utils

# Inicializa DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Radar de Editais API", version="1.0")

# Permitir acesso do Base44 (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir ao domínio do Base44 depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ROTAS ----------------

@app.post("/api/register")
def register_user(form: auth.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, form)
    return {"message": "Usuário criado com sucesso", "user": user.email}


@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/editais")
def listar_editais(uf: str = None, termo: str = None, db: Session = Depends(get_db)):
    # Busca simulada (você pode conectar ao PNCP aqui)
    editais = crud.get_editais(db, uf, termo)
    return editais


@app.post("/api/editais/coletar")
def coletar_editais(db: Session = Depends(get_db)):
    novos = utils.buscar_editais_pncp()
    crud.salvar_editais(db, novos)
    return {"message": f"{len(novos)} editais coletados com sucesso"}


# ---------------- AGENDADOR AUTOMÁTICO ----------------
scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", hour=8, minute=0)
def coleta_diaria():
    db = SessionLocal()
    novos = utils.buscar_editais_pncp()
    crud.salvar_editais(db, novos)
    db.close()
    print(f"[{datetime.datetime.now()}] Coleta diária executada: {len(novos)} editais.")

scheduler.start()

