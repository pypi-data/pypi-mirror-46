# -*- coding: utf-8 -*-
"""
@file
@brief Command line.
"""
import sys
from pyquickhelper.cli import cli_main_helper


def main(args, fLOG=print):
    """
    Implements ``python -m pyquickhelper <command> <args>``.

    @param      args        command line arguments
    @param      fLOG        logging function
    """
    try:
        from .cli.make_ml_app import start_mlrestapi
        from .cli.make_encrypt_pwd import encrypt_pwd
        from .cli.make_ml_store import start_mlreststor
        from .cli.make_ml_upload import upload_model
    except ImportError:
        from lightmlrestapi.cli.make_ml_app import start_mlrestapi
        from lightmlrestapi.cli.make_encrypt_pwd import encrypt_pwd
        from lightmlrestapi.cli.make_ml_store import start_mlreststor
        from lightmlrestapi.cli.make_ml_upload import upload_model

    fcts = dict(start_mlrestapi=start_mlrestapi, encrypt_pwd=encrypt_pwd,
                start_mlreststor=start_mlreststor, upload_model=upload_model)
    return cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])
