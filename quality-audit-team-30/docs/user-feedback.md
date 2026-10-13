# Tests utilisateurs de QuickOrder V3.1

Les sessions ne sont pas encore faites. Ce document contient le protocole, les scénarios et les grilles à remplir. Les cases vides seront complétées avec ce qui aura été réellement observé.

## Objectif

Faire réaliser 3 scénarios par au moins 2 personnes, pour voir les problèmes que mes tests ne montrent pas : ce que les gens ne comprennent pas, là où ils hésitent, là où ils abandonnent.

## Protocole

Je cherche 2 personnes qui ne connaissent pas l'application et qui ne font pas partie du projet. Si possible deux profils différents, par exemple quelqu'un qui commande souvent sur ce genre d'appli et quelqu'un qui le fait rarement.

Chaque session dure 15 à 20 minutes. Avant chacune je remets la base à zéro (`docker compose down -v` puis `docker compose up`) pour que les deux personnes partent du même état.

Je lis la consigne du scénario et ensuite je n'interviens plus. Je demande à la personne de dire à voix haute ce qu'elle pense. Je note ses phrases telles quelles, le temps passé, et si elle a réussi seule, réussi avec de l'aide ou abandonné.

Je préviens la personne que c'est l'application qui est évaluée et pas elle. Je ne note qu'un identifiant (P1, P2).

## Scénarios

### Scénario 1 : première commande

« Vous découvrez QuickOrder. Créez un compte, puis commandez un repas végétarien pour ce soir, livré chez vous, en payant par carte. »

À regarder : est-ce que la personne trouve le filtre végétarien, est-ce qu'elle remarque qu'on ne lui demande jamais son adresse, est-ce qu'elle comprend la page de confirmation.

### Scénario 2 : utiliser une promotion

« Connectez-vous avec alice@example.com et le mot de passe Password123!. On vous a parlé d'une réduction de 15 % chez Couscous Atlas. Commandez pour deux personnes avec cette réduction et dites-moi combien vous allez payer. »

À regarder : est-ce qu'elle trouve le code, est-ce qu'elle trouve où le saisir, est-ce qu'elle vérifie le montant de la réduction.

### Scénario 3 : petit budget, puis annulation

« Connectez-vous avec bob@example.com et le mot de passe Password123!. Vous voulez payer le moins possible en livraison. Trouvez un restaurant dont la livraison coûte 2,50 € au maximum, commandez un seul article en espèces avec un billet de 20 €, puis annulez la commande. »

À regarder : sa réaction devant le résultat du filtre, ce qu'elle comprend du minimum de commande affiché, si elle trouve le bouton d'annulation et si elle pense être remboursée.

## Participants

| | Profil | Date | Contexte (lieu, matériel) |
|---|---|---|---|
| P1 | | | |
| P2 | | | |

## Résultats par scénario

| Scénario | Participant | Résultat | Durée | Remarques |
|---|---|---|---|---|
| 1 | P1 | | | |
| 1 | P2 | | | |
| 2 | P1 | | | |
| 2 | P2 | | | |
| 3 | P1 | | | |
| 3 | P2 | | | |

## Problèmes observés

Une ligne par problème. La fréquence est le nombre de participants concernés. L'impact est bloquant, gênant ou mineur.

| ID | Profil | Contexte | Problème | Fréquence | Impact | Verbatim | Hypothèse d'amélioration | Priorité |
|---|---|---|---|---|---|---|---|---|
| UF-01 | | | | /2 | | | | |
| UF-02 | | | | /2 | | | | |
| UF-03 | | | | /2 | | | | |
| UF-04 | | | | /2 | | | | |

## Ce que je m'attends à voir

Ce sont des suppositions tirées de ma campagne de test, pas des résultats. Je ne les reporterai dans le tableau du dessus que si un participant tombe vraiment dessus.

| Supposition | Vient de | Scénario |
|---|---|---|
| La personne commande sans s'apercevoir qu'elle n'a pas donné d'adresse | [BUG-15](bug-reports/BUG-15-commande-avec-adresse-vide.md) | 1 |
| Les statuts en anglais (`confirmed`, `paid`) ne sont pas compris | observation | 1 |
| Personne ne vérifie le montant de la réduction ATLAS15 | [BUG-06](bug-reports/BUG-06-atlas15-reduction-10-au-lieu-de-15.md) | 2 |
| Le filtre « Livraison max » déroute, la personne arrête de s'en servir | [BUG-07](bug-reports/BUG-07-filtre-livraison-max-inverse.md) | 3 |
| Le minimum de commande affiché fait croire que la commande sera refusée | [BUG-05](bug-reports/BUG-05-minimum-de-commande-non-applique.md) | 3 |
| Après l'annulation, la personne ne sait pas si elle est remboursée | [BUG-11](bug-reports/BUG-11-annulation-sans-restock-ni-remboursement.md) | 3 |
| L'absence de bouton pour retirer une ligne du panier gêne | observation | 1 et 3 |

## Synthèse

À écrire après les sessions.
