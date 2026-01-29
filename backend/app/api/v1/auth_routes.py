from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.auth import CustomerSignupIn, LoginIn, TokenOut
from app.auth.security import hash_password, verify_password
from app.auth.tokens import create_access_token
from app.models.customer_user import CustomerUser
from app.models.admin_user import AdminUser

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/customer/signup", response_model=TokenOut)
def customer_signup(payload: CustomerSignupIn, db: Session = Depends(get_db)):
    existing = db.query(CustomerUser).filter(CustomerUser.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = CustomerUser(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        phone=payload.phone,
        is_verified=False,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id), role="CUSTOMER")
    return TokenOut(access_token=token)

@router.post("/customer/login", response_model=TokenOut)
def customer_login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(CustomerUser).filter(CustomerUser.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_access_token(subject=str(user.id), role="CUSTOMER")
    return TokenOut(access_token=token)

@router.post("/admin/login", response_model=TokenOut)
def admin_login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Admin is inactive")

    token = create_access_token(subject=str(user.id), role="ADMIN")
    return TokenOut(access_token=token)
