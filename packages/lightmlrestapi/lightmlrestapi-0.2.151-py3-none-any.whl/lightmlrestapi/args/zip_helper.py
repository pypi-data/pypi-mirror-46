"""
@file
@brief Machine Learning Post request
"""
import io
import zipfile


def unzip_bytes(buffer):
    """
    Unzips everything from a buffer.

    @param      buffer      bytes
    @return                 dictionary ``{ filename : bytes }``
    """
    if not isinstance(buffer, bytes):
        raise TypeError("buffer must be bytes.")
    res = {}
    st = io.BytesIO(buffer)
    with zipfile.ZipFile(st, "r") as fz:
        names = fz.namelist()
        for name in names:
            with fz.open(name, 'r') as f:
                res[name] = f.read()
    return res


def zip_dict(data, **kwargs):
    """
    Zips a dictionary ``{ str: bytes }``.

    @param      data        dictionary
    @param      kwargs      see :epkg:`*py:zipfile:ZipFile`
    @return                 bytes
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", **kwargs) as fz:
        for k, v in sorted(data.items()):
            if not isinstance(k, str):
                raise TypeError("Keys must be a string.")
            if not isinstance(v, bytes):
                raise TypeError("Values must be bytes.")
            fz.writestr(k, v)
    return buffer.getvalue()
