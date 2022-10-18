# encoding: utf-8

"""
Test module for ``ldpred2.sif`` singularity build 
or ``ldpred2`` dockerfile build

In case ``singularity`` is unavailable, the test function(s) should fall 
back to ``docker``.
"""

import os
import socket
import subprocess


# port used by tests
sock = socket.socket()
sock.bind(('', 0))
port = sock.getsockname()[1]


# Check that (1) singularity exist, and (2) if not, check for docker. 
# If neither are found, tests will not run.
try:
    pth = os.path.join('containers', 'ldpred2.sif')
    out = subprocess.run('singularity')
    cwd = os.getcwd()
    PREFIX = f'singularity run {pth}'
    PREFIX_MOUNT = f'singularity run --home={cwd}:/home/ {pth}'
except FileNotFoundError:    
    try:
        out = subprocess.run('docker')
        pwd = os.getcwd()
        PREFIX = f'docker run -p {port}:{port} ldpred2'
        PREFIX_MOUNT = (f'docker run -p {port}:{port} ' + 
            f'--mount type=bind,source={pwd},target={pwd} ldpred2')
    except FileNotFoundError:
        raise FileNotFoundError('Neither `singularity` nor `docker` found in PATH. Can not run tests!')


def test_ldpred2_R():
    call = f'{PREFIX} R --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0

def test_ldpred2_Rscript():
    call = f'{PREFIX} Rscript --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0

def test_ldpred2_R_libraries():
    pwd = os.getcwd() if PREFIX.rfind('docker') >= 0 else '.'
    call = f'''{PREFIX_MOUNT} Rscript {pwd}/tests/extras/libraries.R'''
    out = subprocess.run(call.split(' '), capture_output=True)
    assert out.returncode == 0