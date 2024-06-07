import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QInputDialog, QLineEdit, QFileDialog

class HardeningApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hardening App")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        

        self.file_button = QPushButton("Securiser Fichier")
        self.file_button.clicked.connect(self.secure_files)
        layout.addWidget(self.file_button)
        
        self.update_button = QPushButton("Mettre à jour le systeme")
        self.update_button.clicked.connect(self.update_system)
        layout.addWidget(self.update_button)

        self.disable_port_button = QPushButton("Desactiver apache2")
        self.disable_port_button.clicked.connect(self.disable_apache2)
        layout.addWidget(self.disable_port_button)

        self.disable_port_button = QPushButton("Configurer firewall")
        self.disable_port_button.clicked.connect(self.configure_firewall)
        layout.addWidget(self.disable_port_button)

        self.disable_port_button = QPushButton("Desactiver port 80")
        self.disable_port_button.clicked.connect(self.disable_port_80)
        layout.addWidget(self.disable_port_button)

        self.disable_port_button = QPushButton("Scan vunerabilité")
        self.disable_port_button.clicked.connect(self.scan_vulnerabilities)
        layout.addWidget(self.disable_port_button)
        
        self.show_iptables_button = QPushButton("Afficher les règles de pare-feu")
        self.show_iptables_button.clicked.connect(self.show_iptables)
        layout.addWidget(self.show_iptables_button)

        self.clear_iptables_button = QPushButton("Supprimer les règles de pare-feu")
        self.clear_iptables_button.clicked.connect(self.clear_iptables)
        layout.addWidget(self.clear_iptables_button)
        

        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        

    def secure_files(self):
        self.status_label.setText("Sécurisation du fichier...")
        file_path, _ = QFileDialog.getOpenFileName(self, "Selectionné un fichier à sécuriser")
        if file_path:
            password, ok = QInputDialog.getText(self, "Password Required", "Enter your sudo password:", QLineEdit.Password)
            if ok and password:
                try:
                    # Changer les permissions du fichier
                    self.run_command(["sudo", "-S", "chmod", "600", file_path], password)
                    # Changer le propriétaire du fichier (optionnel)
                    # self.run_command(["sudo", "-S", "chown", "root:root", file_path], password)
                    self.status_label.setText(f"Le fichier {file_path} est securisé avec succès.")
                except subprocess.CalledProcessError as e:
                    self.status_label.setText(f"Error securing file: {e}")
            else:
                self.status_label.setText("Entré du mot de passe annulé.")
        else:
            self.status_label.setText("Selection du fichié annulé.")
        
    def update_system(self):
        self.status_label.setText("Mise à jour du systeme...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe necessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                # Mise à jour de la liste des paquets
                self.run_command(["sudo", "-S", "apt-get", "update"], password)
                # Mise à jour des paquets installés
                self.run_command(["sudo", "-S", "apt-get", "upgrade", "-y"], password)
                self.status_label.setText("Mise à jour terminée.")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error updating system: {e}")
        else:
            self.status_label.setText("Entré du mot de passe annulé.")
    def disable_apache2(self):
        self.status_label.setText("Désactivation apache2...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe necessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                # Désactiver les services apache2
                self.run_command(["sudo", "-S", "systemctl", "stop", "apache2"], password)
                self.status_label.setText("Apache2 désactivé avec succès.")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error disabling port 80: {e}")
        else:
            self.status_label.setText("L'entrée du mot de passe à été annulé.")

    def run_command(self, command, password):
        """Lance sudo avec le mot de passe fournis"""
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=password.encode() + b'\n')
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)
    def configure_firewall(self):
        self.status_label.setText("Configuration du firewall...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe necessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                
                self.run_command(["sudo", "-S", "iptables", "-P", "INPUT", "DROP"], password) # Définir la politique par défaut pour les paquets entrants comme DROP (rejetés) 
                self.run_command(["sudo", "-S", "iptables", "-P", "FORWARD", "DROP"], password) # Définir la politique par défaut pour les paquets en transit comme DROP (rejetés)
                self.run_command(["sudo", "-S", "iptables", "-P", "OUTPUT", "ACCEPT"], password) # Autoriser tous les paquets sortants
                self.run_command(["sudo", "-S", "iptables", "-A", "INPUT", "-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED", "-j", "ACCEPT"], password) # Autoriser les connexions établies et associées
                self.run_command(["sudo", "-S", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-j", "ACCEPT"], password) # Autoriser les connexions SSH
                self.run_command(["sudo", "-S", "iptables", "-A", "INPUT", "-p", "icmp", "-j", "ACCEPT"], password) # Autoriser les paquets ICMP (Ping)
                self.status_label.setText("Firewall configuré avec succès.")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error configuring firewall: {e}")
        else:
            self.status_label.setText("L'entrée du mot de passe à été annulé.")

    def disable_port_80(self):
        self.status_label.setText("Désactivation du port 80...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe necessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                # Rejeter les connexions entrantes sur le port 80
                self.run_command(["sudo", "-S", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-j", "REJECT"], password)
                self.status_label.setText("Port 80 Désactiver avec succès.")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error disabling port 80: {e}")
        else:
            self.status_label.setText("L'entrée du mot de passe à été annulé.")
    def scan_vulnerabilities(self):
        self.status_label.setText("Scanning des vulnerabilitées...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe necessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                # Utiliser nmap pour un scan de vulnérabilités de base
                result = self.run_command(["sudo", "-S", "nmap", "--script", "vuln", "localhost"], password)
                self.status_label.setText(f"Scan terminé. Results:\n{result}")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error scanning vulnerabilities: {e}")
        else:
            self.status_label.setText("L'entrée du mot de passe à été annulé.")
    def show_iptables(self):
        self.status_label.setText("Affichage des règles de pare-feu...")
        QApplication.processEvents()  # Mettre à jour l'interface utilisateur

        password, ok = QInputDialog.getText(self, "Mot de passe nécessaire", "Entrez votre mot de passe:", QLineEdit.Password)
        
        if ok and password:
            try:
                # Exécuter la commande sudo iptables -L
                process = subprocess.Popen(["sudo", "-S", "iptables", "-L"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=password.encode() + b'\n')
                
                # Vérifier si la commande a réussi
                if process.returncode == 0:
                    result = stdout.decode()  # Convertir la sortie en chaîne de caractères
                    self.status_label.setText(f"Règles de pare-feu affichées:\n{result}")
                else:
                    self.status_label.setText(f"Erreur lors de l'affichage des règles de pare-feu:\n{stderr.decode()}")
            except Exception as e:
                self.status_label.setText(f"Erreur lors de l'affichage des règles de pare-feu: {e}")
        else:
            self.status_label.setText("L'entrée du mot de passe a été annulée.")
    def clear_iptables(self):
        confirm = QMessageBox.question(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer toutes les règles de pare-feu ? Cette action est potentiellement dangereuse.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            password, ok = QInputDialog.getText(self, "Mot de passe nécessaire", "Entrez votre mot de passe:", QLineEdit.Password)
            
            if ok and password:
                try:
                    # Exécuter la commande sudo iptables -F
                    process = subprocess.Popen(["sudo", "-S", "iptables", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate(input=password.encode() + b'\n')
                    
                    # Vérifier si la commande a réussi
                    if process.returncode == 0:
                        self.status_label.setText("Toutes les règles de pare-feu ont été supprimées.")
                    else:
                        self.status_label.setText(f"Erreur lors de la suppression des règles de pare-feu:\n{stderr.decode()}")
                except Exception as e:
                    self.status_label.setText(f"Erreur lors de la suppression des règles de pare-feu: {e}")
            else:
                self.status_label.setText("L'entrée du mot de passe a été annulée.")
        else:
            self.status_label.setText("Opération annulée.")





        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HardeningApp()
    window.show()
    sys.exit(app.exec())
