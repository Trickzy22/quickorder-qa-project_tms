# Rapport d'exécution de la campagne QuickOrder V3.1

## Recommandation : No-Go

Je ne recommande pas de mettre QuickOrder en production pour l'instant. Sur 41 cas exécutés, 17 échouent, et les sept risques que j'avais classés critiques se sont tous produits.

Trois bugs touchent directement l'argent du client. Un paiement PayPal crée deux commandes. Un paiement en espèces trop faible est accepté. Un restaurant fermé prend quand même des commandes.

## Cadre

| | |
|---|---|
| Version | QuickOrder V3.1, commit `d4606da` |
| Date | 13/10/2026 |
| Environnement | Docker Compose sur `http://127.0.0.1:5000`, base créée par `seed.py` |
| Navigateur | Microsoft Edge, 1280 × 800 |
| Comptes | alice et bob (clients), admin, clé API `quickorder-demo-key` |

Le code de l'application n'a pas été modifié.

### Comment les cas ont été exécutés

J'ai automatisé l'exécution. Le script [run_campaign.py](../scripts/run_campaign.py) joue les 41 cas en envoyant les mêmes requêtes HTTP que le navigateur (les formulaires) et que Swagger (l'API avec la clé), et il écrit chaque requête et chaque réponse dans un fichier.

Pour les bugs qui se voient à l'écran, [capture_screenshots.py](../scripts/capture_screenshots.py) les reproduit dans Edge et prend les captures. C'est aussi lui qui fait la manipulation du cas LIM-08, où on retire l'attribut `max` du champ quantité comme on le ferait dans DevTools.

Les bugs de l'API ont été rejoués dans Swagger avec [capture_swagger.py](../scripts/capture_swagger.py) : Authorize, Try it out, Execute, puis capture de la réponse. Les résultats sont les mêmes que ceux de la campagne. Ce script enregistre aussi les échanges réseau du navigateur pour la redirection du BUG-12.

Donc le navigateur et Swagger ont bien été utilisés, mais pilotés par script et non à la main.

## Résultats

| Catégorie | Cas | Pass | Fail | Blocked | Skipped |
|---|---|---|---|---|---|
| Nominaux | 8 | 8 | 0 | 0 | 0 |
| Limites | 9 | 7 | 2 | 0 | 0 |
| Erreurs | 10 | 6 | 4 | 0 | 0 |
| Règles métier | 14 | 3 | 11 | 0 | 0 |
| Total | 41 | 24 | 17 | 0 | 0 |

Le taux de réussite global est de 59 %. Aucun cas n'est bloqué ou ignoré, tout ce qui était prévu a été exécuté.

Ce tableau montre bien où est le problème. Les 8 cas nominaux passent, donc une démonstration rapide du site donne l'impression que tout fonctionne. Par contre 11 règles métier sur 14 échouent. L'application affiche les règles (restaurant fermé, hors stock, minimum de commande, promotion) mais le serveur ne les vérifie pas.

## Détail des cas

| ID | Titre | Statut | Bug |
|---|---|---|---|
| NOM-01 | Connexion d'un client avec des identifiants valides | Pass | |
| NOM-02 | Inscription d'un nouveau client | Pass | |
| NOM-03 | Commande complète par carte bancaire | Pass | |
| NOM-04 | Coupon valide appliqué au checkout | Pass | |
| NOM-05 | API : liste des restaurants avec une clé valide | Pass | |
| NOM-06 | API : création d'une commande par carte | Pass | |
| NOM-07 | API : annulation d'une commande confirmée | Pass | |
| NOM-08 | Recommander une ancienne commande | Pass | |
| LIM-01 | API : quantité maximale autorisée (20) | Pass | |
| LIM-02 | API : quantité juste au-dessus du maximum (21) | Pass | |
| LIM-03 | API : quantité 0 et quantité négative | Pass | |
| LIM-04 | API : quantité égale au stock + 1 | Fail | BUG-04 |
| LIM-05 | API : coupon au montant minimum exact et juste en dessous | Pass | |
| LIM-06 | API : plafond de réduction d'un coupon | Pass | |
| LIM-07 | Inscription : mot de passe de 7 puis 8 caractères | Pass | |
| LIM-08 | Panier : quantité au-delà du maximum affiché et du stock | Fail | BUG-04 |
| LIM-09 | API : paiement en espèces avec le montant exact | Pass | |
| ERR-01 | Connexion avec un mot de passe incorrect | Pass | |
| ERR-02 | API : clé absente ou incorrecte | Pass | |
| ERR-03 | API : identifiants inexistants | Pass | |
| ERR-04 | API : validation d'un coupon expiré ou inconnu | Pass | |
| ERR-05 | API : commande passée avec un coupon expiré | Fail | BUG-08 |
| ERR-06 | API : moyen de paiement invalide | Pass | |
| ERR-07 | API : corps de requête mal formé | Fail | BUG-13 |
| ERR-08 | Contrôle d'accès aux pages protégées | Pass | |
| ERR-09 | API : format des erreurs 404 | Fail | BUG-14 |
| ERR-10 | Connexion : paramètre next vers un site externe | Fail | BUG-12 |
| RM-01 | Un restaurant fermé ne peut pas recevoir de commande | Fail | BUG-01 |
| RM-02 | Le minimum de commande est appliqué | Fail | BUG-05 |
| RM-03 | Un produit hors stock ne peut pas être commandé | Fail | BUG-04 |
| RM-04 | En espèces, le montant remis doit couvrir le total | Fail | BUG-03 |
| RM-05 | Un paiement PayPal crée une seule commande | Fail | BUG-02 |
| RM-06 | ATLAS15 donne bien 15 % | Fail | BUG-06 |
| RM-07 | Un panier ne contient qu'un seul restaurant | Pass | |
| RM-08 | Filtre « Livraison max » | Fail | BUG-07 |
| RM-09 | Une commande livrée ne peut plus être annulée | Pass | |
| RM-10 | L'annulation rend le stock et le paiement | Fail | BUG-11 |
| RM-11 | Admin : changements de statut cohérents | Fail | BUG-09 |
| RM-12 | Il faut avoir commandé pour laisser un avis | Fail | BUG-10 |
| RM-13 | Une commande demande une adresse complète | Fail | BUG-15 |
| RM-14 | TOKYO30 offre la livraison à partir de 30 € | Pass | |

Le résultat obtenu de chaque cas est dans [test-cases.xlsx](test-cases.xlsx) et dans [test-cases.md](test-cases.md). Les échanges HTTP sont dans [bug-reports/evidence/](bug-reports/evidence/), avec un fichier texte par cas.

## Bugs ouverts

Il y a 15 bugs pour 17 cas en échec, parce que le BUG-04 regroupe trois cas sur le stock.

| Sévérité | Nombre | Bugs |
|---|---|---|
| Critique | 3 | [BUG-01](bug-reports/BUG-01-restaurant-ferme-commandable.md), [BUG-02](bug-reports/BUG-02-paypal-commande-en-double.md), [BUG-03](bug-reports/BUG-03-especes-montant-insuffisant-accepte.md) |
| Majeure | 7 | [BUG-04](bug-reports/BUG-04-stock-non-controle.md), [BUG-05](bug-reports/BUG-05-minimum-de-commande-non-applique.md), [BUG-06](bug-reports/BUG-06-atlas15-reduction-10-au-lieu-de-15.md), [BUG-08](bug-reports/BUG-08-coupon-expire-accepte-par-api-commande.md), [BUG-11](bug-reports/BUG-11-annulation-sans-restock-ni-remboursement.md), [BUG-12](bug-reports/BUG-12-redirection-ouverte-apres-connexion.md), [BUG-15](bug-reports/BUG-15-commande-avec-adresse-vide.md) |
| Moyenne | 4 | [BUG-07](bug-reports/BUG-07-filtre-livraison-max-inverse.md), [BUG-09](bug-reports/BUG-09-admin-transitions-de-statut-incoherentes.md), [BUG-10](bug-reports/BUG-10-avis-sans-commande.md), [BUG-13](bug-reports/BUG-13-erreur-500-items-mal-formes.md) |
| Mineure | 1 | [BUG-14](bug-reports/BUG-14-erreurs-404-api-en-html.md) |

## Principaux risques

Le plus grave est que le client peut perdre de l'argent sans rien avoir fait de travers. Avec PayPal il paie deux fois (BUG-02). S'il annule, la commande reste marquée payée (BUG-11). S'il commande dans un restaurant fermé, il paie pour un repas qui ne sera pas préparé (BUG-01).

La plateforme et les restaurants perdent aussi de l'argent : un client peut payer 5 € en espèces pour 26,79 € (BUG-03), utiliser un coupon expiré en passant par l'API (BUG-08) ou commander sous le minimum (BUG-05).

Certaines commandes ne peuvent tout simplement pas être honorées. Des produits épuisés sont vendus et le stock passe en négatif (BUG-04). Un nouveau client peut commander sans adresse (BUG-15).

Il y a un risque d'image et un risque légal avec la promotion ATLAS15, annoncée à 15 % et appliquée à 10 % (BUG-06), et avec les avis que n'importe qui peut publier (BUG-10).

Enfin côté sécurité, la page de connexion peut rediriger vers un site externe (BUG-12).

Presque tous ces bugs ont la même origine. Les contrôles existent dans l'affichage mais pas dans le serveur, et l'interface et l'API ne font pas les mêmes vérifications. L'exemple le plus parlant : `/coupons/validate` refuse un coupon expiré, mais `/orders` l'accepte.

## Autres observations

Ces points ne sont pas des cas de test, je les ai notés en explorant. Les relevés sont dans [EXPLORATOIRE.txt](bug-reports/evidence/EXPLORATOIRE.txt) et [console-navigateur.txt](bug-reports/evidence/console-navigateur.txt).

- La recherche ne regarde que le nom du restaurant. Chercher « salade » ou « japonaise » ne donne rien, alors que ces mots sont dans les descriptions de Green Kitchen et Tokyo Bowl.
- `GET /api/restaurants` renvoie aussi le restaurant fermé.
- Les formulaires n'ont pas de jeton CSRF, et on se déconnecte avec un simple GET sur `/logout`.
- Aucun en-tête de sécurité n'est envoyé. Le cookie de session n'a ni `Secure` ni `SameSite`.
- Le serveur est celui de développement de Werkzeug, qui prévient lui-même qu'il ne faut pas l'utiliser en production.
- Dans le panier, on ne peut pas supprimer une ligne directement. Il faut mettre la quantité à 0 et cliquer sur « Mettre à jour ».
- Le bouton « Annuler la commande » s'affiche même sur une commande livrée ou déjà annulée.
- Les statuts sont en anglais (`confirmed`, `paid`) alors que le site est en français.
- Dans la console du navigateur il n'y a pas d'erreur JavaScript, seulement un 404 sur le favicon et des avertissements sur les champs mot de passe.

## Limites de cette campagne

Je n'ai utilisé qu'un navigateur et une seule taille d'écran. Il n'y a pas eu de test sur mobile, pas de test de charge, et pas d'audit de sécurité sérieux.

Les tests utilisateurs ne sont pas encore réalisés, voir [user-feedback.md](user-feedback.md). Leurs résultats ne sont donc pas pris en compte ici.

La campagne a créé 20 commandes (#2 à #21) et la reproduction dans Swagger 6 de plus (#22 à #27). Les stocks ont bougé. Il faut réinitialiser la base avec `docker compose down -v` avant de relancer.

## Pour passer à Go

Il faudrait :

1. corriger les 3 bugs critiques et les 7 majeurs ;
2. relancer toute la campagne sur une base propre, sans aucun échec sur les cas P1 ;
3. faire les tests utilisateurs et vérifier qu'aucun problème ne bloque la commande.

Aucune correction n'était disponible à la date de ce rapport, donc je n'ai rien revalidé. Quand elles arriveront, le script de campagne servira de test de non-régression : les 17 cas en échec doivent passer, et les 24 autres ne doivent pas casser.
