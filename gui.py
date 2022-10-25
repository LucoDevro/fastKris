from tkinter import *
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Dark")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Protocol designer")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Make tray:",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Create",
                                                command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Reproduce",
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Optimize",
                                                command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_central = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_central.grid(row=0, column=0, columnspan=4, rowspan=3, pady=20, padx=20)

        # ============ frame_central ============

        # configure grid layout (4x3)
        self.frame_central.rowconfigure(3, weight=1)
        self.frame_central.columnconfigure(2, weight=1)

        self.button1 = customtkinter.CTkButton(master=self.frame_central,
                                              text="1",
                                              command=self.button_event)
        self.button2 = customtkinter.CTkButton(master=self.frame_central,
                                               text="2",
                                               command=self.button_event)
        self.button3 = customtkinter.CTkButton(master=self.frame_central,
                                               text="3",
                                               command=self.button_event)
        self.button4 = customtkinter.CTkButton(master=self.frame_central,
                                               text="4",
                                               command=self.button_event)
        self.button5 = customtkinter.CTkButton(master=self.frame_central,
                                               text="5",
                                               command=self.button_event)
        self.button6 = customtkinter.CTkButton(master=self.frame_central,
                                               text="6",
                                               command=self.button_event)
        self.button7 = customtkinter.CTkButton(master=self.frame_central,
                                               text="7",
                                               command=self.button_event)
        self.button8 = customtkinter.CTkButton(master=self.frame_central,
                                               text="8",
                                               command=self.button_event)
        self.button9 = customtkinter.CTkButton(master=self.frame_central,
                                               text="9",
                                               command=self.button_event)
        self.button10 = customtkinter.CTkButton(master=self.frame_central,
                                               text="10",
                                               command=self.button_event)
        self.button11 = customtkinter.CTkButton(master=self.frame_central,
                                               text="11",
                                               command=self.button_event)
        self.button12 = customtkinter.CTkButton(master=self.frame_central,
                                                text="12",
                                                command=self.button_event)
        self.button1.grid(row=3, column=0, pady=0, padx=0)
        self.button2.grid(row=3, column=1, pady=0, padx=0)
        self.button3.grid(row=3, column=2, pady=0, padx=0)
        self.button4.grid(row=2, column=0, pady=0, padx=0)
        self.button5.grid(row=2, column=1, pady=0, padx=0)
        self.button6.grid(row=2, column=2, pady=0, padx=0)
        self.button7.grid(row=1, column=0, pady=0, padx=0)
        self.button8.grid(row=1, column=1, pady=0, padx=0)
        self.button9.grid(row=1, column=2, pady=0, padx=0)
        self.button10.grid(row=0, column=0, pady=0, padx=0)
        self.button11.grid(row=0, column=1, pady=0, padx=0)
        self.button12.grid(row=0, column=2, pady=0, padx=0)

        # ============ frame_right ============

        self.button13 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Generate Protocol",
                                                command=self.button_event)
        self.button13.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")


    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()