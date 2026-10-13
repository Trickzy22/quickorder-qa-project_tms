# Audit qualité de QuickOrder (équipe 30)

Audit de QuickOrder V3.1 réalisé pour le cours Tests et qualité des solutions numériques. La version testée est le commit `d4606da`, sans modification du code.

## Verdict : No-Go

| Cas exécutés | Pass | Fail | Blocked | Skipped |
|---|---|---|---|---|
| 41 | 24 | 17 | 0 | 0 |

Les parcours classiques fonctionnent, mais la plupart des règles métier sont affichées sans être contrôlées par le serveur. Sur les 15 bugs ouverts, 3 sont critiques :

- un paiement PayPal crée deux commandes ([BUG-02](docs/bug-reports/BUG-02-paypal-commande-en-double.md)) ;
- un paiement en espèces inférieur au total est accepté ([BUG-03](docs/bug-reports/BUG-03-especes-montant-insuffisant-accepte.md)) ;
- un restaurant fermé accepte les commandes ([BUG-01](docs/bug-reports/BUG-01-restaurant-ferme-commandable.md)).

## Livrables

| Document | Contenu |
|---|---|
| [Stratégie de test](docs/test-strategy.md) | périmètre, parcours critiques, priorisation |
| [Matrice de risques](docs/risk-matrix.md) | 18 risques notés |
| Cas de test : [Excel](docs/test-cases.xlsx) ou [version lisible](docs/test-cases.md) | 41 cas |
| [Rapport d'exécution](docs/execution-report.md) | résultats et recommandation |
| [Rapports de bug](docs/bug-reports/README.md) | 15 bugs avec preuves |
| [Tests utilisateurs](docs/user-feedback.md) | protocole et grilles, sessions à réaliser |
| [Plan d'amélioration](docs/improvement-plan.md) | 12 améliorations priorisées |
