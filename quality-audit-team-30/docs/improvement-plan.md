# Plan d'amélioration de QuickOrder V3.1

Ce plan vient de la campagne du 13/10/2026, détaillée dans le [rapport d'exécution](execution-report.md). Je le compléterai avec les retours des [tests utilisateurs](user-feedback.md) quand ils seront faits.

## Comment j'ai priorisé

Pour chaque amélioration j'ai estimé le gain (de 1 à 4) et l'effort : S pour moins d'un jour, M pour un à trois jours, L au-delà. Les efforts sont mes estimations, les développeurs auront sans doute un avis plus précis.

J'ai ensuite fait trois lots. Le lot 1 regroupe ce qui bloque la mise en production. Le lot 2 est à faire avant d'ouvrir le site au public. Le lot 3 peut attendre.

| # | Amélioration | Lot | Gain | Effort | Bugs concernés |
|---|---|---|---|---|---|
| A1 | Une seule validation de commande pour l'interface et l'API | 1 | 4 | M | BUG-01, 03, 04, 05, 08 |
| A2 | Une commande par paiement | 1 | 4 | S | BUG-02 |
| A3 | Adresse obligatoire pour commander | 1 | 4 | S | BUG-15 |
| A4 | Annulation avec remboursement et retour en stock | 1 | 3 | M | BUG-11 |
| A5 | Promotions affichées à partir des vrais coupons | 1 | 3 | S | BUG-06 |
| A6 | Filtre de livraison et recherche | 2 | 3 | S | BUG-07 |
| A7 | Sécurité de base | 2 | 4 | M | BUG-12 |
| A8 | Changements de statut encadrés | 2 | 2 | S | BUG-09 |
| A9 | Erreurs de l'API toutes au même format | 3 | 2 | S | BUG-13, 14 |
| A10 | Avis réservés aux clients et affichés | 3 | 2 | M | BUG-10 |
| A11 | Interface plus claire | 3 | 2 | S | |
| A12 | Tests automatiques | 3 | 3 | M | tous |

## Lot 1 : ce qui bloque la mise en production

### A1. Une seule validation de commande

Aujourd'hui l'interface et l'API ont chacune leur code pour créer une commande, et elles ne vérifient pas les mêmes choses. Le restaurant fermé, le stock, le minimum de commande et le montant en espèces ne sont contrôlés nulle part. `/coupons/validate` refuse un coupon expiré que `/orders` accepte.

Je propose une fonction de validation unique, appelée par le checkout et par `POST /api/orders`. Elle vérifierait que le restaurant est ouvert, que les produits sont en stock en quantité suffisante, que le minimum est atteint, que le coupon est encore valable et que le montant en espèces couvre le total. Côté écran, le bouton « Ajouter » devrait être désactivé pour un produit épuisé ou un restaurant fermé.

C'est la première chose à faire parce que cinq bugs, dont deux critiques, ont cette même cause. Corriger chaque bug séparément obligerait à tout faire deux fois.

Ce sera validé quand RM-01, RM-02, RM-03, RM-04, LIM-04, LIM-08 et ERR-05 passeront.

### A2. Une commande par paiement

Chaque paiement PayPal crée deux commandes payées (BUG-02). Il faut retirer la création en double. J'ajouterais aussi une protection contre le double clic sur « Confirmer », avec un identifiant unique par validation, pour qu'un même paiement ne puisse jamais donner deux commandes.

C'est le bug qui coûte le plus cher, puisque tous les clients PayPal paient deux fois, et probablement l'un des plus rapides à corriger. Validation : RM-05 passe sur l'interface et sur l'API.

### A3. Adresse obligatoire

À l'inscription, l'application crée une adresse « Domicile » vide, et le checkout l'accepte (BUG-15). Il ne faudrait plus créer cette adresse vide. Au checkout, si le client n'a pas d'adresse complète, on lui affiche le formulaire et on bloque la confirmation. Le serveur doit aussi refuser une adresse sans rue, sans code postal ou sans ville.

Tous les nouveaux clients sont touchés dès leur première commande. Validation : RM-13 passe.

### A4. Annulation complète

Une commande annulée reste « paid » et le stock n'est pas rendu (BUG-11). À l'annulation il faut remettre les quantités en stock et passer le paiement en remboursé, en l'affichant clairement au client. Le bouton « Annuler la commande » ne devrait apparaître que quand l'annulation est possible.

Validation : RM-10 passe, NOM-07 et RM-09 continuent de passer.

### A5. Promotions tirées des coupons

La page de Couscous Atlas annonce 15 % dans un texte écrit en dur, alors que le coupon enregistré vaut 10 % (BUG-06). Le texte de la promotion devrait être généré à partir du coupon (taux, minimum, date de fin). En attendant, il suffit d'aligner le coupon sur ce qui est annoncé.

Une promotion non tenue, c'est des réclamations assurées, et ça peut être considéré comme de la publicité trompeuse. Validation : RM-06 passe.

## Lot 2 : avant l'ouverture au public

### A6. Filtre de livraison et recherche

Le filtre « Livraison max » renvoie les restaurants au-dessus du plafond au lieu de ceux en dessous (BUG-07). La comparaison est à inverser. J'en profiterais pour élargir la recherche à la description du restaurant et au nom des plats, parce qu'aujourd'hui « salade » ne trouve rien.

Validation : RM-08 passe et la recherche « salade » renvoie Green Kitchen.

### A7. Sécurité de base

Plusieurs points relevés pendant la campagne : la redirection ouverte après connexion (BUG-12), pas de jeton CSRF, déconnexion par GET, pas d'en-têtes de sécurité, cookie sans `Secure` ni `SameSite`, serveur de développement, clé secrète et clé d'API écrites dans les fichiers du dépôt.

Il faudrait n'accepter que des chemins internes dans le paramètre `next`, ajouter une protection CSRF, passer la déconnexion en POST, ajouter les en-têtes, utiliser un vrai serveur WSGI et sortir les secrets du dépôt. Je recommande aussi un audit de sécurité fait par quelqu'un dont c'est le métier, parce que je n'ai fait que des vérifications simples.

Validation : ERR-10 passe, ERR-08 continue de passer.

### A8. Changements de statut encadrés

L'administrateur peut remettre une commande livrée en « confirmed » (BUG-09). Il faut définir l'ordre autorisé (confirmed, preparing, out_for_delivery, delivered, avec une annulation possible seulement avant la livraison) et refuser le reste. La liste déroulante ne devrait proposer que les statuts possibles.

Validation : RM-11 passe.

## Lot 3 : amélioration continue

### A9. Erreurs de l'API au même format

Un élément mal formé dans `items` provoque une erreur 500 (BUG-13) et les 404 sont renvoyées en HTML (BUG-14). Il faudrait valider le corps des requêtes et renvoyer toutes les erreurs de `/api` en JSON avec un champ `error`. Le fichier `openapi.yaml` doit suivre.

Validation : ERR-07 et ERR-09 passent.

### A10. Avis fiables et visibles

N'importe quel utilisateur connecté peut noter un restaurant où il n'a jamais commandé (BUG-10). J'ai aussi remarqué que les avis publiés ne s'affichent nulle part et ne changent pas la note du restaurant, ce qui rend la fonction assez inutile pour l'instant.

Je réserverais l'avis aux clients qui ont une commande livrée dans le restaurant, avec un avis par commande, et j'afficherais les avis sur la fiche. Validation : RM-12 passe.

### A11. Interface plus claire

Quelques détails qui gênent la lecture : les statuts en anglais, pas de bouton pour retirer une ligne du panier, un « Stock -1 » affiché au client, pas de favicon. Je traduirais les statuts, j'ajouterais un bouton « Retirer » et j'afficherais « Indisponible » à la place du stock chiffré. Cette partie sera sûrement à revoir après les tests utilisateurs.

### A12. Tests automatiques

Le dépôt n'a que des tests de fumée dans `tests/test_smoke.py`. Aucune des règles métier qui échouent n'est couverte par un test.

Les 41 cas de la campagne pourraient devenir des tests automatiques lancés à chaque modification, en commençant par les 17 qui échouent. Le script `scripts/run_campaign.py` peut servir de point de départ. Sans ça, chaque correction du lot 1 risque de casser un parcours qui marche aujourd'hui.

## Dans quel ordre

Je commencerais par A2, A3 et A5, qui demandent peu d'effort pour un gros gain. Ensuite A1 puis A4, qui sont le cœur du problème. À ce moment-là il faut relancer toute la campagne sur une base propre et reprendre la décision Go ou No-Go.

A6, A7 et A8 viennent avant l'ouverture au public. Le lot 3 peut se faire au fil de l'eau.
