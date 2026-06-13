import plotly.express as px
from data_preprocessing.banque_mondiale import banque_mondiale_pre_processing
from data_preprocessing.obesity_prevalence import obesity_prevalence_pre_processing, obesity_prevalence_pre_processing_without_year
import pandas as pd

def create_bubble_chart():
    df_indicator = banque_mondiale_pre_processing(scale=False)
    df_obesity = obesity_prevalence_pre_processing_without_year()

    # print(df_indicator.index)
    # print(df_obesity["Country"])

    df = df_indicator.merge(df_obesity, left_on="Country Name", right_on="Country")
    df = df.dropna(subset=["Health_Expenditure"])

    # print(df)

    fig = px.scatter(
        df,
        y='GDP_PPP',
        x='All_Adults_Obesity',
        color='Income_group',
        size='Health_Expenditure',
        # animation_frame='Year',
        # animation_group='Country Name',
        # log_x=True,
        # log_y=True,
        custom_data=["Country", "Income_group", "Year"],
        color_discrete_sequence=px.colors.qualitative.Set1,
        size_max=70,
        labels={
            "GDP_PPP" : "PIB par habitant en parité de pouvoir d'achat",
            "All_Adults_Obesity": "Prévalence de l'obésité (%)",
            "Health_Expenditure": "Dépenses de santé par habitant",
            "Income_group": "Groupe de revenus"
        }
    )

    fig.update_traces(hovertemplate=hover_tempate())

    fig.update_layout(
        # Style de plot
        template="plotly_white",

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Légende
        legend=dict(
            title=dict(text="Groupe de revenus"),
            font=dict(family="Inter, sans serif", size=12, color="#718096"),
            orientation="h", yanchor="top",
            y=-0.3, xanchor="center", x=0.5,
            bordercolor="#e2e8f0", borderwidth=1, 
            bgcolor="#ffffff"
        ),

        # Axes
        xaxis=dict(title=dict(text="Prévalence de l'obésité (%)", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   gridcolor="rgba(0,0,0,0.05)"),

        yaxis=dict(title="PIB par habitant en parité de pouvoir d'achat (en US$)", tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
                   ticklabelstandoff=10),
    )

    fig.update_xaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096")
    )

    fig.update_yaxes(
        title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
        tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
    )

    return fig

def hover_tempate():
    return (
        '<b>%{customdata[0]}</b>'
        "<br>Prévalence de l'obésité : %{x:.1f}%"
        "<br>PIB par habitant (PPA) : %{y:,.0f} $"
        '<br>Année : %{customdata[2]}'
        '<br>Groupe de revenus : %{customdata[1]}'
        '<extra></extra>'
    )