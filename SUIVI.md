### 14/02/2025 - TH1
- (Dorian + Timothée + Alex + Alexis) : Discussion avec l'encadrant pour présenter les objectifs du projets et les ressources existantes

### 18/02/2025 - TH2/TH3
- (Dorian) : Création du fichier SUIVI.md. Création des dossiers personnels. Création du dossier global.

### 19/02/2025
- (Alexis) : Remplacement des dossiers personnels par des branches personnelles.

### 20/02/2025
- (Dorian) : Ajout du planning (fichier PLANNING.md et PLANNING.pdf)

### 21/02/2025
- (Dorian) : Modification de PLANNING.md pour répondre aux attentes de formatage. 

### 04/03/2025 - TH3/TH4
- discussion avec notre encadrant pour une meilleure compréhension des différentes étapes de l'algorithme.
- brainstorm avec l'encadrant quant à la partie intersection gradients-contour
- lecture du code (Python) déjà existant : sur conseil de l'encadrant, nous avons décidé d'ignorer l'implémentation déjà existante (codée à la va-vite)
- donc nous repartons avec une implémentation "from scratch" de l'algorithme, cette fois en C++
- répartition des taches à faire chez soi pour la prochaine séance

### 11/03/2025 - WEEK 3 
- (Dorian et Timothée) : ont regardé le fonctionnement de Blender et des plugs-in 
- (Alexis) : a fait un cours de C++ de OpenCourseWar pour pouvoir coder la suite du projet en C++
- (Alex) : a fait l'implementation de la fonction distance d2 en C++



### 13/03/2025 
- (Alexis) : apprentissage de C++ terminé : passage au code des ribs avec Alex

### 18/03/2025 WEEK 4
- (Groupe entier) : Entretient avec l'encadrant pour faire un point sur l'avancée du projet
- (Alexis + Alex) : Implémentation de la fonction d2 en C++. Le debug est encore à réaliser
- (Dorian + Timothée) : Premier programme Python pour tester les différentes fonctionnalités offertes par l'API Blender et prototype d'IHM

### 25/03/2024 WEEK 5
- (Groupe entier) : Entretient avec l'encadrant pour faire un point sur l'avancée du projet
- (Alexis) : Implémentation du détourrage d'image avec canny
- (Alex) : Débuggage réussi de la fonction d2
- (Dorian) : Implantation Blender du programme permettant de générer le volume grâce aux extrémités des ribs

### 30/03/2025 :
- (Alexis) Début d'implémentation de intersect 
- (Alex, Dorian, Alexis) : concertation sur les returns et arguments des fonctions pour un mise en commun possible des codes
- (Dorian + Timothée) : Première tentative de création de l'UI Blender via fenêtre contextuelle + fonction intégrée à l'API "bpy" : échec car l'API ne permet pas de créer des boutons personnalisées dans une fenêtre contextuelle personnalisée

### 08/04/2025 :
- (Dorian + Timothée) : Nouvelle tentative de création de l'UI Blender : usage d'une scène vide avec blocage caméra + blf (texte) + gpu (image) --> Succès
- (Alex) : debut de l'élaboration d'un meilleur algorithme pour la fonction d2_grad

### 15/04/2025 :
- (Dorian + Timothée) : Première version prête à l'emploi de l'UI : bouton de loading d'image, de dessin, de fermeture de la fenêtre et de validation. 
- (Alex) : deux alternatives à d2grad (avec courbe de bézier quadratique / cubique)

### 18/04/2025 :
- (Alexis) : implémentation du calcul des gradients successifs pour intersecter 

### 22/04/2025 :
- (Alexis) : implémentation du choix basique des départs des stings (gauche et droite) et algo fonctionnel pour les ribs de droite avec gradient.

### 05/05/2025 :
- (Groupe entier) Réunion pour regarder les codes et avancer/débuguer certains codes
- (Dorian + Timothée) Finalisation de l'UI : ajout du mode de dessin "main levée" et améliorations visuelles.
- (Alexis) : debug intensif de la partie "lofting". Choix plus pertinent des points gauche et droite de départ. Calcul des intersections entre gradient et canny edge pour les ribs gauche et droites (et tout fonctionne !)
- (Alex) : meilleure alternative à d2grad (avec smooth min) et debug
- (Timothée) : début des recherches pour le rapport sur les enjeux sociaux et environnementaux de notre projet
- (Dorian) : début de la rédaction du rapport

## 12/05/2025 :
- (Dorian) : Nettoyage du code dans l'objectif d'implémenter une nouvelle UI servant à modifier les points résultants du programme de création de spine.