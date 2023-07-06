#!/bin/bash

cwd=$(pwd)

echo "Installation du CLI Akyos..."

# if dir exist tmp/aky_cli
if [ -d "$TMPDIR/aky_cli" ]; then
    rm -rf "$TMPDIR/aky_cli"
fi

# Clone the repository
git clone https://github.com/akyoscommunication/akyos-wp-cli.git "$TMPDIR/aky_cli"

# Call bin/pre-install.sh
"$TMPDIR/aky_cli/bin/pre-install.sh"
# Check the exit status of pre-install.sh
if [ $? -ne 0 ]; then
    exit 1
fi

# Move to the directory
cd "$TMPDIR/aky_cli" || exit

# Build the image
docker build -t aky-cli -f .docker/Dockerfile --no-cache .

# Create the container
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "docker run --rm --network=\"host\" -it -v \"%cd%\":/cwd aky-cli \"%*\"" > "C:\Program Files\aky\aky.bat"
    setx PATH "%PATH%;C:\Program Files\aky\\" /M
else
    echo "docker run --rm --network=\"host\" -it -v $(pwd):/cwd aky-cli \"\$@\"" > /usr/local/bin/aky
    chmod +x /usr/local/bin/aky
fi

# Store the configuration
mkdir -p "$HOME/.aky"
cp .docker/config/config.json "$HOME/.aky/config.json"

# Call bin/configuration.sh
"$TMPDIR/aky_cli/bin/configuration.sh"

# Clean
cd "$cwd" || exit
rm -rf "$TMPDIR/aky_cli"

echo "Installation terminée !"
echo "Vous pouvez maintenant utiliser la commande 'aky' pour lancer le CLI."

