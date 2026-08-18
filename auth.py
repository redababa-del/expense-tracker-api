from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)






if __name__ == "__main__":
    hashed = hash_password("test123")
    print(hashed)
    print(verify_password("test123", hashed))
    print(verify_password("mauvais_mdp", hashed))


