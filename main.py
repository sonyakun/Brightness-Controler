import base64
import tkinter as tk
from tkinter import messagebox
import math
import sys
import traceback
import os

import customtkinter
import screen_brightness_control as sbc
from pystray import Icon,Menu,MenuItem
from PIL import Image

img_base64 = ""

class srprocess:
    def __init__(self, image):
        self.status = False
        self.image = base64.b64decode(img_base64)
        self.menu = Menu(
            MenuItem('Show UI', self.stopProgram),
            MenuItem('Exit Brightness Controler', self.exit),   
        )

    def stopProgram(self, icon):
        self.icon.stop()
        app.deiconify()

    def exit(self):
        self.icon.stop()
        app.destroy()
        try:
            sys.exit()
        except SystemExit:
            pass

    def runProgram(self):
        try:
            self.icon = Icon(name='Brightness Controler', title='titleTray', icon=self.image, menu=self.menu)
            self.icon.run()
        except WindowsError:
            app.deiconify()
            messagebox.showerror("ERROR!", f"{traceback.format_exc()}")

class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Brightness Controler")

        br = sbc.get_brightness(display=0)[0]
        self.label = customtkinter.CTkLabel(self, text=f"{br}%", fg_color="transparent")
        self.brightness_count = tk.DoubleVar()
        Brightness = customtkinter.CTkSlider(
            self,
            variable=self.brightness_count,
            command=self.slider_scroll,
            from_=0,
            to=100,
            orientation="vertical",
        )
        Brightness.pack()
        Brightness.set(br)
        self.label.pack()

    def slider_scroll(self, event=None):
        br = math.floor(self.brightness_count.get())
        self.label.configure(text=f"{str(br)}%")
        sbc.set_brightness(br)


def hide_window():
    app.withdraw()
    bprc.runProgram()

if __name__ == "__main__":
    if os.name == 'nt':
        bprc = srprocess("assets/icon.png")
        app = Application()
        app.protocol("WM_DELETE_WINDOW", hide_window)
        customtkinter.set_appearance_mode("system")
        app.mainloop()
    else:
        messagebox.showerror("UNSUPPORTED_PLATFORM", "Application is Supported Only Windows, Sorry!")