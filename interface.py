from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askopenfilenames 
import main as mn

class Interface():
    def __init__(self, root):
        self.root = root
        root.title("Locus Extraction Tool")

        self.master = Frame(root)
        self.master.grid(row=0, column=0, padx=10, pady=5)

        #--------------------------------------Needle Input--------------------------------------------
        needle_frame = Frame(self.master, borderwidth=5, relief="groove", padx=5, pady=5)
        needle_browse_frame = Frame(needle_frame)

        self.needle_label = Label(needle_frame, text="Enter Target Genes (needles)", font="Times 10 bold")

        self.needle_v = IntVar()
        self.needle_v.set(0)

        self.needle_file_radio = Radiobutton(needle_frame, text="Choose a file", variable=self.needle_v, value=0, command=self.set_needle_input)
        self.needle_direct_radio = Radiobutton(needle_frame, text="Direct locus input", variable=self.needle_v, value=1, command=self.set_needle_input)

        self.needle_path = ""
        self.needle_browse_button = Button(needle_browse_frame, text="Browse", command=self.needle_file_path)

        self.needle_direct = StringVar()
        self.needle_file_label = Label(needle_browse_frame, text="")   #Limit to 18 chars (a three dot ellipsis at the end (...))
        self.needle_direct_input = Entry(needle_frame, textvariable=self.needle_direct)

        needle_frame.grid(row=0, column=0, sticky=E+W, columnspan=3)
        self.needle_label.grid(row=0, column=0, sticky=W, columnspan=2)
        self.needle_file_radio.grid(row=1, column=0, sticky=W)
        self.needle_direct_radio.grid(row=1, column=1, sticky=W)
        self.needle_direct_input.grid(row=2, column=1)
        self.needle_direct_input.grid_remove()

        needle_browse_frame.grid(row=2, column=0, columnspan=2, sticky=E+W)
        self.needle_browse_button.grid(row=0, column=0, sticky=W)
        self.needle_file_label.grid(row=0, column=1, sticky=W)
        #------------------------------------------------------------------------------------------------

        #---------------------------------------------Haystack Input-------------------------------------
        self.haystack_frame = Frame(self.master, borderwidth=5, relief="groove", padx=5, pady=5)
        self.haystack_radio_frame = Frame(self.haystack_frame)
        self.haystack_browse_frame = Frame(self.haystack_frame)
        self.x_button_frame = Frame(self.haystack_browse_frame)

        self.haystack_v = IntVar()
        self.haystack_v.set(0)
        self.haystack_single_radio = Radiobutton(self.haystack_radio_frame, text="Single file", variable=self.haystack_v, value=0, command=self.haystack_disp_single)
        self.haystack_multi_radio = Radiobutton(self.haystack_radio_frame, text="Multiple files", variable=self.haystack_v, value=1, command=self.haystack_disp_multi)

        self.haystack_label = Label(self.haystack_frame, text="Enter Genes to be Searched (haystack)", font="Times 10 bold")
        self.haystack_browse_button = Button(self.haystack_browse_frame, text="Browse", command=self.haystack_file_path)
        self.haystack_file_label = Label(self.haystack_browse_frame, text="")  #Limit to 15 chars (a three dot ellipsis at the end (...))


        self.haystack_frame.grid(row=1, column=0, columnspan=3, sticky=E+W)
        self.haystack_label.grid(row=0, column=0, sticky=W)

        self.haystack_radio_frame.grid(row=1, column=0, sticky=E+W)
        self.haystack_single_radio.grid(row=0, column=0)
        self.haystack_multi_radio.grid(row=0, column=1)

        self.haystack_browse_frame.grid(row=2, sticky=E+W)
        self.haystack_browse_button.grid(row=1, column=0, sticky=W)
        self.haystack_file_label.grid(row=1, column=1, sticky=W)
        self.x_button_frame.grid(row=1, column=2, sticky=W)
        #------------------------------------------------------------------------------------------------

        #---------------------------------------------Settings-------------------------------------------
        self.settings_frame = Frame(self.master, bd=5, relief="groove", padx=5, pady=5)

        self.settings_label = Label(self.settings_frame, text="Tool Settings", font="Times 10 bold")
        
        self.margin_label = Label(self.settings_frame, text="Margin")
        self.margin_v = IntVar()
        self.margin = Entry(self.settings_frame, textvariable=self.margin_v, width=5)
        self.margin_v.set(50)
        
        self.max_matches_label = Label(self.settings_frame, text="Max Matches")
        self.max_v = IntVar()
        self.max_matches = Entry(self.settings_frame, textvariable=self.max_v, width=5)
        self.max_v.set(10)
        
        self.sig_v = IntVar()
        self.sig_v.set(0)

        self.significant_label = Label(self.settings_frame, text="Filter significant")
        self.significant_true = Radiobutton(self.settings_frame, text="True", variable=self.sig_v, value=1)
        self.significant_false = Radiobutton(self.settings_frame, text="False", variable=self.sig_v, value=0)

        self.settings_frame.grid(row=2, column=0, columnspan=3, sticky=E+W)
        self.settings_label.grid(row=0, column=0, sticky=W)
        self.margin_label.grid(row=1, column=0, sticky=W)
        self.margin.grid(row=1, column=1, sticky=W)
        self.max_matches_label.grid(row=2, column=0, sticky=W)
        self.max_matches.grid(row=2, column=1, sticky=W)
        self.significant_label.grid(row=3, column=0, sticky=W)
        self.significant_true.grid(row=3, column=1, sticky=W)
        self.significant_false.grid(row=3, column=2, sticky=W)
        #------------------------------------------------------------------------------------------------

        #----------------------------------------------Submit--------------------------------------------
        self.submit = Button(self.master, text="Submit", command=lambda: mn.main(self.__get_proper_haystack_list(), self.needle_path, self.needle_direct.get(),
                                                                            self.needle_v.get(), self.sig_v.get(),
                                                                            self.max_v.get(), self.margin_v.get()))
        self.submit.grid(row=3, column=1)
        #------------------------------------------------------------------------------------------------

        #---------------------------------------------Instance Variables---------------------------------
        self.needle_filename = ""
        self.haystack_path = [""]
        self.haystack_filename_disp = [""]
        self.haystack_path_multi = []
        self.haystack_filename_multi_disp = []

        self.x_labels = []
        self.x_label_row = 0
        #------------------------------------------------------------------------------------------------


    def set_needle_input(self):
        value = self.needle_v.get()

        if value == 0:
            self.needle_direct_input.grid_remove()
            self.needle_browse_button.grid()
            self.needle_file_label.grid()
        else:
            self.needle_browse_button.grid_remove()
            self.needle_file_label.grid_remove()
            self.needle_direct_input.grid()


    def get_filename(self, path):
        last_slash = path.rfind("/") + 1
        path_len = len(path)
        return path[last_slash : path_len]        


    def needle_file_path(self):
        temp_path = askopenfilename()
        if temp_path != "":
            self.needle_path = temp_path
        filename = self.get_filename(self.needle_path)
        filename = self.truncate_filename(filename)
        self.needle_file_label["text"] = filename


    def haystack_file_path(self):
        file_option = self.haystack_v.get()

        if file_option == 0:
            temp_path = askopenfilename()
        else:
            temp_path = askopenfilenames()


        if len(temp_path) != 0:
            filename = self.__handle_list(self.get_filename, temp_path)
            
            if file_option == 0:
                self.haystack_path[0] = temp_path
                self.haystack_filename_disp[0] = filename
                self.haystack_disp_single()
            else:
                filename, temp_path = self.__check_for_file(filename, temp_path)
                if filename:
                    self.haystack_path_multi.extend(temp_path)
                    self.haystack_filename_multi_disp.extend(filename)
                    self.haystack_disp_multi()
                    self.create_remove_labels(filename)


    def haystack_disp_single(self):
        self.haystack_file_label["text"] = self.haystack_filename_disp[0]
        for x_lbl in self.x_labels:
            x_lbl.grid_remove()


    def haystack_disp_multi(self):
        disp_filenames = self.__handle_list(self.truncate_filename, self.haystack_filename_multi_disp)
        self.haystack_file_label["text"] = "\n".join(disp_filenames)
        for x_lbl in self.x_labels:
            x_lbl.grid()


    def create_remove_labels(self, filenames):
        for filename in filenames:
            filename = filename.replace(".", ",") #Replace period with comma to adhere to widget naming (extra periods in a widget name will cause tkinter to crash)
            filename = filename.lower() #Only for ensuring that the first letter is lowercase. TKinter crashes if it's uppercase

            label = Label(self.x_button_frame, text="x", name=filename, cursor="hand1", bg="red", fg="white", font=("", 6), borderwidth=1, relief="solid")
            label.grid(row=self.x_label_row, column=2, pady=1, sticky=E)
            label.bind("<Button-1>", self.remove_file)
            self.x_labels.append(label)

            self.x_label_row += 1


    def remove_file(self, e):
        widget_name = str(e.widget).split(".")[-1]
        file_name = widget_name.replace(",", ".")
        file_index = self.insens_list_index(self.haystack_filename_multi_disp, file_name)

        self.x_labels[file_index].destroy()
        del self.haystack_filename_multi_disp[file_index]
        del self.x_labels[file_index]
        del self.haystack_path_multi[file_index]

        self.shift_rows(file_index)
        self.haystack_disp_multi()
        self.x_label_row -= 1


    def insens_list_index(self, haystack, needle):
        for item in haystack:
            if item.lower() == needle.lower():
                return haystack.index(item)


    #NOTE: assumes that this is called after X label has been destroyed
    def shift_rows(self, del_index):
        for i in range(del_index, len(self.x_labels)):
            self.x_labels[i].grid(row=i, column=2, sticky=E)


    def truncate_filename(self, filename):
        if len(filename) > 28:
            dot_index = filename.rfind(".")
            filename = filename[:dot_index - 3] + "..."

            if len(filename) > 28:
                filename = filename[:27] + "..."

        return filename    


    def __handle_list(self, func, arg):
        if isinstance(arg, list) or isinstance(arg, tuple):
            return_val = []            
            for item in arg:
                return_val.append(func(item))
        else:
            return_val = func(arg)

        return return_val


    def __check_for_file(self, filenames, paths):
        cleaned_paths = list(paths)
        cleaned_filenames = filenames.copy()
        
        for i in range(len(filenames)):
            if filenames[i] in self.haystack_filename_multi_disp:
                index = cleaned_filenames.index(filenames[i])
                del cleaned_filenames[index]
                del cleaned_paths[index]

        return cleaned_filenames, cleaned_paths


    def __get_proper_haystack_list(self):
        if self.haystack_v.get() == 0:
            return self.haystack_path
        else:
            return self.haystack_path_multi

    
root = Tk()
root.resizable(width=False, height=False)
my_gui = Interface(root)
root.mainloop()