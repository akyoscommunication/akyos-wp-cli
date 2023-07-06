#!/bin/bash

# Check if Docker is installed
if command -v docker >/dev/null 2>&1; then
    :
else
    echo "Docker n'est pas installé, veuillez l'installer avant de continuer."
    exit 1
fi

# Check if Docker is running
if docker info >/dev/null 2>&1; then
    :
else
    echo "Docker n'est pas en cours d'exécution, veuillez le démarrer avant de continuer."
    exit 1
fi

# Check if aky is already installed
if command -v aky >/dev/null 2>&1; then
    echo "Le CLI Akyos est déjà installé."

    echo "Voulez vous le réinstaller ? (y/n)"
    read -r reinstall

    if [ "$reinstall" = "y" ] || [ "$reinstall" = "Y" ]; then

        echo "Suppression du CLI Akyos..."
        rm -rf "$HOME/.aky"
        rm -rf /usr/local/bin/aky

        echo "CLI Akyos supprimé."

    else
        echo "Installation du CLI Akyos annulée."
        exit 1
    fi

fi