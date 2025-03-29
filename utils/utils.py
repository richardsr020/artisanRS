import tkinter as tk
from PIL import Image, ImageTk

def get_icon(device_name):
    """Retourne une icône redimensionnée en fonction du nom de l'appareil"""
    icon_path = None
    if device_name == 'home':
        icon_path = "icons/icon0.png"
    elif device_name == 'oscilloscope':
        icon_path = "icons/icon1.png"
    elif device_name == 'multimetre':
        icon_path = "icons/icon2.png"
    elif device_name == 'frequencemetre':
        icon_path = "icons/icon3.png"

    if icon_path:
        image = Image.open(icon_path)
        image = image.resize((50, 50))  # Supprime `Image.ANTIALIAS`
        return ImageTk.PhotoImage(image)
    return None
