Languages: English (README.en.txt) | Italiano (README.it.txt) | Español (README.es.txt) | Français (README.fr.txt) | Deutsch (README.de.txt)

CUTITO - télécharge une vidéo YouTube, découpe-la et convertis-la en MP4
========================================================================

INSTALLATION (une seule fois)
-----------------------------
1. Python 3.9 ou plus récent : https://www.python.org/downloads/
   Dans l'installateur, coche "Add python.exe to PATH".
2. ffmpeg : ouvre PowerShell ou l'invite de commandes et lance
       winget install Gyan.FFmpeg
   Puis FERME et rouvre le terminal (sinon il ne voit pas ffmpeg).
3. Extrais tout le zip dans un dossier quelconque (ex. Documents\Cutito).

UTILISATION
-----------
1. Double-clic sur start.bat (la première fois il télécharge les dépendances, environ une minute).
2. La fenêtre de Cutito s'ouvre.
3. Colle le lien, indique début/fin (ex. 1:30 et 3:30), choisis 720p, clique sur
   "Télécharger et convertir".
4. À la fin, clique sur "Télécharger le MP4" ou "Ouvrir le dossier de sortie".
   Les fichiers restent dans le dossier "output" à côté de app.py.

LANGUE
------
Le menu de langue est en haut à droite (Italiano, English, Español, Français,
Deutsch). Au départ il utilise la langue du système ; ton choix est mémorisé.

RÉGLAGES PAR DÉFAUT (pensés pour analyser les coups de pied)
------------------------------------------------------------
- MP4, codec H.264, résolution maximale 720p
- Audio supprimé (coche la case pour le garder)
- Fréquence d'images d'origine conservée : une vidéo à 50/60 ips reste à 50/60

FENÊTRE DÉDIÉE
--------------
Cutito s'ouvre dans sa propre fenêtre (sans barre d'adresse ni onglets), via Edge ou
Chrome en "mode application". Quand tu fermes la fenêtre, l'application s'arrête.
L'adresse interne est cutito.localhost:5000 (*.localhost pointe toujours vers ton PC,
sans droits administrateur).
Si ni Edge ni Chrome n'est trouvé, elle ouvre le navigateur par défaut dans un onglet normal.
Pour forcer un autre navigateur Chromium, définis CUTITO_BROWSER avec le chemin de son exe.

SANS FENÊTRE NOIRE
------------------
Quel que soit le mode de lancement, l'application s'arrête toute seule quand tu fermes
la fenêtre. Si elle télécharge ou convertit encore, elle termine le travail (le fichier
reste dans output) puis se ferme. Si tu la rouvres alors qu'elle tourne encore, elle
rouvre simplement la fenêtre sur l'instance active.

Option A - Cutito.exe (un seul fichier)
  1. Double-clic sur build_exe.bat (une fois ; une ou deux minutes).
  2. Tu obtiens Cutito.exe dans le dossier : double-clic et ça démarre, sans fenêtres.
  3. Les vidéos vont dans Vidéos\Cutito. Si tu utilisais Clipper, les anciennes vidéos
     sont restées dans Vidéos\Clipper. Ferme l'ancien Clipper.exe : il utilise le même port (5000).
  4. L'exe a l'icône du chaton (cutito.ico doit rester à côté de build_exe.bat).
     Si Windows affiche encore l'ancienne icône, c'est le cache de l'Explorateur :
     redémarre-le ou déplace l'exe dans un autre dossier.
  5. ffmpeg reste nécessaire : winget install Gyan.FFmpeg, ou place ffmpeg.exe et
     ffprobe.exe à côté de Cutito.exe.
  L'exe contient une copie "figée" de yt-dlp. Quand YouTube la casse : relance
  build_exe.bat (met à jour et reconstruit) ou place yt-dlp.exe à côté de Cutito.exe
  (github.com/yt-dlp/yt-dlp/releases) : s'il est là, l'application l'utilise.
  Les exe PyInstaller déclenchent parfois de fausses alertes antivirus : c'est un
  faux positif connu de cette méthode.

Option B - sans créer l'exe : start_silent.vbs
  Double-clic : démarre sans fenêtre noire (lance start.bat au moins une fois avant).

Si quelque chose ne démarre pas et que tu ne vois aucune erreur, consulte le journal :
  %TEMP%\Cutito\cutito.log

COMMENT SAVOIR SI ÇA AVANCE
---------------------------
- Sous la barre tu vois le temps écoulé, les Mo sur le disque et la dernière ligne de
  yt-dlp/ffmpeg. Si les Mo augmentent, il télécharge.
- Avec début/fin la barre est "animée" pendant le téléchargement : c'est normal. Le
  vrai pourcentage apparaît pendant la conversion.
- ETA = temps restant estimé, une simple estimation. Dans un téléchargement "normal" la
  vidéo et l'audio sont deux fichiers : % et ETA repartent de 0 à la seconde piste.
- Si rien ne change pendant 45 secondes, un avertissement orange apparaît.

PROBLÈMES COURANTS
------------------
- "yt-dlp a échoué" : YouTube change souvent. Relance start.bat (il met à jour yt-dlp).
- "Sign in to confirm you're not a bot" ou erreurs 403 : réessaie plus tard ou autrement.
- Le programme ne fonctionne que sur ton propre PC (127.0.0.1).

NOTES
-----
Utilise-le uniquement pour des vidéos à toi ou que tu as le droit de télécharger.
Télécharger le contenu d'autrui sans autorisation enfreint les conditions de YouTube.
