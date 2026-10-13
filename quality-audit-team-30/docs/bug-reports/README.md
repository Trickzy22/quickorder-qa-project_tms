# Rapports de bug de QuickOrder V3.1

J'ai reproduit tous ces bugs pendant la campagne du 13/10/2026. Les preuves sont dans le dossier [evidence/](evidence/).

| ID | Titre | Sévérité | Priorité | Cas de test |
|---|---|---|---|---|
| [BUG-01](BUG-01-restaurant-ferme-commandable.md) | Un restaurant affiché FERMÉ accepte les commandes (UI et API) | Critique | P1 | RM-01 |
| [BUG-02](BUG-02-paypal-commande-en-double.md) | Un paiement PayPal crée deux commandes identiques | Critique | P1 | RM-05 |
| [BUG-03](BUG-03-especes-montant-insuffisant-accepte.md) | Paiement en espèces accepté avec un montant inférieur au total | Critique | P1 | RM-04 |
| [BUG-04](BUG-04-stock-non-controle.md) | Le stock n'est jamais contrôlé : produits hors stock commandables, stock négatif, quantité de panier illimitée | Majeure | P1 | RM-03, LIM-04, LIM-08 |
| [BUG-05](BUG-05-minimum-de-commande-non-applique.md) | Le minimum de commande est affiché mais jamais appliqué | Majeure | P1 | RM-02 |
| [BUG-06](BUG-06-atlas15-reduction-10-au-lieu-de-15.md) | Le coupon ATLAS15 applique 10 % alors que 15 % sont annoncés | Majeure | P2 | RM-06 |
| [BUG-07](BUG-07-filtre-livraison-max-inverse.md) | Le filtre « Livraison max » renvoie les restaurants les plus chers au lieu des moins chers | Moyenne | P2 | RM-08 |
| [BUG-08](BUG-08-coupon-expire-accepte-par-api-commande.md) | `POST /api/orders` applique la réduction d'un coupon expiré | Majeure | P1 | ERR-05, ERR-04 |
| [BUG-09](BUG-09-admin-transitions-de-statut-incoherentes.md) | L'administration accepte de repasser une commande livrée à « confirmed » | Moyenne | P3 | RM-11 |
| [BUG-10](BUG-10-avis-sans-commande.md) | Un client peut noter un restaurant où il n'a jamais commandé | Moyenne | P3 | RM-12 |
| [BUG-11](BUG-11-annulation-sans-restock-ni-remboursement.md) | L'annulation d'une commande ne restitue ni le stock ni le paiement | Majeure | P2 | RM-10 |
| [BUG-12](BUG-12-redirection-ouverte-apres-connexion.md) | Redirection ouverte : le paramètre `next` de /login accepte une URL externe | Majeure | P2 | ERR-10 |
| [BUG-13](BUG-13-erreur-500-items-mal-formes.md) | `POST /api/orders` répond 500 lorsqu'un élément de `items` n'est pas un objet | Moyenne | P3 | ERR-07 |
| [BUG-14](BUG-14-erreurs-404-api-en-html.md) | Les erreurs 404 de l'API sont renvoyées en HTML et non en JSON | Mineure | P4 | ERR-09 |
| [BUG-15](BUG-15-commande-avec-adresse-vide.md) | Un nouveau compte peut commander avec une adresse de livraison vide | Majeure | P1 | RM-13 |
