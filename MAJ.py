import re
import requests

# URL du fichier M3U hébergé sur Netlify
m3u_url = 'https://ric-iptv.netlify.app/combined.m3u'

# Télécharger le fichier M3U
response = requests.get(m3u_url)
m3u_content = response.text

# URL de l'API pour obtenir les nouveaux liens
api_url = 'https://iptv-org.github.io/api/channels.json'

# Fonction pour obtenir les nouveaux liens depuis l'API
def get_new_links(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # L'API renvoie un JSON avec les informations des chaînes
    else:
        print("Erreur lors de la récupération des nouveaux liens")
        return []

# Obtenir les nouveaux liens depuis l'API
channels = get_new_links(api_url)

# Créer un dictionnaire de remplacements de liens
link_replacements = {}
for channel in channels:
    if 'url' in channel and 'name' in channel:
        link_replacements[channel['name']] = channel['url']

# Fonction pour mettre à jour les liens
def update_links(content, replacements):
    for name, new_link in replacements.items():
        # Utiliser une expression régulière pour trouver les lignes contenant le nom de la chaîne
        content = re.sub(r'(.*' + re.escape(name) + r'.*http[^\s]+)', lambda match: match.group(1).replace(match.group(1).split()[-1], new_link), content)
    return content

# Afficher le contenu M3U avant la mise à jour
print("Contenu M3U avant mise à jour:")
print(m3u_content)

# Mettre à jour les liens dans le contenu M3U
updated_m3u_content = update_links(m3u_content, link_replacements)

# Afficher le contenu M3U après la mise à jour
print("Contenu M3U après mise à jour:")
print(updated_m3u_content)

# Enregistrer le fichier M3U mis à jour
with open('combined.m3u', 'w', encoding='utf-8') as file:
    file.write(updated_m3u_content)

print("Le fichier M3U a été mis à jour.")
