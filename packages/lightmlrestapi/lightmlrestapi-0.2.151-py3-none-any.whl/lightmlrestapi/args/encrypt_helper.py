"""
@file
@brief Helper about encryption.
"""
import os
import hashlib
from io import StringIO
import pandas


def encrypt_password(pwd, algo="sha224"):
    """
    Encrypts one password.

    @param      pwd     string
    @param      algo    algorithm used to hash passwords
    @return             encrypted password
    """
    if algo == "sha224":
        return hashlib.sha224(pwd.encode('ascii')).hexdigest()
    else:
        raise NotImplementedError(
            "Algorithm '{0}' is not implemented.".format(algo))


def encrypt_passwords(users, algo="sha224"):
    """
    Encrypts users passwords.

    @param      users   dataframe or...
    @param      algo    algorithm used to hash passwords
    @return             password are replaced by the hashed passwords
    """
    if isinstance(users, list):
        res = []
        for login, pwd in users:
            pwd = encrypt_password(pwd, algo=algo)
            res.append((login, pwd))
        return res
    elif hasattr(users, "values"):
        df = users.copy()
        col = df.columns[1]
        df[col] = df[col].apply(lambda pwd: encrypt_password(pwd, algo=algo))
        return df
    else:
        raise TypeError("Unexpected type '{0}'".format(type(users)))


def load_passwords(source):
    """
    Loads the encrypted passwords from a filename, a dataframe,
    a list of tuple.

    @param      source  filename, dataframe
    @return             dictionary ``{user: encrypted_pwd}``
    """
    if isinstance(source, str):
        if "\n" in source or ',' in source:
            st = StringIO(source)
            df = pandas.read_csv(st, encoding="utf-8", header=None)
        elif os.path.exists(source):
            df = pandas.read_csv(source, encoding="utf-8", header=None)
        else:
            raise ValueError("Unexpected string '{0}'".format(source))
    elif isinstance(source, dict):
        return source
    elif hasattr(source, "values"):
        df = source
    elif isinstance(source, list):
        res = {}
        for a, b in source:
            res[a] = b
        return res
    else:
        raise TypeError("Unable to interpret type '{0}'".format(type(source)))

    # dataframe
    res = {}
    for i in range(df.shape[0]):
        res[df.iloc[i, 0]] = df.iloc[i, 1]
    return res
