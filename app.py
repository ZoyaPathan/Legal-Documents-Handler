from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.schemas import UserOut, UserAuth, TokenSchema, Document
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt , JWTError
from app.utils import SECRET_KEY, ALGORITHM 
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

from uuid import uuid4 

app = FastAPI()
users_db = {}
documents_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        role = payload.get("role")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "email": email,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

async def lawyer_only(current_user=Depends(get_current_user)):
    if current_user["role"] != "lawyer":
        raise HTTPException(
            status_code=403,
            detail="Only lawyers can access this route"
        )
    return current_user
async def client_only(current_user=Depends(get_current_user)):
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can access this route"
        )
    return current_user

@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = users_db.get(data.email, None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4()),
        "username": data.username,
        "role": data.role
    }
    users_db[data.email] = user    # saving user to database
    return UserOut(id=user["id"],
                   email=user["email"],
                   username=user["username"],
                   role=user["role"])
# OAuth2PasswordRequestForm uses 'username' field to send email
@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    user = users_db.get(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email'], user['role']),
        "refresh_token": create_refresh_token(user['email']),
    }

@app.get("/users", response_model=list[UserOut])
async def get_users():
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
        for user in users_db.values()
    ]
@app.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/lawyer-dashboard")
async def lawyer_dashboard(
    current_user=Depends(lawyer_only)
):
    return {
        "message": "Welcome Lawyer",
        "user": current_user
    }

@app.get("/client-dashboard")
async def client_dashboard(current_user=Depends(client_only)):
    return {
        "message": "Welcome Client",
        "user": current_user
    }