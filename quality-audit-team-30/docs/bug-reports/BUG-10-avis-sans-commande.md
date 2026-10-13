# BUG-10 : Un client peut noter un restaurant où il n'a jamais commandé

| Sévérité | Priorité | Statut | Cas de test liés |
|---|---|---|---|
| Moyenne | P3 | Ouvert | RM-12 |

## Contexte

Fiche restaurant, formulaire « Laisser un avis ».

Testé sur QuickOrder V3.1 sous Docker Compose (http://127.0.0.1:5000), base créée par seed.py, Microsoft Edge, le 13/10/2026.

## Préconditions

Compte bob@example.com connecté. Bob n'a aucune commande chez Couscous Atlas.

## Étapes de reproduction

1. Ouvrir Couscous Atlas.
2. Choisir la note 1, saisir un commentaire.
3. Cliquer « Publier ».

## Résultat attendu

Publication refusée : l'avis doit être rattaché à une commande du restaurant.

## Résultat obtenu

« Merci pour votre avis ! » : l'avis est enregistré. À noter : les avis publiés ne sont affichés nulle part sur la fiche restaurant.

## Impact

Faux avis possibles (concurrence, spam) ; notes non fiables.

## Preuves

Échanges HTTP du cas RM-12 (fichier complet : [evidence/RM-12.txt](evidence/RM-12.txt))

```text
> POST /login
< 302 -> / ; 200 /
> GET /orders
< 200 /orders
# Bob a des commandes chez Couscous Atlas : False
> POST /restaurant/5/review
< 302 -> /restaurant/5 ; 200 /restaurant/5
  message affiché : [success] Merci pour votre avis !
# RÉSULTAT ATTENDU : Publication refusée (« vous devez avoir commandé dans ce restaurant »).
# RÉSULTAT OBTENU  : Messages : ['[success] Merci pour votre avis !'] ; avis accepté sans commande : oui.
# STATUT           : Fail
```
