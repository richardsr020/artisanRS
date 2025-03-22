# **RS - RealScope**  
### Real-Time Signal Analyzer for Arduino

**RS - RealScope** est un logiciel d'analyse de signaux en temps réel développé en **Python**. Utilisant un **Arduino Nano**, il intègre plusieurs outils de mesure électroniques pour analyser les signaux :  
- **Oscilloscope**
- **Multimètre**
- **Fréquentimètre**
- **Appareil LCR** (pour mesurer inductances, capacités et résistances)

---

## **Features**  
- 🌟 **Analyse en temps réel** des signaux analogiques envoyés par l'Arduino  
- 📊 **Affichage dynamique** des données avec **Matplotlib** pour l'oscilloscope  
- ⚡ **Multimètre** pour mesurer la tension, le courant, et la résistance  
- 🎵 **Fréquentimètre** pour mesurer la fréquence des signaux  
- 📐 **Appareil LCR** pour mesurer les **inductances, résistances, et capacités** des composants
- 🖥️ **Interface graphique conviviale** pour une utilisation simple et intuitive
- 🔄 **Compatibilité multiplateforme** (Linux, Windows, macOS)

---

## **Installation**

### **1. Cloner ce dépôt**  
Cloner ce projet sur votre machine locale :
```bash
git clone https://github.com/richardsr020/artisanRS.git
```

### **2. Installer les dépendances Python**
Assurez-vous d'avoir **Python 3.x** installé sur votre machine. Ensuite, installez les dépendances requises :
```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient les bibliothèques suivantes :  
- `pyserial` - pour la communication série avec l'Arduino  
- `matplotlib` - pour afficher les graphiques  
- `numpy` - pour gérer les tableaux de données

### **3. Configurer l'Arduino**
1. **Téléchargez et installez l'Arduino IDE** : [Télécharger Arduino IDE](https://www.arduino.cc/en/software)
2. **Téléchargez le code de l'Arduino** dans le répertoire `arduino_code` :
    - Ouvrez le fichier `arduino_code/realScope.ino` dans l'Arduino IDE.
    - Sélectionnez le bon modèle de carte et le port de votre Arduino Nano.
    - Téléversez le code sur votre Arduino Nano.

Le code Arduino envoie en continu les valeurs mesurées via le port série à l'ordinateur.

---

## **Utilisation**

### **1. Connectez votre Arduino Nano à votre ordinateur**  
Assurez-vous que l'Arduino Nano est connecté via un câble USB à votre ordinateur.

### **2. Lancer l'application Python**  
Dans le terminal, allez dans le répertoire du projet cloné et lancez le programme Python :
```bash
python realScope.py
```

Cela ouvrira une fenêtre graphique montrant les différentes mesures en temps réel.

---

## **Outils de mesure disponibles**

### **1. Oscilloscope**  
Affiche les signaux analogiques en temps réel, vous permettant de visualiser les variations de voltage.  
- **Entrée** : Signal analogique (ex. tension continue ou alternative)
- **Sortie** : Graphe avec affichage de la forme d'onde et des mesures (période, amplitude, fréquence)

### **2. Multimètre**  
Mesure la **tension**, le **courant** et la **résistance** des composants. Il peut être utilisé pour des mesures de continuité ou pour tester des résistances.

- **Mesures** :  
  - **Tension** (AC/DC)  
  - **Courant** (AC/DC)  
  - **Résistance**

### **3. Fréquentimètre**  
Mesure la **fréquence** d'un signal oscillant, parfait pour tester des circuits à haute fréquence.

- **Mesures** :  
  - **Fréquence** du signal (Hz)

### **4. Appareil LCR**  
Mesure les propriétés de composants passifs comme les **inductances**, **capacités**, et **résistances** des circuits électroniques.

- **Mesures** :  
  - **Inductance** (L)  
  - **Capacité** (C)  
  - **Résistance** (R)

---

## **Dépannage**

### **Problèmes de port série**  
Si vous avez des problèmes pour connecter l'Arduino à votre ordinateur, vérifiez que le port série est correct dans le script Python.  
Modifiez la ligne suivante dans `realScope.py` en fonction de votre port :
```python
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Linux / macOS
# ou
ser = serial.Serial('COM3', 115200, timeout=1)  # Windows
```

---

## **Contribuer**

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations ou des corrections de bugs, n'hésitez pas à ouvrir un **issue** ou à soumettre une **pull request**.


## **Licence**
Ce projet est sous licence propriétaire. Tous les droits sont réservés. Aucune redistribution, modification ou utilisation commerciale n'est permise sans l'accord explicite de l'auteur.

---

## **Auteurs**
- **Votre nom ou pseudonyme** : [richardsr020](https://github.com/richardsr020)

---

### **Remerciements**
- Merci à la communauté Arduino et Python pour leurs outils et bibliothèques puissants.
- À tous les contributeurs pour leur soutien.

---

**RS - RealScope** est un projet open-source, destiné à aider à l'analyse de signaux avec une interface simple et rapide. 🎉

