import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.tix import INTEGER


class GUI:
    def __init__(self, master: Tk):
        
        self.of_data = {
        'filetypes': (('p1112 Data Files', '*.p1112'), ('All Files', '*.*')),
        'initialdir': '/',
        'title': 'Open p1112 Indata File'
        }

        self.font = ("Helvetica", 12)

        self.master = master
        self.master.geometry("400x200+20+20")
        self.master.title('Pipe Difuser Designer')
        self.master.resizable = False

        self.frame = ttk.Frame(self.master, padding=20, borderwidth=2, relief='sunken')
        self.frame.grid(column=0, row=0, sticky=(W, E, N, S))

        lbl_ns = ttk.Label(self.frame, text='Enter number of sections:\t', font=self.font)
        lbl_ns.grid(column=0, row=0, sticky=W)

        self.__num_sec = IntVar()
        self.__num_sec.set(25)
        self.ns_entry = ttk.Entry(self.frame, textvariable=self.__num_sec, 
            font=self.font, width=5
        )
        self.ns_entry.grid(column=1, row=0, sticky=W)

        self.btn_of = ttk.Button(self.frame, text='Open data file', 
        command=lambda: self.select_file(**self.of_data))
        self.btn_of.grid(column=0, row=1, sticky=W)

        self.btn_save = ttk.Button(self.frame, text='Save prt File', 
        command=lambda: self.save_file_as(title='Save NX file'))
        self.btn_save.grid(column=0, row=2, sticky=W)

        self.__indata_file = ''
        self.__saveas = ''

    @property
    def num_sec(self):
        return self.__num_sec.get()

    @property
    def indata_file(self):
        return self.__indata_file

    @property
    def saveas(self):
        return self.__saveas

    def select_file(self, **kwargs):

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

        self.__indata_file = fd.askopenfilename(
            title=title,
            initialdir=initialdir,
            filetypes=filetypes
        )


    def save_file_as(self, **kwargs):

        defaultextension = kwargs.get('defaultextension', (('NX part file', '*.prt'),))
        filetypes = kwargs.get('filetypes', (('NX part file', '*.prt'),))
        initialdir = kwargs.get('initialdir', '/')
        initialfile = kwargs.get('inititalfile', 'pipe_diffuser.prt')
        title = kwargs.get('title', 'Save as')

        self.__saveas = fd.asksaveasfilename(
            defaultextension=defaultextension,
            filetypes=filetypes,
            initialdir=initialdir,
            initialfile=initialfile,
            title=title
        )
        self.master.quit()
