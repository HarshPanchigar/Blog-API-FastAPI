from jose import jwt , JWTError
from datetime import datetime , timedelta , timezone
from fastapi import HTTPException ,Depends
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY  = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

OAuth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#create token
def create_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp" : expire
    })
    token = jwt.encode(to_encode, SECRET_KEY ,algorithm=ALGORITHM) # type: ignore
    return token

def verify_token(token : str = Depends(OAuth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM]) # type: ignore
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")