from tkinter import *
import customtkinter
from tkinter.font import BOLD
from tkinter import filedialog as fd
import os
import re
import webbrowser

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, control, parent, index):
        super().__init__(parent)
        self.units = {"salt": "M", "precipitate": "m%", "buffer": "M"}
        self.units_paramfile = {"salt": "M", "precipitate": "%", "buffer": "M"}
        self.index = index
        self.parent = parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_up = customtkinter.CTkFrame(master=self, width=680)
        # self.frame_up.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame_up.columnconfigure((0, 1), weight=1)
        self.frame_up.grid(row=0, column=0, sticky="nsew")
        # here changed for well_plate
        self.frame_up.grid_propagate(False)

        self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=680)
        self.frame_compounds.grid(row=2, column=0, columnspan=2, sticky="ns")
        ##here changed for well_plate size frame_right
        # self.frame_compounds.grid_propagate(False)

        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.columnconfigure(0, weight=1)  # , uniform="")
        self.frame_down.grid(row=2, column=0, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="name plate: ").grid(row=0, column=0, sticky="W")

        self.PlateLabel = customtkinter.CTkEntry(master=self.frame_up)

        ##ADDED GUI4
        self.valuesPlateOptionMenu = ["Choose...", "Tube rack", "Tip rack", "Well plate"]
        self.plateOptionVar = customtkinter.StringVar()
        ##ADDED GUI4
        #if file already exists:
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)
        if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    plateType = f.readline()
                    if any(t in plateType for t in ["Tube rack", "Tip rack","Well plate"]):
                        self.PlateLabel.insert(END, f.readline()[:-1])
        self.PlateLabel.grid(row=0, column=1, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="add to plate:").grid(row=1, column=0, sticky="W")
        self.PlateOptionMenu = customtkinter.CTkOptionMenu(master=self.frame_up, variable= self.plateOptionVar,
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
        ##END ADDED GUI4
        self.PlateOptionMenu.grid(row=1, column=1, sticky="nsew")

        # set fixed for now, font family can be obtained dynamically (not implemented yet)
        self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
        self.frame_Compounds_input.grid()
        self.frame_Compounds_input.propagate(False)

        self.frame_compounds.rowconfigure(2, minsize=5)  # empty row with minsize as spacing)
        self.irow = 8
        self.dict_compounds = {}

        ##ADDED GUI4
        #print(self.PlateOptionMenu.get())
        self.CompoundsFrameEvent(self.PlateOptionMenu.get())
        ##END ADDED GUI4

        self.buttonApply = customtkinter.CTkButton(master=self.frame_down, text="Apply", command=self.button_event)
        self.buttonApply.grid(column=0, row=3)
        # change to row = 1, column = 0 to let it appear on the bottom instead of the right
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def CompoundsFrameEvent(self, choice):
        ##ADDED GUI4
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)
        ##END ADDED GUI4

        if choice == "Tip rack":
            self.frame_Compounds_input.destroy()
            self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
            self.frame_Compounds_input.grid()
            self.frame_Compounds_input.grid_rowconfigure(0, minsize=3)

            # TODO: make ot align to the left of frame_compounds
            self.AssignedPipetLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input,
                                                             text="Assigned to pipet:", anchor="w")
            self.AssignedPipetLabel.grid(row=2, column=0, sticky="nw")

            self.AssignedPipetOption = customtkinter.CTkOptionMenu(master=self.frame_Compounds_input,
                                                                   values=["left", "right"])
            self.AssignedPipetOption.grid(row=2, column=1, sticky="nsew")

            ##ADDED GUI4
            # bc also called if no prev info known
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    self.AssignedPipetOption.set(lines[3].replace("\n", ""))
            ##END ADDED GUI4

        elif choice == "Tube rack":
            self.frame_Compounds_input.destroy()
            """
            self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
            self.frame_Compounds_input.grid(sticky = "nw")
            self.frame_Compounds_input.propagate(False)

            self.CompoundsLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input, text="Compounds",
                                                         text_font=('Segoe UI', 10, BOLD))
            self.CompoundsLabel.grid(row=2, column=0, sticky="nw")
            self.CompoundsLabel.grid_propagate(False)

            self.AddSalt = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add salt",
                                                   command=self.addsalt,
                                                   width=215)
            self.AddSalt.grid(row=3, column=0, padx=5, sticky="nw")
            self.AddSalt.grid_propagate(False)
            self.AddBuffer = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add buffer",
                                                     command= self.addbuffer,
                                                     width=215)
            self.AddBuffer.grid(row=3, column=1, padx=5, sticky="nw")
            self.AddBuffer.grid_propagate(False)
            self.AddPrecipitate = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add Precipitate",
                                                          command=self.addprecipitate, width=215)
            self.AddPrecipitate.grid(row=3, column=2, padx=5, sticky="nw")
            self.AddPrecipitate.grid_propagate(False)
            """

        elif choice == "Well plate":
            self.frame_Compounds_input.destroy()
            self.frame_Compounds_input = customtkinter.CTkFrame(master=self.frame_compounds, width=680)
            self.frame_Compounds_input.grid()
            self.frame_Compounds_input.propagate(False)

            self.CompoundsLabel = customtkinter.CTkLabel(master=self.frame_Compounds_input, text="Compounds",
                                                         text_font=('Segoe UI', 10, BOLD))
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

            self.AddSalt = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add salt",
                                                   command=lambda *args: self.addsalt(True),
                                                   width=215)
            ##ADDED GUI4
            if os.path.exists(completeFilename):
                with open(completeFilename, "r") as f:
                    lines = f.readlines()
                    self.WorkingVolume.insert(END,lines[9].replace("\n", ""))
                    self.TubeRack.insert(END, lines[6].replace("\n", "")[0])
                    compounds = lines[5].replace("\n", "").split(",")
                    positions = lines[6].replace("\n","").split(",")
                    for j in range(len(compounds)):
                        if 'MQ' == compounds[j]:
                            self.MQposition.insert(END,re.search(r"/(\w+)",positions[j]).group(1))
            ##END ADDED GUI4

            self.AddSalt.grid(row=7, column=0, padx=5, sticky="nw")
            self.AddSalt.grid_propagate(False)
            self.AddBuffer = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add buffer",
                                                     command=lambda *args: self.addbuffer(True),
                                                     width=215)
            self.AddBuffer.grid(row=7, column=1, padx=5, sticky="nw")
            self.AddBuffer.grid_propagate(False)
            self.AddPrecipitate = customtkinter.CTkButton(master=self.frame_Compounds_input, text="Add Precipitate",
                                                          command=lambda *args: self.addprecipitate(True),
                                                          width=215)
            self.AddPrecipitate.grid(row=7, column=2, padx=5, sticky="nw")
            self.AddPrecipitate.grid_propagate(False)

    def openHelpPositions(self):
        webbrowser.open_new(r"https://docs.opentrons.com/ot1/containers.html")

    def button_event(self):
        filename = "Input_plate" + str(self.index) + ".txt"
        completeFilename = os.path.join(self.parent.inputsPath, filename)

        with open(completeFilename, "w+") as f:
            if self.PlateOptionMenu.get() == "Tip rack":
                f.write("Tip rack" + "\n")
                f.write(self.PlateLabel.get() + "\n")
                f.write(str(self.index) + "\n")
                f.write(self.AssignedPipetOption.get() + "\n")

            elif self.PlateOptionMenu.get() == "Well plate":
                f.write("Well plate" + "\n")
                f.write(self.PlateLabel.get() + "\n")
                f.write(str(self.index) + "\n\n")

                # initialize variables
                data = []
                iter = 0
                dimension = 0

                for frame in self.dict_compounds.values():
                    classname = re.search("(\w+):", frame.winfo_children()[0].winfo_children()[1].cget("text"))
                    data.append(classname.group(1))
                    iter += 1
                    data.append([])
                    for child in frame.winfo_children():
                        for widget in child.winfo_children():
                            if widget.winfo_class() == 'Entry':
                                data[iter].append(widget.get())
                    iter += 1

                # parse:
                names_conc = ""
                ranges = ""
                positions = ""
                tuberackpos = str(self.TubeRack.get())
                for i in range(int(len(data) / 2)):
                    # each element of the form: label space (conc unit)
                    names_conc += data[i * 2 + 1][0] + " (" + str(data[i * 2 + 1][1]) + str(
                        self.units_paramfile.get(data[2 * i])) + "),"
                    # user friendly
                    if data[i * 2 + 1][2] != data[i * 2 + 1][3]:
                        dimension += 1
                        if data[i * 2 + 1][2] > data[i * 2 + 1][3]:
                            ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                            # TODO: add warning to let the user now they were switched
                    positions += tuberackpos + "/" + data[i * 2 + 1][4] + ","
                    ranges += str(data[i * 2 + 1][2]) + "-" + str(data[i * 2 + 1][3]) + ","
                names_conc += "MQ"
                positions += tuberackpos + "/" + self.MQposition.get()

                # write to file:
                f.write(str(dimension) + "\n")
                f.write(names_conc + "\n")
                f.write(positions + "\n")
                f.write(ranges[:-1] + "\n")
                f.write(str(self.index) + "\n")
                f.write(str(self.WorkingVolume.get()) + "\n")

            elif self.PlateOptionMenu.get() == "Tube rack":
                f.write("Tube rack" + "\n")
                f.write(self.PlateLabel.get() + "\n")
                f.write(str(self.index) + "\n")

            f.write("\n")
        # removes frame
        self.destroy()

    def addsalt(self, include_range=False):
        irow = self.irow
        frame_salt = customtkinter.CTkFrame(master=self.frame_Compounds_input)
        frame_salt.grid(row=irow, column=0, columnspan=3)

        Label = customtkinter.CTkLabel(master=frame_salt, text="label salt: ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_salt)
        CompoundLabel.grid(row=0, column=1)

        Stock = customtkinter.CTkLabel(master=frame_salt, text="conc (" + self.units.get("salt") + "): ", width=70)
        Stock.grid(row=0, column=2, padx=5)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_salt, width=50)
        CompoundStock.grid(row=0, column=3)

        if include_range == True:
            Gradient = customtkinter.CTkLabel(master=frame_salt, text="range:", width=50, anchor="e")
            Gradient.grid(row=0, column=4)

            FromRange = customtkinter.CTkEntry(master=frame_salt, width=50)
            FromRange.grid(row=0, column=5, padx=5)

            customtkinter.CTkLabel(master=frame_salt, text="-", width=1).grid(row=0, column=6, padx=2)

            ToRange = customtkinter.CTkEntry(master=frame_salt, width=50)
            ToRange.grid(row=0, column=7, padx=5)

        PositionLabel = customtkinter.CTkLabel(master=frame_salt, text="position: ", width=60)
        PositionLabel.grid(row=0, column=8)

        Position = customtkinter.CTkEntry(master=frame_salt, width=40)
        Position.grid(row=0, column=9)

        # update row variable for compounds
        self.dict_compounds[self.irow] = frame_salt
        self.irow = self.irow + 1

    def addprecipitate(self, include_range=False):
        irow = self.irow
        frame_precipitate = customtkinter.CTkFrame(master=self.frame_Compounds_input)
        frame_precipitate.grid(row=irow, column=0, columnspan=5)

        Label = customtkinter.CTkLabel(master=frame_precipitate, text="label precipitate: ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_precipitate)
        CompoundLabel.grid(row=0, column=1)

        Stock = customtkinter.CTkLabel(master=frame_precipitate, text="conc (" + self.units.get("precipitate") + "): ",
                                       width=70)
        Stock.grid(row=0, column=2, padx=5)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_precipitate, width=50)
        CompoundStock.grid(row=0, column=3)

        if include_range == True:
            Gradient = customtkinter.CTkLabel(master=frame_precipitate, text="range:", width=50, anchor="e")
            Gradient.grid(row=0, column=4)

            FromRange = customtkinter.CTkEntry(master=frame_precipitate, width=50)
            FromRange.grid(row=0, column=5, padx=5)

            customtkinter.CTkLabel(master=frame_precipitate, text="-", width=1).grid(row=0, column=6, padx=2)

            ToRange = customtkinter.CTkEntry(master=frame_precipitate, width=50)
            ToRange.grid(row=0, column=7, padx=5)

        PositionLabel = customtkinter.CTkLabel(master=frame_precipitate, text="position: ", width=60)
        PositionLabel.grid(row=0, column=8)

        Position = customtkinter.CTkEntry(master=frame_precipitate, width=40)
        Position.grid(row=0, column=9)

        # update row variable for compounds
        self.dict_compounds[self.irow] = frame_precipitate
        self.irow = self.irow + 1

    def addbuffer(self, include_range=False):
        irow = self.irow
        frame_buffer = customtkinter.CTkFrame(master=self.frame_Compounds_input)
        frame_buffer.grid(row=irow, column=0, columnspan=3)

        Label = customtkinter.CTkLabel(master=frame_buffer, text="label buffer: ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_buffer)
        CompoundLabel.grid(row=0, column=1)

        Stock = customtkinter.CTkLabel(master=frame_buffer, text="conc (" + self.units.get("salt") + "): ", width=70)
        Stock.grid(row=0, column=2, padx=5)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_buffer, width=50)
        CompoundStock.grid(row=0, column=3)

        if include_range == True:
            Gradient = customtkinter.CTkLabel(master=frame_buffer, text="range:", width=50, anchor="e")
            Gradient.grid(row=0, column=4)

            FromRange = customtkinter.CTkEntry(master=frame_buffer, width=50)
            FromRange.grid(row=0, column=5, padx=5)

            customtkinter.CTkLabel(master=frame_buffer, text="-", width=1).grid(row=0, column=6, padx=2)

            ToRange = customtkinter.CTkEntry(master=frame_buffer, width=50)
            ToRange.grid(row=0, column=7, padx=5)

        PositionLabel = customtkinter.CTkLabel(master=frame_buffer, text="position: ", width=60)
        PositionLabel.grid(row=0, column=8)

        Position = customtkinter.CTkEntry(master=frame_buffer, width=40)
        ##TODO add color of original insert in grey to make distinction
        Position.grid(row=0, column=9)

        # update row variable for compounds
        self.dict_compounds[self.irow] = frame_buffer
        self.irow = self.irow + 1


class ControlFrame(customtkinter.CTkFrame):

    def removePipet(self):
        Lst = self.frame_left_pipet.grid_slaves(row=2)
        for l in Lst:
            l.destroy()
        self.AddPipetButton.grid()
        self.hasTwoPipets = False

    def addPipet(self):
        self.AddPipet2 = customtkinter.CTkEntry(master=self.frame_left_pipet)
        self.AddPipet2.grid(row=2, column=1, sticky="nsew")

        self.optionmenu_pip2 = customtkinter.CTkOptionMenu(master=self.frame_left_pipet,
                                                           values=["left", "right"], width=80)
        self.optionmenu_pip2.grid(row=2, column=2, padx=10, sticky="nsew")

        self.RemovePipetButton = customtkinter.CTkButton(master=self.frame_left_pipet,
                                                         text="remove", width=20, command=self.removePipet)
        self.RemovePipetButton.grid(row=2, column=4)

        self.AddPipetButton.grid_remove()
        self.hasTwoPipets = True

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.hasTwoPipets = False
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid(row=0, column=0, sticky="nsew")

        self.selected_value = customtkinter.StringVar()

        # setup for if two pipets available: force on left then other right (not implemented yet)
        self.selected_side_pipet = customtkinter.StringVar()

        self.frame_left = customtkinter.CTkFrame(master=self, width=390)
        self.frame_left.grid_propagate(False)

        self.frame_left.grid(row=0, column=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame_left.grid_rowconfigure(0, minsize=5)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        ##ADDED
        self.frame_left_pipet = customtkinter.CTkFrame(master=self.frame_left)
        self.frame_left_pipet.grid(column=0, row=1)
        self.AddPipetLabel = customtkinter.CTkLabel(master=self.frame_left_pipet, text="Add pipet: ", width=30)
        self.AddPipetLabel.grid(row=0, column=0, padx=10, sticky="nsew")

        self.AddPipet = customtkinter.CTkEntry(master=self.frame_left_pipet)
        self.AddPipet.grid(row=0, column=1, sticky="nsew")

        self.optionmenu_pip = customtkinter.CTkOptionMenu(master=self.frame_left_pipet,
                                                          values=["left", "right"], variable=self.selected_side_pipet,
                                                          width=80)
        self.optionmenu_pip.grid(row=0, column=2, padx=10, sticky="nsew")
        self.optionmenu_pip.grid_propagate(False)

        self.AddPipetButton = customtkinter.CTkButton(master=self.frame_left_pipet, text="Add...",
                                                      command=self.addPipet, width=30)
        self.AddPipetButton.grid(row=0, column=4)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20)

        self.frame_right.rowconfigure(0, weight=10)
        self.frame_right.rowconfigure(1, weight=0)
        self.frame_right.columnconfigure(0, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self.frame_right, width=400, height=480)
        self.frame_top.grid_propagate(False)
        self.frame_top.grid(row=0, column=0)

        self.frame_bottom = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_bottom.grid(row=1, column=0, sticky="nsew", pady=10)

        self.frame_top.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_top.columnconfigure((0, 1, 2), weight=1)

        self.image_button1 = PhotoImage(file='images/1.png')
        self.image_button2 = PhotoImage(file='images/2.png')
        self.image_button3 = PhotoImage(file='images/3.png')
        self.image_button4 = PhotoImage(file='images/4.png')
        self.image_button5 = PhotoImage(file='images/5.png')
        self.image_button6 = PhotoImage(file='images/6.png')
        self.image_button7 = PhotoImage(file='images/7.png')
        self.image_button8 = PhotoImage(file='images/8.png')
        self.image_button9 = PhotoImage(file='images/9.png')
        self.image_button10 = PhotoImage(file='images/10.PNG')
        self.image_button11 = PhotoImage(file='images/11.png')
        self.image_buttontrash = PhotoImage(file='images/trashbin.png')

        self.button1 = Button(master=self.frame_top,
                              image=self.image_button1,
                              command=lambda *args: button_event(self, 1),
                              borderwidth=0)
        self.button2 = Button(master=self.frame_top,
                              image=self.image_button2,
                              command=lambda *args: button_event(self, 2),
                              borderwidth=0)
        self.button3 = Button(master=self.frame_top,
                              image=self.image_button3,
                              command=lambda *args: button_event(self, 3),
                              borderwidth=0)
        self.button4 = Button(master=self.frame_top,
                              image=self.image_button4,
                              command=lambda *args: button_event(self, 4),
                              borderwidth=0)
        self.button5 = Button(master=self.frame_top,
                              image=self.image_button5,
                              command=lambda *args: button_event(self, 5),
                              borderwidth=0)
        self.button6 = Button(master=self.frame_top,
                              image=self.image_button6,
                              command=lambda *args: button_event(self, 6),
                              borderwidth=0)
        self.button7 = Button(master=self.frame_top,
                              image=self.image_button7,
                              command=lambda *args: button_event(self, 7),
                              borderwidth=0)
        self.button8 = Button(master=self.frame_top,
                              image=self.image_button8,
                              command=lambda *args: button_event(self, 8),
                              borderwidth=0)
        self.button9 = Button(master=self.frame_top,
                              image=self.image_button9,
                              command=lambda *args: button_event(self, 9),
                              borderwidth=0)
        self.button10 = Button(master=self.frame_top,
                               image=self.image_button10,
                               command=lambda *args: button_event(self, 10),
                               borderwidth=0)
        self.button11 = Button(master=self.frame_top,
                               image=self.image_button11,
                               command=lambda *args: button_event(self, 11),
                               borderwidth=0)
        self.button12 = Label(master=self.frame_top,
                              image=self.image_buttontrash,
                              borderwidth=0)

        self.button1.grid(row=3, column=0, pady=2, padx=2, sticky="nsew")
        self.button2.grid(row=3, column=1, pady=2, padx=2, sticky="nsew")
        self.button3.grid(row=3, column=2, pady=2, padx=2, sticky="nsew")
        self.button4.grid(row=2, column=0, pady=2, padx=2, sticky="nsew")
        self.button5.grid(row=2, column=1, pady=2, padx=2, sticky="nsew")
        self.button6.grid(row=2, column=2, pady=2, padx=2, sticky="nsew")
        self.button7.grid(row=1, column=0, pady=2, padx=2, sticky="nsew")
        self.button8.grid(row=1, column=1, pady=2, padx=2, sticky="nsew")
        self.button9.grid(row=1, column=2, pady=2, padx=2, sticky="nsew")
        self.button10.grid(row=0, column=0, pady=2, padx=2, sticky="nsew")
        self.button11.grid(row=0, column=1, pady=2, padx=2, sticky="nsew")
        self.button12.grid(row=0, column=2, pady=2, padx=2, sticky="nsew")

        self.frame_bottom.columnconfigure(6, weight=1)
        self.frame_bottom.columnconfigure(7, weight=1)

        self.button13 = customtkinter.CTkButton(master=self.frame_bottom,
                                                text="Generate Protocol",
                                                command=self.generate_protocol)
        self.button13.grid(column=7, row=0, padx=1, pady=2, sticky="we")

        self.button14 = customtkinter.CTkButton(master=self.frame_bottom,
                                                text="Simulate Protocol",
                                                command=self.simulate_protocol)
        self.button14.grid(column=6, row=0, padx=1, pady=2, sticky="we")

        def button_event(self, index):
            # index not used for now in the application, will be important later
            if isinstance(self.frame_right, InputFrame):
                self.frame_right.destroy()  # else if mulitple buttons pressed, all frames will stack
            self.frame_right = InputFrame(self, parent, index)
            self.frame_right.tkraise()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def generate_protocol(self):
        # read all information in

        directory = os.path.join(self.parent.inputsPath)
        tips = ""
        tuberacks = ""
        instruments = ""
        plates = ""
        screens = ""
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file

            if os.path.isfile(f):
                with open(f, "r") as f:
                    type = f.readline().replace("\n", "")
                    if type == "Tube rack":
                        tuberacks += f.read()
                    elif type == "Tip rack":
                        tips += f.read()
                    elif type == "Well plate":
                        segments = f.read().split("\n\n")
                        plates += segments[0] + "\n"
                        screens += segments[1] + "\n"

        instruments += self.AddPipet.get() + "\n" + self.optionmenu_pip.get() + "\n"
        if self.hasTwoPipets == True:
            instruments += self.AddPipet2.get() + "\n" + self.optionmenu_pip2.get() + "\n"

        # The name of the parameterfile will be: projectname (gotten from first window) .param.txt
        paramFilename = os.path.basename(self.parent.UserPath) + ".param.txt"
        paramFilePath = os.path.join(self.parent.UserPath, paramFilename)
        # print("path", paramFilePath)
        with open(paramFilePath, "w+") as f:
            f.write(tips + "\n")
            # don't understand why not +"\n" after tuberacks, but it works TODO: figure out
            f.write(tuberacks)
            f.write(instruments + "\n")
            f.write(plates + "\n")
            f.write(screens)

        # TODO: how to connect to compound library:
        # TODO: maybe it would make more sence if tube rack is where positions of compunds are defined

        # generate the protocol
        # writeTemplate(paramFilePath)

    def simulate_protocol(self):
        pass


class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.input_dict = {key: None for key in range(1, 13)}  # added
        self.title("Protocol designer")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.UserPath = fd.askdirectory()

        # create the necessary folders:
        parent_dir = os.path.join(self.UserPath, "inputs")
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)
        self.inputsPath = parent_dir


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()