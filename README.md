## Installation

### Linux / MacOS
Copier coller la commande suivante dans votre terminal (n'importe ou)
```
/bin/bash -c "$(curl -H 'Cache-Control: no-cache, no-store' -fsSL https://raw.githubusercontent.com/akyoscommunication/akyos-wp-cli/main/bin/installer.sh)"
```

### Windows

[Installer WSL2](https://korben.info/installer-wsl2-windows-linux.html) (Windows Subsystem for Linux) et Ubuntu 20.04 LTS (https://ubuntu.com/wsl)  
Lancer Ubuntu 20.04 LTS et suivre les étapes d'installation ci-dessus :

Copier coller la commande suivante dans votre terminal (n'importe ou)
```
/bin/bash -c "$(curl -H 'Cache-Control: no-cache, no-store' -fsSL https://raw.githubusercontent.com/akyoscommunication/akyos-wp-cli/main/bin/installer.sh)"
```

#### Mettre en place une alias pour lancer le cli depuis Windows:
Créer un fichier .bat et y ajouter cette commande :
```
wsl -d Ubuntu-20.04 -- aky $*
```
Ensuite, ajouter le chemin du fichier .bat dans les [variables d'environnement](https://www.malekal.com/variables-environnement-windows/) de Windows (PATH)

## Documentation

Créer une nouvelle commande :
```
Ajouter une entrée dans config/commands.yaml
Ajouter une classe dans app/commands/{package}/{command}Command.py
La classe doit extend de BaseCommand (core.commands.BaseCommand)
La classe doit implementer la méthode invoke(self, app, io)
```