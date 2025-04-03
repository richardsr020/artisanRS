import serial
import serial.tools.list_ports
import struct
import time

class Serial_manager:
    def __init__(self, baudrate=500000, timeout=1):
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def detect_arduino(self):
        """ Scanne les ports en boucle jusqu'à détecter un Arduino et s'assurer qu'il répond """
        while True:
            ports = list(serial.tools.list_ports.comports())
            print("🔍 Recherche d'un Arduino en cours...")

            for port in ports:
                try:
                    ser = serial.Serial(port.device, self.baudrate, timeout=self.timeout)
                    time.sleep(2)  # Attente pour éviter les erreurs de buffer

                    # Test de communication : on envoie un caractère et attend une réponse
                    ser.write(b'PING\n')
                    response = ser.readline().decode().strip()

                    if response == "PONG":  # L'Arduino doit renvoyer "PONG"
                        print(f"✅ Arduino détecté sur {port.device}")
                        return ser  # Retourne la connexion valide
                    else:
                        ser.close()

                except (serial.SerialException, OSError):
                    pass  # Ignore les erreurs et continue le scan

            print("❌ Aucun Arduino détecté. Nouvel essai dans 2 secondes...")
            time.sleep(2)  # Attente avant le prochain scan

    def read_serial(self):
        """ Lit les données série et les affiche en continu """
        while True:
            try:
                if self.serial_connection.in_waiting >= 2:
                    raw_data = self.serial_connection.read(2)
                    value = struct.unpack('<H', raw_data)[0]  # '<H' = Little Endian, Unsigned 16-bit
                    print(f"📊 Valeur reçue : {value}")
            except (serial.SerialException, OSError):
                print("⚠️ Perte de connexion. Reconnexion en cours...")
                self.serial_connection.close()
                return None  # Redémarre le scan si l'Arduino est déconnecté

    def run(self):
        """ Boucle principale : détecte l'Arduino et affiche les données """
        while True:
            self.serial_connection = self.detect_arduino()  # Attend qu'un Arduino soit connecté
            self.read_serial()  # Lit les données tant que la connexion est stable

# 🔥 Exécution du programme
if __name__ == "__main__":
    sm = Serial_manager()
    sm.run()