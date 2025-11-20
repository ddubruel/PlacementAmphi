# Placement Étudiants

Application Python (Tkinter) permettant de **placer les étudiants dans les amphithéâtres** à partir de fichiers CSV, puis de **générer les documents nécessaires aux examens** (listes d'émargement, mails personnalisés, etc.).
---

##  Fonctionnalités

- Charge des fichiers CSV issus de :
  - **Moodle**
  - **ADE**
  - **Apogée**
- Définit automatiquement le **placement des étudiants dans les amphis**.
- Génère les **listes d'émargement au format PDF**.
- Envoie un **mail personnalisé à chaque étudiant**.
- Interface graphique basée sur **Tkinter**.


- 📄 Listes d’émargement (PDF)
- ✉️ Envoi de mails personnalisés
- 🏛️ Plans d’amphis exportés en images
- 📁 Arborescence organisée par épreuve


##  Installation standard :

Avec la version python **3.11.2**
```bash
#1) créer un environnement virtuel
python -m venv NomDeVotreEnvironnement

#2) activer l'environnement virtuel:
source NomDeVotreEnvironnement/bin/activate # Linux/Mac
# ou pour windows :
# NomDeVotreEnvironnement\Scripts\activate     # Windows

#3 installer les dépendances requises  :
pip install -r requirements.txt

#4 lancer le code dans l'environement virtuel activé
python mainClasse2.py
```

### 🍏 Installation spécifique macOS (si l’installation standard échoue)

#### **👉 macOS Intel**
```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```bash

#### **👉 macOS Apple Silicon (M1/M2/M3)**
```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
```

Activer conda :

```bash
# en fonction de votre shell :
source ~/.zshrc
# source  ~/.bashrc
# pour vérifier si l'installation s'est bien passée :
conda --version
```

Récupérer sur le dépôt le fichier **environment.yml**

Créer l’environnement Conda sur macOS :

```bash
cd /chemin/vers/ton/projet
conda env create -f environment.yml
```

Activer l'environnement virtuel :

```bash
conda activate placement-etudiants
```

Lancer le code :
```bash
python mainClasse2.py
```



###  Prérequis

- **Python 3.11.2**
- `pip` installé
- (Recommandé) Un environnement virtuel

###  Récupérer le projet

git clone https://github.com/ddubruel/PlacementAmphi

####
Avant le lancement il est recommandé de mettre les fichiers de données
dans un même répertoire.

Le code va créer par exemple l'arborescence contenant tous les fichiers de sortie.

```text
├── Amphi_Chimie
│   ├── listes_Emargement_pdf
│   │   ├── Chimie.pdf
│   ├── pngOut
│   │   ├── Chimie_A-11-1.png
│   │   ├── Chimie_A-11-3.png
.../..
│   │   ├── Chimie_B-9-4.png
│   │   └── Chimie_plan_general.png
│   └── texOut
│       ├── Chimie.tex
│       ├── table_alpha.tex
│       └── table.tex
├── Amphi_Informatique
│   ├── listes_Emargement_pdf
│   │   ├── Chimie.pdf
│   ├── pngOut
│   │   ├── Chimie_A-11-1.png
│   │   ├── Chimie_A-11-3.png
.../..
│   │   ├── Chimie_B-9-4.png
│   │   └── Chimie_plan_general.png
│   └── texOut
│       ├── Chimie.tex
│       ├── table_alpha.tex
│       └── table.tex
```

En complément à côté des ffichiers suivants  contenant le statut d'envoi des mails.

├─Z_etudiants_dans_moodle_mais_pas_dans_ADE.csv
├─Z_etudiants_avec_mail_envoyes.csv
├─Z_etudiants_avec_mail_NON_envoyes.csv
