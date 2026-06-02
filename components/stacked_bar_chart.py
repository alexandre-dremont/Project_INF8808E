import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_preprocessing.dietary_compositions import dietary_compositions_pre_processing

def create_stacked_bar_chart(country="Canada"):
    df = dietary_compositions_pre_processing()

    years_to_show = df[df['Year'] % 10 == 0]["Year"].unique()
    df_filtered = df[(df["Year"].isin(years_to_show)) & (df["Entity"]==country)]

    fig = go.Figure()

    categories = ['Other', 'Alcoholic beverages', 'Sugar',
       'Oils and fats', 'Meat', 'Dairy and eggs', 'Fruits and vegetables',
       'Starchy roots', 'Pulses', 'Cereals and grains']
    
    for category in categories:
        fig.add_trace(go.Bar(
                    x=df_filtered["Year"],
                    y=df_filtered[category],
                    name=category,
            ))
    
    fig.update_layout(
        barmode="stack",
        title="Évolution temporelle de la consommation alimentaire",
        xaxis_title="Année",
        yaxis_title="Valeur",
        xaxis=dict(type="category"),
        legend_title="Catégories"
    )
        
    return fig

def create_stacked_bar_chart_multi(countries=["Canada", "United States", "France"]):

    categories = ['Other', 'Alcoholic beverages', 'Sugar',
       'Oils and fats', 'Meat', 'Dairy and eggs', 'Fruits and vegetables',
       'Starchy roots', 'Pulses', 'Cereals and grains']
    
    df = dietary_compositions_pre_processing()

    n_cols = 2
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

        df_country = df[df["Entity"] == country]
        df_filtered = df_country[df_country["Year"] % 10 ==0]
    
        for category in categories:
            fig.add_trace(go.Bar(
                        x=df_filtered["Year"],
                        y=df_filtered[category],
                        name=category,
                        showlegend=(i==0),
                        # text=df_filtered[category].round(1),
                        # textposition="inside",
                        # insidetextanchor="middle"
                ),
                row=row,
                col=col
            )
    
    fig.update_layout(
        barmode="stack",
        title="Évolution temporelle de la consommation alimentaire dans différents pays",
        xaxis_title="Année",
        yaxis_title="Valeur",
        xaxis=dict(type="category"),
        legend_title="Catégories",
        height=300*n_rows
    )

    fig.update_xaxes(type="category")
        
    return fig