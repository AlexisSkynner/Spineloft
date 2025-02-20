# Planning et répartition des tâches

Pour plus d’efficacité, nous nous sommes répartis en deux groupes :
- **Groupe 1** : Alex + Alexis (*Algorithmique*)
- **Groupe 2** : Timothée + Dorian (*Interface & Implémentation Blender*)

## Objectif du projet

L’objectif du projet est de produire un plugin Blender permettant à l’utilisateur de générer un modèle 3D simpliste à partir d’une image. 

### Fonctionnalités principales :
1. L’utilisateur tracera une **ligne directrice** suivant la forme de l’objet (*spine*).
2. Le plugin en déduira une **forme géométrique** représentative de l’objet (*rib cage*, composée de *ribs*).
3. Cette forme sera extrudée pour modéliser l’objet en 3D.

### Phases du projet
- **Phase 1** : Réalisation d’un prototype fonctionnel (*Évaluation intermédiaire : fin avril*).
- **Phase 2** : Amélioration du prototype (*Évaluation finale : fin juin*).
- **Livrable final** : Plugin documenté et user-friendly, publié avant la fin de l’année scolaire.

## Planning détaillé

| Phase | Mois | Semaines | Tâches principales | Groupe |
|-------|------|---------|-------------------|--------|
| **P1 – Établissement d’un prototype** | **Février** | 1 | Rencontre avec l’encadrant et présentation des attentes du projet | 1 et 2 |
| | | 2 | Établissement du planning, répartition des tâches <br> Première lecture des ressources | 1 et 2 |
| | **Mars** | 3-4 | Étude du travail existant (*code et littérature*) <br> Choix des algorithmes (*détection des bords, distance function*) <br> Algorithme d’optimisation des ribs | 1 |
| | | 3-4 | Familiarisation avec l’API Blender <br> Recherche d’une bibliothèque d’interface | 2 |
| | | 3-4 | Rédaction du cahier des charges et spécifications techniques | 1 et 2 |
| | | 5-6 | Implémentation de la génération de ribs et optimisation | 1 |
| | | 5-6 | Création de l’IHM (*Tracer le spine, Modifier les ribs*) <br> Intégration à Blender | 2 |
| | **Avril** | 7-8 | Intégration des fonctionnalités, fusion des codes <br> Sélection d’un jeu de données de test <br> Premiers tests et debug | 1 et 2 |
| | | 9 | Derniers tests et validation du prototype <br> Séance d’évaluation intermédiaire | 1 et 2 |
| **P2 – Création du produit final** | **Mai** | 10 | Débriefing de l’évaluation intermédiaire <br> Réévaluation du cahier des charges | 1 et 2 |
| | | 11-13 | Optimisation des performances (*rapidité et robustesse*) | 1 |
| | | 11-13 | Amélioration de l’interface utilisateur (*ergonomie*) | 2 |
| | | 11-13 | Implémentation de fonctionnalités additionnelles (*à définir avec l’encadrant*) | 1 et 2 |
| | **Juin** | 14-15 | Intégration des nouvelles fonctionnalités, fusion des codes <br> Tests sur jeu de données complexe <br> Résolution des bugs | 1 et 2 |
| | | 14-15 | Rédaction de la documentation <br> Création du tutoriel d’utilisation <br> Publication du plugin | 1 et 2 |
| | | **27 juin** | **Présentation finale du projet** | 1 et 2 |
