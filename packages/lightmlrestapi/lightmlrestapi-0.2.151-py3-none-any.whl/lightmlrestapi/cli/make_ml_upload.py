"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys


def upload_model(login="", pwd="", name="", pyfile="", data="", url='127.0.0.1:8081',   # pylint: disable=W0102
                 timeout=15, fLOG=print):  # pylint: disable=W0622
    """
    Uplaods a machine learned models to a REST API defined by
    @see cl MLStoragePost.

    :param login: user login
    :param pwd: user pasword
    :param name: name of the model, should be unique and not already used
    :param pyfile: python file which computes the prediction,
        the file must follows the specification defined in
        :ref:`l-template-ml`
    :param data: files to upload
    :param url: url of the REST API
    :param timeout: timeout
    :param fLOG: logging function

    .. cmdref::
        :title: Uploads a machine model
        :cmd: -m lightmlrestapi upload_model --help
        :lid: cmd_upload_model_cmd

        Uploads a machine learned model to a REST API
        created with *lightmlrestapi*. The code of this command line is equivalent
        to:

        ::

            from lightmlrestapi.netrest import submit_rest_request, json_upload_model
            req = json_upload_model(name=name, pyfile=pyfile, data=data)
            submit_rest_request(req, login=login, pwd=pwd, url=url)
    """
    try:
        from ..netrest import submit_rest_request, json_upload_model
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.netrest import submit_rest_request, json_upload_model

    if isinstance(data, str):
        data = data.split(',')
    if fLOG:
        fLOG('[upload_model] Prepare the JSON request.')
    req = json_upload_model(name=name, pyfile=pyfile, data=data)
    if fLOG:
        fLOG('[upload_model] Submit request - size:', len(req['zip']))
    submit_rest_request(req, login=login, pwd=pwd, url=url, fLOG=fLOG)
    if fLOG:
        fLOG('[upload_model] Done.')
