---
title: Mon App Dash
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
python_version: 3.10.11
app_file: app.py
pinned: false
---

# Obésité mondiale : Inégalités, causes et impacts

Projet réalisé par un groupe de 6 étudiants dans le cadre du cours **INF8088E - Data Visualization** enseigné à Polytechnique Montréal

La vocation de ce panorama visuel est de rendre compte de manière objective des données actualisées sur l'obésité, sa prévalence, ses causes et les politiques publiques envisageables pour en juguler la croissance.

## Sommaire
 
- [Application](#application)
- [Équipe](#équipe)
- [Persona](#persona)
- [Visualisations](#visualisations)
- [Sources de données](#️sources-de-données)
- [Stack technique](#️stack-technique)
- [Installation locale](#installation-locale)
- [Structure du projet](#structure-du-projet)
- [Licence](#licence)

<a id="application"></a>
## Application

L'application est accessible en ligne à l'adresse suivante :
[https://alexdrmt-mon-app-dash.hf.space/](https://alexdrmt-mon-app-dash.hf.space/)

Le Space Hugging Face se met en veille après 48h d'inactivité. Si l'application n'est pas accessible immédiatement, cliquez sur **"Run this Space"** et patientez 1 à 2 minutes.

<a id="équipe"></a>
## Équipe

- Alexandre D.
- Alexandre V.
- Aly A.
- Benoît D.
- Morad B.
- Yasmine B.

<a id="persona"></a>
## Persona

Notre visualisation est destinée aux différents acteurs publics qui participent à la compréhension du phénomène de l'obésité et sa prise en charge à l'échelle nationale. Plus particulièrement, nous visons les organismes gouvernementaux, les ONG ou les institutions internationales qui conçoivent et évaluent les politiques de prévention afin de réduire les effets délétères de l’obésité sur les sociétés. 

<a id="visualisations"></a>
## Visualisations

Notre application prend la forme d’un scrollitelling dans lequel se succèdent des visuels variés (carte, carte de chaleur, diagrammes en barres…) et interactifs à la fois portés par des explications factuelles et permettant l’exploration libre des données par l’utilisateur final. La vocation de ces visuels est de fournir un support de réflexion permettant de comparer, contextualiser et décider de la marche à suivre en termes de politiques publiques de lutte contre l’obésité.

- **Carte choroplèthe** : répartition mondiale de la prévalence de l'obésité
- **Connected Dot Plot** : classement des pays selon leur taux d'obésité
- **Stacked Area Chart** : évolution de la distribution de la population suivant 4 catégories d'IMC (Indice de Masse Corporelle) entre 1980 à 2024
- **Line Chart** : comparaison de l'évolution de de la prévalence de l'obésité entre pays
- **Bubble chart animé** : relation entre PIB par habitant, dépenses de santé et obésité par groupe de revenus, avec animation temporelle entre 2000 et 2020
- **Heatmaps de corrélation** : lien entre obésité et indicateurs socio-économiques/comportementaux (Gini, apports caloriques, sédentarité)
- **Slope charts** : évolution temporelle de la composition alimentaire et de la prévalence de l'obésité par pays
- **Dumbbell chart** : comparaison des coûts actuels et à l'horizon 2060 de l'obésité selon différents pays
- **Bar chart** : rentabilité des politiques publiques de prévention de l'obésité

<a id="sources-de-données"></a>
## Sources de données

Pour la réalisation de ce projet, nous nous sommes appuyés sur un corpus de jeux de données que nous avons nous-mêmes constitué à partir de diverses sources :

- Synthèse de la prévalence du surpoids et de l'obésité chez l'adulte – Observatoire mondial de l'obésité [World Obesity Federation](https://data.worldobesity.org/tables/prevalence-of-adult-overweight-obesity-2/)\
Ce jeu de données agrège les données relatives à la prévalence du surpoids et de l'obésité dans le monde entier, par pays et niveau de richesse de ces pays. Ces données sont le résultat de la compilation d'enquêtes nationales ou régionales. 

- Estimation statistique de la répartition de l'indice de masse corporelle – NCD Risk Factor Collaboration [NCD-RisC](https://www.ncdrisc.org/data-downloads-adiposity.html)\
Ces données ont été publiées en 2026 et sont issues de travaux de recherche publiés dans la revue Nature. Ce sont des estimations statistiques réalisées sur des échantillons moins exhaustifs que les enquêtes utilisées par la World Obesity Federation. Elles apportent une dimension supplémentaire en fournissant des chiffres historiques complets depuis 1980 pour tous les pays du monde.

- Composition du régime alimentaire moyen par pays [Our World in Data](https://ourworldindata.org/diet-compositions)\
Cette page regroupe un ensemble de jeux de données sur l'alimentation quotidienne moyenne par pays (apport calorique journalier ventilé par groupe d'aliments : céréales, viande, produits laitiers, fruits et légumes, sucres, huiles et graisses, etc.) sur la période 1961-2023. Ces données, rendues disponibles à tous entre 2024 et 2025, permettent d'étudier l'impact de la composition de l'assiette sur la prévalence de l'obésité. 

- Prévalence du manque d'activité physique par sexe et par pays [Organisation mondiale de la Santé](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-insufficient-physical-activity-among-adults-aged-18-years-(age-standardized-estimate)-(-))\
Ce jeu de données est tiré d’une étude The Lancet publiée en 2024 et à été constitué à l’aide d’un groupe représentatif de 5,7 millions d’individus interrogés à travers le monde. Il donne la part d'habitants de chaque pays qui ne pratique pas une activité physique quotidienne minimale recommandée par l'OMS, depuis l'an 2000. Il permet de comparer l'impact de la pratique d'une activité physique sur la prévalence de l'obésité. 

- Indicateurs économiques – [Banque mondiale](https://donnees.banquemondiale.org/)\
Différents indicateurs économiques (mesurés sur la période 2023-2024) ont été réunis pour constituer un jeu de données permettant de comparer les situations économiques et les politiques de santé publique entre pays : PIB en parité de pouvoir d'achat par habitant, dépenses de santé par habitant, indice de Gini pour les inégalités de richesse, etc.

- Projection des coûts économiques du surpoids à l'horizon 2060 – [OCDE](https://www.oecd.org/fr/topics/sub-issues/obesity-diet-and-physical-activity.html)\
Ces données projettent, pour chaque pays disponible, le coût économique annuel du surpoids et de l'obésité en 2060, exprimé à la fois en milliards de dollars US et en pourcentage du PIB. Elles servent à déterminer les politiques efficaces dans la lutte contre l'obésité.

Toutes les données utilisées sont accessibles sous des licences permettant leur réutilisation à des fins non commerciales. Ceci inclut les usages pédagogiques, les réutilisations académiques ou à des fins de sensibilisation et d’information.

<a id="stack-technique"></a>
## Stack technique

- **Framework** : [Dash](https://dash.plotly.com/) (Python)
- **Visualisations** : Plotly
- **Traitement de données** : Pandas, scikit-learn
- **Déploiement** : Hugging Face Spaces (via Docker + GitHub Actions)

<a id="installation-locale"></a>
## Installation locale

```bash
# Cloner le repo
git clone https://github.com/USERNAME/REPO.git
cd REPO

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur [http://localhost:7860](http://localhost:7860).

<a id="structure-du-projet"></a>
## Structure du projet

```
.
├── assets/                  # Fichiers statiques de style (CSS)
├── data/                    # Jeux de données bruts et prétraités
├── data_preprocessing/      # Scripts de nettoyage et transformation des données
├── components/              # Composants de visualisation (un fichier par graphique)
├── sections/                # Sections de la page (scrollytelling)
├── app.py                   # Point d'entrée de l'application
├── Dockerfile                # Configuration du conteneur pour Hugging Face Spaces
├── requirements.txt          # Dépendances Python
└── README.md                 # Présent document
```

<a id="licence"></a>
## Licence

Projet académique réalisé dans le cadre du cours INF8808E à Polytechnique Montréal.
