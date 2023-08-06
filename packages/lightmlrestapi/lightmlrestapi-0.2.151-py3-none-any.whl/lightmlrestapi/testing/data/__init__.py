"""
@file
@brief List of testing resources.
"""
import os


def get_wiki_img():
    """
    Returns a path to local image.
    """
    this = os.path.dirname(__file__)
    img = os.path.join(this, "wiki.png")
    if not os.path.exists(img):
        raise FileNotFoundError("Unable to find '{}'.".format(img))
    return img
