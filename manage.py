import logging
import os
import re
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('manage.py')

UUID = '46ea591951824d8e9376b0f98fe4d48a'
PROJECT_NAME = 'PROJECT_' + UUID
PROJECT_UPPER_NAME = 'PROJECT_UPPER_' + UUID
PROJECT_LOWER_NAME = 'project_lower_' + UUID
APP_NAME = 'APP_' + UUID
APP_UPPER_NAME = 'APP_UPPER_' + UUID
APP_LOWER_NAME = 'app_lower_' + UUID

def showUsage():
    print('''Usage:
    python manage.py <option>
    python manage.py startproject <project-name> <api-app-name> [<output-dir>]
    python manage.py startapp <project-name> <app-name> [<output-dir>]
    python manage.py renameapp <old-name> <new-name> [<output-dir>]
    ''')
    sys.exit()


def sed(old, new, filePath):
    ignoreRegex = re.compile(r'(\.((db)|(png)|(js.map))$)|(\.git)|(dist)')
    if ignoreRegex.search(filePath):
        return
    try:
        lines = [i.replace(old, new) for i in open(filePath) if not ignoreRegex.search(filePath)]
        open(filePath, 'w').writelines(lines)
    except UnicodeDecodeError as e:
        log.warning('old = {}, new = {}, filePath = {}'.format(old, new, filePath))
        log.warning(e)


def mv(old, new, filePath):
    if old in filePath:
        cmdStr = r'mv {} {}'.format(filePath, filePath.replace(old, new))
        log.debug(cmdStr)
        os.system(cmdStr)


def opt_startproject(projectName, appName, base=os.path.join(BASE_DIR, 'output')):
    if os.path.exists(base) and base != os.path.join(BASE_DIR, 'output'):
        log.error("directory <%s> already exist!" % base)
        return
    os.system(r'rm -rf {} && cp -r {} {} && rm -rf {} {}'.format(
        base,
        os.path.join(BASE_DIR, 'template'),
        base,
        os.path.join(base, 'dist'),
        os.path.join(base, 'doc')
        ))
    for root, dirs, files in os.walk(base):
        for name in dirs:
            absPath = os.path.join(root, name)
            mv(PROJECT_NAME, projectName, absPath)
            mv(APP_NAME, appName, absPath)
    for root, dirs, files in os.walk(base):
        for name in files:
            absPath = os.path.join(root, name)
            sed(PROJECT_NAME, projectName, absPath)
            sed(PROJECT_LOWER_NAME, projectName.lower(), absPath)
            sed(PROJECT_UPPER_NAME, projectName.upper(), absPath)
            sed(APP_NAME, appName, absPath)
            sed(APP_LOWER_NAME, appName.lower(), absPath)
            sed(APP_UPPER_NAME, appName.upper(), absPath)
            mv(PROJECT_NAME, projectName, absPath)
            mv(APP_NAME, appName, absPath)


def opt_startapp(projectName, appName, base=os.path.join(BASE_DIR, 'output')):
    os.system(r'cp -r {} {} && cp -r {} {} && cp -r {} {}'.format(
        os.path.join(BASE_DIR, 'template', 'build', APP_NAME), os.path.join(base, 'build'),
        os.path.join(BASE_DIR, 'template', 'cmd', APP_NAME), os.path.join(base, 'cmd'),
        os.path.join(BASE_DIR, 'template', 'internal', APP_NAME), os.path.join(base, 'internal')
        ))
    for root, dirs, files in os.walk(base):
        for name in dirs:
            absPath = os.path.join(root, name)
            mv(PROJECT_NAME, projectName, absPath)
            mv(APP_NAME, appName, absPath)
    for root, dirs, files in os.walk(base):
        for name in files:
            absPath = os.path.join(root, name)
            sed(PROJECT_NAME, projectName, absPath)
            sed(APP_LOWER_NAME, appName.lower(), absPath)
            sed(APP_NAME, appName, absPath)
            sed(APP_UPPER_NAME, appName.upper(), absPath)
            mv(PROJECT_NAME, projectName, absPath)
            mv(APP_NAME, appName, absPath)

def opt_renameapp(oldName, newName, base=os.path.join(BASE_DIR, 'output')):
    for root, dirs, files in os.walk(base):
        for name in dirs:
            absPath = os.path.join(root, name)
            mv(oldName, newName, absPath)
    for root, dirs, files in os.walk(base):
        for name in files:
            absPath = os.path.join(root, name)
            sed(oldName.lower(), newName.lower(), absPath)
            sed(oldName, newName, absPath)
            sed(oldName.upper(), newName.upper(), absPath)
            mv(oldName, newName, absPath)

def _assert_cmd_exist(cmd):
    try:
        subprocess.call(cmd)
    except Exception as e:
        log.warning('{}->{}'.format(type(e), e))
        log.error('Command "{}" not exist!'.format(cmd))
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        showUsage()

    selfModule = __import__(__name__)
    optFunName = 'opt_' + sys.argv[1].strip()
    if optFunName not in selfModule.__dict__:
        showUsage()

    if BASE_DIR.strip():
        os.chdir(BASE_DIR)
    try:
        selfModule.__dict__[optFunName](*sys.argv[2:])
    except TypeError as e:
        log.error('{} failed: {}'.format(optFunName, e))
        raise
