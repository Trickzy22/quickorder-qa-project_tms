"""Reproduction des anomalies API dans Swagger UI (Authorize > Try it out > Execute) avec captures,
et relevé réseau du navigateur pour la redirection ouverte (BUG-12).

    python scripts/capture_swagger.py

Attention : chaque scénario POST /orders crée de vraies commandes dans la base.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"
KEY = "quickorder-demo-key"
OUT = Path(__file__).resolve().parent.parent / "docs" / "bug-reports" / "evidence"

POST_ORDERS = "#operations-Orders-post_orders"
SCENARIOS = [
    ("swagger-ERR-02-sans-cle-401.png", "#operations-Restaurants-get_restaurants", None, False),
    ("swagger-BUG-01-restaurant-ferme-201.png", POST_ORDERS,
     {"items": [{"product_id": 24, "quantity": 1}], "payment_method": "card"}, True),
    ("swagger-BUG-02-paypal-201.png", POST_ORDERS,
     {"items": [{"product_id": 17, "quantity": 1}], "payment_method": "paypal"}, True),
    ("swagger-BUG-03-especes-insuffisantes-201.png", POST_ORDERS,
     {"items": [{"product_id": 1, "quantity": 1}], "payment_method": "cash", "cash_received": 1}, True),
    ("swagger-BUG-05-sous-le-minimum-201.png", POST_ORDERS,
     {"items": [{"product_id": 3, "quantity": 1}], "payment_method": "card"}, True),
    ("swagger-BUG-08-coupon-expire-201.png", POST_ORDERS,
     {"items": [{"product_id": 1, "quantity": 2}], "payment_method": "card", "coupon": "EXPIRED10"}, True),
    ("swagger-BUG-13-items-mal-formes-500.png", POST_ORDERS,
     {"items": [{"product_id": 16, "quantity": 1}, "x"]}, True),
]


def run(page, name, op, body, authorize):
    page.goto(BASE + "/docs/")
    page.wait_for_selector(op)
    if authorize:
        page.click(".btn.authorize")
        page.fill(".auth-container input", KEY)
        page.click(".auth-btn-wrapper .authorize")
        page.click(".auth-btn-wrapper .btn-done")
    block = page.locator(op)
    block.locator(".opblock-summary-control").click()
    block.locator(".try-out__btn").click()
    if body is not None:
        block.locator("textarea.body-param__text").fill(json.dumps(body, indent=2))
    block.locator(".btn.execute").click()
    block.locator(".live-responses-table .response-col_status").first.wait_for()
    status = block.locator(".live-responses-table .response-col_status").first.inner_text().split()[0]
    block.screenshot(path=str(OUT / name))
    print(f"{name} -> HTTP {status}")
    return status


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_context(viewport={"width": 1280, "height": 900}, locale="fr-FR").new_page()
    for name, op, body, authorize in SCENARIOS:
        run(page, name, op, body, authorize)

    # BUG-12 : relevé réseau (équivalent de DevTools > Network) pendant la connexion avec ?next=
    ctx = browser.new_context(locale="fr-FR")
    page = ctx.new_page()
    lines = ["Relevé réseau du navigateur (Edge) : connexion avec /login?next=https://example.org/phishing", ""]

    def on_response(r):
        loc = r.headers.get("location")
        lines.append(f"{r.request.method} {r.url} -> {r.status}" + (f"   Location: {loc}" if loc else ""))

    page.on("response", on_response)
    page.goto(BASE + "/login?next=https://example.org/phishing")
    page.fill("input[name=email]", "alice@example.com")
    page.fill("input[name=password]", "Password123!")
    try:
        page.click("main button")
        page.wait_for_url("**example.org**", timeout=15000)
    except Exception as exc:  # hors ligne : la navigation externe peut échouer, le 302 reste tracé
        lines.append(f"(navigation externe non aboutie : {type(exc).__name__})")
    lines += ["", f"URL finale affichée par le navigateur : {page.url}"]
    (OUT / "BUG-12-reseau-navigateur.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    page.screenshot(path=str(OUT / "BUG-12-navigateur-redirige-hors-site.png"))
    print("\n".join(lines))
    browser.close()
