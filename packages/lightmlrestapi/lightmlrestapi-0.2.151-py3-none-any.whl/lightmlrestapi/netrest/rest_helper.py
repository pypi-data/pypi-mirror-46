"""
@file
@brief Helpers to submit REST API requests.
"""
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
import ujson
from ..args import zip_dict, bytes2string


def json_upload_model(name, pyfile, data=None):
    """
    Builds a REST request to upload a machine learned models to a REST API defined by
    @see cl MLStoragePost.

    :param name: name of the model, should be unique and not already used
    :param pyfile: python file which computes the prediction,
        the file must follows the specification defined in
        :ref:`l-template-ml`
    :param data: binary file, usually everything the models pickled
    :return: dictionary ready to be jsonified
    """
    if name is None or name == '':
        raise ValueError("name cannot be empty.")
    if not os.path.exists(pyfile):
        raise FileNotFoundError("Unable to find '{0}'.".format(pyfile))
    if data is None:
        data = []
    if not isinstance(data, list):
        data = [data]
    for d in data:
        if not os.path.exists(d):
            raise FileNotFoundError("Unable to find '{0}'.".format(d))

    # model file
    last_file = os.path.split(pyfile)[-1]
    with open(pyfile, "rb") as f:
        code = f.read()

    if code == '':
        raise ValueError("File '{0}' cannot be empty.".format(pyfile))
    model_data = {last_file: code}

    # model data
    if data:
        for d in data:
            ld = os.path.split(d)[-1]
            with open(d, "rb") as f:
                content = f.read()
            model_data[ld] = content

    # zip data
    zipped = zip_dict(model_data)
    request = dict(name=name, cmd='upload',
                   zip=bytes2string(zipped))
    return request


def json_predict_model(name, data, format='json'):  # pylint: disable=W0622
    """
    Builds a REST request to compute the prediction of a machine learning model
    upload with @see fn json_upload_model.
    See also @see cl MLStoragePost.

    :param name: name of the model, should be unique and not already used
    :param data: any kind of data the model request
    :param format: ``'json'`` or ``'image'``
    :return: dictionary ready to be jsonified
    """
    if name is None or name == '':
        raise ValueError("name cannot be empty.")

    js = ujson.dumps(data)
    obs = dict(cmd='predict', name=name, input=js, format=format)
    return obs


def submit_rest_request(request, login=None, pwd=None, url='http://127.0.0.1:8081/',
                        timeout=15, fLOG=None):
    """
    Submits a request to a REST API defined by
    @see cl MLStoragePost.

    :param login: login
    :param pwd: password
    :param request: request as a dictionary
    :param url: url
    :param timeout: timeout
    :param fLOG: logging function
    :return: request results as dictionary
    """
    if login:
        if fLOG:
            fLOG("[submit_rest_request] submit authentified request as '{0}' to '{1}'".format(
                login, url))
        auth = HTTPBasicAuth(login, pwd)
        jsonified = ujson.dumps(request)
        response = requests.post(
            url, auth=auth, data=jsonified, timeout=timeout)
    else:
        if fLOG:
            fLOG("[submit_rest_request] submit request to '{0}'".format(url))
        jsonified = ujson.dumps(request)
        response = requests.post(url, data=jsonified, timeout=timeout)

    if response.ok:
        return ujson.loads(response.content)
    else:
        content = None
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, '_content'):
            content = response._content  # pylint: disable=W0212
        if content:
            if isinstance(content, bytes):
                http_error_msg = content.decode('ascii')
                try:
                    val = ujson.loads(http_error_msg)
                    http_error_msg = val
                except ValueError:
                    pass
                finally:
                    pass
            else:
                http_error_msg = ujson.loads(content)
            if isinstance(http_error_msg, dict):
                http_error_msg = "\n".join(
                    ["{0}: {1}".format(k, v) for k, v in sorted(http_error_msg.items())])
        else:
            http_error_msg = "ERROR"
        raise HTTPError(http_error_msg, response=response)
