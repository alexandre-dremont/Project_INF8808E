import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_preprocessing.dietary_compositions import dietary_compositions_pre_processing, load_data_dietary_compositions
from data_preprocessing.obesity_prevalence import obesity_prevalence_pre_processing_without_year
from data_preprocessing.ncd import ncd_risk_pre_processing

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


def create_multiple_slope_chart(nb_countries=10):
    df_dietary = load_data_dietary_compositions()

    categories = df_dietary.columns[3:]
    countries = df_dietary["Entity"].unique()[: nb_countries]

    years_dietary = sorted(df_dietary["Year"].unique())
    first_year_dietary = years_dietary[0]

    n_cols = 3
    n_rows = -(-len(countries) // n_cols)

    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=countries,
        shared_yaxes=True
    )

    for i, country in enumerate(countries):
        row = i // n_cols + 1
        col = i % n_cols + 1

        df_dietary_country = df_dietary[df_dietary["Entity"] == country]
    
        for category in categories:
            # ref_category = df_dietary_country.iloc[0][category]
            # print(f"Affichage en cours {country}, {category}, {row}, {col}")

            # print(df_dietary_country.head())

            fig.add_trace(go.Scatter(
                        x=df_dietary_country["Year"],
                        y=df_dietary_country[category],
                        name=category,
                        showlegend=(i==0),
                        # text=df_dietary[category].round(1),
                        # textposition="inside",
                        # insidetextanchor="middle"
                ),
                row=row,
                col=col
            )

    fig.update_layout(
        title="Variation de l'apport calorique quotidien et de la prévalence de l'obésité",
        xaxis_title="Année",
        yaxis_title="Variation",
        # xaxis=dict(type="category"),
        legend_title="Catégories",
        height=300*n_rows
    )

    # print(years_dietary)

    for year in years_dietary:
        fig.add_vline(
            x=year,
            line=dict(color="#4E4848", width=1)
        )


    # fig.update_xaxes(type="category")

    # print("Affichage terminé")

    return fig


