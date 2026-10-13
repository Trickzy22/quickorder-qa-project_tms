# BUG-14 : Les erreurs 404 de l'API sont renvoyées en HTML et non en JSON

| Sévérité | Priorité | Statut | Cas de test liés |
|---|---|---|---|
| Mineure | P4 | Ouvert | ERR-09 |

## Contexte

API REST, ressources inexistantes.

Testé sur QuickOrder V3.1 sous Docker Compose (http://127.0.0.1:5000), base créée par seed.py, Microsoft Edge, le 13/10/2026.

## Préconditions

Clé API valide.

## Étapes de reproduction

1. `GET /api/restaurants/9999`.
2. Inspecter l'en-tête Content-Type.

## Résultat attendu

HTTP 404, `Content-Type: application/json`, corps `{"error": ...}` comme les autres erreurs de l'API (401, 400, 409).

## Résultat obtenu

HTTP 404 avec `Content-Type: text/html; charset=utf-8` (page d'erreur par défaut).

## Impact

Un client qui analyse systématiquement du JSON plante sur les 404 ; contrat d'erreur incohérent.

## Preuves

Échanges HTTP du cas ERR-09 (fichier complet : [evidence/ERR-09.txt](evidence/ERR-09.txt))

```text
> GET /api/restaurants/9999
< 404 (text/html; charset=utf-8)
# RÉSULTAT ATTENDU : HTTP 404 avec Content-Type application/json et un champ error.
# RÉSULTAT OBTENU  : HTTP 404 ; Content-Type « text/html; charset=utf-8 ».
# STATUT           : Fail
```
