# Cas de test de QuickOrder V3.1

Campagne exécutée le 13/10/2026 14:35 sur http://127.0.0.1:5000 : Docker Compose, base SQLite initialisée par seed.py.
Version Excel : [test-cases.xlsx](test-cases.xlsx). Preuves : [bug-reports/evidence/](bug-reports/evidence/).

| Catégorie | Cas | Pass | Fail | Blocked | Skipped |
|---|---|---|---|---|---|
| Nominal | 8 | 8 | 0 | 0 | 0 |
| Limite | 9 | 7 | 2 | 0 | 0 |
| Erreur | 10 | 6 | 4 | 0 | 0 |
| Règle métier | 14 | 3 | 11 | 0 | 0 |
| Total | 41 | 24 | 17 | 0 | 0 |

## Sommaire

| ID | Titre | Priorité | Statut |
|---|---|---|---|
| [NOM-01](#nom-01) | Connexion d'un client avec des identifiants valides | P1 | Pass |
| [NOM-02](#nom-02) | Inscription d'un nouveau client | P1 | Pass |
| [NOM-03](#nom-03) | Commande complète par carte bancaire (UI) | P1 | Pass |
| [NOM-04](#nom-04) | Application d'un coupon valide au checkout (UI) | P1 | Pass |
| [NOM-05](#nom-05) | API : liste des restaurants avec clé valide | P1 | Pass |
| [NOM-06](#nom-06) | API : création d'une commande par carte | P1 | Pass |
| [NOM-07](#nom-07) | API : annulation d'une commande confirmée | P2 | Pass |
| [NOM-08](#nom-08) | Recommander une ancienne commande (UI) | P3 | Pass |
| [LIM-01](#lim-01) | API : quantité maximale autorisée (20) | P2 | Pass |
| [LIM-02](#lim-02) | API : quantité juste au-dessus du maximum (21) | P2 | Pass |
| [LIM-03](#lim-03) | API : quantité 0 et quantité négative | P2 | Pass |
| [LIM-04](#lim-04) | API : quantité égale au stock + 1 | P1 | Fail |
| [LIM-05](#lim-05) | API : coupon au montant minimum exact et juste en dessous | P2 | Pass |
| [LIM-06](#lim-06) | API : plafond de réduction d'un coupon | P2 | Pass |
| [LIM-07](#lim-07) | Inscription : longueur minimale du mot de passe (7 / 8 caractères) | P2 | Pass |
| [LIM-08](#lim-08) | Panier UI : quantité au-delà du maximum affiché et du stock | P2 | Fail |
| [LIM-09](#lim-09) | API : paiement en espèces avec le montant exact | P2 | Pass |
| [ERR-01](#err-01) | Connexion avec un mot de passe incorrect | P1 | Pass |
| [ERR-02](#err-02) | API : clé absente ou incorrecte | P1 | Pass |
| [ERR-03](#err-03) | API : identifiants inexistants | P2 | Pass |
| [ERR-04](#err-04) | API : validation d'un coupon expiré ou inconnu | P2 | Pass |
| [ERR-05](#err-05) | API : commande passée avec un coupon expiré | P1 | Fail |
| [ERR-06](#err-06) | API : moyen de paiement invalide | P2 | Pass |
| [ERR-07](#err-07) | API : corps de requête mal formé | P2 | Fail |
| [ERR-08](#err-08) | Contrôle d'accès aux pages protégées (UI) | P1 | Pass |
| [ERR-09](#err-09) | API : format des réponses d'erreur 404 | P3 | Fail |
| [ERR-10](#err-10) | Connexion : paramètre next pointant vers un site externe | P1 | Fail |
| [RM-01](#rm-01) | Un restaurant fermé ne peut pas recevoir de commande | P1 | Fail |
| [RM-02](#rm-02) | Le minimum de commande du restaurant est appliqué | P1 | Fail |
| [RM-03](#rm-03) | Un produit hors stock ne peut pas être commandé | P1 | Fail |
| [RM-04](#rm-04) | Paiement en espèces : le montant remis doit couvrir le total | P1 | Fail |
| [RM-05](#rm-05) | Un paiement PayPal crée une seule commande | P1 | Fail |
| [RM-06](#rm-06) | Le coupon ATLAS15 accorde la réduction annoncée (15 %) | P1 | Fail |
| [RM-07](#rm-07) | Le panier ne contient que des produits d'un même restaurant | P2 | Pass |
| [RM-08](#rm-08) | Le filtre « Livraison max » ne retient que les restaurants sous le plafond | P2 | Fail |
| [RM-09](#rm-09) | Une commande livrée ne peut plus être annulée par le client | P2 | Pass |
| [RM-10](#rm-10) | L'annulation d'une commande restitue le stock et le paiement | P2 | Fail |
| [RM-11](#rm-11) | Admin : les transitions de statut respectent le cycle de vie | P2 | Fail |
| [RM-12](#rm-12) | Seul un client ayant commandé peut laisser un avis | P2 | Fail |
| [RM-13](#rm-13) | Une commande nécessite une adresse de livraison complète | P1 | Fail |
| [RM-14](#rm-14) | TOKYO30 offre la livraison dès 30 € d'achat | P3 | Pass |

## Nominal

<a id="nom-01"></a>
### NOM-01 : Connexion d'un client avec des identifiants valides

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier qu'un client existant peut s'authentifier.
- **Préconditions** : Compte alice@example.com existant ; utilisateur déconnecté.
- **Données** : alice@example.com / Password123!
- **Étapes** :
  - 1. Ouvrir /login
  - 2. Saisir email et mot de passe
  - 3. Valider
- **Résultat attendu** : Redirection vers l'accueil ; le nom « Alice Martin » et le lien Déconnexion sont affichés.
- **Résultat obtenu** : HTTP 302 puis page d'accueil ; nom affiché : oui.
- **Preuves** : [NOM-01.txt](bug-reports/evidence/NOM-01.txt)

<a id="nom-02"></a>
### NOM-02 : Inscription d'un nouveau client

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier la création de compte avec des données valides.
- **Préconditions** : Email non encore utilisé.
- **Données** : Nom « Testeur QA », email qa.nom02.1791894922@example.com, mot de passe Password123!
- **Étapes** :
  - 1. Ouvrir /register
  - 2. Remplir le formulaire
  - 3. Valider
- **Résultat attendu** : Compte créé, utilisateur connecté automatiquement et redirigé vers l'accueil.
- **Résultat obtenu** : Compte créé et session ouverte : oui (page finale /).
- **Preuves** : [NOM-02.txt](bug-reports/evidence/NOM-02.txt)

<a id="nom-03"></a>
### NOM-03 : Commande complète par carte bancaire (UI)

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier le parcours critique panier → checkout → confirmation.
- **Préconditions** : Alice connectée ; Burger Factory ouvert ; Classic Burger en stock.
- **Données** : 2 × Classic Burger (11,90 €) ; livraison 2,99 € ; paiement carte.
- **Étapes** :
  - 1. Ajouter 2 Classic Burger au panier
  - 2. Passer commande
  - 3. Choisir Carte bancaire
  - 4. Confirmer
- **Résultat attendu** : Commande créée au statut confirmed, payée ; total = 23,80 + 2,99 = 26,79 € ; stock décrémenté de 2.
- **Résultat obtenu** : Commande #2 statut confirmed, total 26.79 €, paiement « paid · card » ; stock 100 → 98.
- **Preuves** : [NOM-03.txt](bug-reports/evidence/NOM-03.txt)

<a id="nom-04"></a>
### NOM-04 : Application d'un coupon valide au checkout (UI)

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier le calcul de la réduction d'un coupon valide.
- **Préconditions** : Alice connectée ; panier ≥ 20 €.
- **Données** : 2 × Classic Burger (23,80 €) ; coupon WELCOME10 (10 %, min 20 €, plafond 8 €).
- **Étapes** :
  - 1. Ajouter 2 Classic Burger
  - 2. Aller au checkout
  - 3. Saisir WELCOME10
  - 4. Cliquer Appliquer
- **Résultat attendu** : Réduction affichée 2,38 € ; total 23,80 + 2,99 − 2,38 = 24,41 €.
- **Résultat obtenu** : Réduction affichée 2.38 € ; total 24.41 €.
- **Preuves** : [NOM-04.txt](bug-reports/evidence/NOM-04.txt)

<a id="nom-05"></a>
### NOM-05 : API : liste des restaurants avec clé valide

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier que l'API renvoie la liste des restaurants au format JSON.
- **Préconditions** : Clé API valide.
- **Données** : GET /api/restaurants ; X-API-Key: quickorder-demo-key
- **Étapes** :
  - 1. Swagger > Authorize
  - 2. Exécuter GET /restaurants
- **Résultat attendu** : HTTP 200 ; JSON avec count et items ; chaque item contient id, name, delivery_fee, minimum_order, is_open.
- **Résultat obtenu** : HTTP 200 ; count=6 ; 6 items avec les champs attendus : oui.
- **Preuves** : [NOM-05.txt](bug-reports/evidence/NOM-05.txt)

<a id="nom-06"></a>
### NOM-06 : API : création d'une commande par carte

Catégorie : Nominal, priorité : P1, statut : Pass

- **Objectif** : Vérifier la création d'une commande via POST /orders.
- **Préconditions** : Clé API valide ; Pizza Roma ouvert ; produits en stock.
- **Données** : `{"items":[{"product_id":16,"quantity":1},{"product_id":19,"quantity":1}],"payment_method":"card"}`
- **Étapes** :
  - 1. POST /api/orders avec le corps indiqué
- **Résultat attendu** : HTTP 201 ; status confirmed ; subtotal 17,40 ; delivery_fee 2,49 ; total 19,89.
- **Résultat obtenu** : HTTP 201 ; commande #3 confirmed ; subtotal 17.4 ; total 19.89.
- **Preuves** : [NOM-06.txt](bug-reports/evidence/NOM-06.txt)

<a id="nom-07"></a>
### NOM-07 : API : annulation d'une commande confirmée

Catégorie : Nominal, priorité : P2, statut : Pass

- **Objectif** : Vérifier qu'une commande au statut confirmed peut être annulée.
- **Préconditions** : Commande confirmée créée en NOM-06.
- **Données** : POST /api/orders/{id}/cancel
- **Étapes** :
  - 1. POST /api/orders/{id}/cancel
  - 2. GET /api/orders/{id}
- **Résultat attendu** : HTTP 200 ; status cancelled ; le statut est persisté.
- **Résultat obtenu** : HTTP 200 ; statut après annulation : cancelled.
- **Preuves** : [NOM-07.txt](bug-reports/evidence/NOM-07.txt)

<a id="nom-08"></a>
### NOM-08 : Recommander une ancienne commande (UI)

Catégorie : Nominal, priorité : P3, statut : Pass

- **Objectif** : Vérifier que « Commander à nouveau » recharge le panier.
- **Préconditions** : Alice connectée ; commande #1 (Classic Burger + Frites maison) existante.
- **Données** : Commande #1.
- **Étapes** :
  - 1. Ouvrir /orders/1
  - 2. Cliquer « Commander à nouveau »
- **Résultat attendu** : Panier contenant 1 Classic Burger et 1 Frites maison ; message « 2 produit(s) ajouté(s) au panier ».
- **Résultat obtenu** : Panier rechargé avec les 2 produits : oui ; messages : ['[success] 2 produit(s) ajouté(s) au panier.'].
- **Preuves** : [NOM-08.txt](bug-reports/evidence/NOM-08.txt)

## Limite

<a id="lim-01"></a>
### LIM-01 : API : quantité maximale autorisée (20)

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier la borne haute valide de la quantité.
- **Préconditions** : Clé API valide ; Miso Soup stock ≥ 20.
- **Données** : product_id 9 (Miso Soup 3,20 €), quantity 20.
- **Étapes** :
  - 1. POST /api/orders quantity=20
- **Résultat attendu** : HTTP 201 ; subtotal 64,00 ; total 67,49.
- **Résultat obtenu** : HTTP 201 ; subtotal 64.0 ; total 67.49.
- **Preuves** : [LIM-01.txt](bug-reports/evidence/LIM-01.txt)

<a id="lim-02"></a>
### LIM-02 : API : quantité juste au-dessus du maximum (21)

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier le rejet de la première valeur invalide au-dessus de la borne.
- **Préconditions** : Clé API valide.
- **Données** : product_id 9, quantity 21.
- **Étapes** :
  - 1. POST /api/orders quantity=21
- **Résultat attendu** : HTTP 400 ; message « quantity must be between 1 and 20 » ; aucune commande créée.
- **Résultat obtenu** : HTTP 400 ; erreur « quantity must be between 1 and 20 » ; commandes 4 → 4.
- **Preuves** : [LIM-02.txt](bug-reports/evidence/LIM-02.txt)

<a id="lim-03"></a>
### LIM-03 : API : quantité 0 et quantité négative

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier le rejet des valeurs sous la borne basse.
- **Préconditions** : Clé API valide.
- **Données** : product_id 9, quantity 0 puis −1.
- **Étapes** :
  - 1. POST /api/orders quantity=0
  - 2. POST /api/orders quantity=-1
- **Résultat attendu** : HTTP 400 dans les deux cas ; aucune commande créée.
- **Résultat obtenu** : quantity=0 → HTTP 400 ; quantity=-1 → HTTP 400 ; commandes 4 → 4.
- **Preuves** : [LIM-03.txt](bug-reports/evidence/LIM-03.txt)

<a id="lim-04"></a>
### LIM-04 : API : quantité égale au stock + 1

Catégorie : Limite, priorité : P1, statut : Fail

- **Objectif** : Vérifier qu'on ne peut pas commander plus que le stock disponible.
- **Préconditions** : Clé API valide ; Salmon Bowl en stock limité (2 à l'initialisation).
- **Données** : product_id 7 (Salmon Bowl), quantity = stock + 1.
- **Étapes** :
  - 1. GET /api/products/7 (lire le stock)
  - 2. POST /api/orders quantity = stock + 1
  - 3. GET /api/products/7
- **Résultat attendu** : Commande refusée (HTTP 409 ou 400) ; stock inchangé et jamais négatif.
- **Résultat obtenu** : Stock initial 2 ; commande de 3 → HTTP 201 (commande #5) ; stock final -1.
- **Bug** : [BUG-04](bug-reports/BUG-04-stock-non-controle.md)
- **Preuves** : [LIM-04.txt](bug-reports/evidence/LIM-04.txt), [BUG-04-burger-factory-stock-negatif.png](bug-reports/evidence/BUG-04-burger-factory-stock-negatif.png), [BUG-04-panier-quantite-1000.png](bug-reports/evidence/BUG-04-panier-quantite-1000.png), [BUG-04-tokyo-bowl-stock-negatif.png](bug-reports/evidence/BUG-04-tokyo-bowl-stock-negatif.png)

<a id="lim-05"></a>
### LIM-05 : API : coupon au montant minimum exact et juste en dessous

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier la borne du minimum de commande d'un coupon.
- **Préconditions** : Coupon WELCOME10 actif (min 20 €).
- **Données** : subtotal 20.00 puis 19.99.
- **Étapes** :
  - 1. POST /api/coupons/validate subtotal=20.00
  - 2. POST /api/coupons/validate subtotal=19.99
- **Résultat attendu** : 20,00 → valid true, discount 2,00 ; 19,99 → valid false « Montant minimum non atteint ».
- **Résultat obtenu** : 20,00 → valid=True, discount=2.0 ; 19,99 → valid=False (Montant minimum non atteint.).
- **Preuves** : [LIM-05.txt](bug-reports/evidence/LIM-05.txt)

<a id="lim-06"></a>
### LIM-06 : API : plafond de réduction d'un coupon

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier que la réduction est plafonnée à max_discount.
- **Préconditions** : Coupon SAVE20 actif (20 %, min 35 €, plafond 12 €).
- **Données** : subtotal 59.95, 60.00 et 100.00.
- **Étapes** :
  - 1. POST /api/coupons/validate avec chaque sous-total
- **Résultat attendu** : 59,95 → 11,99 ; 60,00 → 12,00 ; 100,00 → 12,00 (plafonné).
- **Résultat obtenu** : Réductions obtenues : 59,95 → 11.99 ; 60,00 → 12.0 ; 100,00 → 12.0.
- **Preuves** : [LIM-06.txt](bug-reports/evidence/LIM-06.txt)

<a id="lim-07"></a>
### LIM-07 : Inscription : longueur minimale du mot de passe (7 / 8 caractères)

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier la borne de 8 caractères sur le mot de passe.
- **Préconditions** : Emails non utilisés.
- **Données** : Mot de passe « Abcdef1 » (7) puis « Abcdef12 » (8).
- **Étapes** :
  - 1. S'inscrire avec 7 caractères
  - 2. S'inscrire avec 8 caractères
- **Résultat attendu** : 7 caractères → refus avec message ; 8 caractères → compte créé.
- **Résultat obtenu** : 7 caractères → refusé ["[danger] Nom, email valide et mot de passe d'au moins 8 caractères requis."] ; 8 caractères → accepté.
- **Preuves** : [LIM-07.txt](bug-reports/evidence/LIM-07.txt)

<a id="lim-08"></a>
### LIM-08 : Panier UI : quantité au-delà du maximum affiché et du stock

Catégorie : Limite, priorité : P2, statut : Fail

- **Objectif** : Vérifier que le serveur borne la quantité du panier (le champ HTML affiche max = stock).
- **Préconditions** : Alice connectée ; Classic Burger dans le panier (stock ≈ 100).
- **Données** : qty_1 = 1000 envoyé au serveur (contournement du max HTML via DevTools).
- **Étapes** :
  - 1. Ajouter 1 Classic Burger
  - 2. Dans DevTools, retirer l'attribut max du champ quantité
  - 3. Saisir 1000 et cliquer « Mettre à jour »
- **Résultat attendu** : Quantité refusée ou ramenée au stock disponible ; message d'erreur.
- **Résultat obtenu** : Stock 98 ; quantité enregistrée dans le panier : 1000 ; total panier 11902.99 € ; aucun message d'erreur : True.
- **Bug** : [BUG-04](bug-reports/BUG-04-stock-non-controle.md)
- **Preuves** : [LIM-08.txt](bug-reports/evidence/LIM-08.txt), [BUG-04-burger-factory-stock-negatif.png](bug-reports/evidence/BUG-04-burger-factory-stock-negatif.png), [BUG-04-panier-quantite-1000.png](bug-reports/evidence/BUG-04-panier-quantite-1000.png), [BUG-04-tokyo-bowl-stock-negatif.png](bug-reports/evidence/BUG-04-tokyo-bowl-stock-negatif.png)

<a id="lim-09"></a>
### LIM-09 : API : paiement en espèces avec le montant exact

Catégorie : Limite, priorité : P2, statut : Pass

- **Objectif** : Vérifier la borne « montant remis = total ».
- **Préconditions** : Clé API valide.
- **Données** : 1 × Margherita (10,90 €) + livraison 2,49 € = 13,39 € ; cash_received 13.39.
- **Étapes** :
  - 1. POST /api/orders payment_method=cash cash_received=13.39
- **Résultat attendu** : HTTP 201 ; change_due = 0,00.
- **Résultat obtenu** : HTTP 201 ; total 13.39 ; change_due 0.0.
- **Preuves** : [LIM-09.txt](bug-reports/evidence/LIM-09.txt)

## Erreur

<a id="err-01"></a>
### ERR-01 : Connexion avec un mot de passe incorrect

Catégorie : Erreur, priorité : P1, statut : Pass

- **Objectif** : Vérifier le refus d'authentification et l'absence de fuite d'information.
- **Préconditions** : Compte alice@example.com existant.
- **Données** : alice@example.com / MauvaisMotDePasse ; inconnu@example.com / Password123!
- **Étapes** :
  - 1. Se connecter avec un mauvais mot de passe
  - 2. Se connecter avec un email inconnu
- **Résultat attendu** : Connexion refusée ; même message générique dans les deux cas ; pas de session.
- **Résultat obtenu** : Connexion refusée ; message identique dans les deux cas : ['[danger] Email ou mot de passe incorrect.'].
- **Preuves** : [ERR-01.txt](bug-reports/evidence/ERR-01.txt)

<a id="err-02"></a>
### ERR-02 : API : clé absente ou incorrecte

Catégorie : Erreur, priorité : P1, statut : Pass

- **Objectif** : Vérifier la protection des endpoints par X-API-Key.
- **Préconditions** : Aucune.
- **Données** : GET /api/restaurants sans en-tête ; puis X-API-Key: mauvaise-cle.
- **Étapes** :
  - 1. GET /api/restaurants sans clé
  - 2. GET /api/restaurants avec une clé erronée
- **Résultat attendu** : HTTP 401 avec un corps JSON d'erreur dans les deux cas.
- **Résultat obtenu** : Sans clé → HTTP 401 ; clé erronée → HTTP 401 ; erreur « missing or invalid X-API-Key ».
- **Preuves** : [ERR-02.txt](bug-reports/evidence/ERR-02.txt)

<a id="err-03"></a>
### ERR-03 : API : identifiants inexistants

Catégorie : Erreur, priorité : P2, statut : Pass

- **Objectif** : Vérifier les codes HTTP pour des ressources inexistantes.
- **Préconditions** : Clé API valide.
- **Données** : restaurant 9999 ; produit 9999 ; commande 9999 ; commande contenant product_id 9999.
- **Étapes** :
  - 1. GET /api/restaurants/9999
  - 2. GET /api/products/9999
  - 3. GET /api/orders/9999
  - 4. POST /api/orders avec product_id 9999
- **Résultat attendu** : HTTP 404 pour les trois GET ; HTTP 400 ou 404 pour le POST ; aucune commande créée.
- **Résultat obtenu** : GET → [404, 404, 404] ; POST commande produit 9999 → HTTP 400 « one or more products do not exist ».
- **Preuves** : [ERR-03.txt](bug-reports/evidence/ERR-03.txt)

<a id="err-04"></a>
### ERR-04 : API : validation d'un coupon expiré ou inconnu

Catégorie : Erreur, priorité : P2, statut : Pass

- **Objectif** : Vérifier le rejet d'un coupon expiré par /coupons/validate.
- **Préconditions** : Coupon EXPIRED10 expiré depuis la veille de l'initialisation.
- **Données** : code EXPIRED10 puis code INCONNU ; subtotal 30.
- **Étapes** :
  - 1. POST /api/coupons/validate EXPIRED10
  - 2. POST /api/coupons/validate INCONNU
- **Résultat attendu** : valid false dans les deux cas, message « Coupon invalide ou expiré ».
- **Résultat obtenu** : EXPIRED10 → HTTP 404 valid=False ; INCONNU → HTTP 404 valid=False.
- **Preuves** : [ERR-04.txt](bug-reports/evidence/ERR-04.txt)

<a id="err-05"></a>
### ERR-05 : API : commande passée avec un coupon expiré

Catégorie : Erreur, priorité : P1, statut : Fail

- **Objectif** : Vérifier qu'un coupon expiré n'accorde aucune réduction lors de la création de commande.
- **Préconditions** : Coupon EXPIRED10 expiré (rejeté par /coupons/validate, cf. ERR-04).
- **Données** : `{"items":[{"product_id":1,"quantity":2}],"payment_method":"card","coupon":"EXPIRED10"}`
- **Étapes** :
  - 1. POST /api/orders avec coupon EXPIRED10
- **Résultat attendu** : Commande refusée, ou créée sans réduction (discount 0 ; total 26,79).
- **Résultat obtenu** : HTTP 201 ; commande #7 ; discount 2.38 ; total 24.41.
- **Bug** : [BUG-08](bug-reports/BUG-08-coupon-expire-accepte-par-api-commande.md)
- **Preuves** : [ERR-05.txt](bug-reports/evidence/ERR-05.txt), [swagger-BUG-08-coupon-expire-201.png](bug-reports/evidence/swagger-BUG-08-coupon-expire-201.png)

<a id="err-06"></a>
### ERR-06 : API : moyen de paiement invalide

Catégorie : Erreur, priorité : P2, statut : Pass

- **Objectif** : Vérifier le rejet d'un payment_method non supporté.
- **Préconditions** : Clé API valide.
- **Données** : payment_method "bitcoin".
- **Étapes** :
  - 1. POST /api/orders payment_method=bitcoin
- **Résultat attendu** : HTTP 400 « invalid payment_method » ; aucune commande créée.
- **Résultat obtenu** : HTTP 400 « invalid payment_method » ; commandes 7 → 7.
- **Preuves** : [ERR-06.txt](bug-reports/evidence/ERR-06.txt)

<a id="err-07"></a>
### ERR-07 : API : corps de requête mal formé

Catégorie : Erreur, priorité : P2, statut : Fail

- **Objectif** : Vérifier que l'API répond 400 (et jamais 500) à des entrées invalides.
- **Préconditions** : Clé API valide.
- **Données** : a) JSON invalide  b) items []  c) quantity "abc"  d) items contenant un élément non-objet : [{"product_id":16,"quantity":1},"x"]
- **Étapes** :
  - 1. POST /api/orders avec chacun des 4 corps
- **Résultat attendu** : HTTP 400 avec message d'erreur JSON pour les 4 requêtes.
- **Résultat obtenu** : Codes obtenus : a) 400  b) 400  c) 400  d) 500.
- **Bug** : [BUG-13](bug-reports/BUG-13-erreur-500-items-mal-formes.md)
- **Preuves** : [ERR-07.txt](bug-reports/evidence/ERR-07.txt), [swagger-BUG-13-items-mal-formes-500.png](bug-reports/evidence/swagger-BUG-13-items-mal-formes-500.png)

<a id="err-08"></a>
### ERR-08 : Contrôle d'accès aux pages protégées (UI)

Catégorie : Erreur, priorité : P1, statut : Pass

- **Objectif** : Vérifier qu'un utilisateur ne peut pas accéder aux ressources qui ne lui appartiennent pas.
- **Préconditions** : Comptes alice, bob ; commande #1 appartenant à Alice.
- **Données** : Anonyme → /checkout ; Alice (client) → /admin/ ; Bob → /orders/1.
- **Étapes** :
  - 1. Sans session, ouvrir /checkout
  - 2. Connecté en client, ouvrir /admin/
  - 3. Connecté en Bob, ouvrir /orders/1
- **Résultat attendu** : 1) redirection vers /login  2) accès refusé « réservé aux administrateurs »  3) « Commande inaccessible ».
- **Résultat obtenu** : 1) HTTP 302 → /login?next=%2Fcheckout ; 2) ['[danger] Accès réservé aux administrateurs.'] ; 3) ['[danger] Commande inaccessible.'].
- **Preuves** : [ERR-08.txt](bug-reports/evidence/ERR-08.txt)

<a id="err-09"></a>
### ERR-09 : API : format des réponses d'erreur 404

Catégorie : Erreur, priorité : P3, statut : Fail

- **Objectif** : Vérifier que toutes les erreurs de l'API sont renvoyées en JSON (contrat OpenAPI).
- **Préconditions** : Clé API valide.
- **Données** : GET /api/restaurants/9999.
- **Étapes** :
  - 1. GET /api/restaurants/9999
  - 2. Inspecter l'en-tête Content-Type et le corps
- **Résultat attendu** : HTTP 404 avec Content-Type application/json et un champ error.
- **Résultat obtenu** : HTTP 404 ; Content-Type « text/html; charset=utf-8 ».
- **Bug** : [BUG-14](bug-reports/BUG-14-erreurs-404-api-en-html.md)
- **Preuves** : [ERR-09.txt](bug-reports/evidence/ERR-09.txt)

<a id="err-10"></a>
### ERR-10 : Connexion : paramètre next pointant vers un site externe

Catégorie : Erreur, priorité : P1, statut : Fail

- **Objectif** : Vérifier que la redirection après connexion reste interne (pas de redirection ouverte).
- **Préconditions** : Compte alice existant.
- **Données** : POST /login?next=https://example.org/phishing
- **Étapes** :
  - 1. Ouvrir /login?next=https://example.org/phishing
  - 2. Se connecter avec des identifiants valides
  - 3. Observer l'en-tête Location (DevTools > Network)
- **Résultat attendu** : Redirection vers une page interne (accueil) ; l'URL externe est ignorée.
- **Résultat obtenu** : HTTP 302 ; Location : https://example.org/phishing.
- **Bug** : [BUG-12](bug-reports/BUG-12-redirection-ouverte-apres-connexion.md)
- **Preuves** : [ERR-10.txt](bug-reports/evidence/ERR-10.txt), [BUG-12-navigateur-redirige-hors-site.png](bug-reports/evidence/BUG-12-navigateur-redirige-hors-site.png)

## Règle métier

<a id="rm-01"></a>
### RM-01 : Un restaurant fermé ne peut pas recevoir de commande

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier le blocage des commandes sur un restaurant au statut FERMÉ.
- **Préconditions** : Alice connectée ; Night Sushi (id 6) affiché FERMÉ.
- **Données** : 1 × Late Sushi Box (product_id 24, 14,00 €) ; paiement carte.
- **Étapes** :
  - UI : 1. Ouvrir Night Sushi  2. Ajouter Late Sushi Box  3. Passer commande et confirmer
  - API : POST /api/orders product_id 24
- **Résultat attendu** : Ajout au panier ou validation refusés (UI) ; HTTP 409 (API) ; aucune commande créée.
- **Résultat obtenu** : UI : commande #8 créée, statut confirmed, total 16.99 € ; API : HTTP 201 commande #9.
- **Bug** : [BUG-01](bug-reports/BUG-01-restaurant-ferme-commandable.md)
- **Preuves** : [RM-01.txt](bug-reports/evidence/RM-01.txt), [BUG-01-commande-confirmee-restaurant-ferme.png](bug-reports/evidence/BUG-01-commande-confirmee-restaurant-ferme.png), [BUG-01-restaurant-ferme-menu.png](bug-reports/evidence/BUG-01-restaurant-ferme-menu.png), [swagger-BUG-01-restaurant-ferme-201.png](bug-reports/evidence/swagger-BUG-01-restaurant-ferme-201.png)

<a id="rm-02"></a>
### RM-02 : Le minimum de commande du restaurant est appliqué

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier le refus d'une commande sous le minimum affiché.
- **Préconditions** : Alice connectée ; Burger Factory minimum 20,00 €.
- **Données** : 1 × Frites maison (3,50 €) ; paiement carte.
- **Étapes** :
  - UI : 1. Ajouter 1 Frites maison  2. Checkout (« Commande minimum : 20.00 € » affiché)  3. Confirmer
  - API : POST /api/orders product_id 3
- **Résultat attendu** : Validation refusée avec message indiquant le minimum ; aucune commande créée.
- **Résultat obtenu** : UI : commande #10 créée, statut confirmed, total 6.49 € (sous-total 3,50 € < 20 €) ; API : HTTP 201 commande #11.
- **Bug** : [BUG-05](bug-reports/BUG-05-minimum-de-commande-non-applique.md)
- **Preuves** : [RM-02.txt](bug-reports/evidence/RM-02.txt), [BUG-05-checkout-sous-le-minimum.png](bug-reports/evidence/BUG-05-checkout-sous-le-minimum.png), [BUG-05-commande-confirmee-sous-le-minimum.png](bug-reports/evidence/BUG-05-commande-confirmee-sous-le-minimum.png), [swagger-BUG-05-sous-le-minimum-201.png](bug-reports/evidence/swagger-BUG-05-sous-le-minimum-201.png)

<a id="rm-03"></a>
### RM-03 : Un produit hors stock ne peut pas être commandé

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier le blocage d'un produit dont le stock est 0.
- **Préconditions** : Alice connectée ; Veggie Burger (id 4) et Gyozas (id 8) à stock 0, affichés « HORS STOCK ».
- **Données** : UI : 1 × Veggie Burger + 2 × Classic Burger ; API : 1 × Gyozas.
- **Étapes** :
  - UI : 1. Ouvrir Burger Factory  2. Cliquer Ajouter sur Veggie Burger (HORS STOCK)  3. Commander
  - API : POST /api/orders product_id 8
- **Résultat attendu** : Ajout au panier refusé (UI) ; HTTP 409 (API) ; stock jamais négatif.
- **Résultat obtenu** : UI : commande #12 créée avec Veggie Burger, stock Veggie Burger = -1 ; API : HTTP 201, stock Gyozas = -1.
- **Bug** : [BUG-04](bug-reports/BUG-04-stock-non-controle.md)
- **Preuves** : [RM-03.txt](bug-reports/evidence/RM-03.txt), [BUG-04-burger-factory-stock-negatif.png](bug-reports/evidence/BUG-04-burger-factory-stock-negatif.png), [BUG-04-panier-quantite-1000.png](bug-reports/evidence/BUG-04-panier-quantite-1000.png), [BUG-04-tokyo-bowl-stock-negatif.png](bug-reports/evidence/BUG-04-tokyo-bowl-stock-negatif.png)

<a id="rm-04"></a>
### RM-04 : Paiement en espèces : le montant remis doit couvrir le total

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier le refus d'un montant en espèces inférieur au total.
- **Préconditions** : Alice connectée.
- **Données** : 2 × Classic Burger = 26,79 € livraison incluse ; montant remis 5,00 € (UI) et 1 (API).
- **Étapes** :
  - UI : 1. Panier 2 Classic Burger  2. Checkout, mode Espèces, montant 5.00  3. Confirmer
  - API : POST /api/orders payment_method=cash cash_received=1
- **Résultat attendu** : Commande refusée avec message « montant insuffisant » ; aucune commande payée.
- **Résultat obtenu** : UI : commande #14 confirmed « paid · cash », total 26.79 €, monnaie calculée -21.79 € ; API : HTTP 201, payment_status paid, change_due -13.89.
- **Bug** : [BUG-03](bug-reports/BUG-03-especes-montant-insuffisant-accepte.md)
- **Preuves** : [RM-04.txt](bug-reports/evidence/RM-04.txt), [BUG-03-especes-monnaie-negative.png](bug-reports/evidence/BUG-03-especes-monnaie-negative.png), [swagger-BUG-03-especes-insuffisantes-201.png](bug-reports/evidence/swagger-BUG-03-especes-insuffisantes-201.png)

<a id="rm-05"></a>
### RM-05 : Un paiement PayPal crée une seule commande

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier l'unicité de la commande et du débit pour un paiement PayPal.
- **Préconditions** : Alice connectée.
- **Données** : 2 × Regina (27,80 €) ; paiement PayPal (UI) ; 1 × Regina PayPal (API).
- **Étapes** :
  - UI : 1. Noter le nombre de commandes  2. Commander 2 Regina via PayPal  3. Ouvrir Mes commandes
  - API : POST /api/orders payment_method=paypal puis GET /api/orders
- **Résultat attendu** : Exactement 1 commande supplémentaire par paiement ; stock décrémenté une seule fois.
- **Résultat obtenu** : UI : commandes 15 → 17 (+2) pour un seul paiement, stock Regina 100 → 96 (2 commandés) ; API : commandes 17 → 19 (+2), stock 96 → 94 (1 commandé).
- **Bug** : [BUG-02](bug-reports/BUG-02-paypal-commande-en-double.md)
- **Preuves** : [RM-05.txt](bug-reports/evidence/RM-05.txt), [BUG-02-liste-commandes-doublon-paypal.png](bug-reports/evidence/BUG-02-liste-commandes-doublon-paypal.png), [swagger-BUG-02-paypal-201.png](bug-reports/evidence/swagger-BUG-02-paypal-201.png)

<a id="rm-06"></a>
### RM-06 : Le coupon ATLAS15 accorde la réduction annoncée (15 %)

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier la cohérence entre la promotion affichée et la réduction appliquée.
- **Préconditions** : Alice connectée ; page Couscous Atlas affichant « ATLAS15 … 15 % de réduction ».
- **Données** : 2 × Couscous Royal (35,80 €) ; coupon ATLAS15.
- **Étapes** :
  - 1. Ouvrir Couscous Atlas (lire la promotion)
  - 2. Ajouter 2 Couscous Royal
  - 3. Checkout, saisir ATLAS15, Appliquer
- **Résultat attendu** : Réduction de 15 % = 5,37 € ; total 35,80 + 2,99 − 5,37 = 33,42 €.
- **Résultat obtenu** : Réduction appliquée 3.58 € (total 35.21 €) ; l'API annonce discount_percent = 10.0.
- **Bug** : [BUG-06](bug-reports/BUG-06-atlas15-reduction-10-au-lieu-de-15.md)
- **Preuves** : [RM-06.txt](bug-reports/evidence/RM-06.txt), [BUG-06-checkout-atlas15-applique.png](bug-reports/evidence/BUG-06-checkout-atlas15-applique.png), [BUG-06-promotion-atlas15-annoncee.png](bug-reports/evidence/BUG-06-promotion-atlas15-annoncee.png)

<a id="rm-07"></a>
### RM-07 : Le panier ne contient que des produits d'un même restaurant

Catégorie : Règle métier, priorité : P2, statut : Pass

- **Objectif** : Vérifier la règle du panier mono-restaurant.
- **Préconditions** : Alice connectée ; panier vide.
- **Données** : Classic Burger (Burger Factory) puis Chicken Teriyaki (Tokyo Bowl) ; API : product_id 1 + 6.
- **Étapes** :
  - UI : 1. Ajouter Classic Burger  2. Ajouter Chicken Teriyaki
  - API : POST /api/orders avec les deux produits
- **Résultat attendu** : Second ajout refusé avec message ; API HTTP 400.
- **Résultat obtenu** : UI : ['[warning] Un panier ne peut contenir que des produits du même restaurant.'] ; panier limité au 1er restaurant : oui ; API : HTTP 400.
- **Preuves** : [RM-07.txt](bug-reports/evidence/RM-07.txt)

<a id="rm-08"></a>
### RM-08 : Le filtre « Livraison max » ne retient que les restaurants sous le plafond

Catégorie : Règle métier, priorité : P2, statut : Fail

- **Objectif** : Vérifier le filtre des frais de livraison sur la page d'accueil.
- **Préconditions** : Frais : Green Kitchen 1,99 ; Pizza Roma 2,49 ; Burger Factory 2,99 ; Couscous Atlas 2,99 ; Night Sushi 2,99 ; Tokyo Bowl 3,49.
- **Données** : Filtre « ≤ 2,50 € » (max_delivery=2.50).
- **Étapes** :
  - 1. Sur l'accueil, choisir Livraison max « ≤ 2,50 € »
  - 2. Cliquer Rechercher
- **Résultat attendu** : Seuls Green Kitchen (1,99 €) et Pizza Roma (2,49 €) sont affichés.
- **Résultat obtenu** : Restaurants affichés : Couscous Atlas, Tokyo Bowl, Burger Factory, Night Sushi.
- **Bug** : [BUG-07](bug-reports/BUG-07-filtre-livraison-max-inverse.md)
- **Preuves** : [RM-08.txt](bug-reports/evidence/RM-08.txt), [BUG-07-filtre-livraison-max-2.50.png](bug-reports/evidence/BUG-07-filtre-livraison-max-2.50.png)

<a id="rm-09"></a>
### RM-09 : Une commande livrée ne peut plus être annulée par le client

Catégorie : Règle métier, priorité : P2, statut : Pass

- **Objectif** : Vérifier la règle d'annulation selon le statut.
- **Préconditions** : Commande #1 d'Alice au statut delivered.
- **Données** : POST /api/orders/1/cancel
- **Étapes** :
  - 1. POST /api/orders/1/cancel
  - 2. GET /api/orders/1
- **Résultat attendu** : HTTP 409 « order cannot be cancelled » ; statut toujours delivered.
- **Résultat obtenu** : HTTP 409 « order cannot be cancelled » ; statut conservé : delivered.
- **Preuves** : [RM-09.txt](bug-reports/evidence/RM-09.txt)

<a id="rm-10"></a>
### RM-10 : L'annulation d'une commande restitue le stock et le paiement

Catégorie : Règle métier, priorité : P2, statut : Fail

- **Objectif** : Vérifier les effets de bord d'une annulation (stock, remboursement).
- **Préconditions** : Clé API valide ; Tiramisu en stock.
- **Données** : 3 × Tiramisu (product_id 19), carte ; puis annulation.
- **Étapes** :
  - 1. Lire le stock
  - 2. POST /api/orders 3 Tiramisu
  - 3. POST /api/orders/{id}/cancel
  - 4. Relire le stock et la commande
- **Résultat attendu** : Stock revenu à sa valeur initiale ; payment_status passé à refunded (ou équivalent).
- **Résultat obtenu** : Stock 99 → 96 après commande → 96 après annulation ; statut cancelled ; payment_status « paid ».
- **Bug** : [BUG-11](bug-reports/BUG-11-annulation-sans-restock-ni-remboursement.md)
- **Preuves** : [RM-10.txt](bug-reports/evidence/RM-10.txt), [BUG-11-commande-annulee-toujours-payee.png](bug-reports/evidence/BUG-11-commande-annulee-toujours-payee.png)

<a id="rm-11"></a>
### RM-11 : Admin : les transitions de statut respectent le cycle de vie

Catégorie : Règle métier, priorité : P2, statut : Fail

- **Objectif** : Vérifier qu'une commande livrée ne peut pas revenir à un statut antérieur.
- **Préconditions** : Admin connecté ; commande #1 au statut delivered.
- **Données** : Commande #1 ; nouveau statut confirmed.
- **Étapes** :
  - 1. Se connecter en admin
  - 2. /admin/ : sur la commande #1 choisir « confirmed »
  - 3. Mettre à jour
- **Résultat attendu** : Transition refusée (« Statut invalide ») ; la commande reste delivered.
- **Résultat obtenu** : ['[success] Statut mis à jour.'] ; statut de la commande #1 après l'action : confirmed (remise à delivered en fin de test).
- **Bug** : [BUG-09](bug-reports/BUG-09-admin-transitions-de-statut-incoherentes.md)
- **Preuves** : [RM-11.txt](bug-reports/evidence/RM-11.txt), [BUG-09-admin-statuts.png](bug-reports/evidence/BUG-09-admin-statuts.png)

<a id="rm-12"></a>
### RM-12 : Seul un client ayant commandé peut laisser un avis

Catégorie : Règle métier, priorité : P2, statut : Fail

- **Objectif** : Vérifier qu'un avis est lié à une commande réelle du restaurant.
- **Préconditions** : Bob connecté ; Bob n'a jamais commandé chez Couscous Atlas.
- **Données** : Note 1 ; commentaire « Avis de test QA sans commande ».
- **Étapes** :
  - 1. Se connecter en Bob
  - 2. Ouvrir Couscous Atlas
  - 3. Publier un avis 1 étoile
- **Résultat attendu** : Publication refusée (« vous devez avoir commandé dans ce restaurant »).
- **Résultat obtenu** : Messages : ['[success] Merci pour votre avis !'] ; avis accepté sans commande : oui.
- **Bug** : [BUG-10](bug-reports/BUG-10-avis-sans-commande.md)
- **Preuves** : [RM-12.txt](bug-reports/evidence/RM-12.txt)

<a id="rm-13"></a>
### RM-13 : Une commande nécessite une adresse de livraison complète

Catégorie : Règle métier, priorité : P1, statut : Fail

- **Objectif** : Vérifier qu'un nouveau compte ne peut pas commander sans adresse renseignée.
- **Préconditions** : Compte créé à l'instant (aucune adresse saisie par l'utilisateur).
- **Données** : Compte qa.rm13.1791894922@example.com ; 2 × Margherita ; carte.
- **Étapes** :
  - 1. Créer un compte
  - 2. Ajouter 2 Margherita
  - 3. Checkout : observer l'adresse proposée
  - 4. Confirmer
- **Résultat attendu** : Le checkout exige la saisie d'une adresse (rue, code postal, ville) avant de confirmer.
- **Résultat obtenu** : Commande #21 confirmée avec l'adresse « Domicile » vide (rue, code postal et ville vides : «»).
- **Bug** : [BUG-15](bug-reports/BUG-15-commande-avec-adresse-vide.md)
- **Preuves** : [RM-13.txt](bug-reports/evidence/RM-13.txt), [BUG-15-commande-adresse-vide.png](bug-reports/evidence/BUG-15-commande-adresse-vide.png)

<a id="rm-14"></a>
### RM-14 : TOKYO30 offre la livraison dès 30 € d'achat

Catégorie : Règle métier, priorité : P3, statut : Pass

- **Objectif** : Vérifier la promotion « Livraison gratuite dès 30 € avec TOKYO30 ».
- **Préconditions** : Coupon TOKYO30 actif ; frais de livraison Tokyo Bowl 3,49 €.
- **Données** : subtotal 29.99 puis 31.80.
- **Étapes** :
  - 1. POST /api/coupons/validate TOKYO30 subtotal=29.99
  - 2. Idem subtotal=31.80
- **Résultat attendu** : 29,99 → non valide ; 31,80 → réduction 3,49 € (= frais de livraison).
- **Résultat obtenu** : 29,99 → valid=False ; 31,80 → valid=True, discount=3.49.
- **Preuves** : [RM-14.txt](bug-reports/evidence/RM-14.txt)
