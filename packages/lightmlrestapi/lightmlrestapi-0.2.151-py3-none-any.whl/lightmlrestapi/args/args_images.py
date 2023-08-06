"""
@file
@brief Playground with images.
"""
import io
import os
import base64
import numpy
from PIL import Image


def image2array(img):
    """
    Converts a color imaged into an array.

    @param      img     :epkg:`PIL:Image.Image`
    @return             :epkg:`numpy:array`
    """
    im_arr = numpy.frombuffer(img.tobytes(), dtype=numpy.uint8)
    return im_arr.reshape((img.size[1], img.size[0], 3))  # pylint: disable=E1121


def image2base64(path, fmt='png'):
    """
    Encodes an image into :epkg:`*pyf:base64`.

    @param      path        filename or an image
    @param      fmt         if the image is given as an image (:epkg:`Pillow`),
                            it must be first saved in a specific format (png, jpg, ...)
    @return                 format, base64

    The format is the file extension.
    """
    if isinstance(path, bytes):
        content = path
        ext = None
    elif hasattr(path, 'convert'):
        # Most probably a Pillow object
        st = io.BytesIO()
        path.save(st, format=fmt)
        content = st.getvalue()
        ext = 'png'
    else:
        ext = os.path.splitext(path)[-1].lower().strip('.')
        with open(path, "rb") as f:
            content = f.read()
    return 'image/' + ext, base64.b64encode(content)


def base642image(encoded):
    """
    Gets an encoded image and builds an
    :epkg:`PIL:Image.Image` from it.

    @param      encoded     :epkg:`*pyf:base64` encoded image
                            (see @see fn image2base64)
    @return                 :epkg:`PIL:Image.Image`
    """
    cont = base64.b64decode(encoded)
    return Image.open(io.BytesIO(cont))


def bytes2string(content):
    """
    Converts bytes to string.
    """
    return base64.b64encode(content)


def string2bytes(content):
    """
    Converts string to bytes.
    """
    return base64.b64decode(content)
