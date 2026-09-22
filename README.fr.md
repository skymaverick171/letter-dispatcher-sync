# Letter Dispatcher — édition Sync

Carnet d'adresses + lettres prêtes à l'emploi + envoi en un clic via Gmail ou Outlook — la même application de base que [Letter Dispatcher (LIGHT)](https://skymaverick171.github.io/letter-dispatcher/), avec en plus un onglet **Sync** qui récupère vos Contacts et vos Lettres directement depuis une feuille Google Sheets.

**Application en ligne :** cette page, une fois GitHub Pages activé pour ce dépôt (voir ci-dessous) — `https://<votre-nom-utilisateur>.github.io/letter-dispatcher-sync/`

## Ce qui diffère de LIGHT

Tout ce que fait LIGHT, plus un onglet **Sync** :

- Connexion avec votre propre compte Google (aucun serveur impliqué — la connexion et la synchronisation se font entièrement dans votre navigateur).
- Un clic récupère à la fois vos feuilles Contacts et Lettres dans l'application.
- **À sens unique pour l'instant** : la feuille met à jour l'application, jamais l'inverse. La synchronisation bidirectionnelle est prévue pour une version ultérieure.
- Rien n'est envoyé ailleurs. Votre jeton de connexion Google reste uniquement en mémoire dans l'onglet du navigateur et n'est jamais enregistré — fermer l'onglet vous déconnecte.

## Configuration initiale (une fois, par une personne)

1. **Créez un projet Google Cloud** et un **ID client OAuth 2.0** (type « Application Web ») dans la [Google Cloud Console](https://console.cloud.google.com/). Ajoutez l'URL exacte de ce site comme **origine JavaScript autorisée** (par ex. `https://<votre-nom-utilisateur>.github.io`).
2. Ouvrez l'onglet **Sync** de l'application, collez cet **ID client**, l'**ID de la feuille** Google Sheets (la longue chaîne dans l'URL de la feuille, entre `/d/` et `/edit`), et la feuille/plage pour les Contacts (par ex. `Contacts!A:D`) et les Lettres (par ex. `Letters!A:E`).
3. Cliquez sur **Enregistrer les paramètres**, puis **Se connecter avec Google**, puis **Synchroniser maintenant**.

La disposition des colonnes est identique à l'import par copier-coller/CSV déjà existant dans LIGHT : Contacts = Nom, Email, Bureau, Groupe ; Lettres = Objet, Corps, Cc, Cci, Personnaliser (oui/non).

## Structure du dépôt

```
index.html   — l'application (c'est ce que GitHub Pages sert)
sw.js        — support hors-ligne / éligibilité à l'installation PWA
docs/        — guides (ajoutés au fur et à mesure)
```

## Déployer une mise à jour

Ce dépôt n'a pas d'étape de build — `index.html` est l'application entière. Pour la mettre à jour : remplacez `index.html` à la racine du dépôt par la nouvelle version et validez (commit). GitHub Pages la prend en compte automatiquement en une à deux minutes.

---
Voir aussi : [Letter Dispatcher (LIGHT)](https://github.com/skymaverick171/letter-dispatcher) — l'édition de base dont celle-ci est dérivée.
