from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth
from routes import llm

app = FastAPI(title="FastAPI Demo")

# create tables (for quick demo; in prod use Alembic migrations)
models.Base.metadata.create_all(bind=database.engine)

@app.post("/users/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user_in)

@app.post("/token", response_model=schemas.Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current = Depends(auth.get_current_user)):
    return current

@app.post("/items/", response_model=schemas.ItemOut)
def create_item(item_in: schemas.ItemCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db), current = Depends(auth.get_current_user)):
    def send_notification(item_id: int):
        print(f"Sending notification for item {item_id}")
    created = crud.create_item_for_user(db, item_in, current.id)
    background_tasks.add_task(send_notification, created.id)
    return created

@app.get("/items/", response_model=list[schemas.ItemOut])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current = Depends(auth.get_current_user)):
    return crud.get_items_by_user(db, current.id, skip, limit)

# 🔥 include the LLM routes
app.include_router(llm.router)