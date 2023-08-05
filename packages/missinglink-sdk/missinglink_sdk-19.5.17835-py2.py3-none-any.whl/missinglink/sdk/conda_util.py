import logging
import os

import requests

conda_timeout_seconds = 3.0

logger = logging.getLogger('missinglink')


def is_conda_env():
    return os.environ.get('CONDA_DEFAULT_ENV') is not None


def get_latest_conda_version(keywords, throw_exception=False):
    try:
        channel = 'missinglink.ai' if 'test' not in keywords else 'missinglink-test'
        url = 'https://api.anaconda.org/package/{}/missinglink-sdk'.format(channel)
        r = requests.get(url, timeout=conda_timeout_seconds)
        r.raise_for_status()

        package_info = r.json()
        versions = package_info['versions']
        max_ver = max(versions, key=lambda v: tuple(int(t) for t in v.split('.')))

        print('latest codna version %s (staging version: %s))' % (max_ver, 'test' in keywords))

        return max_ver
    except Exception as e:
        if throw_exception:
            raise

        logger.exception('could not check for new missinglink-sdk version:\n%s', e)
        return None


def conda_install(keywords, require_package):
    from subprocess import Popen, PIPE

    channel = 'missinglink-test' if 'test' in keywords else 'missinglink.ai'
    env_name = os.environ.get('CONDA_DEFAULT_ENV')
    conda_exe = os.environ.get('CONDA_EXE')
    args = [conda_exe, 'install', '-n', env_name, '-c', channel, '--update-deps', '-y', require_package]
    try:
        logger.info('conda install => %s', ' '.join(args))
        return Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE), args
    except Exception:
        logger.exception("%s failed", " ".join(str(a) for a in args))
        return None, args
