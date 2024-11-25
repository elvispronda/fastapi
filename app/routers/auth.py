from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils


router = APIRouter(tags=['Authentification'])
@router.post("/login")
def login(user_credentials :schemas.UserLogin, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Inalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Invalid credentials")
    
    
    return {"token": "example token"}