import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

st.set_page_config(
    page_title="Consumer Churn Dashboard",
    page_icon="📊",
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown("""
<style>
/* Style for individual metric boxes */
.metric-box {
    padding: 20px;
    border-radius: 8px;
    color: white;
    text-align: center;
    font-size: 16px;
    font-weight: bold;
}

.box1 { background-color: #2c545b;color: #ffffff; }
.box2 { background-color: #66b3ff;color: #000000; }
.box3 { background-color: #2eb8b8; color:#000000;}
.box4 { background-color: #71dada;color: #000000; }

.container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    height: 160px; /* Adjust height to auto for flexibility */
    color: white; /* Text color */
    margin: 5px;  /* Reduced margin */
}
.donut-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    margin:10px;
}
.chart-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
} 
.custom-sidebar-header {
        text-align: center;
        font-size: 24px; /* Adjust font size as needed */
        font-weight: bold;
        margin-bottom: 15px;
 }
 .selected-variable-box {
        background-color: #ff4b4b;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

#def change_df(df):
    
df = pd.read_csv('churn.csv')
quants = list(df.columns)
del quants[quants.index('internationalplan')]
del quants[quants.index('churn')]

with st.sidebar:
    st.header("Consumder Dashboard")
    voicemail_plan = st.multiselect("VoiceMail Plan",['Yes','No'])
    
    interested_variable = st.selectbox("Voice Quant to View",quants)
    
    st.button('Change',on_click=print(voicemail_plan))
    
st.title("Customer Dashboard")

no_of_customers = df.shape[0]
day_charge = round(np.sum(df['totaldaycharge']),2)
evening_and_night_charge = round(np.sum(df['totalevecharge']+df['totalnightcharge']),2)
intl_charge = round(np.sum(df['totalintlcharge']),2)

col1,col2,col3,col4 = st.columns(4)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-box box1'>Total No. of Customers<br><span style='font-size: 24px;'>{no_of_customers}</span></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box box1'>Total. Day Time Charge<br><span style='font-size: 24px;'>{day_charge}</span></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box box1'>Total eve & night charge<br><span style='font-size: 24px;'>{evening_and_night_charge}</span></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box box1'>Total overseas Charge<br><span style='font-size: 24px;'>{intl_charge}</span></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.header("Boxplot based on Churn") 
    fig = px.box(df,y=interested_variable,x="churn",labels={'y':'Values'})
    st.plotly_chart(fig)
   
with col2:
    st.header("Distribution of the data")
    fig_2 = px.histogram(df,x=interested_variable)
    st.plotly_chart(fig_2)
    
with col3:
    st.header("Intl Plan")
    fig = px.box(df,y=interested_variable,x="internationalplan",labels={'y':'Values'})
    st.plotly_chart(fig)
    

col_1, col_2 = st.columns(2)
with col_1:
    labels = ['Stayed','Left']
    # Create a pie chart
    fig = px.pie(names=labels, values=list(df['churn'].value_counts()), title="Pie Chart of Churn Status")

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)
    
with col_2:
    crosstab = pd.crosstab(df['churn'], df['internationalplan'])
    melted_crosstab = crosstab.reset_index().melt(id_vars='churn', var_name='internationalplan', value_name='count')
    # Create a heatmap using Plotly
    fig = px.density_heatmap(melted_crosstab, x='churn', y='internationalplan', z='count', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    

