"""
@file
@brief Machine Learning Post request
"""
import traceback
import pickle
import base64
import falcon
import numpy
import ujson
from .base_logging import BaseLogging
from .mlstorage import MLStorage
from ..args.args_images import string2bytes


class MLStoragePost(BaseLogging):
    """
    Implements a simple :epkg:`REST API` to
    upload zip files. The application assumes
    machine learning models are actionable through
    the following template: :ref:`l-template-ml`.
    """

    def __init__(self, secret=None, folder='.',
                 folder_storage='.', version=None):
        """
        @param      secret              see @see cl BaseLogging
        @param      folder              see @see cl BaseLogging
        @param      folder_storage      see @see cl MLStorage
        @param      version             API REST version
        """
        BaseLogging.__init__(self, secret=secret, folder=folder)
        self._storage = MLStorage(folder_storage)
        self._version = version

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

    def on_post(self, req, resp):
        """
        Processes a :epkg:`POST` request.

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
            if len(es) > 200:
                es = es[:200] + '...'
            log_data = dict(error=str(e))
            log_data.update(add_log_data)
            self.error("ML.load", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(es), excs)

        args = ujson.loads(js)
        self.save_time()
        duration = self.duration()
        log_data = dict(duration=duration)

        command = args.pop('cmd', None)
        if command == 'upload':
            self.save_time()
            try:
                name = self._store(args)
            except Exception as e:
                excs = traceback.format_exc()
                es = str(e)
                if len(es) > 200:
                    es = es[:200] + '...'
                duration = self.duration()
                log_data = dict(error=str(e), duration=duration, data=args)
                log_data.update(add_log_data)
                self.error("MLB.store", log_data)
                raise falcon.HTTPBadRequest(
                    "Unable to upload model due to: {}".format(es), excs)

            duration = self.duration()
            log_data = dict(duration=duration, name=name)
            self.info("MLB.store '%s'" % name, log_data)
            resp.status = falcon.HTTP_201
            answer = {"name": name}

        elif command == 'predict':
            self.save_time()
            try:
                name, pred, version, loaded = self._predict(args)
            except Exception as e:
                excs = traceback.format_exc()
                es = str(e)
                if len(es) > 200:
                    es = es[:200] + '...'
                name = args.get('name', None)
                duration = self.duration()
                log_data = dict(error=str(e), duration=duration, data=args)
                log_data.update(add_log_data)
                if name is not None:
                    log_data['name'] = name
                if format is not None:
                    log_data['format'] = format
                if input in args:
                    log_data['input'] = args['input']
                self.error("MLB.predict", log_data)
                raise falcon.HTTPBadRequest(
                    "Unable to predict with model '{0}' due to: {1}, format='{2}'".format(name, es, format), excs)

            duration = self.duration()
            log_data = dict(duration=duration, version=version, name=name)
            if loaded:
                self.info("MLB.predict '%s' loaded again" % name, log_data)
            else:
                self.info("MLB.predict '%s'" % name, log_data)
            resp.status = falcon.HTTP_201
            answer = {"output": pred, "version": version}
        else:
            es = "Unknown command '{0}'".format(command)
            log_data = dict(msg=es)
            log_data.update(add_log_data)
            self.error("MLStorage", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(es))

        try:
            js = ujson.dumps(answer)
        except OverflowError as e:
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(e))
        resp.body = js

    def _store(self, args):
        """
        Stores the model in the storage.
        """
        name = args.pop('name', None)
        if name is None or name == '':
            keys = ", ".join(sorted(args.keys()))
            try:
                ms = str(args)
            except ValueError:
                ms = ""
            if len(ms) > 300:
                ms = ms[:300] + "..."
            raise KeyError(
                "Unable to find a model name in sent data, keys={0}, args={1}.".format(keys, ms))
        zipped = args.pop('zip', None)
        if zipped is None:
            raise KeyError(
                "The REST API expects to find a zip file data in field 'zip'.")
        unstring = string2bytes(zipped)
        self._storage.add(name, unstring)
        return name

    def _predict(self, args):
        """
        Stores the model in the storage.
        """
        name = args.get('name', None)
        if name is None:
            raise KeyError("Unable to find a model name in sent data.")
        form = args.get('format', 'json')
        data = args.get('input', None)
        if data is None:
            raise KeyError("The REST API expects to find field 'input' which contains stringified data the "
                           "machine learned model can process. Field 'format' indicates which "
                           "preprocessing to do before calling the model which is currently '{0}'".format(form))
        if form == 'json':
            data = ujson.loads(data)
        elif form == 'img':
            simg = base64.b64decode(data)
            data = pickle.loads(simg)
        elif form == 'bytes':
            data = string2bytes(data)
        else:
            raise ValueError("Unrecognized format '{0}'.".format(form))
        res, version, loaded = self._storage.call_predict(
            name, data, version=True, was_loaded=True)
        if isinstance(res, numpy.ndarray):
            res = res.tolist()
        return name, res, version, loaded
