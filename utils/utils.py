import platform
import os
import re
import glob

from tkinter import filedialog as fd


def select_file(**kwargs):

    filetypes = kwargs.get('filetypes', None)
    initialdir = kwargs.get('initialdir', None)
    title = kwargs.get('title', None)

    if not title:
        title = 'Open a file'

    if not filetypes:
        filetypes = (
            ('p1112 data files', '*.p1112'),
            ('Data files', '*.dat'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
    if not initialdir:
        initialdir = '/'

    filename = fd.askopenfilename(
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )

    return filename


def check_points(points: list, attrs: tuple=(int, float)) -> bool:
    for point in points:
        if hasattr(point, '__iter__'):
            if all([isinstance(p, attrs) for p in point]):
                return True
            else:
                return False
        else:
            if all([isinstance(point, attrs) for point in points]):
                return True
            else:
                return False
        

def find_nx_journal_run():
    os_type = platform.system()
    sep = os.sep
    if os_type == 'Windows':
        root_dir = "C:" + sep + 'Siemens' + sep
        if not os.path.exists(root_dir):
            return False
        else:
            run_journal = 'NX*' + sep + 'NXBIN' + sep + 'run_journal.exe'
            nx_journal = glob.glob(pathname=run_journal, root_dir=root_dir, recursive=True)
            if not nx_journal:
                return False
            return os.path.normpath(root_dir + nx_journal[0])


class Utils:

    def __init__(self, in_file: str, **kwargs):
        self.file = in_file

    def find_string(self, string: str = None) -> int or bool:
        
        if not string:
            return False

        pattern = re.compile(string)

        try:
            with open(self.file, 'r') as fi:
                for i, line in enumerate(fi.readlines(), start=1):
                    if re.fullmatch(pattern, line.lower().strip()):
                        return i
        except FileNotFoundError as ex:
            return False

        return False

    def get_line(self, index: int = 1, **kwargs) -> str or bool:
        
        split = kwargs.get('split', False)
        sep = kwargs.get('sep', ' ')

        try:
            with open(self.file, 'r') as fi:
                for i, line in enumerate(fi.readlines(), 1):
                    if i == index:
                        return re.split(sep, line.strip()) if split else line.strip()
            return False
        except FileNotFoundError as ex:
            return False

    def get_lines(self, start: int = 1, stop: int = 1, step: int = 1, **kwargs) -> list:

        split = kwargs.get('split', False)
        sep = kwargs.get('sep', '')

        lines = [(i) for i in range(start, stop+1, step)]

        out = []
        try:
            with open(self.file, 'r') as fi:
                for i, line in enumerate(fi.readlines(), start=1):
                    if i in lines:
                        if split:
                            line = line.strip().split(sep=sep)
                        out.append(line)
            return out
        except FileNotFoundError:
            return False
