import subprocess

from utils.utils import find_nx_journal_run as fnx



if __name__ == "__main__":

    nx_journal = fnx()
    print(nx_journal)
    subprocess.run(nx_journal)
