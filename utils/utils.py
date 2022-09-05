import os
import re

file_name = os.path.join(r'E:\Kokorev\pipe_diffuser\code\samples\diffuser7_test402.p1112')


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
