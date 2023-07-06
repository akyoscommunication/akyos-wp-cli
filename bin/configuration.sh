#!/bin/bash

echo "Configuration du CLI"

# Gitlab Token
echo "[*] Veuillez entrer votre token Gitlab :";
echo "https://gitlab.com/profile/personal_access_tokens";
read -r token;
sed -i "s/\"GITLAB_TOKEN\": \"\"/\"GITLAB_TOKEN\": \"$token\"/g" "$HOME/.aky/config.json"
echo "[*] Token Gitlab enregistré !"

# config.json -> presets
echo "[*] Souhaitez-vous définir les valeurs par défaut pour les nouveaux projets ? (y/n)";
read -r default;

if [ "$default" = "y" ] || [ "$default" = "Y" ]; then

  # db_user
  echo "[*] Veuillez entrer le nom d'utilisateur de la base de données :";
  read -r db_user;

  # db_password
  echo "[*] Veuillez entrer le mot de passe de la base de données :";
  read -r db_password;

  # admin_email
  echo "[*] Veuillez entrer l'adresse email de l'administrateur :";
  read -r admin_email;

  # site_url
  echo "[*] Veuillez entrer l'URL du site :";
  read -r site_url;

  echo "[*] Valeurs par défaut enregistrées !";
else
  db_user="root";
  db_password="root";
  admin_email="admin@akyos.com";
  site_url="http://127.0.0.1:3000";
  echo "[*] Valeurs par défaut non définis !"
fi

sed -i "s/\"DB_USER\": \"\"/\"DB_USER\": \"$db_user\"/g" "$HOME/.aky/config.json"
sed -i "s/\"DB_PASSWORD\": \"\"/\"DB_PASSWORD\": \"$db_password\"/g" "$HOME/.aky/config.json"
sed -i "s/\"ADMIN_EMAIL\": \"\"/\"ADMIN_EMAIL\": \"$admin_email\"/g" "$HOME/.aky/config.json"
sed -i "s/\"SITE_URL\": \"\"/\"SITE_URL\": \"$site_url\"/g" "$HOME/.aky/config.json"

# fetch WPMU_DEV_API_KEY and ACF_PRO_KEY from cli.akyos.ac-dev.fr
echo "[*] Veuillez entrer votre clé d'authentification cli.akyos :";
echo "(https://mon-agence-web.io/app/projects/profile/5c0635f15dbba50004b2a3a7 - ctrl + f - cli.akyos)";
read -r cli_akyos_key;

# get request to http://cli.akyos.ac-dev.fr/wp-json/akyos/v1/secrets w/headers ["Authorization" => "{cli_akyos_key}"]
echo "[*] Récupération des clés WPMU_DEV_API_KEY et ACF_PRO_KEY...";
secrets_url="http://cli.akyos.ac-dev.fr/wp-json/akyos/v1/secrets"
authorization_header="Authorization: $cli_akyos_key"
secrets_response=$(curl -s -H "$authorization_header" "$secrets_url")

while [[ "$secrets_response" == *"Unauthorized"* ]]; do
    echo "[!] La clé d'authentification est incorrecte. Veuillez réessayer."
    echo "[*] Veuillez entrer votre clé d'authentification cli.akyos :"
    echo "(https://mon-agence-web.io/app/projects/profile/5c0635f15dbba50004b2a3a7 - ctrl + f - cli.akyos)";
    read -r cli_akyos_key
    authorization_header="Authorization: $cli_akyos_key"
    secrets_response=$(curl -s -H "$authorization_header" "$secrets_url")
done

wpmudev_api_key=$(echo "$secrets_response" | grep -o '"wpmudev_api_key":"[^"]*' | sed 's/"wpmudev_api_key":"//')
acf_pro_key=$(echo "$secrets_response" | grep -o '"acf_pro_key":"[^"]*' | sed 's/"acf_pro_key":"//')
echo "[*] Clés WPMU_DEV_API_KEY et ACF_PRO_KEY récupérées !"

sed -i "s/\"WPMUDEV_API_KEY\": \"\"/\"WPMUDEV_API_KEY\": \"$wpmudev_api_key\"/g" "$HOME/.aky/config.json"
sed -i "s/\"ACF_PRO_KEY\": \"\"/\"ACF_PRO_KEY\": \"$acf_pro_key\"/g" "$HOME/.aky/config.json"

echo "[*] Configuration terminée !"