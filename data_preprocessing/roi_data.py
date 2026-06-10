import pandas as pd

def load_data():
    """
    Prétraitement de données pour partie IV
    Extraction d'exemples d'actions' et de leur retour sur investissement (roi)
    Pour US$1 investi, combien sont récupérés ?
    """
    # Charge le CSV
    with open("data/export-2026-06-01T18_36_49.673Z.csv", encoding="utf-8-sig") as f:
        lines = f.readlines()
    rows = []
    # Pour chaque ligne/mesure après l'en-tête
    for line in lines[3:]:
        block = line.strip().split(";") # ; est le séparateur entre colonnes
        if len(block) < 2:
            continue
        action = block[0].strip('"') # on extrait chaque action
        if not action:
            continue
        try:
            roi = float(block[1].strip('"').replace(",", ".")) # et le gain associé
            rows.append({"action": action, "roi": roi})
        except:
            pass

    # Construction d'un dataframe trié par retour sur investissement
    df = pd.DataFrame(rows)
    df["rentable"] = df["roi"] >= 1.0
    df = df.sort_values("roi", ascending=True)
    return df
