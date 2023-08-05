import tkinter as tk
from tkinter import ttk

from transvenous_pacing_gui.guiclient import InstructorGUI
from transvenous_pacing_gui.guiserver import StudentGUI

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        s = ttk.Style()
        s.configure('new.TFrame', background='black')

        # GUI design
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.bind("<Button-1>", self.on_click)

        # Student GUI design
        self.student_gui = StudentGUI(self.notebook, style='new.TFrame')

        # Teacher GUI design
        self.instructor_gui = InstructorGUI(self.notebook)

        # Building the notebook
        self.notebook.add(self.student_gui, text="Student")
        self.notebook.add(self.instructor_gui, text="Instructor")
        self.notebook.pack()

    def on_click(self, event):
        # Tcl function to determine tab at position
        clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        active_tab = self.notebook.index(self.notebook.select())
        
        # If switching tabs
        if not clicked_tab == active_tab:
            if clicked_tab == 0:
                self.student_gui.start_plot()
            elif clicked_tab == 1:
                self.student_gui.pause_plot()
            else:
                pass

    def stop_gui(self):
        self.instructor_gui.stop_gui()
        self.student_gui.stop_gui()

def main():
    root = tk.Tk()
    root.title("Tranvenous Pacing GUI")

    main_app = MainApplication(root)
    main_app.pack(side="top", fill="both", expand=True)

    root.mainloop()

    main_app.stop_gui()

if __name__ == "__main__":
    main()
