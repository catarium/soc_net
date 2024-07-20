from app.utils.password_hashing.context import pwd_context


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    verifies password by given plain password
    :param plain_password: unhashed password
    :param hashed_password: same hashed passowrd
    :return: True if hashed password is hashed version of unhashed else False
    '''
    return pwd_context.verify(plain_password, hashed_password)