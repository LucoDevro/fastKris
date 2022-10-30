import tkinter
from tkinter import *
import customtkinter
from tkinter.font import BOLD

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class InputFrame(customtkinter.CTkFrame):
    def __init__(self, control, parent, index):
        super().__init__(parent)
        self.index = index
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_up = customtkinter.CTkFrame(master=self)
        self.frame_up.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.frame_up.columnconfigure((0, 1), weight=1)
        self.frame_up.grid(row=0, column=0, sticky="nsew")

        self.frame_compounds = customtkinter.CTkFrame(master=self.frame_up, width=680)
        self.frame_compounds.grid(row=3, column=0, columnspan=2, sticky="ns")
        self.frame_compounds.grid_propagate(False)

        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.columnconfigure(0, weight=1, uniform="")
        self.frame_down.grid(row=2, column=0, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="name plate: ").grid(row=0, column=0, sticky="W")

        self.PlateLabel = customtkinter.CTkEntry(master=self.frame_up)
        self.PlateLabel.grid(row=0, column=1, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="add to plate:").grid(row=1, column=0, sticky="W")
        self.PlateOptionMenu = customtkinter.CTkOptionMenu(master=self.frame_up,
                                                           values=["Reservoir", "Tip rack", "Well plate"])
        self.PlateOptionMenu.grid(row=1, column=1, sticky="nsew")

        # set fixed for now, font family can be obtained dynamically (not implemented yet)
        self.CompoundsLabel = customtkinter.CTkLabel(master=self.frame_compounds, text="Compounds",
                                                     text_font=('Segoe UI', 10, BOLD))
        self.CompoundsLabel.grid(row=2, column=0, sticky="nw")
        self.CompoundsLabel.grid_propagate(False)

        self.frame_compounds.rowconfigure(2, minsize=5)  # empty row with minsize as spacing)
        self.irow = 3
        self.dict_compounds = {}

        # width = 215 prevents the Buttons from shifting to the right when pressed
        self.AddSalt = customtkinter.CTkButton(master=self.frame_compounds, text="Add salt", command=self.addsalt,
                                               width=215)
        self.AddSalt.grid(row=3, column=0, padx=5, sticky="nw")
        self.AddSalt.grid_propagate(False)
        self.AddBuffer = customtkinter.CTkButton(master=self.frame_compounds, text="Add buffer", command=self.addbuffer,
                                                 width=215)
        self.AddBuffer.grid(row=3, column=1, padx=5, sticky="nw")
        self.AddBuffer.grid_propagate(False)
        self.AddPrecipitate = customtkinter.CTkButton(master=self.frame_compounds, text="Add Precipitate",
                                                      command=self.addprecipitate, width=215)
        self.AddPrecipitate.grid(row=3, column=2, padx=5, sticky="nw")
        self.AddPrecipitate.grid_propagate(False)

        self.buttonApply = customtkinter.CTkButton(master=self.frame_down, text="Apply", command=self.button_event)
        self.buttonApply.grid(column=0, row=3)
        # change to row = 1, column = 0 to let it appear on the bottom instead of the right
        self.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def button_event(self):
        # removes frame
        self.destroy()

    def addsalt(self):
        irow = self.irow
        frame_salt = customtkinter.CTkFrame(master=self.frame_compounds)
        frame_salt.grid(row=irow, column=0, columnspan=3)

        Label = customtkinter.CTkLabel(master=frame_salt, text="label salt: ", width=100)
        Label.grid(row=0, column=0, padx=5)
        Label.grid_propagate(False)

        CompoundLabel = customtkinter.CTkEntry(master=frame_salt)
        CompoundLabel.grid(row=0, column=1)

        Stock = customtkinter.CTkLabel(master=frame_salt, text="conc (M): ", width=70)
        Stock.grid(row=0, column=2, padx=5)
        Stock.grid_propagate(False)

        CompoundStock = customtkinter.CTkEntry(master=frame_salt)
        CompoundStock.grid(row=0, column=3)

        Gradient = customtkinter.CTkCheckBox(master=frame_salt, text="range")
        Gradient.grid(row=0, column=4)

        FromRange = customtkinter.CTkEntry(master=frame_salt, width=50)
        FromRange.grid(row=0, column=5, padx=5)

        customtkinter.CTkLabel(master=frame_salt, text="-", width=1).grid(row=0, column=6, padx=5)

        ToRange = customtkinter.CTkEntry(master=frame_salt, width=50)
        ToRange.grid(row=0, column=7, padx=5)

        # update row variable for compounds
        self.irow = self.irow + 1
        self.dict_compounds[self.irow] = frame_salt

    def addprecipitate(self):
        irow = self.irow
        frame_precipitate = customtkinter.CTkFrame(master=self.frame_compounds)
        frame_precipitate.grid(row=irow, column=0, columnspan=3)

        self.Label = customtkinter.CTkLabel(master=frame_precipitate, text="label precipitate: ", width=100)
        self.Label.grid(row=0, column=0, padx=5)
        self.Label.grid_propagate(False)

        self.CompoundLabel = customtkinter.CTkEntry(master=frame_precipitate)
        self.CompoundLabel.grid(row=0, column=1)

        self.Stock = customtkinter.CTkLabel(master=frame_precipitate, text="conc (m%): ", width=70)
        self.Stock.grid(row=0, column=2, padx=5)
        self.Stock.grid_propagate(False)

        self.CompoundStock = customtkinter.CTkEntry(master=frame_precipitate)
        self.CompoundStock.grid(row=0, column=3)

        Gradient = customtkinter.CTkCheckBox(master=frame_precipitate, text="range")
        Gradient.grid(row=0, column=4)

        FromRange = customtkinter.CTkEntry(master=frame_precipitate, width=50)
        FromRange.grid(row=0, column=5, padx=5)

        customtkinter.CTkLabel(master=frame_precipitate, text="-", width=1).grid(row=0, column=6, padx=5)

        ToRange = customtkinter.CTkEntry(master=frame_precipitate, width=50)
        ToRange.grid(row=0, column=7, padx=5)

        # update row variable for compounds
        self.irow = self.irow + 1
        self.dict_compounds[self.irow] = frame_precipitate

    def addbuffer(self):
        irow = self.irow
        frame_buffer = customtkinter.CTkFrame(master=self.frame_compounds)
        frame_buffer.grid(row=irow, column=0, columnspan=3)

        self.Label = customtkinter.CTkLabel(master=frame_buffer, text="label buffer: ", width=100)
        self.Label.grid(row=0, column=0, padx=5)
        self.Label.grid_propagate(False)

        self.CompoundLabel = customtkinter.CTkEntry(master=frame_buffer)
        self.CompoundLabel.grid(row=0, column=1)

        self.Stock = customtkinter.CTkLabel(master=frame_buffer, text="conc (pH): ", width=70)
        self.Stock.grid(row=0, column=2, padx=5)
        self.Stock.grid_propagate(False)

        self.CompoundStock = customtkinter.CTkEntry(master=frame_buffer)
        self.CompoundStock.grid(row=0, column=3)

        Gradient = customtkinter.CTkCheckBox(master=frame_buffer, text="range")
        Gradient.grid(row=0, column=4)

        FromRange = customtkinter.CTkEntry(master=frame_buffer, width=50)
        FromRange.grid(row=0, column=5, padx=5)

        customtkinter.CTkLabel(master=frame_buffer, text="-", width=1).grid(row=0, column=6, padx=5)

        ToRange = customtkinter.CTkEntry(master=frame_buffer, width=50)
        ToRange.grid(row=0, column=7, padx=5)

        # update row variable for compounds
        self.irow = self.irow + 1
        self.dict_compounds[self.irow] = frame_buffer


class ControlFrame(customtkinter.CTkFrame):

    def removePipet(self):
        Lst = self.frame_left_pipet.grid_slaves(row=2)
        for l in Lst:
            l.destroy()
        self.AddPipetButton.grid()

    def addPipet(self):
        self.AddPipet2 = customtkinter.CTkEntry(master=self.frame_left_pipet)
        self.AddPipet2.grid(row=2, column=1, sticky="nsew")

        self.optionmenu_pip2 = customtkinter.CTkOptionMenu(master=self.frame_left_pipet,
                                                           values=["Left", "Right"], width=80)
        self.optionmenu_pip2.grid(row=2, column=2, padx=10, sticky="nsew")

        self.RemovePipetButton = customtkinter.CTkButton(master=self.frame_left_pipet,
                                                         text="remove", width=20, command=self.removePipet)
        self.RemovePipetButton.grid(row=2, column=4)

        self.AddPipetButton.grid_remove()

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid(row=0, column=0, sticky="nsew")

        self.selected_value = customtkinter.StringVar()

        # setup for if two pipets available: force on Left then other Right (not implemented yet)
        self.selected_side_pipet = customtkinter.StringVar()

        # previously = 180
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
                                                          values=["Left", "Right"], variable=self.selected_side_pipet,
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
        self.button12 = Button(master=self.frame_top,
                               image=self.image_buttontrash,
                               command=lambda *args: button_event(self, 12),
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
                # read all information to a file, to remember input (not implemented yet)
                self.frame_right.destroy()  # else if mulitple buttons pressed, all frames will stack
            self.frame_right = InputFrame(self, parent, index)
            self.frame_right.tkraise()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def generate_protocol(self):
        pass

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


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
