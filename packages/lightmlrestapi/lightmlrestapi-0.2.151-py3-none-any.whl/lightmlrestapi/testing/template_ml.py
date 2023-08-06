"""
@file
@brief Template application for a machine learning model
available through a REST API.
"""
import pickle
import os


# Declare an id for the REST API.
def restapi_version():
    """
    Displays a version.
    """
    return "0.1.1234"


# Declare a loading function.
def restapi_load(files={"model": "iris2.pkl"}):  # pylint: disable=W0102
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
    with open(model, "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model


# Declare a predict function.
def restapi_predict(model, X):
    """
    Computes the prediction for model *clf*.

    :param model: pipeline following :epkg:`scikit-learn` API
    :param X: inputs
    :return: output of *predict_proba*
    """
    return model.predict_proba(X)
