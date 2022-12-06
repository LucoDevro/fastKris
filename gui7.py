#!usr/bin/env python
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
import ScriptBuilder
import easygui as e
import csv
import numpy as np
import xlsxwriter
from tkinter.scrolledtext import ScrolledText
from PIL import Image

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark" (standard), "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


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

        self.input_dict = {key: None for key in range(1, 13)}
        self.UserPath = fd.askdirectory()

        # create the necessary folders:
        parent_dir = os.path.join(self.UserPath, "inputs")
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)
        self.inputsPath = parent_dir

        self.resizable(False, False)

    def on_closing(self, event=0):
        self.destroy()


class ControlFrame(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.grid(row=0, column=1, sticky="nsew")

        # ============ create two frames ============

        # configure grid layout (1x2)
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
        # configure grid layout (20x2)
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
                                              text="pipets",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=11, column=0, columnspan=2, pady=10, padx=10)

        self.hasTwoPipets = False
        self.selected_value = customtkinter.StringVar()

        # setup for if two pipets available: force on left then other right (not implemented yet)
        self.selected_side_pipet = customtkinter.StringVar()

        self.frame_pipet = customtkinter.CTkFrame(master=self.frame_left)

        self.frame_pipet.grid(row=12, column=0, columnspan=2, padx=10, sticky="nsew")

        self.AddPipetLabel = customtkinter.CTkLabel(master=self.frame_pipet, text="Add pipet(s): ", width=30)
        self.AddPipetLabel.grid(row=0, column=0, padx=10, sticky="nsew")

        self.AddPipet = customtkinter.CTkEntry(master=self.frame_pipet)
        self.AddPipet.grid(row=0, column=1, sticky="nsew")

        self.optionmenu_pip = customtkinter.CTkOptionMenu(master=self.frame_pipet,
                                                          values=["left", "right"],
                                                          variable=self.selected_side_pipet,
                                                          width=80)
        self.optionmenu_pip.grid(row=0, column=2, padx=10, sticky="nsew")
        #
        self.AddPipetButton = customtkinter.CTkButton(master=self.frame_pipet, text="Add... ",
                                                      command=self.addPipet, width=54)
        self.AddPipetButton.grid(row=0, column=4)
        self.AddPipetButton.grid_propagate(False)

        pipetsFileName = os.path.join(self.parent.inputsPath, "pipets.txt")
        if os.path.exists(pipetsFileName):
            with open(pipetsFileName, "r") as f:
                lines = f.readlines()
                self.AddPipet.insert(END, lines[0].replace("\n", ""))
                self.optionmenu_pip.set(lines[1].replace("\n", ""))
                if len(lines) == 4:
                    self.addPipet(lines[2].replace("\n", ""), lines[3].replace("\n", ""))

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

        self.frame_panels = customtkinter.CTkFrame(master=self.frame_right, fg_color="transparent",
                                                   bg_color="transparent")
        self.frame_panels.grid(row=1, column=0, columnspan=3, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_panels ============

        imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.waste = customtkinter.CTkImage(light_image=Image.open(os.path.join(imagepath, "wastebin_light.png")),
                                            size=(40, 40), dark_image=Image.open(os.path.join(imagepath, "wastebin_dark.png")))

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
                                               command=lambda *args: button_event(self, 1))
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
                                               command=lambda *args: button_event(self, 2))
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
                                               command=lambda *args: button_event(self, 3))
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
                                               command=lambda *args: button_event(self, 4))
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
                                               command=lambda *args: button_event(self, 5))
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
                                               command=lambda *args: button_event(self, 6))
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
                                               command=lambda *args: button_event(self, 7))
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
                                               command=lambda *args: button_event(self, 8))
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
                                               command=lambda *args: button_event(self, 9))
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
                                                command=lambda *args: button_event(self, 10))
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
                                                command=lambda *args: button_event(self, 11))
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
                                                command=lambda *args: button_event(self, 12),
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
        self.button12.grid(row=0, column=2, pady=2, padx=2, sticky="nesw", )

        def button_event(self, index):
            if isinstance(self.frame_right, InputFrame):
                self.frame_right.destroy()  # else if multiple buttons pressed, all frames will stack
            self.frame_right = InputFrame(parent, index)
            self.frame_right.tkraise()

        self.button13 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Load from parameter file",
                                                text_color=("black", "grey80"),
                                                border_width=2,  # <- custom border_width
                                                fg_color="transparent",  # <- no fg_color
                                                command=self.load_from_parameterfile)
        self.button13.grid(row=8, column=1, columnspan=1, pady=10, padx=5, sticky="e")

        self.button14 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Generate Protocol",
                                                text_color=("black", "grey80"),
                                                border_width=2,  # <- custom border_width
                                                fg_color="transparent",  # <- no fg_color
                                                command=self.generate_protocol)
        self.button14.grid(row=8, column=2, columnspan=1, pady=10, padx=5, sticky="")

    def addPipet(self, label="", place="left"):
        self.AddPipet2 = customtkinter.CTkEntry(master=self.frame_pipet)
        self.AddPipet2.insert(END, label)
        self.AddPipet2.grid(row=2, column=1, sticky="nsew")

        self.optionmenu_pip2 = customtkinter.CTkOptionMenu(master=self.frame_pipet,
                                                           values=["left", "right"], width=80)
        self.optionmenu_pip2.set(place)
        self.optionmenu_pip2.grid(row=2, column=2, padx=10, sticky="nsew")

        self.RemovePipetButton = customtkinter.CTkButton(master=self.frame_pipet,
                                                         text="remove", width=54, command=self.removePipet)
        self.RemovePipetButton.grid(row=2, column=4)
        self.RemovePipetButton.grid_propagate(False)

        self.AddPipetButton.grid_remove()
        self.hasTwoPipets = True

    def removePipet(self):
        Lst = self.frame_pipet.grid_slaves(row=2)
        for l in Lst:
            l.destroy()
        self.AddPipetButton.grid()
        self.hasTwoPipets = False

    def pipetApply(self):
        isExist = os.path.exists(self.parent.inputsPath)
        if not isExist:
            os.makedirs(self.parent.inputsPath)

        if self.AddPipet.get() != "":
            instruments = self.AddPipet.get() + "\n" + self.optionmenu_pip.get() + "\n"
            with open(os.path.join(self.parent.inputsPath, "pipets.txt"), "w") as f:
                f.write(instruments)
        else:
            e.msgbox("First pipet not specified", "Error")
            return None

        if self.hasTwoPipets == True:
            if self.AddPipet2.get() != "":
                with open(os.path.join(self.parent.inputsPath, "pipets.txt"), "a") as f:
                    f.write(self.AddPipet2.get() + "\n" + self.optionmenu_pip2.get() + "\n")
            else:
                e.msgbox("Second pipet not specified", "Error")
                return None

    def change_appearance_mode(self):
        switch = self.switch_darkmode.get()
        if switch == "on":
            self.configure(customtkinter.set_appearance_mode("Dark"))
        else:
            self.configure(customtkinter.set_appearance_mode("Light"))

    ##CHANGED NOW
    def generate_protocol(self):
        isExist = os.path.exists(self.parent.inputsPath)
        if not isExist:
            os.makedirs(self.parent.inputsPath)
            return None

        names_conc_to_add = []
        conc_to_add = []
        labels_to_add = []

        protocolFilename = simpledialog.askstring("Protocol filename", "filename for new protocol\t\t\t")

        # if not cancelled
        if protocolFilename:
            protocolFilename += ".py"

            # read in compound library:
            with open('compLibrary.txt', 'r') as l:
                reader = csv.reader(l, delimiter="\t")
                lines = [entry for line in reader for entry in line]

            labels = str(lines[0::3])[1:-1]
            types = str(lines[1::3])[1:-1]
            # print(labels)
            # print(types)

            # read all information in
            directory = os.path.join(self.parent.inputsPath)
            tips = ""
            tuberacks = ""
            instruments = ""
            plates = ""
            screens = ""
            atLeastOneInput = 0
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    with open(f, "r") as f:
                        Type = f.readline().replace("\n", "")
                        if Type == "Tube rack":
                            atLeastOneInput += 1
                            dictTur = json.loads(f.read())
                            for key in dictTur:
                                if dictTur.get(key) != "":
                                    tuberacks += dictTur.get(key) + "\n"
                                else:
                                    e.msgbox("Empty string value for name plate: " + filename, "Error")
                                    return None

                        elif Type == "Tip rack":
                            atLeastOneInput += 1
                            dictTir = json.loads(f.read())
                            for key in dictTir.keys():
                                if dictTir.get(key) != "":
                                    tips += dictTir.get(key) + "\n"
                                else:
                                    e.msgbox("Empty string value for name plate: " + filename, "Error")
                                    return None

                        elif Type == "Well plate":
                            atLeastOneInput += 1
                            dict = json.loads(f.readline())
                            plates += dict["label"] + "\n" + str(dict["index"]) + "\n"
                            if dict["label"] == "":
                                e.msgbox("Empty string value for name plate: " + filename, "Error")
                                return None

                            screens += str(dict["dimension"]) + "\n"
                            if "" not in dict["names_conc"].split(","):
                                screens += dict["names_conc"] + "\n"
                            else:
                                e.msgbox(
                                    "Empty string value for name or concentration of one of the compounds: " + filename,
                                    "Error")
                                return None

                            if "" not in dict["positions"].split(","):
                                screens += dict["positions"] + "\n"
                            else:
                                e.msgbox("Empty string value for position of one of the compounds: " + filename,
                                         "Error")
                                return None

                            if all(not (string.endswith("-") or string.startswith("-")) for string in
                                   dict["ranges"].split(",")):
                                screens += dict["ranges"] + "\n"
                            else:
                                e.msgbox("Empty string value for ranges of one of the compounds: " + filename, "Error")
                                return None

                            screens += str(dict["index"]) + "\n"

                            if "" != dict["WorkingVolume"]:
                                screens += str(dict["WorkingVolume"]) + "\n"
                            else:
                                e.msgbox("Empty string value for the working volume in: " + filename,
                                         "Error")
                                return None

                            # check if all compounds are already present in the library.
                            names_conc = dict["names_conc"].split(",")[:-1]
                            labels_compounds = dict["labels_compounds"].split(",")
                            concs = []
                            for i in names_conc:
                                try:
                                    concs.append(re.search(r"([0-9]+)", i.split(" (")[1]).group(1))
                                except AttributeError:
                                    e.msgbox(
                                        "Unrecognized or empty value for one of the concentrations in: " + filename,
                                        "Error")
                                    return None

                            zipLabelType = list(map(lambda x, y: (x.replace("\'", ""), y.replace("\'", "")),
                                                    labels.split(", "), types.split(", ")))
                            zipInput = list(map(lambda x, y: (x, y), names_conc, labels_compounds))

                            if any(x not in zipLabelType for x in zipInput):
                                for idx in range(len(zipInput)):
                                    if (zipInput[idx] not in zipLabelType):
                                        if zipInput[idx][0] in list(
                                                map(lambda x: x.replace("\'", ""), labels.split(", "))):
                                            e.msgbox(filename + "\n" + str(zipInput[idx][
                                                                               0]) + ": A compound with the same label, but different type is already present in the library."
                                                     , "Error")
                                            return None
                                        names_conc_to_add.append(names_conc[idx])
                                        labels_to_add.append(labels_compounds[idx])
                                        conc_to_add.append(concs[idx])

                            # create a matrix
                            # TODO: also for 3D
                            if str(dict["dimension"]) == 1 or str(dict["dimension"] == 2):
                                try:
                                    numberOfWells = int(re.search(r'([0-9]+)', dict["label"]).group(1))
                                    ranges = dict["ranges"].split(",")
                                    workbook = xlsxwriter.Workbook(
                                        os.path.join(self.parent.UserPath, protocolFilename.replace(".py", ".xlsx")))
                                    worksheet = workbook.add_worksheet()
                                    headers = ["Name"] + [*range(1, numberOfWells + 1)]
                                    # worksheet.write(row, col, item)
                                    for i in range(len(headers)):
                                        worksheet.write(0, i, headers[i])
                                    for i in range(len(names_conc)):
                                        raw_range = [float(j) for j in ranges[i].split('-')]
                                        RowToAdd = [names_conc[i]] + list(
                                            map(str, np.linspace(raw_range[0], raw_range[1], numberOfWells).tolist()))
                                        for k in range(len(RowToAdd)):
                                            worksheet.write(i + 1, k, RowToAdd[k])
                                    workbook.close()
                                except AttributeError:
                                    continue

                if atLeastOneInput == 0:
                    e.msgbox("No input files with slot information found. Specify input for at least one slot", "Error")
                    return None

            if len(names_conc_to_add) > 0:
                answer = messagebox.askquestion(
                    message="Are you sure you want to continue and add following compounds to the library?\n" +
                            "\n".join(' '.join(map(str, tup)) for tup in
                                      list(zip(names_conc_to_add, labels_to_add, conc_to_add))))

                if answer == "yes":
                    with open("compLibrary.txt", "a") as f:
                        for idx in range(len(names_conc_to_add)):
                            f.write("\n" + names_conc_to_add[idx] + "\t")
                            f.write(labels_to_add[idx].capitalize() + "\t")
                            f.write(conc_to_add[idx])

            FilenamePipets = os.path.join(self.parent.inputsPath, "pipets.txt")
            if os.path.isfile(FilenamePipets):
                with open(FilenamePipets) as f:
                    instruments += "".join(f.readlines())
            else:
                e.msgbox("no prior information of pipet(s) saved. Specify name and position.", "Error")
                return None

            # The name of the parameterfile will be: protocol filename.param.txt
            paramFilename = protocolFilename.replace(".py", ".param.txt")
            paramFilePath = os.path.join(self.parent.UserPath, paramFilename)
            # print("path", paramFilePath)
            with open(paramFilePath, "w+") as f:
                f.write(tips + "\n")
                f.write(tuberacks + "\n")
                f.write(instruments + "\n")
                f.write(plates + "\n")
                f.write(screens)

            # generate the protocol
            ##leave for now, but change once added to left frame
            #
            ScriptBuilder.BuildWithMetadata(paramFilePath, os.path.join(self.parent.UserPath, protocolFilename),
                                            self.name.get(), self.description.get("0.0", "end"), self.author.get()) # CHANGE IN DESCRIPTION; old: self.description.get()

    def load_from_parameterfile(self):
        try:
            isExist = os.path.exists(self.parent.inputsPath)
            if not isExist:
                os.makedirs(self.parent.inputsPath)

            parampath = askopenfilename()
            with open(parampath, 'r') as f:
                lines = f.read()
                lines = lines.split("\n\n")

            tips_raw = lines[0].split("\n")
            tuberack_raw = lines[1].split("\n")
            instr_raw = lines[2].split("\n")
            plates_raw = lines[3].split("\n")
            screens_raw = lines[4].split('\n')
            if screens_raw[-1] == '':
                screens_raw = screens_raw[:-1]
            else:
                screens_raw = screens_raw

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

            tuberacksInput = tuberack_raw[0::2]
            tuberacksLocation = tuberack_raw[1::2]

            for i in range(len(tuberacksLocation)):
                filename = "Input_plate" + str(tuberacksLocation[i]) + ".txt"
                filePath = os.path.join(self.parent.inputsPath, filename)
                with open(filePath, "w") as f:
                    f.write("Tube rack" + "\n")
                    dict = {"label": tuberacksInput[i], "index": str(tuberacksLocation[i])}
                    f.write(json.dumps(dict))

            instrumentInput = instr_raw[0::2]
            instrumentLocation = instr_raw[1::2]
            filename = "pipets.txt"
            filePath = os.path.join(self.parent.inputsPath, filename)
            with open(filePath, "w") as f:
                for i in range(len(instrumentInput)):
                    f.write(instrumentInput[i] + "\n")
                    f.write(instrumentLocation[i] + "\n")

            self.AddPipet.delete(0, END)
            self.AddPipet.insert(END, instrumentInput[0])
            self.optionmenu_pip.set(instrumentLocation[0])
            if len(instrumentInput) == 2:
                self.addPipet(instrumentInput[1], instrumentLocation[1])

            platesInput = plates_raw[0::2]
            platesLocation = plates_raw[1::2]
            all_screen_types = screens_raw[0::6]
            all_screen_compounds = screens_raw[1::6]
            all_screen_stocks = screens_raw[2::6]
            all_screen_ranges = screens_raw[3::6]
            all_screen_plates = screens_raw[4::6]
            all_screen_workVol = screens_raw[5::6]

            with open('compLibrary.txt', 'r') as l:
                reader = csv.reader(l, delimiter="\t")
                lines = [entry for line in reader for entry in line]

            labels = lines[0::3]
            types = lines[1::3]
            label_compounds = []
            for i in range(len(all_screen_plates)):
                list_screen_compounds = all_screen_compounds[i].split(",")
                labels_i = []
                for j in range(len(list_screen_compounds)):
                    comp = list_screen_compounds[j]
                    compIdx = labels.index(comp)
                    if compIdx != None:
                        labels_i.append(types[compIdx])
                    else:
                        e.msgbox("Unknown compound " + comp + " in parameter file", "Error")
                        return None
                label_compounds.append(labels_i)

            for i in range(len(platesLocation)):
                filename = "Input_plate" + str(platesLocation[i]) + ".txt"
                filePath = os.path.join(self.parent.inputsPath, filename)

                with open(filePath, "w") as f:
                    f.write("Well plate" + "\n")
                    dict = {"label": platesInput[i], "index": platesLocation[i], "dimension": str(all_screen_types[i]),
                            "names_conc": all_screen_compounds[i], "positions": all_screen_stocks[i],
                            "ranges": all_screen_ranges[i],
                            "WorkingVolume": all_screen_workVol[i], "Tuberack": all_screen_stocks[i][0],
                            "labels_compounds": ",".join(label_compounds[i][:-1])}
                    f.write(json.dumps(dict))

        except Exception as err:
            e.msgbox(
                "Something went wrong during loading of the parameter file. Make sure the file follows the correct format exactly, including newline characters.\n" + str(
                    err), "Error")
            return None


class InputFrame(customtkinter.CTkFrame):
    def __init__(self, parent, index):
        super().__init__(parent)
        self.units = {"Salt": "M", "Precipitant": "%", "Buffer": "M"}
        self.units_paramfile = {"Salt": "M", "Precipitant": "%", "Buffer": "M"}
        self.index = index
        self.parent = parent
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nes")
        # self.config(width=140)
        # self.pack_propagate(0)

        self.frame_up = customtkinter.CTkFrame(master=self, width=650, height=472)
        self.frame_up.columnconfigure((0, 1), weight=1)
        self.frame_up.grid(row=0, column=0, sticky="nsew")
        # # here changed for well_plate
        self.frame_up.grid_propagate(False)

        self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=650, height=367)
        self.frame_compounds.grid(row=3, column=0, columnspan=2, sticky="ns")
        ##here changed for well_plate size frame_right
        self.frame_compounds.grid_propagate(False)

        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.columnconfigure([0, 1, 2], weight=1)
        self.frame_down.grid(row=2, column=0, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="slot " + str(self.index), font=('Segoe UI', 11, BOLD)) \
            .grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(1, 10))
        customtkinter.CTkLabel(master=self.frame_up, text="name container: ").grid(row=1, column=0, sticky="W")

        self.PlateLabel = customtkinter.CTkEntry(master=self.frame_up)

        self.valuesPlateOptionMenu = ["Choose...", "Tube rack", "Tip rack", "Well plate"]
        self.plateOptionVar = customtkinter.StringVar()

        # if file already exists:
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)
        if os.path.exists(completeFilename):
            with open(completeFilename, "r") as f:
                plateType = f.readline()
                # clean up
                if any(t in plateType for t in ["Tip rack", "Tube rack", "Well plate"]):
                    self.PlateLabel.insert(END, json.loads(f.readline())['label'])

        self.PlateLabel.grid(row=1, column=1, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="add to slot:").grid(row=2, column=0, sticky="W")
        self.PlateOptionMenu = customtkinter.CTkOptionMenu(master=self.frame_up, variable=self.plateOptionVar,
                                                           values=self.valuesPlateOptionMenu,
                                                           command=self.CompoundsFrameEvent)
        if os.path.exists(completeFilename):
            with open(completeFilename, "r") as f:
                Platetype = f.readline()
                if "Tube rack" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[1])
                elif "Tip rack" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[2])
                elif "Well plate" in Platetype:
                    self.PlateOptionMenu.set(self.valuesPlateOptionMenu[3])
        else:
            self.PlateOptionMenu.set(self.valuesPlateOptionMenu[0])
        self.PlateOptionMenu.grid(row=2, column=1, sticky="nsew")

        # set fixed for now, font family can be obtained dynamically (not implemented yet)
        self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
        self.frame_Compounds_input.grid()
        self.frame_Compounds_input.propagate(False)

        self.frame_compounds.rowconfigure(2, minsize=5)  # empty row with minsize as spacing)
        self.irow = 8
        self.dict_compounds = {}

        # print(self.PlateOptionMenu.get())
        self.CompoundsFrameEvent(self.PlateOptionMenu.get())

        self.buttonReset = customtkinter.CTkButton(master=self.frame_down, text="reset", command=self.reset,
                                                   fg_color="grey")
        self.buttonReset.grid(column=0, row=3, sticky="nsew")
        self.buttonCancel = customtkinter.CTkButton(master=self.frame_down, text="cancel", command=self.cancel,
                                                    fg_color="grey")
        self.buttonCancel.grid(column=1, row=3, sticky="nsew")
        self.buttonApply = customtkinter.CTkButton(master=self.frame_down, text="apply", command=self.button_event)
        self.buttonApply.grid(column=2, row=3, sticky="nsew")
        # change to row = 1, column = 0 to let it appear on the bottom instead of the right
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def CompoundsFrameEvent(self, choice):
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)

        if choice == "Tip rack":
            self.frame_Compounds_input.destroy()
            self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
            self.frame_Compounds_input.grid()
            self.frame_Compounds_input.grid_rowconfigure(0, minsize=3)

            self.AssignedPipetLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input,
                                                             text="Assigned to pipet:", anchor="w")
            self.AssignedPipetLabel.grid(row=2, column=0, sticky="nw")

            self.AssignedPipetOption = customtkinter.CTkOptionMenu(master=self.frame_Compounds_input,
                                                                   values=["left", "right"])
            self.AssignedPipetOption.grid(row=2, column=1, sticky="nsew")

            # bc also called if no prev info known
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Tip rack" in lines[0]:
                        self.AssignedPipetOption.set(json.loads(lines[1])['AssignedPipetOption'])


        elif choice == "Tube rack":
            self.frame_Compounds_input.destroy()

        elif choice == "Well plate":
            self.frame_Compounds_input.destroy()
            self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
            self.frame_Compounds_input.grid()
            self.frame_Compounds_input.propagate(False)

            self.CompoundsLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input, text="Compounds",
                                                         font=('Segoe UI', 10, BOLD))
            self.CompoundsLabel.grid(row=2, column=0, sticky="nw")
            self.CompoundsLabel.grid_propagate(False)

            self.WorkingVolumeLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input,
                                                             text="working volume (µl): ")
            self.WorkingVolumeLabel.grid(row=3, column=0)

            self.WorkingVolume = customtkinter.CTkEntry(master=self.frame_Compounds_input)
            self.WorkingVolume.grid(row=3, column=1)

            self.TubeRackLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input,
                                                        text="tube rack position: ")
            self.TubeRack = customtkinter.CTkEntry(master=self.frame_Compounds_input)
            self.TubeRackLabel.grid(row=4, column=0)
            self.TubeRack.grid(row=4, column=1)

            self.MQpositionLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input, text="Milli-Q position: ")
            self.MQpositionLabel.grid(row=5, column=0)
            # B2
            # self.MQposition = customtkinter.CTkEntry(master = self.frame_Compounds_input, text = "Milli-Q position: ")
            self.MQposition = customtkinter.CTkEntry(master=self.frame_Compounds_input)
            self.MQposition.grid(row=5, column=1)

            self.HelpPositions = customtkinter.CTkButton(master=self.frame_Compounds_input, text="?", corner_radius=5,
                                                         width=0.1, height=0.1, fg_color="gray33",
                                                         command=self.openHelpPositions)
            self.HelpPositions.grid(row=5, column=2, sticky="w", padx=5)

            self.frame_Compounds_input.grid_rowconfigure(6, minsize=5)  # empty row with minsize as spacing

            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Well plate" in lines[0]:
                        dict = json.loads(lines[1])
                        self.WorkingVolume.insert(END, dict["WorkingVolume"])
                        self.TubeRack.insert(END, dict["Tuberack"])
                        compounds = dict["names_conc"].split(",")
                        positions = dict["positions"].split(",")
                        # compounds is a list
                        for j in range(len(compounds)):
                            if 'MQ' == compounds[j]:
                                # in case no position previously given by user, suppress AttributeError
                                try:
                                    self.MQposition.insert(END, re.search(r"/(\w+)", positions[j]).group(1))
                                except AttributeError:
                                    pass

            self.AddSalt = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add salt",
                                                   command=lambda *args: self.addcompound("salt", True),
                                                   width=215)
            self.AddSalt.grid(row=7, column=0, padx=0, sticky="nw")
            self.AddSalt.grid_propagate(False)
            self.AddBuffer = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add buffer",
                                                     command=lambda *args: self.addcompound("buffer", True),
                                                     width=215)
            self.AddBuffer.grid(row=7, column=1, padx=0, sticky="nw")
            self.AddBuffer.grid_propagate(False)
            self.AddPrecipitant = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add precipitant",
                                                          command=lambda *args: self.addcompound("precipitant", True),
                                                          width=215)
            self.AddPrecipitant.grid(row=7, column=2, padx=0, sticky="nw")
            self.AddPrecipitant.grid_propagate(False)

            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    if "Well plate" in lines[0]:
                        dict = json.loads(lines[1])
                        labels_compounds = dict["labels_compounds"].split(",")
                        names_conc = dict["names_conc"].split(",")[:-1]
                        # [letter for letter in 'human']
                        names = [i.split(" (")[0] for i in names_conc]
                        # stopped here
                        units = [re.search(r"[0-9]+([%M])", i.split(" (")[1]).group(1) for i in names_conc]
                        concs = []
                        for i in names_conc:
                            # bc will output " (M)" in case no concentration provided by the user
                            try:
                                concs.append(re.search(r"([0-9]+)", i.split(" (")[1]).group(1))
                            except AttributeError:
                                concs.append("")
                        ranges = dict["ranges"].split(",")
                        positions = dict["positions"].split(",")[:-1]
                        shortpositions = [i.split("/")[1] for i in positions]

                        it = [names, concs, ranges, shortpositions]
                        if all(len(l) == len(labels_compounds) for l in it):
                            for i in range(len(labels_compounds)):
                                if labels_compounds[i] == "Salt" or labels_compounds[i] == "Buffer" or labels_compounds[
                                    i] == "Precipitant":
                                    self.addcompound(labels_compounds[i].lower(), True, names[i], concs[i],
                                                     ranges[i].split("-")[0],
                                                     ranges[i].split("-")[1], shortpositions[i], units[i])

    def openHelpPositions(self):
        webbrowser.open_new(r"https://docs.opentrons.com/ot1/containers.html")

    def reset(self):
        Filename = os.path.join(self.parent.inputsPath, "Input_plate" + str(self.index) + ".txt")
        try:
            os.unlink(Filename)
            InputFrame(self.parent, self.index)
            self.destroy()
        except FileNotFoundError:
            InputFrame(self.parent, self.index)
            self.destroy()
            return None
        except OSError as err:
            e.msgbox(repr(err), "Error")
            return None

    def cancel(self):
        self.destroy()

    def button_event(self):
        if self.PlateOptionMenu.get() == "Choose...":
            self.destroy()
            # Return exits the current function or method. Pass is a null operation and allows execution to continue at the next statement
            return None
        else:
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

                    for value in self.dict_compounds.values():
                        frame = value["frame"]
                        classname = re.search("(\w+):", frame.winfo_children()[0].winfo_children()[1].cget("text"))
                        data.append(classname.group(1).capitalize())
                        iter += 1
                        data.append([])
                        for child in frame.winfo_children():
                            for widget in child.winfo_children():
                                if widget.winfo_class() == 'Entry':
                                    data[iter].append(widget.get())
                        data[iter].append(value["unit"].get())
                        iter += 1

                    # parse:
                    names_conc = ""
                    ranges = ""
                    positions = ""
                    labels_compounds = ""
                    tuberackpos = str(self.TubeRack.get())
                    for i in range(int(len(data) / 2)):
                        labels_compounds += data[i * 2] + ","
                        # each element of the form: label space (conc unit)
                        names_conc += data[i * 2 + 1][0] + " (" + str(data[i * 2 + 1][1]) + data[i * 2 + 1][5] + "),"
                        # user friendly
                        if data[i * 2 + 1][2] != data[i * 2 + 1][3]:
                            dimension += 1
                            if data[i * 2 + 1][2] > data[i * 2 + 1][3]:
                                ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                                # TODO: add warning to let the user now they were switched
                        positions += tuberackpos + "/" + data[i * 2 + 1][4] + ","
                        ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                    names_conc += "MQ"
                    ranges = ranges[:-1]
                    labels_compounds = labels_compounds[:-1]
                    positions += tuberackpos + "/" + self.MQposition.get()

                    # write to file:
                    dict = {"label": self.PlateLabel.get(), "index": self.index, "dimension": str(dimension),
                            "names_conc": names_conc, "positions": positions, "ranges": ranges,
                            "WorkingVolume": self.WorkingVolume.get(), "Tuberack": self.TubeRack.get(),
                            "labels_compounds": labels_compounds}
                    f.write(json.dumps(dict))

                elif self.PlateOptionMenu.get() == "Tube rack":
                    f.write("Tube rack" + "\n")
                    dict = {"label": self.PlateLabel.get(), "index": str(self.index)}
                    f.write(json.dumps(dict))
            # removes frame
            self.destroy()

    def addcompound(self, typecomp, include_range=False, compoundlabel="", compoundstock="", fromrange="", torange="",
                    position="", unit=""):
        irow = self.irow
        frame_comp = customtkinter.CTkFrame(master=self.frame_Compounds_input)
        frame_comp.grid(row=irow, column=0, columnspan=3)

        Label = customtkinter.CTkLabel(master=frame_comp, text="label " + typecomp + ": ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_comp, width=100)
        CompoundLabel.insert(END, compoundlabel)
        CompoundLabel.grid(row=0, column=1)

        Stock = customtkinter.CTkLabel(master=frame_comp, text="conc: ", width=50)
        Stock.grid(row=0, column=2, padx=2)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_comp, width=50)
        CompoundStock.insert(END, compoundstock)
        CompoundStock.grid(row=0, column=3)

        if include_range == True:
            Gradient = customtkinter.CTkLabel(master=frame_comp, text="range:", width=50, anchor="e")
            Gradient.grid(row=0, column=4)

            FromRange = customtkinter.CTkEntry(master=frame_comp, width=40)
            FromRange.insert(END, fromrange)
            FromRange.grid(row=0, column=5, padx=2)

            customtkinter.CTkLabel(master=frame_comp, text="-", width=1).grid(row=0, column=6, padx=2)

            ToRange = customtkinter.CTkEntry(master=frame_comp, width=40)
            ToRange.insert(END, torange)
            ToRange.grid(row=0, column=7, padx=2)

        Unit = customtkinter.CTkOptionMenu(master=frame_comp, values=["M", "%"], width=40)
        if unit in ["%", "M"]:
            Unit.set(unit)
        Unit.grid(row=0, column=8)
        Unit.grid_propagate(False)

        PositionLabel = customtkinter.CTkLabel(master=frame_comp, text="position: ", width=60)
        PositionLabel.grid(row=0, column=9)

        Position = customtkinter.CTkEntry(master=frame_comp, width=40)
        Position.insert(END, position)
        Position.grid(row=0, column=10)

        def remove_event():
            frame_comp.destroy()
            # remove also from self.dict
            del self.dict_compounds[irow]

        RemoveButton = customtkinter.CTkButton(master=frame_comp, command=remove_event, fg_color="firebrick",
                                               text="x", width=0.05)
        RemoveButton.grid(row=0, column=11)

        # update row variable for compounds
        self.dict_compounds[self.irow] = {"frame": frame_comp, "unit": Unit}
        self.irow = self.irow + 1


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
