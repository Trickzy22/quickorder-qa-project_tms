# Matrice de risques de QuickOrder V3.1

## Comment j'ai noté

Chaque risque a une note de probabilité (P) et une note d'impact (I), de 1 à 4. La criticité est le produit des deux.

| Note | Probabilité | Impact |
|---|---|---|
| 1 | rare, cas très particulier | gêne légère, facile à contourner |
| 2 | possible, erreur de saisie ou utilisateur curieux | une fonction marche mal mais personne ne perd d'argent |
| 3 | probable, arrive en usage courant | perte d'argent ou commande non livrée pour quelques clients |
| 4 | presque sûr, arrive sur le parcours normal | perte d'argent à chaque fois, ou problème légal |

De 12 à 16 le risque est critique (P1), de 8 à 11 élevé (P2), de 4 à 7 modéré (P3), en dessous faible (P4).

## Les risques

La dernière colonne dit si le risque s'est vraiment produit pendant la campagne du 13/10/2026.

| ID | Risque | P | I | Note | Priorité | Cas de test | Constaté ? |
|---|---|---|---|---|---|---|---|
| R01 | Un paiement crée plusieurs commandes | 4 | 4 | 16 | P1 | NOM-03, NOM-06, RM-05 | oui, [BUG-02](bug-reports/BUG-02-paypal-commande-en-double.md) |
| R02 | Commande acceptée dans un restaurant fermé | 3 | 4 | 12 | P1 | RM-01 | oui, [BUG-01](bug-reports/BUG-01-restaurant-ferme-commandable.md) |
| R03 | Commande marquée payée alors que le montant ne suffit pas | 3 | 4 | 12 | P1 | LIM-09, RM-04 | oui, [BUG-03](bug-reports/BUG-03-especes-montant-insuffisant-accepte.md) |
| R04 | Vente d'un produit épuisé, stock faux | 4 | 3 | 12 | P1 | LIM-04, LIM-08, RM-03 | oui, [BUG-04](bug-reports/BUG-04-stock-non-controle.md) |
| R05 | Commande payée sans adresse de livraison | 4 | 3 | 12 | P1 | NOM-02, RM-13 | oui, [BUG-15](bug-reports/BUG-15-commande-avec-adresse-vide.md) |
| R06 | Réduction mal calculée ou coupon invalide accepté | 3 | 4 | 12 | P1 | NOM-04, LIM-05, LIM-06, ERR-04, ERR-05, RM-06, RM-14 | oui, [BUG-06](bug-reports/BUG-06-atlas15-reduction-10-au-lieu-de-15.md) et [BUG-08](bug-reports/BUG-08-coupon-expire-accepte-par-api-commande.md) |
| R07 | Minimum de commande non respecté | 4 | 3 | 12 | P1 | RM-02 | oui, [BUG-05](bug-reports/BUG-05-minimum-de-commande-non-applique.md) |
| R08 | Accès aux commandes d'un autre ou à l'admin | 2 | 4 | 8 | P2 | ERR-01, ERR-02, ERR-08 | non |
| R09 | Utilisateur envoyé vers un autre site à la connexion | 2 | 4 | 8 | P2 | ERR-10 | oui, [BUG-12](bug-reports/BUG-12-redirection-ouverte-apres-connexion.md) |
| R10 | Annulation sans remboursement ni retour en stock | 3 | 3 | 9 | P2 | NOM-07, RM-09, RM-10 | oui, [BUG-11](bug-reports/BUG-11-annulation-sans-restock-ni-remboursement.md) |
| R11 | Recherche ou filtres qui donnent de mauvais résultats | 4 | 2 | 8 | P2 | RM-08 | oui, [BUG-07](bug-reports/BUG-07-filtre-livraison-max-inverse.md) |
| R12 | Quantités hors limites acceptées par l'API | 2 | 3 | 6 | P3 | LIM-01, LIM-02, LIM-03 | non |
| R13 | Statut de commande incohérent côté admin | 2 | 3 | 6 | P3 | RM-11 | oui, [BUG-09](bug-reports/BUG-09-admin-transitions-de-statut-incoherentes.md) |
| R14 | Faux avis | 3 | 2 | 6 | P3 | RM-12 | oui, [BUG-10](bug-reports/BUG-10-avis-sans-commande.md) |
| R15 | Erreur serveur sur une entrée invalide de l'API | 2 | 3 | 6 | P3 | ERR-03, ERR-06, ERR-07 | oui, [BUG-13](bug-reports/BUG-13-erreur-500-items-mal-formes.md) |
| R16 | Panier avec des produits de plusieurs restaurants | 2 | 3 | 6 | P3 | RM-07 | non |
| R17 | Inscription ou connexion qui ne marche pas | 1 | 4 | 4 | P3 | NOM-01, NOM-02, LIM-07 | non |
| R18 | Erreurs de l'API dans un format différent selon les cas | 3 | 1 | 3 | P4 | ERR-09 | oui, [BUG-14](bug-reports/BUG-14-erreurs-404-api-en-html.md) |

## Vue d'ensemble

| | Impact 1 | Impact 2 | Impact 3 | Impact 4 |
|---|---|---|---|---|
| Probabilité 4 | | R11 | R04, R05, R07 | R01 |
| Probabilité 3 | R18 | R14 | R10 | R02, R03, R06 |
| Probabilité 2 | | | R12, R13, R15, R16 | R08, R09 |
| Probabilité 1 | | | | R17 |

## Ce que j'en retiens

Les sept risques que j'avais classés critiques se sont tous produits. Ils concernent tous la commande, le paiement ou les promotions, donc exactement ce qui touche à l'argent.

Au total 14 risques sur 18 sont constatés. Les quatre qui ne le sont pas concernent la connexion, le contrôle d'accès, les limites de quantité de l'API et le panier limité à un restaurant.

Attention pour R08 : je n'ai rien trouvé, mais mes vérifications de sécurité sont restées basiques. Ça ne veut pas dire que l'application est sûre.
