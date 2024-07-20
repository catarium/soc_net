from app.utils.password_hashing.context import pwd_context


def get_password_hash(password: str) -> str:
    '''
    generates hashed version of password
    :param password: unhashed password
    :return: hashed version of password
    '''
    return pwd_context.hash(password)
