import plotly.express as px
from data_preprocessing.banque_mondiale import load_reduced_banque_mondiale
from data_preprocessing.obesity_prevalence import load_income_group
from data_preprocessing.ncd import load_ncd_risk
import math


def create_bubble_chart():
    "Fonction chargée de créer le diagramme à bulles"
    # Chargement des données prétraitées 
    df_indicator = load_reduced_banque_mondiale()
    df_obesity = load_ncd_risk()
    df_income_group = load_income_group()

    # Catégorie des pays par niveau de richesse
    category_labels = {
        "Low income": "Revenu faible", 
        "Lower-middle income": "Revenu intermédiaire inférieur", 
        "Upper-middle income": "Revenu intermédiaire supérieur", 
        "High income": "Revenu élevé"
    }

    # Couleurs associées aux catégories
    color_map = {
        "Low income" : "#cf5228", 
        "Lower-middle income" : "#f1b64f", 
        "Upper-middle income": "#2ab3a3", 
        "High income": "#6999b7"
    }

    # Fusion/complétion de jeux de données
    df = df_indicator.merge(df_obesity, left_on=["Country Code", "Year"], 
                                        right_on=["ISO", "Year"], how="inner")
    df = df.dropna(subset=["Health_Expenditure", "GDP_PPP", "Prevalence of BMI>=30 kg/m² (obesity)"])

    # Ajouter Income_group
    df = df.merge(df_income_group, left_on="Country Name", right_on="Country", how="left")

    df["Income_group"] = df["Income_group"].map(category_labels).fillna(df["Income_group"])

    # Définition d'une figure type scatter
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


    # Création de la légende des bulles
    # Paramètres de la légende bulles
    unites = [(50, "50$/hab./an"), (500, "500$/hab./an"), (2500, "2.500$/hab./an")]
    x_mid =  0.9
    y_ub = 0.98

    bubble_shapes = []
    bubble_texts = []

    # Création d'un cadre
    bubble_shapes.append(dict(
        type="rect",
        xref="paper", yref="paper",
        x0=0.8, y0=y_ub-0.57,
        x1=1, y1=y_ub,
        line=dict(color="#718096", width=0.5),
        fillcolor="white",
    ))

    # Ajout d'un titre au cardre
    bubble_texts.append(dict(
        text="Dépenses de santé<br>par habitant (US$ PPA)",
        xref="paper", yref="paper",
        x=x_mid, y=0.95, 
        xanchor="center", yanchor="top",
        showarrow=False, 
        font=dict(family="Inter, sans serif", size=12, color="#1d2a37")
    )) 

    # Pour chaque bulle de la légende
    for i, (m, t) in enumerate(unites):
        radius = (math.sqrt(m)/math.sqrt(df["Health_Expenditure"].max()))*0.05
        y_pos = y_ub - (i+1)*0.15
        if i==1:
            y_pos += 0.015

        # Créer un marker circulaire
        bubble_shapes.append(dict(type="circle", 
                                  xref="paper", yref="paper",
                                  x0=x_mid-radius, y0=y_pos-radius*2,
                                  x1=x_mid+radius, y1=y_pos+radius*2,
                                  line=dict(color="#2c3e50", width=0.5),
                                  fillcolor="white",
                                  layer="above"))
        
        # Annoter le montant associé à chaque cercle
        bubble_texts.append(dict(
            text=t,
            xref="paper", yref="paper",
            x=x_mid, y=y_pos - 2*(radius+0.02),
            xanchor="center", yanchor="bottom",
            showarrow=False, 
            font=dict(family="Inter, sans serif", size=10, color="#718096")
        ))


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
        height=650,
        margin=dict(l=80, r=60, t=60, b=60),

        # Info-bulles
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e2e8f0",
                        font=dict(family="Inter, sans serif", size=12, color="#2c3e50")),

        # Légende groupes de richesse
        legend=dict(
            title=dict(text="Groupes de richesse :"),
            font=dict(family="Inter, sans serif", size=12, color="#718096"),
            orientation="h", yanchor="bottom",
            y=1.03, xanchor="center", x=0.5,
            bgcolor="#ffffff"
        ),

        # Barre d'animation
        sliders=[dict(
            y=-0.03,
            yanchor="top",
            currentvalue=dict(
                font=dict(family="Inter, sans serif", size=12, color="#718096"),
                prefix="Année : ",
                visible=True,
            )
        )],       

        # Axes
        xaxis=dict(range=[0, df["Prevalence of BMI>=30 kg/m² (obesity)"].max() * 1.05],
                   title=dict(text="Prévalence de l'obésité (%)", 
                   font=dict(family="Inter, sans serif", size=12, color="#718096")), 
                   tickfont=dict(family="Inter, sans serif", size=11, color="#718096"),
                   tickformat=".0%",
                   gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(range=[0, y_max],
                   title="PIB par habitant en parité de pouvoir d'achat (US$)", tickfont=dict(family="Inter, sans serif", size=12, color="#2c3e50"),
                   ticklabelstandoff=10),

        # Légende des bulles
        shapes=bubble_shapes,
        annotations=bubble_texts
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

    # Paramètres du slider
    menu.x = 0
    menu.y = -0.05
    menu.yanchor = "top"
    menu.xanchor = "left"
    menu.showactive = False

    # Vitesse du slider
    for step in fig.layout.sliders[0]["steps"]:
        step["args"][1]["frame"]["duration"] = frame_duration

    # Uniformisation du style des axes
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
    """Fonction chargée de définir le contenu des étiquettes (hover)"""
    return (
        '<b>%{customdata[0]}</b>'
        "<br>Prévalence de l'obésité : %{x:.1%}"
        "<br>PIB par habitant (PPA) : %{y:,.0f} $"
        "<br>Dépenses de santé par habitant : %{customdata[3]:,.0f} $"
        '<br>Année : %{customdata[2]}'
        '<br>Groupe de revenus : %{customdata[1]}'
        '<extra></extra>'
    )