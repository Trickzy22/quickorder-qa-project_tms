# Stratégie de test de QuickOrder V3.1

## Contexte

QuickOrder est un site de commande de repas développé en Flask avec une base SQLite. Il a une interface web et une API REST documentée dans Swagger. Je dois dire si l'application peut partir en production dans son état actuel.

Je n'avais pas le temps de tout tester avec la même profondeur, donc j'ai choisi de partir des risques. J'ai mis le plus d'effort là où un bug coûte de l'argent au client ou au restaurant, c'est-à-dire la commande, le paiement, le stock et les promotions.

## Périmètre

Ce que j'ai testé :

| Domaine | Fonctions | Par où |
|---|---|---|
| Authentification | inscription, connexion, accès client et admin | interface |
| Catalogue | liste des restaurants, recherche, filtres, tri | interface et API |
| Panier | ajout, changement de quantité, vidage, un seul restaurant par panier | interface |
| Coupons | validité, expiration, montant minimum, plafond | interface et API |
| Commande | checkout, adresse, minimum de commande, restaurant ouvert, stock | interface et API |
| Paiement simulé | carte, PayPal, espèces | interface et API |
| Suivi | liste des commandes, annulation, recommander | interface et API |
| Avis | publication d'un avis | interface |
| Administration | tableau de bord, changement de statut | interface |
| API | clé X-API-Key, codes HTTP, format des réponses, entrées invalides | Swagger |

## Hors périmètre

Je n'ai pas testé les points suivants, et je préfère le dire clairement plutôt que de laisser croire qu'ils sont couverts.

- La performance. L'application tourne sur le serveur de développement de Flask, des mesures de charge n'auraient pas de sens.
- Le paiement réel. Il est simulé, il n'y a pas de prestataire derrière.
- Les autres navigateurs et le mobile. Tout a été fait sur Edge en 1280 × 800.
- L'accessibilité.
- La sécurité en profondeur. J'ai fait quelques vérifications de base (accès aux pages protégées, redirection après connexion, en-têtes HTTP) mais ce n'est pas un test d'intrusion.
- L'installation. J'ai utilisé le Docker fourni sans le remettre en question.

## Parcours critiques

J'ai identifié sept parcours. Les quatre premiers sont ceux qui comptent le plus.

1. Chercher un restaurant, ouvrir son menu, ajouter au panier. Sans ça il n'y a aucune vente.
2. Aller du panier jusqu'à la confirmation de commande. C'est le moment où le client paie.
3. Utiliser un coupon. Une réduction fausse touche directement le montant payé.
4. S'inscrire puis passer une première commande. C'est ce que fait tout nouveau client.
5. Suivre, annuler ou recommander une commande.
6. Créer une commande par l'API, pour les éventuels partenaires.
7. Changer le statut d'une commande côté administrateur.

## Risques

Les risques sont listés et notés dans [risk-matrix.md](risk-matrix.md). Dans les grandes lignes, je craignais surtout :

- une commande acceptée alors qu'elle ne peut pas être livrée (restaurant fermé, produit épuisé, pas d'adresse)
- un montant payé qui n'est pas le bon (double paiement, espèces insuffisantes, mauvaise réduction)
- des règles commerciales affichées mais pas appliquées, comme le minimum de commande
- des données qui deviennent incohérentes, par exemple un stock négatif
- un utilisateur qui accède aux commandes d'un autre
- une API qui ne se comporte pas comme l'interface

## Types de tests

| Type | Ce que ça donne ici |
|---|---|
| Nominal | les parcours de bout en bout quand tout va bien |
| Limites | quantités 0, 1, 20 et 21, stock + 1, montant minimum exact d'un coupon, mot de passe de 7 et 8 caractères |
| Erreurs | mauvais mot de passe, clé API absente ou fausse, identifiants qui n'existent pas, corps de requête mal formé |
| Règles métier | une règle par cas, vérifiée sur l'interface et sur l'API quand c'est possible |
| Sécurité de base | contrôle d'accès, paramètre next de la page de connexion, en-têtes |
| Exploratoire | recherche, console du navigateur, différences entre interface et API |
| Tests utilisateurs | 3 scénarios avec 2 personnes |

Les cas sont écrits dans [test-cases.xlsx](test-cases.xlsx). Je les ai exécutés avec un script, [run_campaign.py](../scripts/run_campaign.py), qui envoie les mêmes requêtes que le navigateur et Swagger et garde une trace de chaque réponse. Les bugs visibles à l'écran ont ensuite été reproduits dans Edge pour les captures. L'intérêt du script est de pouvoir tout relancer à l'identique une fois les corrections livrées.

## Priorisation

Chaque risque reçoit une note de probabilité et une note d'impact, de 1 à 4. Je multiplie les deux.

| Note | Niveau | Priorité | Ce que je teste |
|---|---|---|---|
| 12 à 16 | critique | P1 | nominal, limites, erreurs et règle métier, sur l'interface et l'API |
| 8 à 11 | élevé | P2 | nominal, règle métier, limites principales |
| 4 à 7 | modéré | P3 | nominal |
| 1 à 3 | faible | P4 | exploratoire s'il reste du temps |

J'ai exécuté les P1 en premier, puis les P2, puis le reste.

## Environnement et données

L'application est lancée avec `docker compose up` sur `http://127.0.0.1:5000`, Swagger est sur `/docs/`. La base est celle créée par `seed.py` : 6 restaurants dont un fermé, 25 produits dont 6 en rupture, 6 coupons dont un expiré.

J'ai utilisé les comptes fournis (alice et bob comme clients, admin comme administrateur) et la clé API `quickorder-demo-key`.

Pour repartir d'une base propre : `docker compose down -v` puis `docker compose up --build`.

## Critères

Pour commencer la campagne, il faut que l'application réponde sur `/health` et que la base soit dans son état initial.

Je considère la campagne terminée quand tous les cas P1 et P2 ont été exécutés et que chaque échec a son rapport de bug avec une preuve.

Pour la décision : c'est Go s'il ne reste aucun bug critique ou majeur ouvert sur la commande, les coupons et la première commande d'un nouveau client. Un seul bug critique sur la commande ou le paiement suffit pour un No-Go.
