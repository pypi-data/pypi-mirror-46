import contextlib
import os
import shutil
import tempfile
import sys
import traceback

def readtextfile(path):
    return open(path, 'rt', newline='').read()

def readbinaryfile(path):
    return open(path, 'rb').read()

def writebinaryfile(path, body):
    with open(path, 'wb') as g:
        g.write(body)

def make_resp(content, status = 200, mimetype = 'text/plain'):
    import flask
    resp = flask.make_response(content, status)
    resp.headers['Content-Type'] = mimetype
    return resp

@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()

@contextlib.contextmanager
def tempdir(remove_upon_completion=True):
    dirpath = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dirpath)

    if remove_upon_completion:
        with cd(dirpath, cleanup):
            yield dirpath
    else:
        with cd(dirpath):
            yield dirpath

def get_exc_info():
    return '\n'.join(traceback.format_exception(*sys.exc_info()))
