import plotly.express as px
from data_preprocessing.banque_mondiale import banque_mondiale_pre_processing
from data_preprocessing.obesity_prevalence import obesity_prevalence_pre_processing
import pandas as pd

def create_bubble_chart():
    df_indicator = banque_mondiale_pre_processing(scale=False)
    df_obesity = obesity_prevalence_pre_processing()

    # print(df_indicator.index)
    # print(df_obesity["Country"])

    df = df_indicator.merge(df_obesity, left_on="Country Name", right_on="Country")

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
        log_y=True,
        hover_data="Country",
        color_discrete_sequence=px.colors.qualitative.Set1,
        size_max=100,
    )

    return fig