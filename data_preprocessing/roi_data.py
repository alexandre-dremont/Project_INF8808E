import pandas as pd

def load_data():
    lines = open('data/export-2026-06-01T18_36_49.673Z.csv', encoding='utf-8-sig').readlines()
    rows = []
    for line in lines[3:]:
        parts = line.strip().split(';')
        if len(parts) < 2:
            continue
        policy = parts[0].strip('"')
        if not policy:
            continue
        try:
            roi = float(parts[1].strip('"').replace(',', '.'))
            rows.append({'policy': policy, 'roi': roi})
        except:
            pass

    df = pd.DataFrame(rows)
    df['profitable'] = df['roi'] >= 1.0
    df = df.sort_values('roi', ascending=True)
    return df
