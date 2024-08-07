# Documentation application durcissement sécurité ubuntu
<img src="https://github.com/CatharsisCoding/Python-Hardening-framatome/assets/97361977/002b785d-1a1b-4475-aced-ce47b6a506a3" alt="Image A" width="400" style="margin-right: 20px;"> <img src="https://github.com/CatharsisCoding/Python-Hardening-framatome/assets/97361977/e17b5503-70a8-420e-b093-b56d9841ca4a" alt="Image B" width="400">


## Description
L'application de renforcement de sécurité est une interface utilisateur graphique (GUI) développée en Python avec PySide6 qui permet d'exécuter diverses tâches de renforcement de la sécurité sur un système Linux.


## Prérequis

Avant d'exécuter cette application, assurez-vous d'avoir installé les logiciels et les modules nécessaires sur votre système.

### Logiciels requis :

- **iptables** : Un utilitaire de ligne de commande pour configurer le pare-feu du noyau Linux. Vous pouvez l'installer sur Ubuntu en utilisant la commande suivante :
```
sudo apt install iptables
```

- **Apache2** : Un serveur HTTP populaire. Si vous prévoyez d'utiliser la fonctionnalité de désactivation d'Apache2, vous pouvez l'installer sur Ubuntu avec :
```
sudo apt install apache2
```

- **Nmap** : Un scanner de réseau et d'analyse de sécurité. Vous pouvez l'installer sur Ubuntu avec :
```
sudo apt install nmap
```

### Modules Python requis :

- **PySide6** : Une bibliothèque permettant de créer des interfaces graphiques utilisateurs (GUI) en utilisant Qt 6. Vous pouvez l'installer via pip :
```
pip install PySide6
```


- **pyqt-tools** : Un ensemble d'outils supplémentaires pour PyQt, y compris le Designer Qt, un outil de conception d'interfaces graphiques. Vous pouvez l'installer via pip :
```
pip install pyqt-tools
```
- **libxcb-cursor0** : Une bibliothèque nécessaire pour charger le plugin de plate-forme Qt xcb. Vous pouvez l'installer sur Ubuntu avec :
```
sudo apt install libxcb-cursor0

```


## Utilisation
Pour lancer l'application, exécutez simplement la commande suivante dans votre terminal :

```bash
python3 hardening.py
```
**L'application est conçue pour être simple et intuitive à utiliser. Voici comment utiliser chaque fonctionnalité :**

**Sécurisation des fichiers** : Cliquez sur le bouton "Sécuriser Fichier" et sélectionnez le fichier à sécuriser. Entrez ensuite votre mot de passe sudo lorsque vous y êtes invité.

**Mise à jour du système** : Cliquez sur le bouton "Mettre à jour le système" pour mettre à jour le système. Entrez votre mot de passe sudo lorsque vous y êtes invité.

**Désactivation d'apache2** : Cliquez sur le bouton "Désactiver apache2" pour arrêter le service Apache2. Entrez votre mot de passe sudo lorsque vous y êtes invité.

**Configuration du pare-feu** : Cliquez sur le bouton "Configurer le pare-feu" pour configurer le pare-feu avec des règles spécifiques. Entrez votre mot de passe sudo lorsque vous y êtes invité.

**Désactivation du port 80** : Cliquez sur le bouton "Désactiver le port 80" pour bloquer les connexions entrantes sur le port 80. Entrez votre mot de passe sudo lorsque vous y êtes invité.

**Scan des vulnérabilités** : Cliquez sur le bouton "Scan des vulnérabilités" pour scanner les vulnérabilités du système local. Entrez votre mot de passe sudo lorsque vous y êtes invité.

**Affichage des règles de pare-feu** : Utilisez le bouton "Afficher les règles de pare-feu" pour afficher les règles de pare-feu actuellement en vigueur.

**Suppression des règles de pare-feu** : Utilisez le bouton "Supprimer les règles de pare-feu" pour supprimer toutes les règles de pare-feu. Une confirmation sera demandée car cette action est potentiellement dangereuse.


## Remarques
Assurez-vous d'avoir le mot de passe sudoer appropriés pour exécuter les différentes fonctionnalités de l'application.
