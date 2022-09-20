from time import sleep
from pynput.keyboard import GlobalHotKeys
from pynput.mouse import Controller, Button
from threading import Thread
from tkinter import Tk, Label, Entry

class MainWindow:
    def __init__(self) -> None:
        #main window
        self.root = Tk()

        #window ui
        self.root.geometry("400x100")
        self.root.title("Auto Clicker")

        #states
        self.status_text = "NOT RUNNING"
        self.is_clicking = False
        self.is_program_closed = False
        self.click_interval = 1

        #click thread
        self.clicker_thread = Thread(target=self.handle_click)

        #main window close event
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        #mouse click controller
        self.mouse_controller = Controller()
        
        #hotkey listener
        self.listener = GlobalHotKeys({
            '<ctrl>+<alt>+1': self.toggle_click_status
        })

        self.initialize_ui()
        self.initialize_listeners()

    def initialize_listeners(self):
        self.listener.start()
        self.clicker_thread.start()
        self.root.mainloop()
        self.listener.join()
    
    def initialize_ui(self):
        #interval
        Label(self.root, text="Interval (ms): ", width=10).place(x=0, y=0)
        self.interval_entry = Entry(self.root, width=25)
        self.interval_entry.place(x=80, y=0)
        self.interval_entry.insert(0, "1000")

        #status
        self.status_label = Label(self.root, text="Status: NOT RUNNING")
        self.status_label.place(x=0, y=20)

        #guide
        Label(self.root, text="TOGGLE AUTO CLICKER: <ctrl>+<alt>+1").place(x=0, y=40)

        #info
        Label(self.root, text="If intveral input is empty, it will default to 1000ms")
    
    def toggle_click_status(self):
        input_interval = self.interval_entry.get()

        if input_interval == "":
            input_interval = "1000"
            self.interval_entry.insert(0, input_interval)
        
        self.click_interval = int(input_interval) / 1000

        if self.is_clicking:
            self.is_clicking = False
            self.status_text = "NOT RUNNING"
        else:
            self.is_clicking = True
            self.status_text = "RUNNING"
        
        self.status_label.config(text="Status: " + self.status_text)
    
    def handle_click(self):
        while not self.is_program_closed:
            if self.is_clicking:
                self.mouse_controller.click(Button.left, 1)
            sleep(self.click_interval)
    
    def close_app(self):
        self.is_program_closed = True
        self.listener.stop()
        self.root.destroy()

clicker = MainWindow()