#####################################################################################################
#####################################################################################################
#################   _____ ____________ ______ ______          _                     #################
#################  |  ___|___  /| ___ \___  / | ___ \        | |                    #################
#################  | |__    / / | |_/ /  / /  | |_/ /_ _  ___| | ____ _  __ _  ___  #################
#################  |  __|  / /  |  __/  / /   |  __/ _` |/ __| |/ / _` |/ _` |/ _ \ #################
#################  | |___./ /___| |   ./ /___ | | | (_| | (__|   < (_| | (_| |  __/ #################
#################  \____/\_____/\_|   \_____/ \_|  \__,_|\___|_|\_\__,_|\__, |\___| #################
#################                                                        __/ |      #################
#################                                                       |___/       #################
#################                                                                   #################
#################                                        Author: Jacob Brehm (2019) #################
#####################################################################################################
#####################################################################################################

## GUI PACKAGES
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import filedialog as fd
from tkinter import messagebox as mb

#####################################################################################################
#################                            GUI BUILDING                           #################
#####################################################################################################

class Application(tk.Frame):

    def __init__(self, *args, padding=None, **kwargs):

        self.root = tk.Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        tk.Frame.__init__(self, *args, master=self.root, **kwargs)

        if padding and type(padding) == int:
            padx = padding
            pady = padding
        elif padding and type(padding) == tuple:
            padx = padding[0]
            pady = padding[1]
        else:
            padx = 0
            pady = 0

        self.grid(row=0, column=0, padx=padx, pady=pady, sticky='NSEW')
        self.grid_columnconfigure(0, weight=1)

    def configure(self, title=None, resizable=(True, True)):
        self.root.title(title)

        if resizable and type(resizable) == bool:
            self.root.resizable(width=True, height=True)
        elif not resizable and type(resizable) == bool:
            self.root.resizable(width=False, height=False)
        elif resizable and type(resizable) == tuple and len(resizable) == 2:
            self.root.resizable(width=resizable[0], height=resizable[1])
        else:
            self.root.resizable(width=True, height=True)

    def window(self, center=True):

        self.root.update()

        padding_x = self.root.winfo_width() - self.winfo_width()
        padding_y = self.root.winfo_height() - self.winfo_height()

        frames = self.winfo_children()

        frame_heights = []
        for frame in frames:
            if frame.winfo_ismapped():
                frame_heights.append(frame.winfo_height())
        PROGRAM_HEIGHT = sum(frame_heights) + padding_y

        frame_widths = []
        for frame in frames:
            if frame.winfo_ismapped():
                frame_widths.append(frame.winfo_width())
        PROGRAM_WIDTH = max(frame_widths) + padding_x

        X_POSITION = ( self.root.winfo_screenwidth() - PROGRAM_WIDTH )/2
        Y_POSITION = ( self.root.winfo_screenheight() - PROGRAM_HEIGHT )/2

        if center:
            self.root.geometry(str(PROGRAM_WIDTH) + "x" + str(PROGRAM_HEIGHT) + "+" \
                          + str(int(X_POSITION)) + "+" + str(int(Y_POSITION)))
        elif not center:
            self.root.geometry(str(PROGRAM_WIDTH) + "x" + str(PROGRAM_HEIGHT))

    @property
    def parent(self):
        return self.root

    def mainloop(self):
        self.window()
        self.root.mainloop()


class Header(tk.Frame):

    def __init__(self, *args, logo=None, downscale=None, **kwargs):

        # from PIL import Image, ImageTk

        tk.Frame.__init__(self, *args, **kwargs)
        MARGIN_SIZE = 20

        logo_title = tk.Frame(self)
        logo_title.grid_columnconfigure(0, weight=1)
        logo_title.grid(row=0, column=0, sticky='EW')

        if logo:
            try:
                logo_render = RenderImage(logo, downscale=downscale)
                title = ttk.Label(logo_title, image=logo_render)
                title.photo = logo_render
            except FileNotFoundError:
                title = ttk.Label(logo_title, text=logo, font=('Helvetica', 22, 'bold'))
        else:
            title = ttk.Label(logo_title, text='EZPZ', font=('Helvetica', 22, 'bold'))
        title.grid(row=0, column=0, padx=10)

        self.grid_columnconfigure(0, weight=1)


class Separator(tk.Frame):

    def __init__(self, *args, padding=None, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        if padding and type(padding) == int:
            padx = (padding, padding)
            pady = (padding, padding)
        elif padding and type(padding) == tuple:
            if type(padding[0]) == tuple and len(padding[0]) == 2:
                padx = padding[0]
            else:
                padx = (padding[0], padding[0])

            if type(padding[1]) == tuple and len(padding[1]) == 2:
                pady = padding[1]
            else:
                pady = (padding[1], padding[1])
        else:
            padx = (0, 0)
            pady = (0, 0)

        ttk.Separator(self, orient='horizontal').grid(row=1, column=1, sticky="EW")
        self.columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=pady[0])
        self.grid_rowconfigure(2, minsize=pady[1])
        self.grid_columnconfigure(0, minsize=padx[0])
        self.grid_columnconfigure(2, minsize=padx[1])


class Space(tk.Frame):

    def __init__(self, *args, row, column, padding=20, **kwargs):
        tk.Frame.__init__(self, *args, height=padding, **kwargs)
        self.grid(row=row, column=column, sticky='NSEW')


class InputField(tk.Frame):

    def __init__(self, *args, quantity, fullpath=True, width=40,
                 title='Select the input', **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.quantity = quantity
        self.width = width
        self.fullpath = fullpath
        self.title = title

        self.inputs = []

        if quantity == 'single':
            label = ttk.Label(self, text='Input location:')
            label.grid(row=0, column=0, sticky='EW')
            self.entry = ttk.Entry(self, state='readonly')
            self.entry.grid(row=1, column=0, padx=(0,2), sticky='EW')
            button = ttk.Button(self, takefocus=0, text='Browse...', command=self.Browse)
            button.grid(row=1, column=1, sticky='NSEW')
            self.columnconfigure(0, weight=1)

        elif quantity == 'multiple':
            self.list = tk.Listbox(self, state='normal', height=5, width=self.width, justify='center')
            self.list.grid(row=1, column=0, padx=(0,2), sticky="EW")
            info = ['',
                          '',
                          'Selecting multiple files is optional.',
                          '',
                          '']
            [self.list.insert('end', item) for item in info]
            self.list.config(state='disabled')

            controls = tk.Frame(self)
            button = ttk.Button(controls, takefocus=0, text='Browse...', command=self.Browse)
            button.grid(row=0, column=0, sticky="NSEW")
            controls.grid_rowconfigure(0, weight=1)
            controls.grid(row=1, column=1, sticky="NSEW")

        self.grid_columnconfigure(0, weight=1)

    def Browse(self):

        if self.quantity == 'single':
            file = fd.askopenfilename(title=self.title)
            if file:
                self.entry.config(state='normal')
                self.entry.delete(0, 'end')
                if self.fullpath:
                    self.entry.insert(0, file)
                else:
                    filename = file.split('/')[-1]
                    self.entry.insert(0, filename)
                self.entry.config(state='readonly')
                self.entry.update_idletasks()
                self.entry.xview_moveto(1)
            self.inputs = file

        elif self.quantity == 'multiple':
            files = fd.askopenfilenames(title=self.title)
            if files:
                self.inputs = list(files)
                self.list.config(state='normal')
                self.list.delete(0, 'end')
                if self.fullpath:
                    [self.list.insert('end', ' ' + file) for file in self.inputs]
                else:
                    filenames = [file.split('/')[-1] for file in self.inputs]
                    [self.list.insert('end', ' ' + file) for file in filenames]
                self.list.config(state='disabled')
                self.list.config(justify='left')

    @property
    def get(self):
        return self.inputs


class OutputField(tk.Frame):

    def __init__(self, *args, quantity, filetypes, default, fullpath=True,
                 title='Choose output destination', **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.quantity = quantity
        self.filetypes = filetypes
        self.default = default
        self.fullpath = fullpath
        self.title = title

        self.output = None

        label = ttk.Label(self, text='Output destination:')
        label.grid(row=0, column=0, sticky='EW')
        self.entry = ttk.Entry(self, state='readonly')
        self.entry.grid(row=1, column=0, padx=(0,2), sticky='EW')
        button = ttk.Button(self, takefocus=0, text='Browse...', command=self.Browse)
        button.grid(row=1, column=1, sticky='NSEW')
        self.columnconfigure(0, weight=1)

    def Browse(self):

        if self.quantity == 'saveas':
            self.output = fd.asksaveasfilename(title=self.title,
                                          filetypes=self.filetypes,
                                          defaultextension=self.default)
            if self.output:
                self.entry.config(state='normal')
                self.entry.delete(0, 'end')
                if self.fullpath:
                    self.entry.insert(0, self.output)
                else:
                    filename = self.output.split('/')[-1]
                    self.entry.insert(0, filename)
                # self.entry.insert(0, self.output)
                self.entry.config(state='readonly')
                self.entry.update_idletasks()
                self.entry.xview_moveto(1)

        elif self.quantity == 'directory':
            self.output = fd.askdirectory(title=self.title)
            if self.output:
                self.entry.config(state='normal')
                self.entry.delete(0, 'end')
                self.entry.insert(0, self.output)
                self.entry.config(state='readonly')
                self.entry.update_idletasks()
                self.entry.xview_moveto(1)

    @property
    def get(self):
        return self.output


class ScrollableTab(tk.Frame):

    def __init__(self, notebook, title, *args, cheight=False, cwidth=False, **kwargs):

        self.notebook = notebook

        parent_name = self.notebook.winfo_parent()
        parent = self.notebook._nametowidget(parent_name)

        self.frame = tk.Frame(parent)
        self.frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.frame, text=title)

        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        if cwidth: self.canvas.config(width=cwidth)
        if cheight: self.canvas.config(height=cheight)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.scrollbar.grid(row=0, column=1, sticky='NSE')

        tk.Frame.__init__(self, *args, master=self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self, anchor='nw', tags='inner')
        self.grid_columnconfigure(0, weight=1)
        if cwidth: self.grid_columnconfigure(0, minsize=cwidth)

    def scroll(self, canvas, frame):

        def EnterCanvas(event):
            canvas.bind_all('<MouseWheel>', ScrollCanvas)

        def LeaveCanvas(event):
            canvas.unbind_all('<MouseWheel>')

        def ScrollCanvas(event):
            canvas.yview_scroll(int(-1*(event.delta/2)), 'units')

        frame.bind('<Enter>', EnterCanvas)
        frame.bind('<Leave>', LeaveCanvas)

    def update(self):
        self.update_idletasks()
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.config(yscrollincrement=1)
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        self.scroll(self.canvas, self.frame)


#####################################################################################################
#################                           GUI FUNCTIONS                           #################
#####################################################################################################

# def UpdateDimensions(application):

#     parent = application.winfo_parent()
#     master = application._nametowidget(parent)

#     master.update()

#     if application:
#         padding_x = master.winfo_width() - application.winfo_width()
#         padding_y = master.winfo_height() - application.winfo_height()

#     frames = master.winfo_children()

#     frame_heights = []
#     for frame in frames:
#         if frame.winfo_ismapped():
#             frame_heights.append(frame.winfo_height())
#     PROGRAM_HEIGHT = sum(frame_heights) + padding_y if application else sum(frame_heights)

#     frame_widths = []
#     for frame in frames:
#         if frame.winfo_ismapped():
#             frame_widths.append(frame.winfo_width())
#     PROGRAM_WIDTH = max(frame_widths) + padding_x if application else max(frame_widths)

#     X_POSITION = ( master.winfo_screenwidth() - PROGRAM_WIDTH )/2
#     Y_POSITION = ( master.winfo_screenheight() - PROGRAM_HEIGHT )/2

#     master.geometry(str(PROGRAM_WIDTH) + "x" + str(PROGRAM_HEIGHT))
#     master.geometry(str(PROGRAM_WIDTH) + "x" + str(PROGRAM_HEIGHT) + "+" \
#                   + str(int(X_POSITION)) + "+" + str(int(Y_POSITION)))


def ResourcePath(relative_path):
    import sys, os
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('__main__')))
    return os.path.join(base_path, relative_path)


def RenderImage(filepath, downscale=None):
    from PIL import Image, ImageTk
    # First load in order to get dimensions of the image
    loaded = Image.open(ResourcePath(filepath))
    render = ImageTk.PhotoImage(loaded)
    width = render.width()
    height = render.height()
    # Second load in order to resize the original image
    # This was done because only ImageTk has width and height methods
    if downscale and ( type(downscale) == int or type(downscale) == float ):
        scaled_width =  int( width / downscale )
        scaled_height = int( height / downscale )
        loaded = loaded.resize((scaled_width, scaled_height), Image.ANTIALIAS)
    elif downscale and type(downscale) == tuple and len(downscale) == 2:
        width_scale = downscale[0]
        height_scale = downscale[1]
        print(width_scale, height_scale)
        scaled_width = int( width / width_scale )
        scaled_height = int( height / height_scale )
        loaded = loaded.resize((scaled_width, scaled_height), Image.ANTIALIAS)
    else:
        pass
    render = ImageTk.PhotoImage(loaded)
    return render


#####################################################################################################
#####################################################################################################
##############################  ______ _       _     _              _  ##############################
##############################  |  ___(_)     (_)   | |            | | ##############################
##############################  | |_   _ _ __  _ ___| |__   ___  __| | ##############################
##############################  |  _| | | '_ \| / __| '_ \ / _ \/ _` | ##############################
##############################  | |   | | | | | \__ \ | | |  __/ (_| | ##############################
##############################  \_|   |_|_| |_|_|___/_| |_|\___|\__,_| ##############################
##############################                                         ##############################
#####################################################################################################
#####################################################################################################