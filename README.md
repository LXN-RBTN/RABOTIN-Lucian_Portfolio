# Portfolio Lucian Rabotin — version corrigée

## Pourquoi ta capture affichait une page bizarre ?
Le rendu « Thank you for trying it out / Counter is 0 » vient d'un projet de démarrage différent. Dans le dossier portfolio, les fichiers CSS/JS manquaient également, donc le navigateur affichait le HTML sans mise en forme. Cette version remet le CSS, le JavaScript, les données et un index propre.

## Lancer
Ouvre ce dossier dans VS Code puis utilise Live Server sur `index.html`.

## Veille cyber
24 vrais articles sont dans `data/cyber-articles.json`. La page `veille-cyber.html` permet la recherche et les filtres.

## Automatisation
`scripts/update-cyber.py` montre une automatisation RSS -> Python -> JSON. Installe `feedparser` avec `py -m pip install feedparser` puis lance `py scripts/update-cyber.py`.

## À compléter
- tes liens GitHub/LinkedIn ;
- ton e-mail/téléphone/ville ;
- ton CV dans `assets/documents/CV-Lucian-Rabotin.pdf` ;
- ta photo ;
- tes 24 articles 5G/6G.


## Veille : 48 articles

`data/cyber-articles.json` contient 24 articles cybersécurité.
`data/5g-6g-articles.json` contient 24 articles 5G / 6G.

Chaque article comporte une date, une catégorie, un titre, une source,
un lien, un résumé, une idée d'image (`image_prompt`) et une phrase
courte de mise en avant (`featured_text`).

Les articles 5G/6G suivent une progression volontaire :
histoire de la 5G → déploiement en France → transition vers la 6G →
IMT-2030 → IA, ISAC, satellites, sécurité, automatisation et
standardisation.


## Informations personnelles renseignées

- Lucian Rabotin
- BTS SIO, option SISR, 2ème année
- Lycée Paul Sabatier, Carcassonne
- Bac Pro SN, option C
- Lycée La Salle, Alès
- Email : lucian.rabotin@gmail.com

La localisation personnelle n'est pas affichée dans la page Contact.

## Mentions légales

Une page `mentions-legales.html` est incluse. Elle indique l'éditeur,
le directeur de publication, l'adresse email, la propriété des contenus,
la gestion du stockage local et les informations à compléter concernant
l'hébergeur. L'adresse personnelle n'est volontairement pas affichée.


## Sécurité et conformité technique

Le portfolio est statique et ne possède pas de base de données ni de
comptes utilisateurs.

Protections prévues :
- HTTPS/TLS 1.2 ou 1.3 en production ;
- HSTS à activer après validation complète du HTTPS ;
- Content-Security-Policy ;
- X-Content-Type-Options ;
- X-Frame-Options ;
- Referrer-Policy ;
- Permissions-Policy ;
- absence d'indexation des répertoires ;
- blocage de plusieurs fichiers de configuration/développement ;
- `security.txt` pour le signalement de vulnérabilités ;
- `noopener noreferrer` sur les liens externes ouverts dans un nouvel onglet ;
- pas de formulaire connecté à un serveur dans cette version ;
- pas de service publicitaire ou de suivi tiers.

### Vérifications avant mise en ligne

1. Activer HTTPS avec un certificat valide.
2. Décommenter HSTS dans `.htaccess` uniquement après validation du HTTPS.
3. Vérifier que les en-têtes HTTP de sécurité sont bien envoyés.
4. Vérifier les liens et les fichiers publiés.
5. Tester le site avec un outil d'audit comme OWASP ZAP.
6. Mettre régulièrement à jour le code et contrôler les dépendances.

La configuration ne doit pas être présentée comme une garantie absolue :
la sécurité dépend également de l'hébergeur, du DNS, du TLS, des mises
à jour et de la configuration réellement appliquée en production.

## Images à ajouter
- Photo personnelle : `assets/images/photo-moi.jpg`
- Veille cybersécurité : `assets/images/veille/cyber-01.jpg` à `cyber-24.jpg`

Les images de cybersécurité sont référencées directement par le site avec ces noms.
