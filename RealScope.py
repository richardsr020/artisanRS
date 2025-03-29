import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime
from PIL import ImageGrab

class SignalVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisation de Signaux Électriques")
        self.root.geometry("1400x900")
        self.root.configure(bg='#333333')
        
        # Initialisation des variables
        self.measurements_history = []
        self.osc_channels = 4  # Nombre total de canaux
        self.active_channels = [True, True, False, False]  # CH1 et CH2 activés par défaut
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Couleurs
        self.bg_color = '#333333'
        self.fg_color = '#FFFFFF'
        self.measure_bg = '#222222'
        self.channel_colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00']  # Rouge, Vert, Bleu, Jaune
        
        # Configuration des styles
        self.configure_styles()
        
        # Création des frames principales
        self.create_main_frames()
        
        # Configuration des composants
        self.setup_measurement_bar()
        self.setup_control_panel()
        self.setup_oscilloscope()
        self.setup_logic_analyzer()
        
        # Simulation de données
        self.simulate_data()
        
        # Mise à jour périodique des données
        self.update_data()
    
    def configure_styles(self):
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Arial', 10))
        self.style.configure('Large.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'), foreground='#FFFF00')
        self.style.configure('TButton', background='#444444', foreground=self.fg_color)
        self.style.configure('TCombobox', fieldbackground='#444444', foreground=self.fg_color)
        self.style.configure('TCheckbutton', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('Horizontal.TScale', background=self.bg_color)
    
    def create_main_frames(self):
        # Barre de mesures (horizontale en haut)
        self.measurement_bar = ttk.Frame(self.root, height=120)
        self.measurement_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Panneau principal (oscilloscope + analyseur logique)
        main_panel = ttk.Frame(self.root)
        main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Panneau de contrôle (vertical à droite)
        self.control_panel = ttk.Frame(main_panel, width=300)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Conteneur pour oscilloscope et analyseur logique
        display_frame = ttk.Frame(main_panel)
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Oscilloscope (60%)
        self.oscilloscope_frame = ttk.Frame(display_frame, height=500)
        self.oscilloscope_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Analyseur logique (40%)
        self.logic_analyzer_frame = ttk.Frame(display_frame, height=300)
        self.logic_analyzer_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def setup_measurement_bar(self):
        # Configuration de la barre de mesures horizontale
        measurements = [
            ("Courant (A)", "current", "#00FF00"),
            ("Tension CH1 (V)", "voltage_ch1", "#FF0000"),
            ("Tension CH2 (V)", "voltage_ch2", "#00FFFF"),
            ("Tension CH3 (V)", "voltage_ch3", "#FFFF00"),
            ("Tension CH4 (V)", "voltage_ch4", "#FF00FF"),
            ("Fréquence (Hz)", "frequency", "#FFFFFF"),
            ("Capacité (F)", "capacitance", "#FF9900"),
            ("Résistance (Ω)", "resistance", "#99FF00")
        ]
        
        for idx, (title, var_name, color) in enumerate(measurements):
            frame = tk.Frame(self.measurement_bar, bg=self.measure_bg, bd=1, relief='sunken')
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            # Titre
            tk.Label(frame, text=title, bg=self.measure_bg, fg=color, 
                    font=('Arial', 10)).pack(pady=(5, 0))
            
            # Valeur (grande taille)
            value_label = tk.Label(frame, text="0.000", bg=self.measure_bg, fg=color,
                                 font=('Arial', 18, 'bold'))
            value_label.pack(pady=(5, 10))
            
            # Stockage des références
            setattr(self, f"{var_name}_label", value_label)
    
    def setup_control_panel(self):
        # Titre
        ttk.Label(self.control_panel, text="CONTROLES", style='Title.TLabel').pack(pady=10)
        
        # Notebook pour organiser les onglets
        control_notebook = ttk.Notebook(self.control_panel)
        control_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet Oscilloscope
        osc_tab = ttk.Frame(control_notebook)
        control_notebook.add(osc_tab, text="Oscilloscope")
        self.setup_oscilloscope_controls(osc_tab)
        
        # Onglet Analyseur Logique
        logic_tab = ttk.Frame(control_notebook)
        control_notebook.add(logic_tab, text="Analyseur Logique")
        self.setup_logic_analyzer_controls(logic_tab)
        
        # Boutons généraux
        button_frame = ttk.Frame(self.control_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Sauvegarder Mesures", 
                  command=self.save_measurements).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Capture Écran", 
                  command=self.take_screenshot).pack(fill=tk.X, pady=2)
    
    def setup_oscilloscope_controls(self, parent):
        # Sélection des canaux
        channel_frame = ttk.LabelFrame(parent, text="Canaux Oscilloscope")
        channel_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i in range(self.osc_channels):
            ch_name = f"CH{i+1}"
            var = tk.BooleanVar(value=self.active_channels[i] if i < len(self.active_channels) else False)
            
            chk = ttk.Checkbutton(channel_frame, text=ch_name, variable=var,
                                command=lambda idx=i: self.toggle_channel(idx),
                                style='TCheckbutton')
            chk.pack(side=tk.LEFT, padx=5)
            setattr(self, f"ch{i+1}_var", var)
        
        # Contrôles d'échelle
        scale_frame = ttk.LabelFrame(parent, text="Échelles")
        scale_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(scale_frame, text="Temps/div:").pack()
        self.time_scale = ttk.Scale(scale_frame, from_=0.1, to=2, value=1)
        self.time_scale.pack(fill=tk.X)
        
        for i in range(self.osc_channels):
            if i >= len(self.active_channels):
                break
                
            ttk.Label(scale_frame, text=f"CH{i+1} V/div:").pack()
            scale = ttk.Scale(scale_frame, from_=0.1, to=5, value=1)
            scale.pack(fill=tk.X)
            setattr(self, f"volt_scale_ch{i+1}", scale)
        
        # Contrôles de déclenchement
        trigger_frame = ttk.LabelFrame(parent, text="Déclenchement")
        trigger_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(trigger_frame, text="Source:").pack()
        self.trigger_source = ttk.Combobox(trigger_frame, values=[f"CH{i+1}" for i in range(self.osc_channels)])
        self.trigger_source.current(0)
        self.trigger_source.pack(fill=tk.X)
        
        ttk.Label(trigger_frame, text="Niveau:").pack()
        self.trigger_level = ttk.Scale(trigger_frame, from_=-5, to=5, value=0)
        self.trigger_level.pack(fill=tk.X)
    
    def setup_logic_analyzer_controls(self, parent):
        # Sélection des canaux
        channel_frame = ttk.LabelFrame(parent, text="Canaux Logiques")
        channel_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i in range(8):
            var = tk.BooleanVar(value=i < 4)  # 4 premiers canaux activés par défaut
            chk = ttk.Checkbutton(channel_frame, text=f"D{i}", variable=var,
                                style='TCheckbutton')
            chk.pack(side=tk.LEFT, padx=5)
            setattr(self, f"logic_ch{i}_var", var)
        
        # Contrôles d'analyse
        analysis_frame = ttk.LabelFrame(parent, text="Analyse")
        analysis_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(analysis_frame, text="Protocole:").pack()
        self.protocol_select = ttk.Combobox(analysis_frame, 
                                          values=["Aucun", "UART", "I2C", "SPI", "1-Wire"])
        self.protocol_select.current(0)
        self.protocol_select.pack(fill=tk.X)
        
        ttk.Button(analysis_frame, text="Décoder", 
                  command=self.decode_protocol).pack(fill=tk.X, pady=5)
    
    def setup_oscilloscope(self):
        # Figure Matplotlib
        self.osc_fig = plt.Figure(figsize=(8, 4), dpi=100, facecolor='black')
        self.osc_ax = self.osc_fig.add_subplot(111)
        self.osc_ax.set_facecolor('black')
        self.osc_ax.tick_params(axis='x', colors='white')
        self.osc_ax.tick_params(axis='y', colors='white')
        self.osc_ax.grid(True, color='#444444')
        
        # Canvas Tkinter
        self.osc_canvas = FigureCanvasTkAgg(self.osc_fig, master=self.oscilloscope_frame)
        self.osc_canvas.draw()
        self.osc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_logic_analyzer(self):
        # Figure Matplotlib
        self.logic_fig = plt.Figure(figsize=(8, 2), dpi=100, facecolor='black')
        self.logic_ax = self.logic_fig.add_subplot(111)
        self.logic_ax.set_facecolor('black')
        self.logic_ax.tick_params(axis='x', colors='white')
        self.logic_ax.tick_params(axis='y', colors='white')
        self.logic_ax.grid(True, color='#444444')
        
        # Canvas Tkinter
        self.logic_canvas = FigureCanvasTkAgg(self.logic_fig, master=self.logic_analyzer_frame)
        self.logic_canvas.draw()
        self.logic_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def toggle_channel(self, channel_idx):
        """Active/désactive un canal de l'oscilloscope"""
        self.active_channels[channel_idx] = not self.active_channels[channel_idx]
        self.update_oscilloscope()
    
    def simulate_data(self):
        # Données simulées pour démonstration
        self.time = np.linspace(0, 2*np.pi, 500)
        
        # Signaux pour l'oscilloscope (4 canaux)
        self.osc_signals = [
            np.sin(self.time),                  # CH1
            np.cos(self.time),                 # CH2
            np.sin(self.time * 2) * 0.8,       # CH3
            np.cos(self.time * 0.5) * 1.2      # CH4
        ]
        
        # Signaux pour l'analyseur logique (8 canaux)
        self.logic_signals = [np.where(np.sin(self.time * (i+1)) > 0, 1, 0) for i in range(8)]
        
        # Valeurs simulées
        self.current_value = 0.5
        self.voltage_values = [3.3, 2.8, 1.5, 4.0]  # Pour CH1 à CH4
        self.frequency_value = 50.0
        self.capacitance_value = 0.0001
        self.resistance_value = 1000.0
    
    def update_data(self):
        # Mise à jour des valeurs aléatoires
        self.current_value = 0.5 + np.random.rand()*0.1 - 0.05
        self.voltage_values = [
            3.3 + np.random.rand()*0.5 - 0.25,
            2.8 + np.random.rand()*0.4 - 0.2,
            1.5 + np.random.rand()*0.3 - 0.15,
            4.0 + np.random.rand()*0.6 - 0.3
        ]
        self.frequency_value = 50.0 + np.random.rand()*5 - 2.5
        self.capacitance_value = 0.0001 + np.random.rand()*0.00001 - 0.000005
        self.resistance_value = 1000.0 + np.random.rand()*100 - 50
        
        # Mise à jour des signaux
        for i in range(4):
            self.osc_signals[i] = self.osc_signals[i] * (0.95 + np.random.rand()*0.1)
        
        # Mise à jour des affichages
        self.update_measurements()
        self.update_oscilloscope()
        self.update_logic_analyzer()
        
        # Enregistrement des mesures
        self.record_measurements()
        
        # Rappel après 100ms
        self.root.after(100, self.update_data)
    
    def update_measurements(self):
        """Met à jour les valeurs affichées dans la barre de mesures"""
        self.current_label.config(text=f"{self.current_value:.3f}")
        for i in range(4):
            getattr(self, f"voltage_ch{i+1}_label").config(text=f"{self.voltage_values[i]:.3f}")
        self.frequency_label.config(text=f"{self.frequency_value:.1f}")
        self.capacitance_label.config(text=f"{self.capacitance_value:.6f}")
        self.resistance_label.config(text=f"{self.resistance_value:.1f}")
    
    def update_oscilloscope(self):
        """Met à jour l'affichage de l'oscilloscope"""
        self.osc_ax.clear()
        time_scale = self.time_scale.get()
        scaled_time = self.time * time_scale
        
        for i in range(self.osc_channels):
            if i < len(self.active_channels) and self.active_channels[i]:
                volt_scale = getattr(self, f"volt_scale_ch{i+1}").get()
                scaled_signal = self.osc_signals[i] * volt_scale
                self.osc_ax.plot(scaled_time, scaled_signal, 
                                color=self.channel_colors[i], 
                                linewidth=1, 
                                label=f'CH{i+1}')
        
        self.osc_ax.set_xlabel("Temps (s)", color='white')
        self.osc_ax.set_ylabel("Tension (V)", color='white')
        self.osc_ax.grid(True, color='#444444')
        
        if any(self.active_channels):
            self.osc_ax.legend(loc='upper right', facecolor='black', labelcolor='white')
        
        self.osc_canvas.draw()
    
    def update_logic_analyzer(self):
        """Met à jour l'affichage de l'analyseur logique"""
        self.logic_ax.clear()
        time_scale = self.time_scale.get()
        scaled_time = self.time * time_scale
        
        active_channels = 0
        for i in range(8):
            if getattr(self, f"logic_ch{i}_var").get():
                self.logic_ax.step(scaled_time, self.logic_signals[i] + active_channels*1.5, 
                                 where='post', color=self.channel_colors[i % 4])
                active_channels += 1
        
        self.logic_ax.set_xlabel("Temps (s)", color='white')
        self.logic_ax.set_ylabel("Canal", color='white')
        self.logic_ax.set_yticks([])
        self.logic_ax.grid(True, color='#444444')
        self.logic_canvas.draw()
    
    def record_measurements(self):
        """Enregistre les mesures courantes dans l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        measurements = {
            "timestamp": timestamp,
            "current": self.current_value,
            "voltage_ch1": self.voltage_values[0],
            "voltage_ch2": self.voltage_values[1],
            "voltage_ch3": self.voltage_values[2],
            "voltage_ch4": self.voltage_values[3],
            "frequency": self.frequency_value,
            "capacitance": self.capacitance_value,
            "resistance": self.resistance_value
        }
        self.measurements_history.append(measurements)
        
        # Garder seulement les 100 dernières mesures
        if len(self.measurements_history) > 100:
            self.measurements_history.pop(0)
    
    def save_measurements(self):
        """Sauvegarde les mesures dans un fichier JSON"""
        if not self.measurements_history:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            title="Enregistrer les mesures"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.measurements_history, f, indent=4)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {e}")
    
    def take_screenshot(self):
        """Capture l'écran de l'application"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Images PNG", "*.png"), ("Tous les fichiers", "*.*")],
            title="Enregistrer la capture d'écran"
        )
        
        if file_path:
            try:
                 # ... (code existant)
                if file_path:
                    x = self.root.winfo_rootx()
                    y = self.root.winfo_rooty()
                    width = self.root.winfo_width()
                    height = self.root.winfo_height()
                    ImageGrab.grab(bbox=(x, y, x+width, y+height)).save(file_path)
            except Exception as e:
                print(f"Erreur lors de la capture: {e}")
    
    def decode_protocol(self):
        """Décode le protocole sélectionné"""
        protocol = self.protocol_select.get()
        print(f"Décodage du protocole {protocol}...")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalVisualizerApp(root)
    root.mainloop()