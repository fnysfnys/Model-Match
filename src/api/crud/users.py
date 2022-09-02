from sqlalchemy.orm import Session

from .. import models, auth, schemas

def create_user(db: Session, user: schemas.users.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        permissions=user.permissions
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
        ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_password(
    db: Session,
    current_user: schemas.users.User,
    new_password: schemas.users.NewPassword
    ):
    hashed_password = auth.get_password_hash(new_password.password)
    db_user = get_user_by_email(db, current_user.email)
    db_user.hashed_password=hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user
