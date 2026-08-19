# Imports
from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta

# Password Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# JWT
SECRET_KEY = "change_moi_avec_une_vraie_cle_secrete_longue"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None



# Tests
if __name__ == "__main__":
    hashed = hash_password("test123")
    print(hashed)
    print(verify_password("test123", hashed))
    print(verify_password("mauvais_mdp", hashed))