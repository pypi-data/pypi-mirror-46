# -*- coding: utf-8 -*-

"""Top-level package for sg-prototype.

Example usage:
from pynwb.docutils.sg_prototype import  build
build('/Users/nicholasc/projects/pynwb/issues/414/helloworld.py', conda_env='pynwb')

"""

import tempfile
import os
import subprocess
import argparse
import shutil
from sys import platform as _platform
import webbrowser
import urllib.parse

__author__ = """Nicholas Cain"""
__email__ = 'nicholasc@alleninstitute.org'
__version__ = '0.1.0'

OPEN_DEFAULT = False
TGT_DIR_DEFAULT_SUFFIX = os.path.abspath('_html_sg-prototype')
TGT_DIR_DEFAULT = os.path.abspath(os.path.join('.', TGT_DIR_DEFAULT_SUFFIX))

def assert_firefox():

    try:
        subprocess.check_output(['firefox', '--version'])
        return True
    except Exception:
        return False


def check_tgt_dir(tgt_dir, clobber=False):
    if os.path.exists(tgt_dir) and not clobber:
        raise RuntimeError('Target directory %s already exists; '
                           'specify a different directory using the -o flag '
                           'or use the --clobber flag to replace' % tgt_dir)
    elif os.path.exists(tgt_dir) and clobber:
        shutil.rmtree(tgt_dir)


def build(src_file, tgt_dir=TGT_DIR_DEFAULT, open_html=OPEN_DEFAULT, conda_env=None, clobber=False):

    if _platform == 'win32':
        raise RuntimeError('Windows is not supported')

    # Get temporary build dir, and make html using template:
    temp_dir = tempfile.mkdtemp()
    template_loc = 'https://github.com/nicain/sg-template.git'

    err_code = subprocess.call('git clone %s %s' % (template_loc, temp_dir), shell=True)
    assert err_code == 0

    # remove the template example, and replace with user-supplied file
    if src_file is not None:
        os.remove(os.path.join(temp_dir, 'docs', 'gallery', 'helloworld.py'))
        shutil.copy(src_file, os.path.join(temp_dir, 'docs', 'gallery', os.path.basename(src_file)))

    docs_dir = os.path.join(temp_dir, 'docs')
    print(docs_dir)
    if conda_env is None:
        err_code = subprocess.call('make html', shell=True, cwd=docs_dir)
    else:
        err_code = subprocess.call('source activate %s && \
                                    make html' % (conda_env, docs_dir), shell=True, cwd=docs_dir)
    assert err_code == 0

    # Move built html to tgt_dir:
    check_tgt_dir(tgt_dir, clobber)
    shutil.move(os.path.join(temp_dir, 'docs', '_build', 'html'), tgt_dir)

    # Grab out generated example file:
    if src_file is not None:
        infile_slug = os.path.basename(src_file).split('.')[0]
    else:
        infile_slug = 'helloworld'
    fname_slug = '%s.html' % infile_slug
    output_file = os.path.join(tgt_dir, 'tutorials', fname_slug)
    if not os.path.exists(output_file):
        raise RuntimeError('File generation failed')
    print('Output file generated: %s' % output_file)

    # Open or print file:
    if open_html is True:
        output_file_split = urllib.parse.urlsplit(output_file, scheme='file')
        output_file_unsplit = urllib.parse.urlunsplit(output_file_split)
        webbrowser.open(output_file_unsplit)

    return 0


def main():

    # Define command line args:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('src_file', type=str, help='file to convert; if not supplied, will use a helloworld', nargs='*')
    parser.add_argument('-o', '--output', type=str, help='output directory of build', default=None, dest='tgt_dir')
    parser.add_argument('--open', action='store_true', default=OPEN_DEFAULT, help='automatically open after build (experimental)')
    parser.add_argument('--clobber', action='store_true', dest='clobber', default=False, help='remove target directory if it exists')

    # Unpack args:
    args = parser.parse_args()
    if len(args.src_file) != 0:
        src_file = os.path.expanduser(args.src_file[0])
    else:
        src_file = None
    open_html = args.open
    tgt_dir = args.tgt_dir
    if tgt_dir is None:
        tgt_dir = os.path.join(os.path.abspath(os.path.expanduser(os.path.curdir)), TGT_DIR_DEFAULT_SUFFIX)

    check_tgt_dir(tgt_dir, args.clobber)

    return build(src_file, tgt_dir=tgt_dir, open_html=open_html, clobber=args.clobber)

if __name__ == "__main__":
    main()
