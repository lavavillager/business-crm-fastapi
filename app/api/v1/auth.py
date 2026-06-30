from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead
from app.services.activity import ActivityService
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
def register(data: UserCreate, db: Session = Depends(get_db)) -> User:
    user = AuthService(db).register(data)
    ActivityService(db).log(
        user_id=user.id, action="register", entity="user", entity_id=user.id
    )
    return user


@router.post("/login", response_model=Token, summary="Вход (JSON)")
def login(data: LoginRequest, db: Session = Depends(get_db)) -> Token:
    token = AuthService(db).login(data.email, data.password)
    return Token(access_token=token)


@router.post(
    "/login/oauth",
    response_model=Token,
    summary="Вход (OAuth2 form, для кнопки Authorize в Swagger)",
)
def login_oauth(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    # В форме OAuth2 поле логина называется username — используем как email.
    token = AuthService(db).login(form.username, form.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead, summary="Текущий пользователь")
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
