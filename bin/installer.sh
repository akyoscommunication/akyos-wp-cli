#!/bin/bash

cwd=$(pwd)

echo "Installation du CLI Akyos..."

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

# Clone the repository
git clone https://gitlab.com/akyos-autres/sage-dev.git "$TMPDIR/aky_cli" --branch="docker"

# Move to the directory
cd "$TMPDIR/aky_cli" || exit

# Build the image
docker build -t aky-cli -f .docker/Dockerfile --no-cache .

# Create the container
echo "docker run --rm --network=\"host\" -it -v $(pwd):/cwd aky-cli \"\$@\"" > /usr/local/bin/aky
chmod +x /usr/local/bin/aky

# Clean
cd "$cwd" || exit
rm -rf "$TMPDIR/aky_cli"

echo "Installation terminée !"
echo "Vous pouvez maintenant utiliser la commande 'aky' pour lancer le CLI."

