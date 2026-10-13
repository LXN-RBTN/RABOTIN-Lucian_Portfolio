# Checklist de sécurité du portfolio

Cette checklist documente les mesures techniques du projet.

## Code et navigateur
- [x] Content Security Policy prévue
- [x] X-Content-Type-Options
- [x] X-Frame-Options
- [x] Referrer-Policy
- [x] Permissions-Policy
- [x] Protection des liens `target="_blank"`
- [x] Pas de scripts tiers nécessaires
- [x] Pas de base de données
- [x] Pas d'authentification
- [x] Pas de mot de passe dans le projet

## Serveur
- [x] Configuration Apache fournie
- [x] Configuration Nginx fournie
- [x] HSTS prévu mais volontairement non activé en local
- [x] HTTPS/TLS obligatoire en production
- [x] Listing des répertoires désactivé
- [x] Fichiers de développement bloqués

## Vie privée
- [x] Adresse personnelle non publiée
- [x] Formulaire de contact non connecté à un serveur
- [x] Pas d'outil d'analyse tiers
- [x] Gestion des cookies documentée
- [x] Mentions légales présentes

## À faire au moment de l'hébergement
- [ ] Installer un certificat TLS valide
- [ ] Activer HSTS
- [ ] Renseigner l'hébergeur dans les mentions légales
- [ ] Tester les en-têtes HTTP
- [ ] Tester le site avec OWASP ZAP
- [ ] Vérifier les permissions des fichiers
- [ ] Vérifier les sauvegardes et la configuration DNS

> Aucune configuration ne rend un site « 100 % sécurisé ». Cette
> checklist vise les bonnes pratiques applicables à ce portfolio
> statique et doit être validée avec la configuration réelle de
> l'hébergement.
