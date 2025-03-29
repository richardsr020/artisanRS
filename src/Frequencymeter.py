import tkinter as tk

class Frequencymeter:
    def __init__(self, master):
        self.master = master

    def display(self):
        label = tk.Label(self.master, text="Fréquentimètre - Analyse", font=("Arial", 20))
        label.pack(pady=20)

        # Affichage de la fréquence mesurée
        meter_frame = tk.Frame(self.master)
        meter_frame.pack(pady=50)

        frequency_label = tk.Label(meter_frame, text="Fréquence mesurée : 50 Hz")
        frequency_label.pack()
