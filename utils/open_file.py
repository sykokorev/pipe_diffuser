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


def save_file_as(**kwargs):

    defaultextension = kwargs.get('defaultextension', (('NX part file', '*.prt'),))
    filetypes = kwargs.get('filetypes', (('NX part file', '*.prt'),))
    initialdir = kwargs.get('initialdir', '/')
    initialfile = kwargs.get('inititalfile', 'pipe_diffuser.prt')
    title = kwargs.get('title', 'Save as')

    saveas = fd.asksaveasfilename(
        defaultextension=defaultextension,
        filetypes=filetypes,
        initialdir=initialdir,
        initialfile=initialfile,
        title=title
    )

    return saveas
