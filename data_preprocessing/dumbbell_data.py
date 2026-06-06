import pandas as pd

def load_data():
    # GDP PPA par habitant 
    gdp = pd.read_csv('data/API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_121708.csv', skiprows=4)
    gdp = gdp[['Country Name', '2023']].dropna(subset=['2023'])
    gdp.columns = ['Country', 'gdp_ppp_per_capita']

    # FR vers EN
    fr_to_en = {
        'États-Unis': 'United States', 'Allemagne': 'Germany',
        'Pays-Bas': 'Netherlands', 'Norvège': 'Norway', 'Suède': 'Sweden',
        'Luxembourg': 'Luxembourg', 'Canada': 'Canada', 'Belgique': 'Belgium',
        'Danemark': 'Denmark', 'Autriche': 'Austria', 'Irlande': 'Ireland',
        'Finlande': 'Finland', 'Suisse': 'Switzerland', 'Italie': 'Italy',
        'Portugal': 'Portugal', 'Espagne': 'Spain', 'Japon': 'Japan',
        'Australie': 'Australia', 'Royaume-Uni': 'United Kingdom',
        'Islande': 'Iceland', 'Grèce': 'Greece', 'Nouvelle-Zélande': 'New Zealand',
        'France': 'France', 'Tchéquie': 'Czechia', 'Corée': 'Korea, Rep.',
        'Slovénie': 'Slovenia', 'République slovaque': 'Slovak Republic',
        'Hongrie': 'Hungary', 'Chili': 'Chile', 'Türkiye': 'Turkiye',
        'Israël': 'Israel', 'Pologne': 'Poland', 'Lituanie': 'Lithuania',
        'Lettonie': 'Latvia', 'Mexique': 'Mexico', 'Costa Rica': 'Costa Rica',
        'Colombie': 'Colombia', 'Estonie': 'Estonia'}

    # Dépenses actuelles
    lines = open('data/export-2026-06-01T18_36_49.684Z.csv', encoding='utf-8-sig').readlines()
    rows = []
    for line in lines[3:]:
        parts = line.strip().split(';')
        if len(parts) < 2:
            continue
        fr = parts[0].strip('"')
        en = fr_to_en.get(fr)
        if not en:
            continue
        try:
            rows.append({'Country': en, 'current_usd_ppa': float(parts[1].strip('"').replace(',', '.'))})
        except:
            pass
    df684 = pd.DataFrame(rows).drop_duplicates('Country')

    # Projections 2060
    proj = pd.read_csv('data/proj_cost_2060_overweight.csv')
    proj['2060_GDP_pct_num'] = proj['2060_GDP_pct'].str.replace('%', '').astype(float)
    proj['Country_std'] = proj['Country'].replace({
        'Korea  Rep.': 'Korea, Rep.',
        'Turkey': 'Turkiye'})
    proj = proj.drop_duplicates('Country_std')

    # Merge : dépenses actuelles + projections + GDP pour conversion
    merged = df684.merge(
        proj[['Country_std', '2060_GDP_pct_num']],
        left_on='Country', right_on='Country_std', how='inner')
    merged = merged.merge(gdp, on='Country', how='left')
    merged['cost_2060_usd_ppa'] = (merged['2060_GDP_pct_num'] / 100) * merged['gdp_ppp_per_capita']
    merged = merged.dropna(subset=['cost_2060_usd_ppa'])
    merged = merged.drop_duplicates('Country')
    merged = merged.sort_values('cost_2060_usd_ppa', ascending=True)

    return merged[['Country', 'current_usd_ppa', 'cost_2060_usd_ppa']]
