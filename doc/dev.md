1 -> Télécharge et execute le script d'installation  
```/bin/bash -c "$(curl -fsSL https://gitlab.com/akyos-autres/sage-dev/-/raw/main/bin/aky_installer.sh)"```

2 -> Verifier que docker est installé sur le systeme  
```docker --version```

3 -> Cloner le projet dans tmp  
```git clone https://gitlab.com/akyos-autres/sage-dev.git /tmp/aky-cli```

4 -> Se deplacer dans le dossier du projet  
```cd /tmp/aky-cli```

5 -> Build l'image docker  
```docker build -t aky-cli .docker```

6 -> Creer un bin pour lancer le container  
```echo "docker run --rm -it -v $(pwd):/app aky-cli" > /usr/local/bin/aky```
```chmod +x /usr/local/bin/aky```

7 -> Lancer le container  
```aky```

