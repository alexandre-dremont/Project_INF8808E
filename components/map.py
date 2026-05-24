import plotly.express as px

def create_map(df):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="All_Adults_Obesity",
        range_color=(0, 50),
        color_continuous_scale="Reds",
        title="L'obésité dans le monde"
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True),
        coloraxis_colorbar=dict(title="%")
    )

    return fig
