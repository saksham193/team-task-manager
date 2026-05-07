from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_PASSWORD_BYTES = 72


def _validate_bcrypt_password(password: str) -> None:
    # bcrypt only uses the first 72 bytes, so reject longer passwords clearly.
    if len(password.encode("utf-8")) > BCRYPT_MAX_PASSWORD_BYTES:
        raise ValueError("Password cannot be longer than 72 bytes")


def hash_password(password: str) -> str:
    _validate_bcrypt_password(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    _validate_bcrypt_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)
