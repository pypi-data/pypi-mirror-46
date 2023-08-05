from typing import *


from fifteenrock.core import deploy
from fifteenrock import helper
from fifteenrock.lib import util

import nbformat
import nbconvert
from nbconvert import PythonExporter

from notebook.notebookapp import list_running_servers
import re
from urllib.parse import urlencode, urljoin

import logging

log = logging.getLogger(__name__)


class StripMagicsProcessor(nbconvert.preprocessors.Preprocessor):
    """
    Preprocessor to convert notebooks to Python source while stripping
    out all magics (i.e IPython specific syntax).
    """

    _magic_pattern = re.compile('^\s*(?P<magic>%%\w\w+)($|(\s+))')

    def strip_magics(self, source):
        """
        Given the source of a cell, filter out all cell and line magics.
        """
        filtered = []
        for line in source.splitlines():
            match = self._magic_pattern.match(line)
            if match is None:
                filtered.append(line)
            else:
                msg = 'Stripping out IPython magic {magic} in code cell {cell}'
                message = msg.format(cell=self._cell_counter, magic=match.group('magic'))
                log.warn(message)
        return '\n'.join(filtered)

    def preprocess_cell(self, cell, resources, index):
        if cell['cell_type'] == 'code':
            self._cell_counter += 1
            cell['source'] = self.strip_magics(cell['source'])
        return cell, resources

    def __call__(self, nb, resources):
        self._cell_counter = 0
        return self.preprocess(nb, resources)


PREPROCESSORS = [StripMagicsProcessor()]


#
# def notebook_file_name(ikernel):
#     """Return the full path of the jupyter notebook."""
#     # Check that we're running under notebook
#     if not (ikernel and ikernel.config['IPKernelApp']):
#         return
#
#     kernel_id = re.search('kernel-(.*).json',
#                           ipykernel.connect.get_connection_file()).group(1)
#     print('Kernel Id')
#     print(kernel_id)
#     servers = list_running_servers()
#     print('Running Servers')
#     print(servers)
#
#     for srv in servers:
#         query = {'token': srv.get('token', '')}
#         print('Query')
#         print(query)
#         print('Server Url')
#         print(srv['url'])
#         url = urljoin(srv['url'], 'api/sessions') + '?' + urlencode(query)
#         print("Url")
#         print(url)
#         for session in json.load(urlopen(url)):
#             if session['kernel']['id'] == kernel_id:
#                 relative_path = session['notebook']['path']
#                 return path.join(srv['notebook_dir'], relative_path)


def notebook_file_name(ikernel):
    from IPython import get_ipython
    import ipykernel
    """Return the full path of the jupyter notebook."""
    # Check that we're running under notebook
    if not (ikernel and ikernel.config['IPKernelApp']):
        return

    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    print('Kernel Id')
    print(kernel_id)
    servers = list_running_servers()
    print('Running Servers')
    print(servers)

    for srv in servers:
        query = {'token': srv.get('token', '')}
        print('Query')
        print(query)
        print('Server Url')
        print(srv['url'])
        url = urljoin(srv['url'], 'api/sessions') + '?' + urlencode(query)
        print("Url")
        print(url)
        # for session in json.load(urlopen(url)):
        #     if session['kernel']['id'] == kernel_id:
        #         relative_path = session['notebook']['path']
        #         return path.join(srv['notebook_dir'], relative_path)

    return 'FakeServer/Path'


def deploy_notebook(project: str, function: str, url: str = None, dependencies: List = None,
                    credentials: Dict = None) -> None:
    if is_notebook():
        save_current_notebook()
        from IPython import get_ipython
        import ipykernel
        # credentials = credentials or helper.determine_credentials()

        tmp_dir = util.tmp_folder()

        try:
            module_path = tmp_dir / 'main.py'
            kernel = get_ipython()
            print('Kernel:')
            print(kernel)

            notebook_path = notebook_file_name(kernel)
            print('Notebook Path')
            print(notebook_path)

            print('This file')
            print(__file__)
            # convert_notebook(notebook_path, module_path)
            convert_notebook(notebook_path, module_path, PREPROCESSORS)
            print('Deploying notebook. This will take a while...')
            result = deploy(credentials=credentials, main_file=str(module_path), project=project, function=function,
                            url=url,
                            dependencies=dependencies)
            print('Result:')
            print(result)
            return result
        except Exception as e:
            raise e
        finally:
            # util.remove_dir(tmp_dir)
            pass

    else:
        print('WARNING: deploy_notebook is only executed from a notebook')
        pass


def save_current_notebook():
    from IPython.display import Javascript

    script = '''
    require(["base/js/namespace"],function(Jupyter) {
        Jupyter.notebook.save_checkpoint();
    });
    '''
    Javascript(script)
    print('This notebook has been saved.')


# def convert_notebook(notebook_path, module_path):
#     with open(notebook_path) as fh:
#         nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
#
#     exporter = PythonExporter()
#     source, meta = exporter.from_notebook_node(nb)
#
#     with open(module_path, 'w') as fh:
#         fh.writelines(source)


def convert_notebook(notebook_path, module_path, preprocessors):
    with open(notebook_path) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

    exporter = PythonExporter()
    for preprocessor in preprocessors:
        exporter.register_preprocessor(preprocessor)

    source, meta = exporter.from_notebook_node(nb)
    source = source.replace('get_ipython().run_line_magic', '')

    with open(module_path, 'w') as fh:
        fh.writelines(source)


def is_notebook():
    from IPython import get_ipython
    import ipykernel
    try:
        kernel = get_ipython()
        shell = kernel.__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter
