"""Captures d'écran des anomalies dans un vrai navigateur (Microsoft Edge piloté par Playwright).

À lancer après scripts/run_campaign.py : les numéros de commande sont lus dans
docs/campaign-results.json.

    python scripts/capture_screenshots.py
"""
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "bug-reports" / "evidence"
RESULTS = {r["id"]: r for r in json.loads((ROOT / "docs" / "campaign-results.json").read_text(encoding="utf-8"))["results"]}


def order_id(case_id):
    return re.search(r"commande #(\d+)", RESULTS[case_id]["obtenu"], flags=re.I).group(1)


def shot(page, name):
    page.screenshot(path=str(OUT / name), full_page=True)
    print("capture", name)


def login(page, email, password):
    page.goto(BASE + "/login")
    page.fill("input[name=email]", email)
    page.fill("input[name=password]", password)
    page.click("main button")
    page.wait_for_load_state()


def add(page, restaurant_id, product_name, qty=1):
    page.goto(f"{BASE}/restaurant/{restaurant_id}")
    card = page.locator("article.card", has=page.get_by_role("heading", name=product_name, exact=True))
    card.locator("input[name=quantity]").fill(str(qty))
    card.get_by_role("button", name="Ajouter").click()
    page.wait_for_load_state()


def clear_cart(page):
    page.goto(BASE + "/cart")
    if page.get_by_role("button", name="Vider le panier").count():
        page.get_by_role("button", name="Vider le panier").click()
        page.wait_for_load_state()


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, locale="fr-FR")
    page = ctx.new_page()
    console = []
    page.on("console", lambda m: console.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: console.append(f"[pageerror] {e}"))

    # BUG-07 : filtre livraison (page publique)
    page.goto(BASE + "/?max_delivery=2.50")
    shot(page, "BUG-07-filtre-livraison-max-2.50.png")

    login(page, "alice@example.com", "Password123!")

    # BUG-01 : restaurant fermé
    page.goto(BASE + "/restaurant/6")
    shot(page, "BUG-01-restaurant-ferme-menu.png")
    page.goto(f"{BASE}/orders/{order_id('RM-01')}")
    shot(page, "BUG-01-commande-confirmee-restaurant-ferme.png")

    # BUG-02 : doublon PayPal
    page.goto(BASE + "/orders")
    shot(page, "BUG-02-liste-commandes-doublon-paypal.png")

    # BUG-03 : espèces insuffisantes
    page.goto(f"{BASE}/orders/{order_id('RM-04')}")
    shot(page, "BUG-03-especes-monnaie-negative.png")

    # BUG-04 : stock négatif, produit hors stock commandable
    page.goto(BASE + "/restaurant/1")
    shot(page, "BUG-04-burger-factory-stock-negatif.png")
    page.goto(BASE + "/restaurant/2")
    shot(page, "BUG-04-tokyo-bowl-stock-negatif.png")

    # BUG-04 (LIM-08) : quantité 1000 dans le panier après retrait de l'attribut max
    clear_cart(page)
    add(page, 1, "Classic Burger")
    page.goto(BASE + "/cart")
    page.eval_on_selector("input[name=qty_1]", "el => el.removeAttribute('max')")
    page.fill("input[name=qty_1]", "1000")
    page.get_by_role("button", name="Mettre à jour").click()
    page.wait_for_load_state()
    shot(page, "BUG-04-panier-quantite-1000.png")

    # BUG-05 : minimum de commande affiché mais non bloquant
    clear_cart(page)
    add(page, 1, "Frites maison")
    page.goto(BASE + "/checkout")
    shot(page, "BUG-05-checkout-sous-le-minimum.png")
    page.goto(f"{BASE}/orders/{order_id('RM-02')}")
    shot(page, "BUG-05-commande-confirmee-sous-le-minimum.png")

    # BUG-06 : ATLAS15 annoncé 15 %, appliqué 10 %
    clear_cart(page)
    page.goto(BASE + "/restaurant/5")
    shot(page, "BUG-06-promotion-atlas15-annoncee.png")
    add(page, 5, "Couscous Royal", 2)
    page.goto(BASE + "/checkout")
    page.fill("input[name=coupon]", "ATLAS15")
    page.get_by_role("button", name="Appliquer").click()
    page.wait_for_load_state()
    shot(page, "BUG-06-checkout-atlas15-applique.png")
    clear_cart(page)

    # BUG-11 : commande annulée toujours « paid »
    page.goto(f"{BASE}/orders/{order_id('NOM-06')}")
    shot(page, "BUG-11-commande-annulee-toujours-payee.png")
    page.goto(BASE + "/logout")

    # BUG-09 : tableau de bord admin
    login(page, "admin@quickorder.local", "Admin123!")
    page.goto(BASE + "/admin/")
    shot(page, "BUG-09-admin-statuts.png")
    # BUG-15 : commande d'un compte sans adresse (vue admin de la commande)
    page.goto(f"{BASE}/orders/{order_id('RM-13')}")
    shot(page, "BUG-15-commande-adresse-vide.png")
    page.goto(BASE + "/logout")

    # Swagger
    page.goto(BASE + "/docs/")
    page.wait_for_timeout(2500)
    shot(page, "swagger-ui.png")

    (OUT / "console-navigateur.txt").write_text(
        "\n".join(console) if console else "Aucun message ni erreur dans la console du navigateur pendant le parcours.\n",
        encoding="utf-8")
    browser.close()
