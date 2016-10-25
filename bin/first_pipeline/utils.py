import glob
import os

def mkdir_if_not_exist(dir_path: str) -> None:
    """

    :rtype: None
    :param dir_path: str
    """
    if not os.path.isdir(dir_path):
        print('Creating {dir_path}'.format(dir_path=dir_path))
        os.mkdir(dir_path)
    return None