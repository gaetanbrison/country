import streamlit as st
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: monospace;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#272727,#272727);
    color: white;
}
.Widget>label {
    color: white;
    font-family: monospace;
}
[class^="st-b"]  {
    color: white;
    font-family: monospace;
    text-align: center;
}
[data-baseweb="base-input"] {
    background-color: transparent;
}
.st-av {
    background-color: transparent;
}
.st-at {
   background-color: #000000;
}
footer {
    font-family: monospace;
}
header .decoration {
    background-image: none;
}
.st-eq {
    color: white;
}
::-webkit-scrollbar {
    background-color: white;
}
.menu-item-highlighted {
    background-color: rgb(246, 51, 102);
}
body {
    text-align: center;
}
table {
    margin: 0 auto;
}
.css-1eucglo {
    display: inline-table;
}
.streamlit-button.primary-button {
    background-color: rgb(246, 51, 102);
    color: white;
    border: 1px solid #000000;
    transition: 0.1s all;
}
button.streamlit-button.small-button.primary-button:hover {
    color: black;
    border: 1px solid #000000;
}
button.streamlit-button.xsmall-button.primary-button:hover {
    color: black;
    border: 1px solid #000000;    
}
.streamlit-button.primary-button:focus:not(:active) {
    border-color: black;
    color: white;
}
.streamlit-button:focus {
    box-shadow: none;
    outline: none;
}
button.streamlit-button.small-button.primary-button:active { 
    transform: scale(0.98);  
    box-shadow: 3px 2px 22px 1px rgba(0, 0, 0, 0.24); 
}
.fixed-width.stText {
    font-size: 24px;
    color: rgb(246, 51, 102);
}
hr:not([size]) {
    height: 2px;
}
.streamlit-button.icon-button:hover {
    border-color: #f63366;
    color: #f63366;
}
.streamlit-button.icon-button {
    background-color: initial;
    border: 1px solid #d2d2d2;
    color: #d2d2d2;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.sidebar.subheader('Input Features')

# User input controls
feat_popu = st.sidebar.number_input('Population (Example: 1000000)', min_value=int(7e3), max_value=int(14e8), value=int(3e7),step=int(1e3))
feat_area = st.sidebar.slider('Area (sq. Km)', min_value=0, max_value=int(17e6), value=int(10e5), step=int(1e3))
feat_dens = st.sidebar.slider('Population Density (per sq. Km)', min_value=0, max_value=12000, value=2500, step=10)
feat_cost = st.sidebar.slider('Coastline/Area Ratio', min_value=0, max_value=900, value=300, step=1)
feat_migr = st.sidebar.slider('Annual Net Migration (per 1000 people)', min_value=-21, max_value=25, value=5, step=1) 
feat_mort = st.sidebar.slider('Infant Mortality (per 1000 births)', min_value=0, max_value=195, value=40, step=1)
feat_litr = st.sidebar.slider('Population Literacy (%)', min_value=0, max_value=100, value=80, step=1)
feat_phon = st.sidebar.slider('Phones (per 1000 people)', min_value=0, max_value=1050, value=250, step=1)
st.sidebar.write('----------------------------------')
st.sidebar.write('Arable, Crops, and Other land should add up to 100%')
st.sidebar.write('----------------------------------')
feat_arab = st.sidebar.slider('Arable Land (%)', min_value=0, max_value=100, value=25, step=1)
feat_crop = st.sidebar.slider('Crops Land (%)', min_value=0, max_value=100, value=5, step=1)
feat_othr = st.sidebar.slider('Other Land (%)', min_value=0, max_value=100, value=70, step=1)
st.sidebar.write('----------------------------------')
st.sidebar.write('See the climate table on the main page for what the climate values represent')
st.sidebar.write('----------------------------------')
feat_clim = st.sidebar.selectbox('Climate', options=(1, 1.5, 2, 2.5, 3, 4), index=5)
feat_brth = st.sidebar.slider('Annual Birth Rate (births/1,000 people)', min_value=7, max_value=50, value=20, step=1)
feat_deth = st.sidebar.slider('Annual Death Rate (deaths/1,000 people)', min_value=2, max_value=30, value=10, step=1)
st.sidebar.write('----------------------------------')
st.sidebar.write('Agricultural, Industrial, and Service sector should all add up to 1')
st.sidebar.write('----------------------------------')
feat_agrc = st.sidebar.slider('Agricultural Sector', min_value=0.0, max_value=1.0, value=0.15, step=0.05)
feat_inds = st.sidebar.slider('Industrial Sector', min_value=0.0, max_value=1.0, value=0.25, step=0.05)
feat_serv = st.sidebar.slider('Service Sector', min_value=0.0, max_value=1.0, value=0.60, step=0.05)
st.sidebar.write('----------------------------------')
st.sidebar.write('See the region table on the main page for what the region values represent')
st.sidebar.write('----------------------------------')
feat_regn = st.sidebar.selectbox('Region', options=(1,2,3,4,5,6,7,8,9,10,11), index=10)

if feat_regn == 1:
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 2: 
    feat_regn_2 = 1
    feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 3: 
    feat_regn_3 = 1
    feat_regn_2 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 4: 
    feat_regn_4 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 5: 
    feat_regn_5 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 6: 
    feat_regn_6 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 7: 
    feat_regn_7 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_8 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 8: 
    feat_regn_8 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_9 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 9: 
    feat_regn_9 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_10 = feat_regn_11 = 0
elif feat_regn == 10: 
    feat_regn_10 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_11 = 0
else: 
    feat_regn_11 = 1
    feat_regn_2 = feat_regn_3 = feat_regn_4 = feat_regn_5 = feat_regn_6 = feat_regn_7 = feat_regn_8 = feat_regn_9 = feat_regn_10 = 0

user_input = np.array([feat_popu, feat_area, feat_dens, feat_cost, feat_migr, 
                        feat_mort, feat_litr, feat_phon, feat_arab, feat_crop, 
                        feat_othr, feat_clim, feat_brth, feat_deth, feat_agrc, 
                        feat_inds, feat_serv, feat_regn_2, feat_regn_3,
                        feat_regn_4, feat_regn_5, feat_regn_6, feat_regn_7, 
                        feat_regn_8, feat_regn_9, feat_regn_10, feat_regn_11]).reshape(1,-1)

# Title
st.title('GDP Prediciton App')
'''
         Use this app to estimate the GDP per capita for a country.
         
         Use the sliders and input boxes on the left to choose the feature 
         values and then click the **Estimate GDP** button to get a prediction
         for the GDP per capita.
'''

# Load model
model = pickle.load(open('./rf_grid_model.pkl', 'rb'))

# Padding
st.text(" \n")
st.text(" \n")
st.text(" \n")

# Estimate GDP on button press
if st.button('Estimate GDP'):
    
    # Make predictions
    gdp_predictions = model.predict(user_input)
    st.text(" \n")
    st.text(" \n")
    st.write('The estimated GDP per capita is:')
    st.text('$' + str(format(gdp_predictions[0], '.2f')))

st.markdown('---')

# Padding
st.text(" \n")
st.text(" \n")
st.text(" \n")

st.write('''
          | Value | Climate |
          | :-: | :- |
          | **1** | Dry tropical or tundra and ice |
          | **1.5** | A mixture of dry and wet tropical |
          | **2** | Wet tropical |
          | **2.5** | A mixture of wet tropical and humid subtropical |
          | **3** | Temperate humid subtropical and temperate continental |
          | **4** | Dry hot summers and wet winters |
''')

# Padding
st.text(" \n")
st.text(" \n")
st.text(" \n")

st.write('''
          | Value | Region |
          | :-: | :- |
          | **1** | ASIA (EX. NEAR EAST) |
          | **2** | BALTICS |
          | **3** | C.W. OF IND. STATES |
          | **4** | EASTERN EUROPE |
          | **5** | LATIN AMER. & CARIB |
          | **6** | NEAR EAST |
          | **7** | NORTHERN AFRICA |
          | **8** | NORTHERN AMERICA |
          | **9** | OCEANIA |
          | **10** | SUB-SAHARAN AFRICA |
          | **11** | WESTERN EUROPE | 
''')
