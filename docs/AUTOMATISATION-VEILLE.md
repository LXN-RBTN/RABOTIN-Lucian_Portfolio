# Automatisation de la veille — BTS SIO SISR

## Statut
Cette fonctionnalité est proposée sur une branche séparée. Le site public et les articles actuels ne changent pas tant que la pull request n'est pas fusionnée.

## Fonctionnement
1. Tous les lundis à 08:00 (Europe/Paris), le workflow .github/workflows/veille.yml lit plusieurs flux RSS.
2. Il évite les URL déjà publiées et propose jusqu'à trois articles pour la cybersécurité et jusqu'à trois pour la 5G/6G.
3. Chaque suggestion apparaît comme une **Issue GitHub**. Elle contient source, lien, date et résumé RSS (pas de résumé IA inventé).
4. Le propriétaire du dépôt commente exactement **oui** ou **non** dans l'Issue.
5. **non** : l'Issue est fermée sans modification du site.
6. **oui** : si le quota hebdomadaire du thème est disponible, le script met à jour le JSON, le JSON intégré à la page HTML et le registre data/veille-publications.json, puis publie avec GitHub Pages.
7. L'Issue est fermée seulement une fois la publication réussie.

**Quota :** un seul article accepté par thème et par semaine civile ISO, du lundi au dimanche, sur la base de l'heure française. Les articles existants restent inchangés.

## Configuration GitHub à effectuer par le propriétaire
- Settings → Actions → General → Workflow permissions : autoriser **Read and write permissions** pour GITHUB_TOKEN (sinon créations d'Issues et push refusés).
- Settings → Pages → Build and deployment → Source : sélectionner **GitHub Actions** pour que le workflow déploie le site après validation.
- Settings → Actions : vérifier que les Actions sont autorisées. Le workflow doit exister sur la branche principale pour que les recherches planifiées et commentaires le déclenchent.
- Un GitHub Actions **workflow_dispatch** permet de lancer une collecte manuellement via Actions → Veille hebdomadaire avec validation → Run workflow.

## Images et résumés
Le workflow ne copie jamais les images de journaux : les nouveaux articles utilisent des SVG originaux génériques du dépôt (veille-cyber.svg et veille-5g.svg). Remplacer, si souhaité, par une photo dont la licence a été vérifiée.

Les résumés proviennent du flux RSS et **ne sont ni traduits ni vérifiés automatiquement**. Le propriétaire doit consulter le texte et la source avant de répondre oui ; pour personnaliser le résumé avant publication, il faut améliorer le pipeline ou corriger la proposition et les fichiers avant fusion. Les liens de Google News peuvent mener à des redirections : contrôler la destination finale.

## Dépannage
- Aucune proposition : vérifier les logs Actions, les flux accessibles et les doublons.
- Permission denied (403) : revoir les droits du GITHUB_TOKEN dans les réglages du dépôt.
- GitHub Pages refuse le déploiement : sélectionner GitHub Actions comme source de publication.
- Les Actions planifiées peuvent subir des retards ; GitHub peut désactiver le planning après 60 jours d'inactivité du dépôt public.
- Si le déploiement échoue après le commit, l'article est déjà dans la branche principale : inspecter Actions et relancer le déploiement ; ne pas donner un second oui pour contourner le quota.

## Technique
- scripts/weekly_veille.py : collecte (propose), traitement des réponses (respond).
- data/cyber-articles.json et data/5g-6g-articles.json : données publiées.
- veille-cyber.html et veille-5g-6g.html : JSON intégré utilisé par js/veille.js.
- data/veille-publications.json : créé au premier accord pour empêcher deux publications par thème la même semaine.

Aucune clé personnelle / token GitHub ne doit être ajoutée aux fichiers du dépôt.
