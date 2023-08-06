import atexit
import git
import os
import shutil
import sys
import tempfile
import warnings

from pip._internal import main

def remote_import(url, what=None, install=False):
    """
    For execution of snippets. Returns a module or package
    and adds it to the path. If what is given, import via
    name first, then search for url.
    """
    try:
        assert isinstance(what, str)
        return __import__(what)
    except (ModuleNotFoundError, AssertionError):
        wd = os.getcwd()
        try:
            random_path = tempfile.mkdtemp()
            atexit.register(lambda: shutil.rmtree(random_path))
            repo = git.Repo.clone_from(url, random_path)
            os.chdir(random_path)
            if not isinstance(what, str):
                what = [x for x in os.listdir(".") if os.path.isdir(x)]
                what = [x for x in what if "__init__.py" in os.listdir(x)]
                if len(what) > 1:
                    raise ImportError("There are more than one package in the directory. "
                                      "Please specify `what` to import")
                elif len(what) < 1:
                    raise ImportError("There are no packages in the directory. "
                                      "Please specify `what` to import")
                what = what[0]
            if install:
                try:
                    assert not main(["install", "."])
                except AssertionError:
                    warnings.warn("Cannot install, will import the module once")
                    sys.path.append(random_path)
                    return __import__(what)
                else:
                    return __import__(what)
            else:
                sys.path.append(random_path)
                return __import__(what)
        finally:
            os.chdir(wd)
