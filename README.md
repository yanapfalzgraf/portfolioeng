# Yana – Streamlit Portfolio Starter

Ein responsives Starter-Portfolio nach der bereitgestellten Designreferenz.

## Lokal starten

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Als Nächstes anpassen

1. In `app.py` E-Mail, LinkedIn, GitHub und Standort ersetzen.
2. Das Portrait als `assets/images/portrait.jpg` ablegen und den Platzhalter ersetzen.
3. Titel und Texte der drei Data-Projekte ergänzen.
4. Die SVG-Platzhalter durch echte Screenshots austauschen.
5. Für ausführliche Case Studies später separate Streamlit-Seiten ergänzen.

## Bilder

Statische Dateien unter `assets/` sind über `app/static/...` erreichbar, weil
`enableStaticServing = true` gesetzt ist.

## Deployment

Repository zu GitHub pushen und in Streamlit Community Cloud `app.py` als
Entrypoint auswählen.
