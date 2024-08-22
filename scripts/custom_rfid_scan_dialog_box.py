from typing import Union, Tuple, Optional

from customtkinter.windows.widgets import CTkLabel
from customtkinter.windows.widgets import CTkEntry
from customtkinter.windows.widgets import CTkButton
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets.font import CTkFont

import customtkinter
import tkinter
import serial
import time
import sys
import threading


class RFIDScannerDialog(CTkToplevel):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 title: str = "CTkDialog",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 text: str = "CTkDialog"):

        super().__init__(fg_color=fg_color)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else self._check_color_type(button_hover_color)
        #self._button_fg_color = ThemeManager.theme["CTkButton"]["fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        #self._button_hover_color = ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        #self._button_text_color = ThemeManager.theme["CTkButton"]["text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        #self._entry_fg_color = ThemeManager.theme["CTkEntry"]["fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        #self._entry_border_color = ThemeManager.theme["CTkEntry"]["border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        #self._entry_text_color = ThemeManager.theme["CTkEntry"]["text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self.data=''
        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top

        self.protocol("WM_DELETE_WINDOW", self._dummy_close)
        self.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.after(4000, self._on_closing)
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable
        try:
            self.serial_port=serial.Serial(port="COM6",baudrate=9600,timeout=1)

        except Exception as e:
            tkinter.messagebox.showerror(title="RFID dialogue ERROR", message=e)
            self._label.configure(text='ERROR \nCLOSING THE WINDOW')
            #self._on_closing()

        #print(self.serial_port)    
        self.after(20, self._scan_event)
        #self.mainloop()

    def _dummy_close(self):
        pass
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._label = CTkLabel(master=self,
                               width=300,
                               wraplength=300,
                               fg_color="transparent",
                               text_color=self._text_color,
                               text=self._text,
                               font=self._font)
        self._label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        #self.after(150, lambda: self._entry.focus())  # set focus to entry with slight delay, otherwise it won't work
    def _scan_event(self):        
        try:
            temp=str(self.serial_port.readline())
            temp=str(self.serial_port.readline())
            temp=''.join([i for i in temp if i.isdigit()])
            if temp!='' and temp!=' ':
                print(temp)
                self.data=temp
                self._label.configure(text='SCAN COMPLETE \nCLOSING THE WINDOW')
                #self._on_closing()
                #self.after(1, self._scan_event)    
        except Exception as e:
            print(e)   
        

    def _on_closing(self):
        try:
            self.serial_port.close()
        except:
            pass
        self.grab_release()
        self.destroy()
        return 
        #sys.exit()

    def get_input(self):
        self.master.wait_window(self)
        return self.data    

def front_endL(text='text', title='Title'):
    RFIDScannerDialog(text=text,title=title)

def serial_listener():
    try:
        serial_port=serial.Serial(port="COM6",baudrate=9600)
        temp=str(serial_port.readline())
        temp=str(serial_port.readline())
        temp=''.join([i for i in temp if i.isdigit()])
        if temp!='' and temp!=' ':
            print(temp)
    except:
        pass        

if __name__=='__main__':  
    c=RFIDScannerDialog(text='SCANNING....')