"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import pandas


def encrypt_pwd(input="", output="", algo="sha224", fLOG=print):  # pylint: disable=W0622
    """
    Encrypts passwords to setup a REST API
    with *lightmlrestapi*.

    :param input: file containing two columns <login>,<clear password>
        (comma separated values), no header, encoding is *utf-8*
    :param output: file containing two columns <login>,<encrypted password>,
        csv, encoding is *utf-8*
    :param algo: algorithm used to hash the passwords
    :param fLOG: logging function

    .. cmdref::
        :title: Encrypts password
        :cmd: -m lightmlrestapi encrypt_pwd --help
        :lid: cmd_encrypt_pwd_cmd

        Encrypts passwords for a REST API created by *lightmlrestapi*.
    """
    try:
        from ..args.encrypt_helper import encrypt_passwords
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.args.encrypt_helper import encrypt_passwords

    if not os.path.exists(input):
        raise FileNotFoundError("File '{0}' not found".format(input))

    if fLOG:
        fLOG("[encrypt_pwd] encrypt '{0}'".format(input))
    df = pandas.read_csv(input, sep=',', encoding='utf-8', header=None)
    df2 = encrypt_passwords(df, algo=algo)
    if fLOG:
        fLOG("[encrypt_pwd] to      '{0}'".format(output))
    df2.to_csv(output, sep=',', encoding='utf-8', header=False, index=False)
    if fLOG:
        fLOG("[encrypt_pwd] done.")
