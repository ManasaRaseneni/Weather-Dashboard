import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from weather_api import WeatherAPI
from data_handler import load_favorites, save_favorites

class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")

        self.api = WeatherAPI()

        self.city_var = tk.StringVar()
        self.favorites = load_favorites()

        self.weather_label = tk.Label(self.root, text="", justify="left")
        self.fav_listbox = tk.Listbox(self.root)
        self.figure = plt.Figure(figsize=(5,4), dpi=100)
        self.chart = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)

        self.create_widgets()
        self.update_favorites()

    def create_widgets(self):
        tk.Label(self.root, text="city:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.city_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Check the Weather", command=self.show_weather).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Add to Favorites", command=self.add_favorite).grid(row=0, column=3, padx=5, pady=5)

        self.weather_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        tk.Label(self.root, text="Favorites:").grid(row=2, column=0, padx=5, pady=5)
        self.fav_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=4)
        self.fav_listbox.bind("<<ListboxSelect>>", self.select_favorite)

        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=4, padx=5, pady=5)

    def show_weather(self):
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("Warning", "Enter a city name")
            return

        current = self.api.get_current_weather(city)
        forecast = self.api.get_forecast(city)

        if current:
            weather_text = (
                f"City: {current['name']}\n"
                f"Temperature: {current['main']['temp']}°C\n"
                f"Weather: {current['weather'][0]['description']}"
            )
            self.weather_label.config(text=weather_text)
        else:
            self.weather_label.config(text="Current weather data not available.")

        if forecast and 'list' in forecast:
            self.plot_forecast(forecast)
        else:
            messagebox.showerror("Error", "Forecast data not available")

    def plot_forecast(self, forecast):
        temps = [f['main']['temp'] for f in forecast['list'][:6]]
        times = [f['dt_txt'].split(" ")[1] for f in forecast['list'][:6]]

        self.chart.clear()
        self.chart.plot(times, temps, marker='o')
        self.chart.set_title("Temperature Forecast")
        self.chart.set_ylabel("°C")
        self.chart.set_xlabel("Time")
        self.canvas.draw()

    def add_favorite(self):
        city = self.city_var.get()
        if city and city not in self.favorites:
            self.favorites.append(city)
            save_favorites(self.favorites)
            self.update_favorites()

    def update_favorites(self):
        self.fav_listbox.delete(0, tk.END)
        for city in self.favorites:
            self.fav_listbox.insert(tk.END, city)

    def select_favorite(self, _):
        selection = self.fav_listbox.curselection()
        if selection:
            city = self.fav_listbox.get(selection[0])
            self.city_var.set(city)
            self.show_weather()



