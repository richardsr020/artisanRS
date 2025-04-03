#!/bin/bash

# Donner l'accès en lecture/écriture au port série
sudo chmod 666 /dev/ttyUSB0

# Exécuter le script Python
python3 main.py
