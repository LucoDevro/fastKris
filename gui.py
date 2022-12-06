#!/usr/bin/env python
from tkinter import *
import customtkinter
from tkinter.font import BOLD
from tkinter import simpledialog
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import re
import webbrowser
import json
from PIL import Image
import easygui
import ScriptBuilder
import easygui as e
import csv
import numpy as np
import xlsxwriter

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark" (standard), "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

"""class App is an extension of a toplevel CTk widget with an associated folder in the file system"""
class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 530

    def __init__(self):
        super().__init__()

        self.title("Protocol designer")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # ask for directory in which all temporary files (folder input) and result files will be written
        self.UserPath = fd.askdirectory()

        # create the necessary inputs folder in case it does not exist:
        parent_dir = os.path.join(self.UserPath, "inputs")
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)
        # keep the path to the inputs folder
        self.inputsPath = parent_dir

        self.resizable(False, False)

    def on_closing(self, event=0):
        self.destroy()


"""
An object of class ControlFrame handles all general protocol information (metadata, pipets) and has an interactive 
visualization of the slots connected to InputFrames.
"""
class ControlFrame(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # grid ControlFrame object
        self.grid(row=0, column=1, sticky="nsew")

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky="nsew")

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # ============ frame_left ============
        # configure grid layout (2x20)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(10, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(15, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(20, minsize=10)  # empty row with minsize as spacing

        # Title: Protocol metadata
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Protocol metadata",
                                              font=("Roboto Medium", -20))  # font name and size in px
        self.label_1.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Name protocol fill-in
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Name protocol:")
        self.label_2.grid(row=2, column=0, pady=5, padx=0)

        self.name = customtkinter.CTkEntry(master=self.frame_left)
        self.name.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        # Author fill-in
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Author:")
        self.label_3.grid(row=3, column=0, pady=5, padx=0)

        self.author = customtkinter.CTkEntry(master=self.frame_left)
        self.author.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Description fill-in
        self.label_6 = customtkinter.CTkLabel(master=self.frame_left, text="Description:")
        self.label_6.grid(row=4, column=0, pady=1, padx=0, sticky="ew")

        self.description = customtkinter.CTkTextbox(master=self.frame_left, width=400, height=150, border_width=2)
        self.description.grid(row=5, column=0, columnspan=2, pady=0, padx=10, sticky="ns")

        # Title: Pipets
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Pipets",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=11, column=0, columnspan=2, pady=10, padx=10)

        # initialize the hasTwoPipets attribute. True indicates that two input rows are present in the "Pipets" section
        self.hasTwoPipets = False

        # create frame for pipets
        self.selected_side_pipet = customtkinter.StringVar()
        self.frame_pipet = customtkinter.CTkFrame(master=self.frame_left)
        self.frame_pipet.grid(row=12, column=0, columnspan=2, padx=10, sticky="nsew")

        # First pipet fill-in
        self.AddPipetLabel = customtkinter.CTkLabel(master=self.frame_pipet, text="Add pipet(s): ", width=30)
        self.AddPipetLabel.grid(row=0, column=0, padx=10, sticky="nsew")
        self.AddPipet = customtkinter.CTkEntry(master=self.frame_pipet)
        self.AddPipet.grid(row=0, column=1, sticky="nsew")
        self.optionmenu_pip = customtkinter.CTkOptionMenu(master=self.frame_pipet,
                                                          values=["left", "right"],
                                                          variable=self.selected_side_pipet,
                                                          width=80)
        self.optionmenu_pip.grid(row=0, column=2, padx=10, sticky="nsew")

        # Button: add second pipet
        self.AddPipetButton = customtkinter.CTkButton(master=self.frame_pipet, text="Add... ",
                                                      command=self.addPipet, width=54)
        self.AddPipetButton.grid(row=0, column=4)
        self.AddPipetButton.grid_propagate(False)

        ##autofill all information about the pipets that is already available in the inputs folder
        # path to pipet information
        pipetsFileName = os.path.join(self.parent.inputsPath, "pipets.txt")
        if os.path.exists(pipetsFileName):
            with open(pipetsFileName, "r") as f:
                lines = f.readlines()
                # label and position of the first pipet (at least one defined)
                self.AddPipet.insert(END, lines[0].replace("\n", ""))
                self.optionmenu_pip.set(lines[1].replace("\n", ""))
                # read and fill in the information of a second pipet if available
                if len(lines) == 4:
                    self.addPipet(lines[2].replace("\n", ""), lines[3].replace("\n", ""))

        # Apply button: write pipet information to file in inputsfolder
        self.ApplyButton = customtkinter.CTkButton(master=self.frame_pipet, text="Apply", command=self.pipetApply,
                                                   width=100)
        self.ApplyButton.grid(row=5, column=0, padx=5, pady=20, sticky="ew")

        # Dark mode switch
        switch_var = customtkinter.StringVar(value="on")

        self.switch_darkmode = customtkinter.CTkSwitch(master=self.frame_left, text="Dark mode",
                                                       command=self.change_appearance_mode, variable=switch_var,
                                                       onvalue="on", offvalue="off")
        self.switch_darkmode.grid(row=20, column=0, columnspan=2, pady=10, padx=20, sticky="")
        self.switch_darkmode.select()

        # ============ frame_right ============

        # configure grid layout (7x3)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1, 2), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_panels = customtkinter.CTkFrame(master=self.frame_right, fg_color="transparent", bg_color="transparent")
        self.frame_panels.grid(row=1, column=0, columnspan=3, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_panels ============

        imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.waste = customtkinter.CTkImage(light_image=Image.open(os.path.join(imagepath, "wastebin_light.png")),
                                            size=(40, 40),dark_image=Image.open(os.path.join(imagepath, "wastebin_dark.png")))
        # configure grid layout (3x4)
        self.frame_panels.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_panels.columnconfigure((0, 1, 2), weight=1)

        self.button1 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="1",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 1))
        self.button2 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="2",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 2))
        self.button3 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="3",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 3))
        self.button4 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="4",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 4))
        self.button5 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="5",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 5))
        self.button6 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="6",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 6))
        self.button7 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="7",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 7))
        self.button8 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="8",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 8))
        self.button9 = customtkinter.CTkButton(master=self.frame_panels,
                                               height=148,
                                               width=175,
                                               text="9",
                                               text_color=("black", "grey80"),
                                               font=("Verdana", -40),
                                               fg_color="transparent",
                                               bg_color="transparent",
                                               border_width=2,
                                               border_color=("black", "grey80"),
                                               corner_radius=10,
                                               command=lambda *args: createInputFrame(self, 9))
        self.button10 = customtkinter.CTkButton(master=self.frame_panels,
                                                height=148,
                                                width=175,
                                                text="10",
                                                text_color=("black", "grey80"),
                                                font=("Verdana", -40),
                                                fg_color="transparent",
                                                bg_color="transparent",
                                                border_width=2,
                                                border_color=("black", "grey80"),
                                                corner_radius=10,
                                                command=lambda *args: createInputFrame(self, 10))
        self.button11 = customtkinter.CTkButton(master=self.frame_panels,
                                                height=148,
                                                width=175,
                                                text="11",
                                                text_color=("black", "grey80"),
                                                font=("Verdana", -40),
                                                fg_color="transparent",
                                                bg_color="transparent",
                                                border_width=2,
                                                border_color=("black", "grey80"),
                                                corner_radius=10,
                                                command=lambda *args: createInputFrame(self, 11))
        self.button12 = customtkinter.CTkButton(master=self.frame_panels,
                                                height=148,
                                                width=175,
                                                text='',
                                                image=self.waste,
                                                font=("Verdana", -30),
                                                fg_color="transparent",
                                                bg_color="transparent",
                                                border_width=2,
                                                border_color=("black", "grey80"),
                                                corner_radius=10,
                                                command=lambda *args: createInputFrame(self, 12),
                                                state="disabled")

        self.button1.grid(row=3, column=0, pady=2, padx=2, sticky="nesw")
        self.button2.grid(row=3, column=1, pady=2, padx=2, sticky="nesw")
        self.button3.grid(row=3, column=2, pady=2, padx=2, sticky="nesw")
        self.button4.grid(row=2, column=0, pady=2, padx=2, sticky="nesw")
        self.button5.grid(row=2, column=1, pady=2, padx=2, sticky="nesw")
        self.button6.grid(row=2, column=2, pady=2, padx=2, sticky="nesw")
        self.button7.grid(row=1, column=0, pady=2, padx=2, sticky="nesw")
        self.button8.grid(row=1, column=1, pady=2, padx=2, sticky="nesw")
        self.button9.grid(row=1, column=2, pady=2, padx=2, sticky="nesw")
        self.button10.grid(row=0, column=0, pady=2, padx=2, sticky="nesw")
        self.button11.grid(row=0, column=1, pady=2, padx=2, sticky="nesw")
        self.button12.grid(row=0, column=2, pady=2, padx=2, sticky="nesw")

        # create an InputFrame for the slot selected
        def createInputFrame(self, index):
            if isinstance(self.frame_right, InputFrame):
                self.frame_right.destroy()  # else if multiple buttons pressed, all frames will stack
            self.frame_right = InputFrame(parent, index)
            self.frame_right.tkraise()

        # action buttons
        self.button13 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Load from parameter file",
                                                border_width=2,  # <- custom border_width
                                                fg_color="transparent",  # <- no fg_color
                                                command=self.load_from_parameterfile)
        self.button13.grid(row=8, column=1, columnspan=1, pady=10, padx=5, sticky="e")

        self.button14 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Generate Protocol",
                                                border_width=2,  # <- custom border_width
                                                fg_color="transparent",  # <- no fg_color
                                                command=self.generate_protocol)
        self.button14.grid(row=8, column=2, columnspan=1, pady=10, padx=5, sticky="")

    """
    The addPipet method inserts a second row in the "Pipets" section where information of a second pipet can be specified. 
    It removes the AddPipetButton in the first row and creates a RemovePipetButton in the second row to enforce that 
    always at least one and at most two pipets are specified.
    """

    def addPipet(self, label="", place="left"):
        # create second row
        self.AddPipet2 = customtkinter.CTkEntry(master=self.frame_pipet)
        self.AddPipet2.insert(END, label)
        self.AddPipet2.grid(row=2, column=1, sticky="nsew")

        self.optionmenu_pip2 = customtkinter.CTkOptionMenu(master=self.frame_pipet,
                                                           values=["left", "right"], width=80)
        self.optionmenu_pip2.set(place)
        self.optionmenu_pip2.grid(row=2, column=2, padx=10, sticky="nsew")
        # create the RemovePipetButton
        self.RemovePipetButton = customtkinter.CTkButton(master=self.frame_pipet,
                                                         text="remove", width=54, command=self.removePipet)
        self.RemovePipetButton.grid(row=2, column=4)
        self.RemovePipetButton.grid_propagate(False)
        # remove the AddPipetButton
        self.AddPipetButton.grid_remove()
        self.hasTwoPipets = True

    # The removePipet method removes the input row for the second pipet in the "Pipets" section
    def removePipet(self):
        Lst = self.frame_pipet.grid_slaves(row=2)
        for l in Lst:
            l.destroy()
        self.AddPipetButton.grid()
        self.hasTwoPipets = False

    """
    The pipetApply method writes all currently specified information in the "Pipets" section to a 'pipets.txt' file 
    in the inputs folder. If such a file is already present, its content will be overwritten.
    """

    def pipetApply(self):
        # ensure the existence of the inputs folder
        isExist = os.path.exists(self.parent.inputsPath)
        if not isExist:
            os.makedirs(self.parent.inputsPath)
        # ensure label of first pipet not empty
        if self.AddPipet.get() != "":
            instruments = self.AddPipet.get() + "\n" + self.optionmenu_pip.get() + "\n"
            with open(os.path.join(self.parent.inputsPath, "pipets.txt"), "w") as f:
                f.write(instruments)
        else:
            e.msgbox("First pipet not specified", "Error")
            return None
        # same if second input row present in "Pipets" section
        if self.hasTwoPipets == True:
            if self.AddPipet2.get() != "":
                with open(os.path.join(self.parent.inputsPath, "pipets.txt"), "a") as f:
                    f.write(self.AddPipet2.get() + "\n" + self.optionmenu_pip2.get() + "\n")
            else:
                e.msgbox("Second pipet not specified", "Error")
                return None

    # swith Dark/Light mode
    def change_appearance_mode(self):
        switch = self.switch_darkmode.get()
        if switch == "on":
            self.configure(customtkinter.set_appearance_mode("Dark"))
        else:
            self.configure(customtkinter.set_appearance_mode("Light"))

    """
    The generate_protocol method reads all information of slots and pipets in the inputsFolder, creates a parameter file
    (params.txt) in the predefined format, a protocol file (.txt) through ScriptBuilder and in case of a 1D or 2D screen, 
    an excel file (.xlsx file) with for every well plate and compound, the concentrations in each well
    """
    def generate_protocol(self):
        # ensure existence of the inputs folder
        isExist = os.path.exists(self.parent.inputsPath)
        if not isExist:
            os.makedirs(self.parent.inputsPath)
            return None

        # initialize lists for information of unknown compounds (i.e. not in compLibrary.txt)
        names_conc_to_add = []
        conc_to_add = []
        labels_to_add = []

        # ask user for protocol (and parameter) filename
        protocolFilename = simpledialog.askstring("Protocol filename", "filename for new protocol\t\t\t")
        # if not cancelled
        if protocolFilename:
            protocolFilename += ".py"

            # read in compound library:
            with open(os.path.join(os.path.dirname(__file__),'compLibrary.txt'), 'r') as l:
                reader = csv.reader(l, delimiter="\t")
                lines = [entry for line in reader for entry in line]

            labels = str(lines[0::3])[1:-1]
            types = str(lines[1::3])[1:-1]

            # read in all user-specified information stored in the inputs folder
            directory = os.path.join(self.parent.inputsPath)
            tips = ""
            tuberacks = ""
            instruments = ""
            plates = ""
            screens = ""
            # ensure at least one slot has information stored
            atLeastOneInput = 0

            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # check if it is a file
                if os.path.isfile(f):
                    with open(f, "r") as f:
                        # In all slot files, first line is Type of container
                        Type = f.readline().replace("\n", "")
                        if Type == "Tube rack":
                            atLeastOneInput += 1
                            # read in dictionary
                            dictTur = json.loads(f.read())
                            for key in dictTur:
                                # ensure all necessary input specified, else: error message to user
                                if dictTur.get(key) != "":
                                    tuberacks += dictTur.get(key) + "\n"
                                else:
                                    e.msgbox("Empty string value for name plate: " + filename, "Error")
                                    return None

                        elif Type == "Tip rack":
                            atLeastOneInput += 1
                            # read in dictionary
                            dictTir = json.loads(f.read())
                            for key in dictTir.keys():
                                # ensure all necessary input specified, else: error message to user
                                if dictTir.get(key) != "":
                                    tips += dictTir.get(key) + "\n"
                                else:
                                    e.msgbox("Empty string value for name plate: " + filename, "Error")
                                    return None

                        elif Type == "Well plate":
                            atLeastOneInput += 1
                            # read in dictionary
                            dict = json.loads(f.readline())
                            plates += dict["label"] + "\n" + str(dict["index"]) + "\n"
                            # ensure label specified, else: error message to user
                            if dict["label"] == "":
                                e.msgbox("Empty string value for name plate: " + filename, "Error")
                                return None

                            screens += str(dict["dimension"]) + "\n"
                            # if every compound has a label and concentration, proceed. Else: error message to user
                            if "" not in dict["names_conc"].split(","):
                                screens += dict["names_conc"] + "\n"
                            else:
                                e.msgbox(
                                    "Empty string value for name or concentration of one of the compounds: " + filename,
                                    "Error")
                                return None
                            # if every compound has a position, proceed. Else: error message to user
                            if "" not in dict["positions"].split(","):
                                screens += dict["positions"] + "\n"
                            else:
                                e.msgbox("Empty string value for position of one of the compounds: " + filename,
                                         "Error")
                                return None
                            # if every compound has a completely specified range, proceed. Else: error message to user
                            if all(not (string.endswith("-") or string.startswith("-")) for string in
                                   dict["ranges"].split(",")):
                                screens += dict["ranges"] + "\n"
                            else:
                                e.msgbox("Empty string value for ranges of one of the compounds: " + filename, "Error")
                                return None

                            screens += str(dict["index"]) + "\n"
                            # if well plate has a WorkingVolume, proceed. Else: error message to user
                            if "" != dict["WorkingVolume"]:
                                screens += str(dict["WorkingVolume"]) + "\n"
                            else:
                                e.msgbox("Empty string value for the working volume in: " + filename,
                                         "Error")
                                return None

                            # check if all compounds are already present in the library.
                            names_conc = dict["names_conc"].split(",")[:-1]
                            types_compounds = dict["types_compounds"].split(",")
                            # get stock concentration of each compound. names_conc elements are of
                            # the form: "label (concentration unit)"
                            concs = []
                            for i in names_conc:
                                # get concentration, if regex matching fails: error message to the user
                                try:
                                    concs.append(re.search(r"([0-9]+)", i.split(" (")[1]).group(1))
                                except AttributeError:
                                    e.msgbox(
                                        "Unrecognized or empty value for one of the concentrations in: " + filename,
                                        "Error")
                                    return None

                            # tuples (label,type) for each compound in compLibrary
                            zipLabelType = list(map(lambda x, y: (x.replace("\'", ""), y.replace("\'", "")),
                                                    labels.split(", "), types.split(", ")))
                            # tuples (label,type) for each compound in input
                            zipInput = list(map(lambda x, y: (x, y), names_conc, types_compounds))

                            # if any (label,type) in input not in compLibrary:
                            if any(x not in zipLabelType for x in zipInput):
                                # iterate over input
                                for idx in range(len(zipInput)):
                                    # if compound not in compLibrary yet
                                    if (zipInput[idx] not in zipLabelType):
                                        # if same label with different type already in compLibrary: error message to user.
                                        # Else: add information to lists
                                        if zipInput[idx][0] in list(
                                                map(lambda x: x.replace("\'", ""), labels.split(", "))):
                                            e.msgbox(filename + "\n" + str(zipInput[idx][
                                                                               0]) + ": A compound with the same label, but different type is already present in the library."
                                                     , "Error")
                                            return None
                                        names_conc_to_add.append(names_conc[idx])
                                        labels_to_add.append(types_compounds[idx])
                                        conc_to_add.append(concs[idx])

                            # if screen 1D or 2D: create concentrations matrix as Excel file
                            # TODO: also for 3D
                            if str(dict["dimension"]) == 1 or str(dict["dimension"] == 2):
                                try:
                                    # get the number of wells from the well plate's label (assuming that it follows
                                    # the Opentrons naming convention!)
                                    numberOfWells = int(re.search(r'([0-9]+)', dict["label"]).group(1))
                                    ranges = dict["ranges"].split(",")
                                    # create workbook with one worksheet
                                    workbook = xlsxwriter.Workbook(
                                        os.path.join(self.parent.UserPath, protocolFilename.replace(".py", ".xlsx")))
                                    worksheet = workbook.add_worksheet()
                                    headers = ["Name"] + [*range(1, numberOfWells + 1)]
                                    # write column names
                                    for i in range(len(headers)):
                                        worksheet.write(0, i, headers[i])
                                    for i in range(len(names_conc)):
                                        # for compound i, get range boundaries
                                        raw_range = [float(j) for j in ranges[i].split('-')]
                                        # append label compound and concentration gradient
                                        RowToAdd = [names_conc[i]] + list(
                                            map(str, np.linspace(raw_range[0], raw_range[1], numberOfWells).tolist()))
                                        # write label and concentrations
                                        for k in range(len(RowToAdd)):
                                            worksheet.write(i + 1, k, RowToAdd[k])
                                    workbook.close()
                                # catch error due to deviation from Opentrons' well plate naming convention
                                except AttributeError:
                                    continue
                # if no slots have information specified, stop the program from creating an incomplete parameter file
                if atLeastOneInput == 0:
                    e.msgbox("No input files with slot information found. Specify input for at least one slot", "Error")
                    return None

            # if list with information of compounds not yet in compLibrary is non-empty.
            # First, ask permission of user to add to compLibrary
            if len(names_conc_to_add) > 0:
                answer = messagebox.askquestion(
                    message="Are you sure you want to continue and add following compounds to the library?\n" +
                            "\n".join(' '.join(map(str, tup)) for tup in
                                      list(zip(names_conc_to_add, labels_to_add, conc_to_add))))
                # If user allows, write new compounds to compLibrary
                if answer == "yes":
                    with open(os.path.join(os.path.dirname(__file__),'compLibrary.txt'), "a") as f:
                        for idx in range(len(names_conc_to_add)):
                            f.write("\n" + names_conc_to_add[idx] + "\t")
                            f.write(labels_to_add[idx].capitalize() + "\t")
                            f.write(conc_to_add[idx])

            # read stored information for pipets. If none specified: error message to user
            FilenamePipets = os.path.join(self.parent.inputsPath, "pipets.txt")
            if os.path.isfile(FilenamePipets):
                with open(FilenamePipets) as f:
                    instruments += "".join(f.readlines())
            else:
                e.msgbox("no prior information of pipet(s) saved. Specify name and position.", "Error")
                return None

            #if no plates defined for screen: error messsage to user
            if plates == "":
                easygui.msgbox("Add at least one well plate to the screen")
                return None

            #if no tipracks defined for screen: error message to user
            if tips == "":
                easygui.msgbox("Add at least one tip rack to the screen")
                return None

            # write all information to parameter file
            paramFilename = protocolFilename.replace(".py", ".param.txt")
            paramFilePath = os.path.join(self.parent.UserPath, paramFilename)
            with open(paramFilePath, "w+") as f:
                f.write(tips + "\n")
                f.write(tuberacks + "\n")
                f.write(instruments + "\n")
                f.write(plates + "\n")
                f.write(screens)

            # generate the protocol
            ScriptBuilder.BuildWithMetadata(paramFilePath, os.path.join(self.parent.UserPath, protocolFilename),
                                            self.name.get(), self.description.get("0.0","end"), self.author.get())

    """
    The load_from_parameterfile method allows the user to select an existing parameter file. The method then tries to write the 
    contents of this file to temporary files located in the inputs folder.
    """

    def load_from_parameterfile(self):
        # ensure the inputs folder exists
        try:
            isExist = os.path.exists(self.parent.inputsPath)
            if not isExist:
                os.makedirs(self.parent.inputsPath)
            # ask user to select a parameter file
            parampath = askopenfilename()
            # read contents
            with open(parampath, 'r') as f:
                lines = f.read()
                lines = lines.split("\n\n")
            # parse parameter file
            tips_raw = lines[0].split("\n")
            tuberack_raw = lines[1].split("\n")
            instr_raw = lines[2].split("\n")
            plates_raw = lines[3].split("\n")
            screens_raw = lines[4].split('\n')
            if screens_raw[-1] == '':
                screens_raw = screens_raw[:-1]
            else:
                screens_raw = screens_raw

            ## write files for Tip rack assigned slots
            tipsInput = tips_raw[0::3]
            tipsLocation = tips_raw[1::3]
            tipsPipette = tips_raw[2::3]

            for i in range(len(tipsLocation)):
                filename = "Input_plate" + str(tipsLocation[i]) + ".txt"
                filePath = os.path.join(self.parent.inputsPath, filename)
                with open(filePath, "w") as f:
                    f.write("Tip rack" + "\n")
                    dict = {"label": tipsInput[i], "index": str(tipsLocation[i]),
                            "AssignedPipetOption": tipsPipette[i]}
                    f.write(json.dumps(dict))

            ## write files for Tube rack assigned slots
            tuberacksInput = tuberack_raw[0::2]
            tuberacksLocation = tuberack_raw[1::2]

            for i in range(len(tuberacksLocation)):
                filename = "Input_plate" + str(tuberacksLocation[i]) + ".txt"
                filePath = os.path.join(self.parent.inputsPath, filename)
                with open(filePath, "w") as f:
                    f.write("Tube rack" + "\n")
                    dict = {"label": tuberacksInput[i], "index": str(tuberacksLocation[i])}
                    f.write(json.dumps(dict))

            ## write pipets.txt, a file with all pipets information
            instrumentInput = instr_raw[0::2]
            instrumentLocation = instr_raw[1::2]
            filename = "pipets.txt"
            filePath = os.path.join(self.parent.inputsPath, filename)
            with open(filePath, "w") as f:
                for i in range(len(instrumentInput)):
                    f.write(instrumentInput[i] + "\n")
                    f.write(instrumentLocation[i] + "\n")

            # after the new pipets information is loaded, update the information displayed in the "Pipets" section
            self.AddPipet.delete(0, END)
            self.AddPipet.insert(END, instrumentInput[0])
            self.optionmenu_pip.set(instrumentLocation[0])
            if len(instrumentInput) == 2:
                self.addPipet(instrumentInput[1], instrumentLocation[1])

            ## write files for Well plate assigned slots
            platesInput = plates_raw[0::2]
            platesLocation = plates_raw[1::2]
            all_screen_types = screens_raw[0::6]
            all_screen_compounds = screens_raw[1::6]
            all_screen_stocks = screens_raw[2::6]
            all_screen_ranges = screens_raw[3::6]
            all_screen_plates = screens_raw[4::6]
            all_screen_workVol = screens_raw[5::6]
            # read in compLibrary
            with open(os.path.join(os.path.dirname(__file__),'compLibrary.txt'), 'r') as l:
                reader = csv.reader(l, delimiter="\t")
                lines = [entry for line in reader for entry in line]
            labels = lines[0::3]
            types = lines[1::3]

            # check if all compounds are already in compLibrary
            # initialize a list with all labels of the compounds
            label_compounds = []
            # For each screen
            for i in range(len(all_screen_plates)):
                # get compound labels
                list_screen_compounds = all_screen_compounds[i].split(",")
                # initialize a list with all types of the compounds in screen i
                types_i = []
                # For each label, get type from compLibrary. If label not yet in compLibrary: error message to user
                for j in range(len(list_screen_compounds)):
                    comp = list_screen_compounds[j]
                    compIdx = labels.index(comp)
                    if compIdx != None:
                        types_i.append(types[compIdx])
                    else:
                        e.msgbox("Unknown compound " + comp + " in parameter file", "Error")
                        return None
                label_compounds.append(types_i)

            # write files for Well plate assigned slots
            for i in range(len(platesLocation)):
                filename = "Input_plate" + str(platesLocation[i]) + ".txt"
                filePath = os.path.join(self.parent.inputsPath, filename)

                with open(filePath, "w") as f:
                    f.write("Well plate" + "\n")
                    dict = {"label": platesInput[i], "index": platesLocation[i], "dimension": str(all_screen_types[i]),
                            "names_conc": all_screen_compounds[i], "positions": all_screen_stocks[i],
                            "ranges": all_screen_ranges[i],
                            "WorkingVolume": all_screen_workVol[i], "Tuberack": all_screen_stocks[i][0],
                            "types_compounds": ",".join(label_compounds[i][:-1])}
                    f.write(json.dumps(dict))
        # If anything goes wrong during the reading of the parameter file or writing of the temporary files,
        # display the error message to the user.
        except Exception as err:
            e.msgbox(
                "Something went wrong during loading of the parameter file. Make sure the file follows the correct format exactly, including newline characters.\n" + str(
                    err), "Error")
            return None


"""
A frame of class InputFrame appears on top of the right side of the app when the user clicks on a slot.
All information for that slot can be added/removed/modified in this frame.
"""
class InputFrame(customtkinter.CTkFrame):
    def __init__(self, parent, index):
        super().__init__(parent)
        self.index = index
        self.parent = parent
        # grid ControlFrame object
        self.grid(row=0, column=0, sticky="nes")

        # ============ create frame up ============
        self.frame_up = customtkinter.CTkFrame(master=self, width=650, height=472)
        self.frame_up.columnconfigure((0, 1), weight=1)
        self.frame_up.grid(row=0, column=0, sticky="nsew")
        self.frame_up.grid_propagate(False)

        # Title: slot + index
        customtkinter.CTkLabel(master=self.frame_up, text="slot " + str(self.index), font=('Segoe UI', 15, BOLD)) \
            .grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(1, 10))

        # name container fill-in
        customtkinter.CTkLabel(master=self.frame_up, text="name container: ").grid(row=1, column=0, sticky="W")
        self.PlateLabel = customtkinter.CTkEntry(master=self.frame_up)
        self.PlateLabel.grid(row=1, column=1, sticky="nsew")
        # type container selection
        self.valuesPlateOptionMenu = ["Choose...", "Tube rack", "Tip rack", "Well plate"]
        self.plateOptionVar = customtkinter.StringVar()
        customtkinter.CTkLabel(master=self.frame_up, text="add to slot:").grid(row=2, column=0, sticky="W")
        self.PlateOptionMenu = customtkinter.CTkOptionMenu(master=self.frame_up, variable=self.plateOptionVar,
                                                           values=self.valuesPlateOptionMenu,
                                                           command=self.CompoundsFrameEvent)
        self.PlateOptionMenu.grid(row=2, column=1, sticky="nsew")

        # autofill label and type of container for selected slot
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)
        # if file already exists
        if os.path.exists(completeFilename):
            with open(completeFilename, "r") as f:
                Platetype = f.readline()
                # autofill label
                if any(t in Platetype for t in ["Tip rack", "Tube rack", "Well plate"]):
                    self.PlateLabel.insert(END, json.loads(f.readline())['label'])
                # autofill type
                if "Tube rack" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[1])
                elif "Tip rack" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[2])
                elif "Well plate" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[3])
        else:
            self.PlateOptionMenu.set(self.valuesPlateOptionMenu[0])

        # ============ create frame compounds (middle frame) ============
        self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=680)
        self.frame_compounds.grid(row=3, column=0, columnspan=2, sticky="ns")
        self.frame_compounds.grid_propagate(False)
        self.frame_compounds.rowconfigure(2, minsize=5)  # empty row with minsize as spacing)

        ## initialize attributes
        # first available rowindex in frame_compounds for frame_comp objects generated by method addcompound
        self.irow = 8
        # dictionary to store irow : {frame_comp, unit} pairs
        self.dict_compounds = {}

        # evoke the creation of frame_compounds based on the value of PlateOptionMenu
        self.CompoundsFrameEvent(self.PlateOptionMenu.get())

        # ============ create frame down ============
        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.columnconfigure([0, 1, 2], weight=1)
        self.frame_down.grid(row=2, column=0, sticky="nsew")

        #reset button
        self.buttonReset = customtkinter.CTkButton(master=self.frame_down, text="reset", command=self.reset,
                                                   fg_color="grey")
        self.buttonReset.grid(column=0, row=3, sticky="nsew")

        #cancel button
        self.buttonCancel = customtkinter.CTkButton(master=self.frame_down, text="cancel", command=self.cancel,
                                                    fg_color="grey")
        self.buttonCancel.grid(column=1, row=3, sticky="nsew")

        # apply button
        self.buttonApply = customtkinter.CTkButton(master=self.frame_down, text="apply", command=self.button_event)
        self.buttonApply.grid(column=2, row=3, sticky="nsew")
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    """
    The method CompoundsFrameEvent creates a frame based on the type of container specified for the slot. 
    Here, all information about the contents associated to the container can be specified
    """
    def CompoundsFrameEvent(self, choice):
        #filename for current slot in inputs folder
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)

        if choice == "Tip rack":
            self.frame_compounds.destroy()
            self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=680, fg_color=["#F9F9FA", "#343638"])
            self.frame_compounds.grid(row=3, column=0, columnspan=2, sticky="nw")
            self.frame_compounds.grid_rowconfigure(0, minsize=3)

            #select pipet associated to tips in Tip rack
            self.AssignedPipetLabel = customtkinter.CTkLabel(master=self.frame_compounds,
                                                             text="Assigned to pipet:", anchor="w")
            self.AssignedPipetLabel.grid(row=2, column=0, sticky="nw")
            self.AssignedPipetOption = customtkinter.CTkOptionMenu(master=self.frame_compounds,
                                                                   values=["left", "right"])
            self.AssignedPipetOption.grid(row=2, column=1, sticky="nsew")

            # if information is already stored in the inputs folder for this combination
            # of slot and container type == Tip rack
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Tip rack" in lines[0]:
                        self.AssignedPipetOption.set(json.loads(lines[1])['AssignedPipetOption'])

        elif choice == "Tube rack":
            self.frame_compounds.destroy()

        elif choice == "Well plate":
            self.frame_compounds.destroy()
            self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=680)
            self.frame_compounds.grid(row=3, column=0, columnspan=2, sticky="ns")
            self.frame_compounds.propagate(False)
            self.frame_compounds.grid_rowconfigure(6, minsize=5)  # empty row with minsize as spacing

            #Title Compounds
            self.CompoundsLabel = customtkinter.CTkLabel(master=self.frame_compounds, text="Compounds",
                                                         font=('Segoe UI', 10, BOLD))
            self.CompoundsLabel.grid(row=2, column=0, sticky="nw")
            self.CompoundsLabel.grid_propagate(False)

            # fill-in WorkingVolume
            self.WorkingVolumeLabel = customtkinter.CTkLabel(master=self.frame_compounds,
                                                             text="working volume (µl): ")
            self.WorkingVolumeLabel.grid(row=3, column=0)

            self.WorkingVolume = customtkinter.CTkEntry(master=self.frame_compounds)
            self.WorkingVolume.grid(row=3, column=1)

            # fill-in position of associated Tube rack
            self.TubeRackLabel = customtkinter.CTkLabel(master=self.frame_compounds,
                                                        text="tube rack position: ")
            self.TubeRack = customtkinter.CTkEntry(master=self.frame_compounds)
            self.TubeRackLabel.grid(row=4, column=0)
            self.TubeRack.grid(row=4, column=1)

            # fill-in position in Tube rack of milli-Q (i.e. the diluent)
            self.MQpositionLabel = customtkinter.CTkLabel(master=self.frame_compounds, text="Milli-Q position: ")
            self.MQpositionLabel.grid(row=5, column=0)
            self.MQposition = customtkinter.CTkEntry(master=self.frame_compounds)
            self.MQposition.grid(row=5, column=1)

            #redirect to page in OT-2 API V2 with info on Tube rack position labels
            self.HelpPositions = customtkinter.CTkButton(master=self.frame_compounds, text="?",
                                                         width=0.2, height=0.1, fg_color="grey33",
                                                         command=self.openHelpPositions)
            self.HelpPositions.grid(row=5, column=2, sticky="w", padx=5)

            # if information is already stored in the inputs folder for this combination of
            # slot and container type == Well plate: fill in WorkingVolume, Tube rack & milli-Q position
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Well plate" in lines[0]:
                        dict = json.loads(lines[1])
                        self.WorkingVolume.insert(END, dict["WorkingVolume"])
                        self.TubeRack.insert(END, dict["Tuberack"])
                        compounds = dict["names_conc"].split(",")
                        positions = dict["positions"].split(",")
                        # extract the position of compound 'MQ'. If this info isn't stored, ignore
                        for j in range(len(compounds)):
                            if 'MQ' == compounds[j]:
                                # in case no position previously given by user, suppress AttributeError
                                try:
                                    self.MQposition.insert(END, re.search(r"/(\w+)", positions[j]).group(1))
                                except AttributeError:
                                    pass
            #button Add salt
            self.AddSalt = customtkinter.CTkButton(master=self.frame_compounds, text="Add salt",
                                                   command=lambda *args: self.addcompound("salt"),
                                                   width=215)
            self.AddSalt.grid(row=7, column=0, padx=0, sticky="nw")
            self.AddSalt.grid_propagate(False)
            # button Add buffer
            self.AddBuffer = customtkinter.CTkButton(master=self.frame_compounds, text="Add buffer",
                                                     command=lambda *args: self.addcompound("buffer"),
                                                     width=215)
            self.AddBuffer.grid(row=7, column=1, padx=0, sticky="nw")
            self.AddBuffer.grid_propagate(False)
            # button Add precipitant
            self.AddPrecipitant = customtkinter.CTkButton(master=self.frame_compounds, text="Add precipitant",
                                                          command=lambda *args: self.addcompound("precipitant"),
                                                          width=215)
            self.AddPrecipitant.grid(row=7, column=2, padx=0, sticky="nw")
            self.AddPrecipitant.grid_propagate(False)

            # if information is already stored in the inputs folder for this combination of
            # slot and container type == Well plate: fill in the compounds
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Well plate" in lines[0]:
                        dict = json.loads(lines[1])
                        types_compounds = dict["types_compounds"].split(",")
                        names_conc = dict["names_conc"].split(",")[:-1]
                        # get name of each compound
                        names = [i.split(" (")[0] for i in names_conc]
                        # get unit for each compound
                        units = [re.search(r"[0-9]+([%M])", i.split(" (")[1]).group(1) for i in names_conc]
                        #get concentration for each compound
                        concs = []
                        for i in names_conc:
                            try:
                                concs.append(re.search(r"([0-9]+)", i.split(" (")[1]).group(1))
                            except AttributeError:
                                concs.append("")
                        #get range for each compound
                        ranges = dict["ranges"].split(",")
                        # get position of each compound
                        positions = dict["positions"].split(",")[:-1]
                        shortpositions = [i.split("/")[1] for i in positions]

                        # add frame_comp objects to frame_compounds with all retrieved information on names, units,
                        # ranges and positions of the compounds
                        it = [names, concs, ranges, shortpositions]
                        if all(len(l) == len(types_compounds) for l in it):
                            for i in range(len(types_compounds)):
                                if types_compounds[i] == "Salt" or types_compounds[i] == "Buffer" or types_compounds[
                                    i] == "Precipitant":
                                    self.addcompound(types_compounds[i].lower(), names[i], concs[i],
                                                     ranges[i].split("-")[0],
                                                     ranges[i].split("-")[1], shortpositions[i], units[i])

    """ method openHelpPositions opens a 'help' page from manual OT-2 API v2 on Tube rack position labels"""
    def openHelpPositions(self):
        webbrowser.open_new(r"https://docs.opentrons.com/ot1/containers.html")

    """
    The method reset clears all information from the InputFrame and deletes all info for the selected slot 
    in the temporary files (inputs folder)
    """
    def reset(self):
        Filename = os.path.join(self.parent.inputsPath, "Input_plate" + str(self.index) + ".txt")
        try:
            os.unlink(Filename)
            InputFrame(self.parent, self.index)
            self.destroy()
        #unless no temporary file exists yet for this slot
        except FileNotFoundError:
            InputFrame(self.parent, self.index)
            self.destroy()
            return None
        except OSError as err:
            e.msgbox(repr(err), "Error")
            return None

    def cancel(self):
        self.destroy()

    """
    The method button_event writes all information filled in the InputsFrame to a slot-specific temporary file in the
    inputs folder. If the type of container is not specified (i.e. equal to "Choose..."), no files are changed.
    """
    def button_event(self):
        if self.PlateOptionMenu.get() == "Choose...":
            self.destroy()
            return None
        else:
            #write to slot input file. First line is the type of container. The second line is a dictionary containing
            # all information that was given by the user.
            filename = "Input_plate" + str(self.index) + ".txt"
            completeFilename = os.path.join(self.parent.inputsPath, filename)

            with open(completeFilename, "w+") as f:
                if self.PlateOptionMenu.get() == "Tip rack":
                    f.write("Tip rack" + "\n")
                    dict = {"label": self.PlateLabel.get(), "index": str(self.index),
                            "AssignedPipetOption": self.AssignedPipetOption.get()}
                    f.write(json.dumps(dict))

                elif self.PlateOptionMenu.get() == "Well plate":
                    f.write("Well plate" + "\n")

                    # initialize variables
                    data = []
                    iter = 0
                    dimension = 0

                    #for all frames in self.dict_compounds (dictionary of irow : {frame_comp, unit} pairs)
                    for value in self.dict_compounds.values():
                        frame = value["frame"]
                        #get type of compound
                        classname = re.search("(\w+):", frame.winfo_children()[0].winfo_children()[1].cget("text"))
                        data.append(classname.group(1).capitalize())
                        iter += 1
                        data.append([])
                        #for all customtkinter.CTkEntry widgets in this frame, get values
                        for child in frame.winfo_children():
                            for widget in child.winfo_children():
                                if widget.winfo_class() == 'Entry':
                                    data[iter].append(widget.get())
                        # get unit for compound
                        data[iter].append(value["unit"].get())
                        iter += 1

                    # parse
                    names_conc = ""
                    ranges = ""
                    positions = ""
                    types_compounds = ""
                    tuberackpos = str(self.TubeRack.get())
                    for i in range(int(len(data) / 2)):
                        types_compounds += data[i * 2] + ","
                        # each element of the form: label space (conc unit)
                        names_conc += data[i * 2 + 1][0] + " (" + str(data[i * 2 + 1][1]) + data[i * 2 + 1][5] + "),"
                        # if min and max value of range different, dimension + 1 in iteration
                        if data[i * 2 + 1][2] != data[i * 2 + 1][3]:
                            dimension += 1
                            #if min > max boundary for range, swap
                            if data[i * 2 + 1][2] > data[i * 2 + 1][3]:
                                ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                                # TODO: add warning to let the user now they were switched
                        positions += tuberackpos + "/" + data[i * 2 + 1][4] + ","
                        ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                    names_conc += "MQ"
                    ranges = ranges[:-1]
                    types_compounds = types_compounds[:-1]
                    positions += tuberackpos + "/" + self.MQposition.get()

                    # write to file:
                    dict = {"label": self.PlateLabel.get(), "index": self.index, "dimension": str(dimension),
                            "names_conc": names_conc, "positions": positions, "ranges": ranges,
                            "WorkingVolume": self.WorkingVolume.get(), "Tuberack": self.TubeRack.get(),
                            "types_compounds": types_compounds}
                    f.write(json.dumps(dict))

                elif self.PlateOptionMenu.get() == "Tube rack":
                    f.write("Tube rack" + "\n")
                    dict = {"label": self.PlateLabel.get(), "index": str(self.index)}
                    f.write(json.dumps(dict))
            # removes frame
            self.destroy()

    """
    The method addcompound creates a frame_comp object in the middle frame of InputsFrame (= frame_compounds). 
    In this frame, all information of a compound can be specified.
    """
    def addcompound(self, typecomp, compoundlabel="", compoundstock="", fromrange="", torange="",
                    position="", unit=""):
        irow = self.irow
        frame_comp = customtkinter.CTkFrame(master=self.frame_compounds)
        frame_comp.grid(row=irow, column=0, columnspan=3)

        #fill in label
        Label = customtkinter.CTkLabel(master=frame_comp, text="label " + typecomp + ": ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_comp, width=100)
        CompoundLabel.insert(END, compoundlabel)
        CompoundLabel.grid(row=0, column=1)

        # fill in stock
        Stock = customtkinter.CTkLabel(master=frame_comp, text="conc: ", width=50)
        Stock.grid(row=0, column=2, padx=2)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_comp, width=50)
        CompoundStock.insert(END, compoundstock)
        CompoundStock.grid(row=0, column=3)

        # fill in range
        Gradient = customtkinter.CTkLabel(master=frame_comp, text="range:", width=50, anchor="e")
        Gradient.grid(row=0, column=4)

        FromRange = customtkinter.CTkEntry(master=frame_comp, width=40)
        FromRange.insert(END, fromrange)
        FromRange.grid(row=0, column=5, padx=2)

        customtkinter.CTkLabel(master=frame_comp, text="-", width=1).grid(row=0, column=6, padx=2)
        ToRange = customtkinter.CTkEntry(master=frame_comp, width=40)
        ToRange.insert(END, torange)
        ToRange.grid(row=0, column=7, padx=2)

        #fill in unit
        Unit = customtkinter.CTkOptionMenu(master=frame_comp, values=["M", "%"], width=40)
        if unit in ["%", "M"]:
            Unit.set(unit)
        Unit.grid(row=0, column=8)
        Unit.grid_propagate(False)

        #fill in position
        PositionLabel = customtkinter.CTkLabel(master=frame_comp, text="position: ", width=60)
        PositionLabel.grid(row=0, column=9)

        Position = customtkinter.CTkEntry(master=frame_comp, width=40)
        Position.insert(END, position)
        Position.grid(row=0, column=10)

        """ The method remove_event deletes the frame_comp frame (i.e. a compound)"""
        def remove_event():
            frame_comp.destroy()
            # remove also from self.dict
            del self.dict_compounds[irow]
        # remove button (red 'X' at the end of the row)
        RemoveButton = customtkinter.CTkButton(master=frame_comp, command=remove_event, fg_color="firebrick",
                                               text="x", width=0.05)
        RemoveButton.grid(row=0, column=11)

        # update
        self.dict_compounds[self.irow] = {"frame": frame_comp, "unit": Unit}
        self.irow = self.irow + 1


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
