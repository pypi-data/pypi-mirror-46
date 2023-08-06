"""
@file
@brief Template application for a machine learning model
based on :epkg:`keras` available through a REST API.
"""
import os
import numpy
import skimage.transform as skt


# Declare an id for the REST API.
def restapi_version():
    """
    Displays a version.
    """
    return "0.1.1237"


# Declare a loading function.
def restapi_load(files={'model': "dlmodel.keras"}):  # pylint: disable=W0102
    """
    Loads the model.
    The model name is relative to this file.
    When call by a REST API, the default value is always used.
    """
    from keras.models import load_model  # pylint: disable=E0401
    model = files["model"]
    here = os.path.dirname(__file__)
    model = os.path.join(here, model)
    if not os.path.exists(model):
        raise FileNotFoundError("Cannot find model '{0}' (full path is '{1}')".format(
            model, os.path.abspath(model)))
    loaded_model = load_model(model)
    return loaded_model


# Declare a predict function.
def restapi_predict(model, X):
    """
    Computes the prediction for model *clf*.

    :param model: pipeline following :epkg:`scikit-learn` API
    :param X: image as a :epkg:`numpy` array
    :return: output of *predict_proba*
    """
    if not isinstance(X, numpy.ndarray):
        raise TypeError("X must be an array")
    im = X
    im = skt.resize(im, (3, 224, 224))
    im = numpy.transpose(im, (1, 2, 0))
    im = im[numpy.newaxis, :, :, :]
    return model.predict(im)
