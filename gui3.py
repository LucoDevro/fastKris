import tkinter
from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, control, parent, index):
        super().__init__(parent)
        self.index = index
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #still working on
        self.frame_up = customtkinter.CTkFrame(master = self)
        self.frame_up.columnconfigure((0,1,2,3,4,5), weight = 1)
        self.frame_up.columnconfigure((0,1), weight = 1)
        self.frame_up.grid(row=0, column=0, sticky="nsew")

        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.columnconfigure(0, weight = 1, uniform = "")
        self.frame_down.grid(row=1, column=0, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="name plate: ").grid(row=0, column=0, sticky="E")

        self.PlateLabel = customtkinter.CTkEntry(master= self.frame_up)
        self.PlateLabel.grid(row=0, column=1)

        customtkinter.CTkLabel(master = self.frame_up, text = "Range: " + "\t" + "from").grid(row=1, column=0, sticky="E")

        self.EntryRangeMin = customtkinter.CTkEntry(master = self.frame_up)
        self.EntryRangeMin.grid(row=1, column=1, sticky="nsew")

        customtkinter.CTkLabel(master=self.frame_up, text="to").grid(row=1, column=2)

        self.EntryRangeMax = customtkinter.CTkEntry(master=self.frame_up)
        self.EntryRangeMax.grid(row=1, column=3, sticky="nsew")

        self.buttonApply = customtkinter.CTkButton(master=self.frame_down, text="Apply", command = self.button_event)
        self.buttonApply.grid(column=0, row=2)
        self.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

    def button_event(self):
       #removes frame
       self.destroy()

class ControlFrame(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid(row = 0, column = 0, sticky = "nsew")

        self.selected_value = customtkinter.StringVar()

        self.frame_left = customtkinter.CTkFrame(master=self, width = 180)

        self.frame_left.grid(row=0, column=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame_left.grid_rowconfigure(0, minsize=5)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Title",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)  # put in row 1 of frame_left

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.frame_right.rowconfigure(0, weight=10)
        self.frame_right.rowconfigure(1, weight=0)
        self.frame_right.columnconfigure(0, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_top.grid(row=0, column=0, sticky="nsew")

        self.frame_bottom = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_bottom.grid(row=1, column=0, sticky="nsew", pady=10)

        self.frame_top.rowconfigure(0, weight=1)
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_top.columnconfigure(1, weight=1)

        self.frame_topleft = customtkinter.CTkFrame(master=self.frame_top)
        self.frame_topleft.grid(row=0, column=0, sticky="nsew")

        self.frame_topleft.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_topleft.columnconfigure((0, 1, 2), weight=1)

        self.button1 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="1",
                                               command=lambda *args: button_event(self,1))
        self.button2 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="2",
                                               command=lambda *args: button_event(self,2))
        self.button3 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="3",
                                               command=lambda *args: button_event(self,3))
        self.button4 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="4",
                                               command=lambda *args: button_event(self,4))
        self.button5 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="5",
                                               command=lambda *args: button_event(self,5))
        self.button6 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="6",
                                               command=lambda *args: button_event(self,6))
        self.button7 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="7",
                                               command=lambda *args: button_event(self,7))
        self.button8 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="8",
                                               command=lambda *args: button_event(self,8))
        self.button9 = customtkinter.CTkButton(master=self.frame_topleft,
                                               text="9",
                                               command=lambda *args: button_event(self,9))
        self.button10 = customtkinter.CTkButton(master=self.frame_topleft,
                                                text="10",
                                                command=lambda *args: button_event(self,10))
        self.button11 = customtkinter.CTkButton(master=self.frame_topleft,
                                                text="11",
                                                command=lambda *args: button_event(self,11))
        self.button12 = customtkinter.CTkButton(master=self.frame_topleft,
                                                text="12",
                                                command=lambda *args: button_event(self,12))

        self.button1.grid(row=3, column=0, pady=0, padx=0, sticky="nsew")
        self.button2.grid(row=3, column=1, pady=0, padx=0, sticky="nsew")
        self.button3.grid(row=3, column=2, pady=0, padx=0, sticky="nsew")
        self.button4.grid(row=2, column=0, pady=0, padx=0, sticky="nsew")
        self.button5.grid(row=2, column=1, pady=0, padx=0, sticky="nsew")
        self.button6.grid(row=2, column=2, pady=0, padx=0, sticky="nsew")
        self.button7.grid(row=1, column=0, pady=0, padx=0, sticky="nsew")
        self.button8.grid(row=1, column=1, pady=0, padx=0, sticky="nsew")
        self.button9.grid(row=1, column=2, pady=0, padx=0, sticky="nsew")
        self.button10.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")
        self.button11.grid(row=0, column=1, pady=0, padx=0, sticky="nsew")
        self.button12.grid(row=0, column=2, pady=0, padx=0, sticky="nsew")

        self.frame_bottom.columnconfigure(7, weight=1)

        self.button13 = customtkinter.CTkButton(master=self.frame_bottom,
                                                text="Generate Protocol",
                                                command=self.generate_protocol)
        self.button13.grid(column=7, sticky="e")

        def button_event(self,index):
            #index not used for now in the application, will be important later
            self.frame_right = InputFrame(self,parent,index)
            self.frame_right.tkraise()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def generate_protocol(self):
        pass

class App(customtkinter.CTk):
    # change to depending size screen? xy
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.input_dict = {key: None for key in range(1, 13)}  # added
        self.title("Protocol designer")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()