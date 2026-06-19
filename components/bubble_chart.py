import plotly.express as px
import plotly.graph_objects as go
from data_preprocessing.banque_mondiale import load_reduced_banque_mondiale
from data_preprocessing.obesity_prevalence import load_income_group
from data_preprocessing.ncd import load_ncd_risk
import pandas as pd

# def create_bubble_chart():
#     df_indicator = banque_mondiale_pre_processing(scale=False)
#     df_obesity = obesity_prevalence_pre_processing_without_year()

#     # print(df_indicator.index)
#     # print(df_obesity["Country"])

#     df = df_indicator.merge(df_obesity, left_on="Country Name", right_on="Country")
#     df = df.dropna(subset=["Health_Expenditure"])

#     # print(df)

#     fig = px.scatter(
#         df,
#         y='GDP_PPP',
#         x='All_Adults_Obesity',
#         color='Income_group',
#         size='Health_Expenditure',
#         # animation_frame='Year',
#         # animation_group='Country Name',
#         # log_x=True,
#         # log_y=True,
#         custom_data=["Country", "Income_group", "Year", "Health_Expenditure"],
#         color_discrete_sequence=px.colors.qualitative.Set1,
#         size_max=70,
#         labels={
#             "GDP_PPP" : "PIB par habitant en parité de pouvoir d'achat",
#             "All_Adults_Obesity": "Prévalence de l'obésité (%)",
#             "Health_Expenditure": "Dépenses de santé par habitant",
#             "Income_group": "Groupe de revenus"
#         }
#     )

#     fig.update_traces(hovertemplate=hover_tempate())

#     fig.update_layout(
#         # Style de plot
#         template="plotly_white",

#         # Info-bulles
#         hovermode="closest",
#         hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
#                         font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

#         # Légende
#         legend=dict(
#             title=dict(text="Groupe de revenus"),
#             font=dict(family="Inter, sans serif", size=12, color="#718096"),
#             orientation="h", yanchor="top",
#             y=-0.3, xanchor="center", x=0.5,
#             bordercolor="#e2e8f0", borderwidth=1, 
#             bgcolor="#ffffff"
#         ),

#         # Axes
#         xaxis=dict(title=dict(text="Prévalence de l'obésité (%)", 
#                    font=dict(family="Inter, sans serif", size=12, color="#718096")), 
#                    tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
#                    gridcolor="rgba(0,0,0,0.05)"),

#         yaxis=dict(title="PIB par habitant en parité de pouvoir d'achat (en US$)", tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
#                    ticklabelstandoff=10),
#     )

#     fig.update_xaxes(
#         title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
#         tickfont=dict(family="Inter, sans serif", size=11, color="#718096")
#     )

#     fig.update_yaxes(
#         title_font=dict(family="Inter, sans serif", size=12, color="#718096"),
#         tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
#     )

#     return fig

def create_bubble_chart():
    df_indicator = load_reduced_banque_mondiale()
    df_obesity = load_ncd_risk()
    df_income_group = load_income_group()

    # print(df_indicator.head())
    # print(df_obesity.head())

    category_labels = {
        "Low income": "Revenu faible", 
        "Lower-middle income": "Revenu intermédiaire inférieur", 
        "Upper-middle income": "Revenu intermédiaire supérieur", 
        "High income": "Revenu élevé"
    }

    # Couleurs associées aux catégories
    color_map = {
        "Low income" : "#e63946", 
        "Lower-middle income" : "#f4a261", 
        "Upper-middle income": "#2a9d8f", 
        "High income": "#457b9d"
    }

    df = df_indicator.merge(df_obesity, left_on=["Country Code", "Year"], 
                                        right_on=["ISO", "Year"], how="inner")
    df = df.dropna(subset=["Health_Expenditure", "GDP_PPP", "Prevalence of BMI>=30 kg/m² (obesity)"])

    # Ajouter Income_group
    df = df.merge(df_income_group, left_on="Country Name", right_on="Country", how="left")

    df["Income_group"] = df["Income_group"].map(category_labels).fillna(df["Income_group"])

    # print(df.head())

    fig = px.scatter(
        df,
        y='GDP_PPP',
        x='Prevalence of BMI>=30 kg/m² (obesity)',
        color='Income_group',
        size='Health_Expenditure',
        animation_frame='Year',
        animation_group='Country Name',
        custom_data=["Country Name", "Income_group", "Year", "Health_Expenditure"],
        color_discrete_map={category_labels[k]: v for k, v in color_map.items()},
        category_orders={"Income_group": list(category_labels.values())},
        size_max=70,
        labels={
            "GDP_PPP" : "PIB par habitant en parité de pouvoir d'achat",
            "All_Adults_Obesity": "Prévalence de l'obésité (%)",
            "Health_Expenditure": "Dépenses de santé par habitant",
            "Income_group": "Groupe de revenus"
        }
    )

    # # Valeurs de référence pour l'échelle des bulles
    # size_legend_values = [57, 221, 690, 4655]
    # size_legend_labels = ["57 $ (Q25)", "221 $ (Q50)", "690 $ (Q75)", "4 655 $ (Q95)"]

    # size_ref = 2 * df["Health_Expenditure"].max() / (70*2)

    # for val, label in zip(size_legend_values, size_legend_labels):
    #     fig.add_trace(go.Scatter(
    #         x=[None],
    #         y=[None],
    #         mode="markers",
    #         marker=dict(
    #             size=val,
    #             sizemode="area",
    #             sizeref=size_ref,
    #             color="rgba(150,150,150,0.5)",
    #             line=dict(color="#718096", width=1)
    #         ),
    #         name=label,
    #         legendgroup="size_legend",
    #         showlegend=True
    #     ))

    # Valeur max sur l'axe Y
    y_max = df["GDP_PPP"].max() * 1.1

    # Info-bulles pour l'animation
    hovertemplate = hover_tempate()
    fig.update_traces(hovertemplate=hovertemplate)

    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hovertemplate

    fig.update_layout(
        # Style de plot
        template="plotly_white",

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Légende
        legend=dict(
            title=dict(text="Groupes de richesse"),
            font=dict(family="Inter, sans serif", size=12, color="#718096"),
            orientation="h", yanchor="top",
            y=-0.5, xanchor="center", x=0.5,
            bordercolor="#e2e8f0", borderwidth=1, 
            bgcolor="#ffffff"
        ),

        # Barre d'animation
        sliders=[dict(
            y=2,
            currentvalue=dict(
                font=dict(family="Inter, sans serif", size=12, color="#718096"),
                prefix="Année : ",
                visible=True,
            )
        )],       

        # Axes
        xaxis=dict(range=[0, df["Prevalence of BMI>=30 kg/m² (obesity)"].max() * 1.1],
                   title=dict(text="Prévalence de l'obésité (%)", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   gridcolor="rgba(0,0,0,0.05)"),

        yaxis=dict(range=[0, y_max],
                   title="PIB par habitant en parité de pouvoir d'achat (US$)", tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
                   ticklabelstandoff=10),
    )

    # Boutons play/pause 
    frame_duration = 1500 # Vitesse d'animation

    menu = fig.layout.updatemenus[0]

    menu.buttons = [
        dict(
            label="Animer",
            method="animate",
            args=[
                None, {
                    "frame": {"duration": frame_duration, "redraw": True},
                    "transition": {"duration": 500},
                    "fromcurrent": True
                }
            ]
        )
    ]

    menu.x = 0
    menu.y = 2
    menu.xanchor = "left"
    menu.showactive = False

    # Vitesse du slider
    for step in fig.layout.sliders[0]["steps"]:
        step["args"][1]["frame"]["duration"] = frame_duration

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
        "<br>Prévalence de l'obésité : %{x:.1%}"
        "<br>PIB par habitant (PPA) : %{y:,.0f} $"
        "<br>Dépenses de santé par habitant : %{customdata[3]:,.0f} $"
        '<br>Année : %{customdata[2]}'
        '<br>Groupe de revenus : %{customdata[1]}'
        '<extra></extra>'
    )