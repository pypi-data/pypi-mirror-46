"""
@file
@brief Template application for a machine learning model
based on :epkg:`torch` available through a REST API.
"""
import os
import numpy
import skimage.transform as skt


# Declare an id for the REST API.
def restapi_version():
    """
    Displays a version.
    """
    return "0.1.1238"


# Declare a loading function.
def restapi_load(files={"model": "dlmodel.torch"}):  # pylint: disable=W0102
    """
    Loads the model.
    The model name is relative to this file.
    When call by a REST API, the default value is always used.
    """
    model = files["model"]
    here = os.path.dirname(__file__)
    model = os.path.join(here, model)
    if not os.path.exists(model):
        raise FileNotFoundError("Cannot find model '{0}' (full path is '{1}')".format(
            model, os.path.abspath(model)))
    import torch  # pylint: disable=E0401
    loaded_model = torch.load(model)
    return loaded_model

# Declare a predict function.


def restapi_predict(model, X):
    """
    Computes the prediction for model *clf*.

    :param model: pipeline following :epkg:`scikit-learn` API
    :param X: image as a :epkg:`numpy` array
    :return: output of *predict_proba*
    """
    from torch import from_numpy  # pylint: disable=E0611,E0401
    if not isinstance(X, numpy.ndarray):
        raise TypeError("X must be an array")
    im = X
    im = skt.resize(im, (3, 224, 224))
    #im = numpy.transpose(im, (1, 2, 0))
    im = im[numpy.newaxis, :, :, :]
    ten = from_numpy(im.astype(numpy.float32))
    pred = model.forward(ten)
    return pred.detach().numpy()
