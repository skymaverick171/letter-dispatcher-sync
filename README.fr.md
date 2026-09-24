# Letter Dispatcher — édition Sync

Carnet d'adresses + lettres prêtes à l'emploi + envoi en un clic via Gmail ou Outlook — la même application de base que [Letter Dispatcher (LIGHT)](https://skymaverick171.github.io/letter-dispatcher/), avec en plus un onglet **Sync** qui récupère vos Contacts et vos Lettres directement depuis une feuille Google Sheets.

**Application en ligne :** cette page, une fois GitHub Pages activé pour ce dépôt (voir ci-dessous) — `https://<votre-nom-utilisateur>.github.io/letter-dispatcher-sync/`

## Ce qui diffère de LIGHT

Tout ce que fait LIGHT, plus un onglet **Sync** :

- Connexion avec votre propre compte Google (aucun serveur impliqué — la connexion et la synchronisation se font entièrement dans votre navigateur).
- Un clic récupère à la fois vos feuilles Contacts et Lettres dans l'application.
- **Bidirectionnelle pour les administrateurs, à sens unique pour tout le monde**. Le fait que « Synchroniser maintenant » renvoie aussi les modifications locales vers la feuille, ou se contente de les récupérer (comme à l'Étape 1), dépend de la présence du compte Google connecté dans la liste des administrateurs de la feuille — voir ci-dessous.
- Chaque contact peut avoir un numéro de téléphone, avec un bouton 📞 Appeler à côté de tout contact qui en a un — il ouvre l'application téléphone de votre appareil si une est disponible.
- Rien n'est envoyé ailleurs. Votre jeton de connexion Google reste uniquement en mémoire dans l'onglet du navigateur et n'est jamais enregistré — fermer l'onglet vous déconnecte.

## Configuration initiale (une fois, par une personne)

1. **Créez un projet Google Cloud** et un **ID client OAuth 2.0** (type « Application Web ») dans la [Google Cloud Console](https://console.cloud.google.com/). Ajoutez l'URL exacte de ce site comme **origine JavaScript autorisée** (par ex. `https://<votre-nom-utilisateur>.github.io`).
2. Dans votre feuille Google, ajoutez une **colonne ID** cachée à la fin de chaque feuille de données — colonne **F** pour Contacts comme pour Lettres (déjà présente si vous partez des modèles fournis). Laissez-la vide pour les lignes existantes ; l'application la remplit elle-même la première fois que chaque ligne est synchronisée. N'y écrivez rien à la main.
3. Optionnel, pour la synchro bidirectionnelle : ajoutez une feuille/onglet nommé **Admins** avec un email de compte Google par ligne (colonne A). Tout compte absent de cette liste reste en synchro à sens unique (lecture seule), quoi qu'il arrive — c'est un confort, pas une vraie sécurité, puisqu'il s'agit d'un site statique sans serveur pour l'imposer.
4. Ouvrez l'onglet **Sync** de l'application, collez cet **ID client**, l'**ID de la feuille** Google Sheets (la longue chaîne dans l'URL de la feuille, entre `/d/` et `/edit`), la feuille/plage pour les Contacts (par ex. `Contacts!A:F`) et les Lettres (par ex. `Letters!A:F`), et — si vous en avez créé une — la feuille/plage des Admins (par ex. `Admins!A:A`).
5. Cliquez sur **Enregistrer les paramètres**, puis **Se connecter avec Google** (les comptes déjà autorisés sous les permissions plus restreintes de l'Étape 1 devront réapprouver — la synchro bidirectionnelle a besoin d'un accès en écriture, pas seulement en lecture), puis **Synchroniser maintenant**.

Disposition des colonnes : Contacts = Nom, Email, Bureau, Groupe, Téléphone, ID ; Lettres = Objet, Corps, Cc, Cci, Personnaliser (oui/non), ID.

### Si vous aviez déjà configuré la synchro des Contacts avant cette mise à jour

La feuille Contacts a gagné une colonne **Téléphone**, insérée juste avant la colonne ID existante — la colonne ID passe donc de **E** à **F**. Dans Google Sheets, faites un clic droit sur l'en-tête de votre colonne ID actuelle et choisissez **Insérer 1 colonne à gauche** ; cela ouvre une colonne E vide pour le téléphone et décale vos valeurs ID existantes vers F sans les modifier (rien n'est renuméroté ni perdu). Mettez ensuite à jour la plage Contacts dans l'onglet Sync de l'application, de `…!A:E` à `…!A:F`. Les Lettres ne sont pas concernées.

### Comment la synchro bidirectionnelle décide

Google Sheets n'ayant pas d'horodatage de « dernière modification » par ligne, l'application garde son propre relevé (dans ce navigateur uniquement) de ce qu'elle a vu en dernier pour chaque contact/lettre. À chaque « Synchroniser maintenant », elle compare ce relevé à l'état actuel de l'application et à l'état actuel de la feuille :

- Changé seulement ici → envoyé vers la feuille.
- Changé seulement dans la feuille → récupéré dans l'application.
- Changé des deux côtés, vers des valeurs différentes → on vous demande laquelle garder, une par une.
- Supprimé ici, ou supprimé dans la feuille → **jamais propagé dans un sens ou dans l'autre** — l'application ne supprime pas la ligne de la feuille, et la feuille ne supprime pas l'enregistrement de l'application. Cela évite qu'une suppression accidentelle d'un côté ne se répercute en cascade, mais une suppression volontaire doit être répétée à la main de l'autre côté.

Ce relevé vivant dans le stockage local du navigateur, il est propre à chaque appareil — le même comportement « ça marche sur mon ordinateur mais pas sur mon téléphone tant que je ne m'y suis pas connecté aussi » que pour les réglages de l'Étape 1.

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
