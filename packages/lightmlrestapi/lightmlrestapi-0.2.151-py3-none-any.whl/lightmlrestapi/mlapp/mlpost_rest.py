"""
@file
@brief Machine Learning Post request
"""
import traceback
import json
import falcon
import numpy
import ujson
from .base_logging import BaseLogging


class MachineLearningPost(BaseLogging):
    """
    Implements a simple :epkg:`REST API` which handles
    a post request, no authentification
    is required. The model ingests a vector *X*
    and outputs another one or a number *Y*.
    An basic example of an application is given by
    @see fn dummy_application.
    """

    _call_convention = {'single': 0, 'multi': 1, 'both': 2}

    def __init__(self, load_function, predict_function,
                 secret=None, folder='.',
                 log_features=True, log_prediction=True,
                 load_params=None, ccall='single', version=None):
        """
        @param      predict_function    predict function
        @param      load_function       load function
        @param      secret              see @see cl BaseLogging
        @param      folder              see @see cl BaseLogging
        @param      log_features        log the features
        @param      log_prediction      log the prediction
        @param      load_params         given to the loading function
        @param      ccall               see below
        @param      version             API REST version

        Some models can only computes predictions for a sequence
        of observations, not just one. Parameter *ccall* defines what
        the prediction function can ingest.
        * single: only one observation
        * multi: only multiple ones
        * both: the function determines what it must do
        """
        BaseLogging.__init__(self, secret=secret, folder=folder)
        self._predict_fct = predict_function
        self._log_features = log_features
        self._log_prediction = log_prediction
        self._load_fct = load_function
        self._load_params = {} if load_params is None else load_params
        self._loaded_results = None
        self._version = version
        if ccall not in MachineLearningPost._call_convention:
            raise ValueError("ccall '{0}' must be in {1}".format(
                ccall, MachineLearningPost._call_convention))
        self._ccall = MachineLearningPost._call_convention[ccall]
        if not isinstance(self._load_params, dict):
            raise TypeError("load_params must be a dictionary.")

    @staticmethod
    def data2json(data):
        """
        :epkg:`numpy:array` cannot be converted into
        :epkg:`json`. We change the type into a list.
        """
        if isinstance(data, numpy.ndarray):
            return dict(shape=data.shape, data=data.tolist())
        else:
            return data

    def _load(self):
        return self._load_fct(**(self._load_params))

    def _predict_single(self, obj, features):
        if self._ccall == 1:
            return self._predict_fct(obj, [features])
        else:
            return self._predict_fct(obj, features)

    def check_single(self, features):
        """
        Checks the sequence load + predict returns
        something with the given observations.
        """
        obj = self._load()
        return self._predict_single(obj, features)

    def on_post(self, req, resp):
        """
        @param      req         request
        @param      resp        ...
        """
        add_log_data = dict(user=req.get_header('uid'), ip=req.access_route)
        if self._version is not None:
            add_log_data = self._version

        # To get the parameters
        # req.get_params
        js = None
        try:
            while True:
                chunk = req.stream.read(2**16)
                if len(chunk) == 0:
                    break
                if js is None:
                    js = chunk
                else:
                    js += chunk
        except AssertionError as e:
            excs = traceback.format_exc()
            es = str(e)
            if len(es) > 400:
                es = es[:400] + '...'
            log_data = dict(error=str(e))
            log_data.update(add_log_data)
            if self._load_params:
                log_data['load_params'] = self._load_params
            self.error("ML.load", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(es), excs)

        args = ujson.loads(js)
        X = args["X"]

        # load the model
        if self._loaded_results is None:
            self.save_time()
            try:
                self._loaded_results = self._load()
            except Exception as e:
                excs = traceback.format_exc()
                es = str(e)
                if len(es) > 200:
                    es = es[:200] + '...'
                duration = self.duration()
                log_data = dict(duration=duration, error=str(e))
                log_data.update(add_log_data)
                if self._load_params:
                    log_data['load_params'] = self._load_params
                self.error("ML.load", log_data)
                raise falcon.HTTPBadRequest(
                    'Unable to load due to: {0}'.format(es), excs)
            duration = self.duration()
            log_data = dict(duration=duration)
            log_data.update(add_log_data)
            if self._load_params:
                log_data['load_params'] = self._load_params
            self.info("ML.load", log_data)

        # predict
        self.save_time()
        try:
            res = self._predict_single(self._loaded_results, X)
        except Exception as e:
            excs = traceback.format_exc()
            es = str(e)
            if len(es) > 200:
                es = es[:200] + '...'
            duration = self.duration()
            log_data = dict(duration=duration)
            log_data.update(add_log_data)
            if self._log_features:
                log_data['X'] = MachineLearningPost.data2json(X)
            log_data["error"] = str(e)
            self.error("ML.predict", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to predict due to: {0}'.format(es), excs)
        duration = self.duration()

        # see http://falcon.readthedocs.io/en/stable/api/request_and_response.html
        log_data = dict(duration=duration)
        log_data.update(add_log_data)
        if self._log_features:
            log_data['X'] = MachineLearningPost.data2json(X)
        if self._log_prediction:
            log_data['Y'] = MachineLearningPost.data2json(res)
        self.info("ML.predict", log_data)

        resp.status = falcon.HTTP_201
        answer = {"Y": res}
        if self._version is not None:
            answer[".version"] = self._version
        try:
            js = ujson.dumps(answer)
        except OverflowError as e:
            try:
                json.dumps(answer)
            except Exception as ee:
                raise OverflowError(
                    'res probably contains numpy arrays or numpy.types ({0}), they cannot be serialized.'.format(type(res))) from ee
            raise OverflowError(
                'res probably contains numpy arrays ({0}), they cannot be serialized with ujson but with json.'.format(type(res))) from e
        resp.body = js
