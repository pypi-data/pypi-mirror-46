import os
import errno
import ntpath


def ensure_folder(path):
    """Ensures that a folder exists. If it doesn't, it creates it."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def split_path(filepath):
    """Splits a file path into folder path, file name and extension"""
    head, tail = ntpath.split(filepath)
    filename, extension = os.path.splitext(tail)
    return head, filename, extension


def get_file_extension(filepath):
    _, file_extension = os.path.splitext(filepath)
    return file_extension


def get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

