import tkinter as tk

class Multimeter(tk.Frame):
    def __init__(self, ):
        super().__init__()

        self.title("Interface de Mesure")
        self.geometry("400x300")

        # Cadre principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Bouton pour afficher le multimètre
        self.show_multimeter_btn = tk.Button(self.main_frame, text="Ouvrir Multimètre",
                                             command=self.open_multimeter)
        self.show_multimeter_btn.pack(pady=20)

    def open_multimeter(self):
        """Ouvre le multimètre dans un sous-frame."""
        child_frame = tk.Toplevel(self)  # Crée une nouvelle fenêtre enfant
        child_frame.geometry("300x250")
        child_frame.title("Multimètre")

        multimeter = multimeter(child_frame)  # Passe la nouvelle fenêtre comme parent
        multimeter.display()

if __name__ == "__main__":
    app = Multimeter()
    app.mainloop()

