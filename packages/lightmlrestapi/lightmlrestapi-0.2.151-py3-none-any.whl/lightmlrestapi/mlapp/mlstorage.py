"""
@file
@brief Machine Learning Post request
"""
import os
import sys
import json
import threading
import importlib
from datetime import datetime
# from filelock import Timeout, FileLock
from ..args.zip_helper import unzip_bytes


class AlreadyExistsException(Exception):
    """
    Exception raised when a project already exists.
    """
    pass


class ZipStorage:
    """
    Stores and restores zipped files.
    """

    def __init__(self, folder):
        """
        @param      folder      folder
        """
        self._folder = folder

    def enumerate_names(self):
        """
        Returns the list of sub folders.
        """
        for root, dirs, _ in os.walk(self._folder):
            for name in dirs:
                desc = os.path.join(root, name, ".desc")
                if os.path.exists(desc):
                    zoo = os.path.relpath(
                        os.path.join(root, name), self._folder)
                    yield zoo.replace("\\", "/")

    def exists(self, name):
        """
        Tells if project *name* exists.

        @param      name        name
        @return                 boolean
        """
        r = os.path.exists(self.get_full_name(name))
        if not r:
            return r
        return os.path.exists(os.path.join(self.get_full_name(name), ".desc"))

    def get_full_name(self, name):
        """
        Returns the full name of a project.

        @param      name        project name
        @return                 full name
        """
        return os.path.join(self._folder, name)

    def _check_name(self, name, data=False):
        """
        A name is valid if it is a variable name
        or a filename if *data* is True.
        """
        if name is None or not isinstance(name, str) or len(name) == 0:
            raise ValueError("name cannot be empty.")
        for i, c in enumerate(name):
            if "a" <= c <= "z":
                continue
            if "A" <= c <= "Z":
                continue
            if "0" <= c <= "9" and i > 0:
                continue
            if c in '_/':
                continue
            if c == '.' and data:
                continue
            raise ValueError(
                "A name contains a forbidden character '{0}'".format(name))

    def verify_data(self, data):
        """
        Performs verifications to ensure the data to store
        is ok.

        @param      data    dictionary
        @return             None or information about the data
        @raises             raises an exception if not ok
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")
        for k, v in data.items():
            if not isinstance(k, str):
                raise TypeError("Key must be a string.")
            self._check_name(k, data=True)
            if not isinstance(v, bytes):
                raise TypeError(
                    "Values must be bytes for key '{0}'.".format(k))
        return {}

    def _makedirs(self, subfold):
        """
        Creates a subfolder and add a file ``__init__.py``.
        The function overwrites it file ``__init__.py``
        to let the interpreter know there was some changes.
        """
        spl = subfold.replace("\\", "/").split("/")
        fold = self._folder
        for sp in spl:
            fold = os.path.join(fold, sp)
            init = os.path.join(fold, '__init__.py')
            if not os.path.exists(fold):
                os.mkdir(fold)
                with open(init, 'w') as f:
                    f.write('def do_exists():\n    print("do exists")\n')
            else:
                with open(init, "r") as f:
                    content = f.read()
                spl = content.split('do_exists')
                content += '\ndef do_exists{0}():\n    print("do exists{0}")\n'.format(
                    len(spl))
                with open(init, "w") as f:
                    f.write(content)

    def add(self, name, data):
        """
        Adds a project based on the data.
        A project which already exists cannot be added.

        @param      name        project name, should only contain
                                ascii characters + ``'/'``
        @param      data        dictionary or bytes produced by
                                function @see fn zip_dict
        """
        # Verifications.
        self._check_name(name)
        if self.exists(name):
            raise AlreadyExistsException(
                "Project '{0}' already exists.".format(name))
        if isinstance(data, bytes):
            data = unzip_bytes(data)
        dump = self.verify_data(data)

        # Creates dictionary.
        full = self.get_full_name(name)
        self._makedirs(name)
        desc = os.path.join(full, ".desc")
        with open(desc, "w", encoding="utf-8") as fd:
            fd.write("# ")
            if dump is not None:
                json.dump(dump, fd)
            fd.write("\n")

        # Stores.
        # lock = FileLock(desc, timeout=2)
        # with lock:
        with open(desc, "a") as fd:
            for k, v in sorted(data.items()):
                subn = "{0}/{1}".format(name, k)
                self._check_name(subn, data=True)
                fd.write("{0}\n".format(k))
                n = self.get_full_name(subn)
                with open(n, "wb") as f:
                    f.write(v)

    def get(self, name):
        """
        Retrieves a project based on its name.

        @param      name        project name
        @return                 data
        """
        if not self.exists(name):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        full = self.get_full_name(name)
        desc = os.path.join(full, ".desc")
        if not os.path.exists(desc):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        res = {}
        # lock = FileLock(desc, timeout=1)
        # with lock.acquire():
        with open(desc, "r") as fd:
            lines = fd.readlines()
            lines = [_ for _ in lines if not _.startswith("#")]
        for line in lines:
            line = line.strip("\r\n ")
            if line:
                n = os.path.join(full, line)
                with open(n, "rb") as f:
                    res[line] = f.read()
        return res

    def get_metadata(self, name):
        """
        Restores the data procuded by *verify_data*.
        """
        if not self.exists(name):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        full = self.get_full_name(name)
        desc = os.path.join(full, ".desc")
        if not os.path.exists(desc):
            raise FileNotFoundError(
                "Project '{0}' does not exist.".format(name))
        with open(desc, "r", encoding="utf-8") as f:
            first_line = f.readline().strip("# \n")
            return json.loads(first_line)


class MLStorage(ZipStorage):
    """
    Stores machine learned models into folders. The storages
    expects to find at least one :epkg:`python` following
    the specifications described at :ref:`l-mlapp-def`.
    More template for actionable machine learned models
    through the following template: :ref:`l-template-ml`.
    """

    def __init__(self, folder, cache_size=10):
        """
        @param      folder      folder
        @param      cache_size  cache size
        """
        ZipStorage.__init__(self, folder)
        self._cache_size = cache_size
        self._cache = {}
        self._lock = threading.Lock()

    def verify_data(self, data):
        """
        Performs verifications to ensure the data to store
        is ok. The storages expects to find at least one script
        python with

        @param      data    dictionary
        @return             python file which describes the model
        @raises             raises an exception if not ok
        """
        res = ZipStorage.verify_data(self, data)
        main_script = None
        for k, v in data.items():
            if k.endswith(".py"):
                content = v.decode("utf-8")
                if "def restapi_version():" in content:
                    main_script = k
                    break
        if main_script is None:
            sorted_keys = ", ".join(sorted(data.keys()))
            raise RuntimeError(
                "Unable to find a script with 'def restapi_version():' inside.. List of found keys is {0}.".format(sorted_keys))
        res.update(dict(main_script=main_script))
        return res

    def empty_cache(self):
        """
        Removes one place in the cache if the cache
        is full. Sort them by last access.
        """
        if len(self._cache) < self._cache_size:
            return
        els = [(v['last'], k) for k, v in self._cache.items()]
        els.sort()
        self._lock.acquire()
        del self._cache[els[0][1]]
        self._lock.release()

    def _import(self, name):
        """
        Imports the main module for one model.

        @param      name        model name
        @return                 imported module
        """
        meta = self.get_metadata(name)
        loc = self.get_full_name(name)
        script = os.path.join(loc, meta['main_script'])
        if not os.path.exists(script):
            raise FileNotFoundError(
                "Unable to find script '{0}'".format(script))

        fold, modname = os.path.split(script)
        sys.path.insert(0, self._folder)
        full_modname = ".".join([name.replace("/", "."),
                                 os.path.splitext(modname)[0]])

        def import_module():
            try:
                mod = importlib.import_module(full_modname)
                # mod = __import__(full_modname)
            except (ImportError, ModuleNotFoundError) as e:
                with open(script, "r") as f:
                    code = f.read()
                values = dict(self_folder=self._folder, name=name, meta=str(meta),
                              loc=loc, script=script, fold=fold, modname=modname,
                              full_modname=full_modname)
                values = '\n'.join('{}={}'.format(k, v)
                                   for k, v in values.items())
                raise ImportError(
                    "Unable to compile file '{0}'\ndue to {1}\n{2}\n---\n{3}".format(script, e, code, values)) from e
            return mod

        try:
            mod = import_module()
        except ImportError as e:
            # Reload modules.
            specs = []
            spl = full_modname.split('.')
            for i in range(len(spl) - 1):
                name = '.'.join(spl[:i + 1])
                if name in sys.modules:
                    del sys.modules[name]
                importlib.invalidate_caches()
                spec = importlib.util.find_spec(name)
                specs.append((name, spec))
                mod = importlib.import_module(name)
                importlib.reload(mod)
            try:
                mod = import_module()
            except ImportError as e:
                del sys.path[0]
                mes = "\n".join("{0}: {1}".format(a, b) for a, b in specs)
                raise ImportError("Unable to import module '{0}', specs=\n{1}".format(
                    full_modname, mes)) from e

        del sys.path[0]

        if not hasattr(mod, "restapi_load"):
            raise ImportError(
                "Unable to find function 'restapi_load' in module '{0}'".format(mod.__name__))
        return mod

    def load_model(self, name, was_loaded=False):
        """
        Loads a model into the cache if not loaded
        and returns it.

        @param      name        cache name
        @param      was_loaded  if True, tells if the model was loaded again
        @return                 dictionary with keys: *last*, *model*, *module*.
        """
        if name in self._cache:
            self._lock.acquire()
            res = self._cache[name]
            res['last'] = datetime.now()
            self._lock.release()
            if was_loaded:
                return res, False
            else:
                return res

        self.empty_cache()

        # Imports the module.
        self._lock.acquire()
        try:
            mod = self._import(name)
        finally:
            self._lock.release()

        # Loads the models.
        self._lock.acquire()
        try:
            model = mod.restapi_load()
        finally:
            self._lock.release()

        res = dict(last=datetime.now(), model=model, module=mod)
        self._lock.acquire()
        self._cache[name] = res
        self._lock.release()
        if was_loaded:
            return res, True
        else:
            return res

    def call_predict(self, name, data, version=False, was_loaded=False, loaded_model=None):
        """
        Calls method *restapi_predict* from a stored script *python*.

        @param      name            model name
        @param      data            input data
        @param      version         returns the version as well
        @param      was_loaded      if True, return if the model was loaded again
        @param      loaded_model    skip cached model if exists, should be the result of
                                    a previous call to @see me loaded_model
        @return                     *predictions* or *predictions, version*
        """
        if loaded_model is None:
            res = self.load_model(name, was_loaded=was_loaded)
            if was_loaded:
                res, loaded = res
        else:
            res, loaded = loaded_model, False
        pred = res['module'].restapi_predict(res['model'], data)
        if version:
            version = res['module'].restapi_version()
            if was_loaded:
                return pred, version, loaded
            else:
                return pred, version
        else:
            if was_loaded:
                return pred, loaded
            else:
                return pred

    def call_version(self, name):
        """
        Calls method *restapi_version* from a stored script *python*.
        """
        res = self.load_model(name)
        return res['module'].restapi_version()
