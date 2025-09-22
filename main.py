import tkinter as tk
from gui import WeatherGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherGUI(root)
    root.mainloop()
