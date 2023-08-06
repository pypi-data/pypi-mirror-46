"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import logging


def start_mlrestapi(name='dummy', host='127.0.0.1', port=8081, nostart=False, wsgi='waitress',
                    options='', secret='', ccall='single', users='', fLOG=print):
    """
    Creates an :epkg:`falcon` application and
    runs it through a :epkg:`wsgi` server.

    :param name: class name or filename which defines the application
    :param host: host
    :param port: port
    :param nostart: do not start the wsgi server
    :param wsgi: :epkg:`wsgi` framework which runs the falcon application
    :param options: additional options as a string (depends on the application)
    :param ccall: calling convention, 'single', 'multi' or 'both' depending on the
        fact that the prediction function can predict for only one observation,
        multiple ones or both
    :param secret: secret used to encrypt the logging, default is empty which
        disables the encryption
    :param users: registred users, file with two columns login, encrypted password,
        and no header
    :param fLOG: logging function

    Only :epkg:`waitress` is implemented right now.
    Other alternative such as :epkg:`mod_wsgi` with :epkg:`Apache`.
    :epkg:`uwsgi` are not implemented.

    .. cmdref::
        :title: Creates an falcon application and starts it through a wsgi application
        :cmd: -m lightmlrestapi start_mlrestapi --help
        :lid: cmd_start_mlrestapi_cmd

        Creates an :epkg:`falcon` application and starts it through a :epkg:`wsgi` server.
    """
    try:
        from ..testing import dummy_application, dummy_application_image, dummy_application_fct
        from ..testing import dummy_application_neighbors, dummy_application_neighbors_image
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.testing import dummy_application, dummy_application_image, dummy_application_fct
        from lightmlrestapi.testing import dummy_application_neighbors, dummy_application_neighbors_image

    if name == "dummy":
        # Dummy application.
        if users:
            raise NotImplementedError("users not None, not implemented")
        app = dummy_application()

    elif name == "dummyfct":
        # Dummy application with a function.
        name = options
        if not os.path.exists(name):
            raise FileNotFoundError("Unable to find '{0}'.".format(name))
        path, loc = os.path.split(name)
        if path not in sys.path:
            sys.path.append(path)
            rem = True
        else:
            rem = False
        loc = os.path.splitext(loc)[0]
        try:
            mod = __import__(loc)
        except ImportError as e:
            if rem:
                sys.path.pop()
            with open(name, "r") as f:
                code = f.read()
            raise ImportError(
                "Unable to compile file '{0}'\n{1}".format(name, code)) from e
        if rem:
            sys.path.pop()

        if not hasattr(mod, 'restapi_version'):
            with open(name, "r") as f:
                code = f.read()
            raise AttributeError(
                "Unable to find function 'restapi_version' in file '{0}'\n{1}".format(name, code))
        if not hasattr(mod, 'restapi_load'):
            with open(name, "r") as f:
                code = f.read()
            raise AttributeError(
                "Unable to find function 'restapi_load' in file '{0}'\n{1}".format(name, code))
        if not hasattr(mod, 'restapi_predict'):
            with open(name, "r") as f:
                code = f.read()
            raise AttributeError(
                "Unable to find function 'restapi_predict' in file '{0}'\n{1}".format(name, code))

        if secret == '':
            secret = None
        app = dummy_application_fct(mod.restapi_load, mod.restapi_predict, secret=secret,
                                    version=mod.restapi_version, users=users)

    elif name == "dummyimg":
        # Dummy application with an image.
        if users:
            raise NotImplementedError("users not None, not implemented")
        app = dummy_application_image(options=options, secret=secret)

    elif name == "dummyknn":
        # Dummy application with neighbors.
        if users:
            raise NotImplementedError("users not None, not implemented")
        app = dummy_application_neighbors()

    elif name == "dummyknnimg":
        # Dummy application with neighbors and an image.
        if users:
            raise NotImplementedError("users not None, not implemented")
        app = dummy_application_neighbors_image(options=options, secret=secret)

    elif '.py' in name:
        raise NotImplementedError(
            "Unable to get application from filename '{}'. Not implemented.".format(name))

    else:
        raise NotImplementedError(
            "Application '{}' is not implemented.".format(name))

    if wsgi == 'waitress':
        from waitress import serve
        if not nostart:
            fLOG("[start_mlrestapi] serve(app, host='{}', port='{}')".format(host, port))
            logger = logging.getLogger('waitress')
            logger.setLevel(logging.INFO)
            serve(app, host=host, port=port)
        else:
            fLOG("[start_mlrestapi] do not run serve(app, host='{}', port='{}')".format(
                host, port))
    else:
        raise NotImplementedError(
            "Server '{}' is not implemented.".format(wsgi))

    return app
