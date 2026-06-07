import plotly.graph_objects as go
from data_preprocessing.banque_mondiale import banque_mondiale_pre_processing
from data_preprocessing.dietary_compositions import dietary_compositions_pre_processing_total
from data_preprocessing.physical_activity import physical_activity_pre_processing
import pandas as pd

def create_radar_chart(countries=["Canada", "France", "United States"]):
    df_indicator = banque_mondiale_pre_processing()
    df_dietary = dietary_compositions_pre_processing_total()
    df_activity = physical_activity_pre_processing()

    # print(df_indicator[df_indicator["Entity"]==countries[-1]])
    # print(df_dietary[df_dietary["Entity"]==countries[-1]])
    # print(df_activity[df_activity["Location"]==countries[-1]])

    # print(df_indicator.columns)
    # print(df_dietary.columns)
    # print(df_activity.columns)

    df = df_indicator.merge(df_dietary, on="Entity", how="inner").drop(columns=["Code"])\
                    .merge(df_activity, left_on="Entity", right_on="Location", how="inner").drop(columns=["Location"])
    df.set_index("Entity", inplace=True)

    # print(df.head())
    # print(df.columns)

    categories = {
        "GDP_PPP": "PIB par habitant en parité de pouvoir d'achat",
        "Health_Expenditure": "Dépense de santé par habitant",
        "Gini": "Index de Gini",
        "Total":"Apports caloriques quotidiens",
        "Both_sexes_val": "Sédentarité"
    }

    colors = [
        "rgba(255, 99,  71,  0.3)",   # tomate
        "rgba(30,  144, 255, 0.3)",   # bleu
        "rgba(50,  205, 50,  0.3)",   # vert
    ]

    fig = go.Figure()

    for i, c in enumerate(countries):
        # print(df.loc[c, categories.keys()])

        fig.add_trace(go.Scatterpolar(
            r=df.loc[c, categories.keys()],
            theta=list(categories.values()),
            fill='toself',
            name=c,
            fillcolor=colors[i % len(colors)],
            line=dict(color=colors[i % len(colors)].replace("0.3", "1"))
        ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        ),
    ),
    showlegend=True,
    title="Comparaison des indicateurs par pays"
    )

    # fig.update_layout(
    #     paper_bgcolor="rgba(0,0,0,0)",
    #     plot_bgcolor="rgba(0,0,0,0)"
    # )

    return fig

# print(create_radar_chart())