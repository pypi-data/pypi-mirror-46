from typing import *
import requests
import json
import os
import zipfile
from pathlib import Path
import functools


def hello(name: str = 'Raja') -> str:
    return f"Hello, {name}"


def print_dir_values(obj):
    for d in dir(obj):

        try:
            func = getattr(obj, d)
            if callable(func):
                print(func())
            else:
                print(func)
            print('^' + str(d))
        #         print(d + ":" + func())
        except:
            pass


def post_json(a_url: str, raw_data: Dict):
    headers = {"Content-type": "application/json"}

    mandatory = dict(headers=headers, data=json.dumps(raw_data))

    inp = mandatory
    try:
        result = requests.post(a_url, **inp)
        result.raise_for_status()
        return result.json()

    except requests.exceptions.RequestException as e:
        print(e)
        if result:
            print(f'Error:{result.json()}')
        raise e


# def post(a_url: str, raw_data: Dict, headers: Dict = None, files: Dict = None):
#     mandatory = dict(headers=headers, data=json.dumps(raw_data))
#
#     inp = {**mandatory, **optional(files=files)}
#     try:
#         result = requests.post(a_url, **inp)
#         result.raise_for_status()
#         return result.json()
#
#     except requests.exceptions.RequestException as e:
#         print(e)
#         if result:
#             print(f'Error:{result.json()}')
#         raise e

def post(url: str, raw_data: Dict = None, files: Dict = None, headers: Dict = None):
    import os
    result = None
    payload = raw_data
    inp = dict()
    if raw_data:
        inp = {**inp, **dict(json=(None, json.dumps(payload), 'application/json'))}
    if files:
        file_dict = dict()
        for k, v in files.items():
            file_dict[k] = (os.path.basename(v), open(v, 'rb'), 'application/octet-stream')
        # files = dict(file=(os.path.basename(file), open(file, 'rb'), 'application/octet-stream'))
        inp = {**inp, **file_dict}
        pass

    try:
        if headers:
            result = requests.post(url, headers=headers, files=inp, verify=False)
        else:
            result = requests.post(url, files=inp, verify=False)
        result.raise_for_status()
        return result.json()

    except requests.exceptions.RequestException as e:
        print(e)
        if result:
            print(f'Error:{result.json()}')
        raise e

    pass


def post_file(a_url: str, files: Dict):
    headers = {'Content-type': 'multipart/form-data'}

    try:
        result = requests.post(a_url, headers=headers, files=files)
        result.raise_for_status()
        return result

    except requests.exceptions.RequestException as e:
        print(e)
        if result:
            print(f'Error:{result.json()}')
        raise e


def optional(**kwargs):
    return {k: v for k, v in kwargs.items() if v}


def module_path(file_or_dir_module_or_python_object_or_file_path):
    try:
        if os.path.exists(file_or_dir_module_or_python_object_or_file_path):
            return file_or_dir_module_or_python_object_or_file_path
    except:
        if '__path__' in file_or_dir_module_or_python_object_or_file_path.__dict__:
            return file_or_dir_module_or_python_object_or_file_path.__path__[0]
        elif '__file__' in file_or_dir_module_or_python_object_or_file_path.__dict__:
            return file_or_dir_module_or_python_object_or_file_path.__file__
        elif callable(file_or_dir_module_or_python_object_or_file_path):
            if type(file_or_dir_module_or_python_object_or_file_path) == functools.partial:
                return file_or_dir_module_or_python_object_or_file_path.func.__globals__['__file__']
            else:
                return file_or_dir_module_or_python_object_or_file_path.__globals__['__file__']
            # return file_or_dir_module_or_python_object_or_file_path.__globals__['__file__']
        else:
            raise ValueError('Is {} a module at all??'.format(str(file_or_dir_module_or_python_object_or_file_path)))


def archive(output_path: Path, dir_or_files=List[str]):
    make_zipfile(output_path, dir_or_files)


def make_zipfile(output_filename, source_dirs_or_files):
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for source_dir_or_file in source_dirs_or_files:
            relroot = os.path.abspath(os.path.join(source_dir_or_file, os.pardir))
            if os.path.isdir(source_dir_or_file):
                for root, dirs, files in os.walk(source_dir_or_file):
                    for file in files:
                        filename = os.path.join(root, file)
                        if os.path.isfile(filename):  # regular files only
                            arcname = os.path.join(os.path.relpath(root, relroot), file)
                            if '__pycache__' in arcname or '.pyc' in arcname:
                                continue
                            zip.write(filename, arcname)
            else:
                filename = source_dir_or_file.split('/')[-1]
                zip.write(source_dir_or_file, filename)


def file_name(path: str) -> str:
    return os.path.basename(path)


def make_requirements_file(working_dir: Path) -> Path:
    from sys import stderr
    from subprocess import run, PIPE
    cmd = ['pip', 'freeze']
    # out = run(cmd, env=env, stdout=PIPE, stderr=PIPE)
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    result = out.stdout.decode('utf-8')
    if out.returncode != 0:
        print(out.stdout.decode('utf-8'))
        print(out.stderr.decode('utf-8'), file=stderr)
        raise ValueError('Cannot determine requirements')

    req_path = working_dir / 'requirements.txt'
    req_path.write_text(result)
    return req_path


def determine_project_folder() -> str:
    return 'dummpy_project_folder'


def tmp_folder(folder_name: str = None, prefix='delete_me') -> Path:
    import uuid
    import tempfile
    folder_name = folder_name or (prefix + '_' + str(uuid.uuid4()))

    tmp_dir = Path(tempfile.gettempdir()) / folder_name
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def remove_dir(a_dir: Path):
    import shutil
    shutil.rmtree(a_dir)
    pass


def read_json(path: Path) -> Dict:
    with path.open('r') as json_file:
        return json.load(json_file)


if __name__ == '__main__':
    # wdir = tmp_folder()
    # req_path = make_requirements_file(wdir)
    # print('Req Path')
    # print(req_path.read_text())
    print(module_path('/Users/rabraham/Documents/dev/python/fifteenrock/fifteenrock/lib'))
    pass
