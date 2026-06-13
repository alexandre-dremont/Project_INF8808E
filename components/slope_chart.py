import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from data_preprocessing.dietary_compositions import dietary_compositions_pre_processing, load_data_dietary_compositions
from data_preprocessing.obesity_prevalence import obesity_prevalence_pre_processing_without_year
from data_preprocessing.ncd import ncd_risk_pre_processing, load_ncd_risk
from plotly.colors import qualitative


def create_multiple_slope_chart(nb_countries=10):

    df_dietary = load_data_dietary_compositions() 
    df_obesity = load_ncd_risk()

    categories = ["Boissons alcoolisées", "Sucre", "Huiles et graisses", "Viande", "Produits laitiers et œufs",
                "Fruits et légumes", "Racines féculentes", "Légumineuses", "Céréales et grains", "Autres", "Total"]
    obesity_col = "Prevalence of BMI>=30 kg/m² (obesity)"
    all_categories = categories + [obesity_col]

    years_dietary = sorted(df_dietary["Year"].unique())
    # first_year_dietary = years_dietary[0]

    df = df_dietary.merge(df_obesity, left_on=["Code", "Year"], right_on=["ISO", "Year"], how="left")\
                    .drop(columns=["ISO", "Country/Region/World"])
    
    # Première année commune aux deux datasets pour l'indexation
    # common_start_year = df.dropna(subset=[obesity_col])["Year"].min()
    common_start_year = 1980

    # On garde uniquement les pays avec des données d'obésité dès 1980
    countries_with_obesity = df[
        (df["Year"]==1980) & (df[obesity_col].notna())
    ]["Entity"].unique()[: nb_countries] # On affiche les n premiers pays
    countries = [c for c in df_dietary["Entity"].unique() if c in countries_with_obesity]

    # Couleurs 
    palette = qualitative.Dark24
    color_map = {category: palette[i % len(palette)] for i, category in enumerate(categories)}
    color_map[obesity_col] = "#FF0000"

    n_cols = 4
    n_rows = -(-len(countries) // n_cols)

    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=countries,
        # shared_yaxes=True
    )

    # Modifier la police des titres des subplots
    fig.update_annotations(
        font=dict(family="Inter, sans serif", size=13, color="#4a5568")
    )

    for i, country in enumerate(countries):
        row = i // n_cols + 1
        col = i % n_cols + 1

        df_country = df[df["Entity"] == country].sort_values("Year").copy()

        # print(df_country)

        # Valeurs de référence à la date commune
        ref_row = df_country[df_country["Year"] == common_start_year]

        if ref_row.empty:
            continue

        ref_values = ref_row[all_categories].iloc[0]

        # Indexation de toutes les données par rapport à la date commune
        for col_name in all_categories:
            ref = ref_values[col_name]
            if ref != 0 and pd.notna(ref):
                df_country[col_name] = (df_country[col_name] - ref) / ref
            else:
                df_country[col_name] = float('nan')
    
        # Affichage des apports caloriques journaliers
        for category in categories:
            fig.add_trace(go.Scatter(
                        x=df_country["Year"],
                        y=df_country[category],
                        name=category,
                        mode="lines+markers",
                        line=dict(color=color_map[category]),
                        showlegend=(i==0),
                        hovertemplate=hover_template_category(),
                        customdata=[[country, category]] * len(df_country)
                ),
                row=row,
                col=col
            )
        
        # Affichage de l'obésité
        fig.add_trace(go.Scatter(
                        x=df_country["Year"],
                        y=df_country["Prevalence of BMI>=30 kg/m² (obesity)"],
                        name="Obésité",
                        mode="lines+markers",
                        line=dict(color=color_map[obesity_col], width=3, dash="dash"),
                        showlegend=(i==0),
                        hovertemplate=hover_template_obesity(),
                        customdata=[[country]] * len(df_country)
                ),
                row=row,
                col=col
            )
        
        # Ligne verticale rouge à la date commune de référence
        fig.add_vline(
            x=common_start_year,
            line=dict(color="#BF5555", width=2)
        )



    fig.update_layout(

        # Style de plot
        template="plotly_white",
        height=300*n_rows,

        # Légende
        legend=dict(
            orientation="h", yanchor="top",
            y=-0.1, xanchor="center", x=0.5,
            itemclick=False, itemdoubleclick=False,
            font=dict(family="Inter, sans serif", size=11, color="#2c3e50"),
            # Cadre
            bordercolor="#2c3e50",
            borderwidth=1,
            bgcolor="#ffffff"
        ),

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        xaxis=dict(title=dict(text="Année", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   gridcolor="rgba(0,0,0,0.05)"),

        yaxis=dict(title="Variation par rapport à l'année " + str(common_start_year), tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
                   ticklabelstandoff=10),

        # title="Variation de l'apport calorique quotidien et de la prévalence de l'obésité",
    )

    fig.update_xaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096")
    )

    fig.update_yaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
        tickformat=".0%"
    )

    # Lignes verticales
    for year in years_dietary:
        fig.add_vline(
            x=year,
            line=dict(color="#4E4848", width=1)
        )

    return fig

def hover_template_category():
    return (
        'Pays : %{customdata[0]}'
        '<br>Année : %{x}'
        '<br>Catégorie : %{customdata[1]}'
        '<br>Valeur : %{y}'
        '<extra></extra>'
    )

def hover_template_obesity():
    return (
        'Pays : %{customdata[0]}'
        '<br>Année : %{x}'
        '<br>Obésité : %{y}'
        '<extra></extra>'
    )

def create_slope_chart(country="Canada"):
    df_dietary = dietary_compositions_pre_processing()
    df_dietary_country = df_dietary[df_dietary["Entity"]==country].drop(columns="Entity")

    categories = df_dietary.columns[2:]

    years_dietary = sorted(df_dietary_country.index)
    first_year_dietary = years_dietary[0]

    df_obesity = ncd_risk_pre_processing(country=country)
    df_obesity_country = df_obesity[df_obesity["Country/Region/World"]==country].drop(columns=["Country/Region/World", "ISO"])

    years_obesity = sorted(df_obesity_country.index)
    first_year_obesity = years_obesity[0]
    col = "Prevalence of BMI>=30 kg/m² (obesity)"

    df_obesity_country_men = df_obesity[df_obesity["Sex"]=="Men"].drop(columns="Sex")
    ref_obesity_men = df_obesity_country_men.loc[first_year_obesity, col]
    # print(ref_obesity_men)

    df_obesity_country_women = df_obesity[df_obesity["Sex"]=="Women"].drop(columns="Sex")
    ref_obesity_women = df_obesity_country_women.loc[first_year_obesity, col]
    # print(ref_obesity_women)

    fig=go.Figure()

    fig.add_trace(go.Scatter(
            x=df_obesity_country_men.index,
            y=df_obesity_country_men[col]/ref_obesity_men,
            name="Obesité chez les hommes"
        ))
    
    fig.add_trace(go.Scatter(
            x=df_obesity_country_women.index,
            y=df_obesity_country_women[col]/ref_obesity_women,
            name="Obesité chez les femmes"
        ))

    for c in categories:

        if first_year_dietary < first_year_obesity :
            first_year_dietary = first_year_obesity

        ref_category = df_dietary_country.loc[first_year_dietary, c]

        # print(ref)
        fig.add_trace(go.Scatter(
            x=df_dietary_country.index,
            y=df_dietary_country[c]/ref_category,
            name=c
        ))

    fig.update_layout(
        title="Variation de l'apport calorique quotidien et de la prévalence de l'obésité",
        xaxis_title="Année"
    )

    for year in years_obesity:
        fig.add_vline(
            x=year,
            line=dict(color="#4E4848", width=1)
        )

    return fig 