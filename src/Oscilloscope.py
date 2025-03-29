import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class OscFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.simulate_data()

    def create_widgets(self):
        """Creates the widgets for the oscilloscope frame"""
        # Main container
        self.osc_frame = tk.Frame(self)
        self.osc_frame.pack(fill=tk.BOTH, expand=True)

        # Matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.osc_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Control panel
        self.control_frame = tk.Frame(self.osc_frame)
        self.control_frame.pack(fill=tk.X)

        self.gain_scale = tk.Scale(self.control_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                   label="Gain", command=self.update_plot)
        self.gain_scale.pack(side=tk.LEFT)

        self.acquire_button = tk.Button(self.control_frame, text="Acquérir", 
                                        command=self.simulate_data)
        self.acquire_button.pack(side=tk.RIGHT)

    def simulate_data(self):
        """Simulates oscilloscope data (to be replaced with real hardware)"""
        t = np.linspace(0, 1, 1000)
        self.y = np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(1000)
        self.x = t
        self.update_plot()

    def update_plot(self, *args):
        """Updates the plot"""
        gain = float(self.gain_scale.get())
        self.ax.clear()
        self.ax.plot(self.x, gain * self.y)
        self.ax.set_xlabel('Temps (s)')
        self.ax.set_ylabel('Tension (V)')
        self.ax.set_title(f'Oscilloscope (Gain: {gain}x)')
        self.ax.grid(True)
        self.canvas.draw()

    def pack(self, **kwargs):
        """Override pack to apply to the main frame"""
        self.osc_frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Override grid to apply to the main frame"""
        self.osc_frame.grid(**kwargs)

    def place(self, **kwargs):
        """Override place to apply to the main frame"""
        self.osc_frame.place(**kwargs)