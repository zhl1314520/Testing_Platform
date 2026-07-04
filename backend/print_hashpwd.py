from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# $2b$12$NbHy8TGwh28N6BM/tyar6O9rRblCVzmIxleq5sqLyXCLww7i8OhVS
if __name__ == "__main__":
    print(pwd_context.hash("123456"))