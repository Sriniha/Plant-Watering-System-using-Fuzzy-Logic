import streamlit as st
import numpy as np
from algorithm.fuzzy_logic import FuzzyLogic
from algorithm.visualizer import TemperatureVisualizer
from algorithm.visualizer import SoilMoistureVisualizer
from algorithm.visualizer import LightIntensityVisualizer
from algorithm.visualizer import WateringSpeedVisualizer
import matplotlib.pyplot as plt
import pandas as pd

# Initialize st.session_state.page1 if it doesn't exist
if 'page1' not in st.session_state:
    st.session_state.page1 = {'is_first_load': True, 'temperature': 20.0, 'soil_moisture': 50.0, 'light_intensity': 500.0}


st.set_page_config(page_title='Automatic Plant Watering System', page_icon=r"C:\Users\91709\Downloads\watering-system-master\watering-system-master\images\logo.png")
st.image(image=r"C:\Users\91709\Downloads\watering-system-master\watering-system-master\images\logo.png", width=100)
st.title('Automatic Plant Watering System')

st.markdown(
    f"""
        <style>
            /* Make the default header of streamlit invisible */
            .css-18ni7ap.e8zbici2 {{
                opacity: 0
            }}

            /* Make the default footer of streamlit invisible */
            .css-h5rgaw.egzxvld1 {{
            opacity: 0
            }}

            /* Change width and padding of the page */
            .block-container.css-91z34k.egzxvld4 {{
                width: 100%;
                padding: 0.5rem 1rem 10rem;
                # max-width: none;
            }}

            /* Change padding of the pages list in the sidebar */
            .css-wjbhl0, .css-hied5v {{
                padding-top: 2rem;
                padding-bottom: 0.25rem;
            }}

            .text {{
                font-size: 20px
            }}

            .center {{
                text-align: center
            }}

            .text.center {{
                font-size: 25px

            }}
        </style>
        """, unsafe_allow_html=True
    )

submitted = False
temperature_input = 0
soil_moisture_input = 0
light_intensity_input = 0

with st.sidebar:

    # A workaround using st.session_state and callback to keep input value during navigating through other pages
    if "page1" not in st.session_state:
        st.session_state.page1 = {'is_first_load': True, 'temperature': 20.0, 'soil_moisture': 50.0, 'light_intensity': 500.0}

    for k, v in st.session_state.items():
        st.session_state[k] = v

    def submit_temperature():
        st.session_state.page1['temperature'] = st.session_state.temperature_input_value

    def submit_soil_moisture():
        st.session_state.page1['soil_moisture'] = st.session_state.soil_moisture_input_value

    def submit_light_intensity():
        st.session_state.page1['light_intensity'] = st.session_state.light_intensity_input_value

    st.title("Input Parameters")
    temperature_input = st.number_input("**Temperature (°C):**", min_value=-20.0, max_value=50.0, step=0.1, value=st.session_state.page1['temperature'], key='temperature_input_value', on_change=submit_temperature)
    soil_moisture_input = st.number_input("**Soil Moisture (%)**", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.page1['soil_moisture'], key='soil_moisture_input_value', on_change=submit_soil_moisture)
    light_intensity_input = st.number_input("**Light Intensity PAR (µmol/m²/s)**", min_value=0.0, max_value=1000.0, step=0.1, value=st.session_state.page1['light_intensity'], key='light_intensity_input_value', on_change=submit_light_intensity)

    col1, col2, col3 = st.columns([1, 0.5, 0.477])
    with col1:
        if st.button("Submit"):
            st.session_state.page1['is_first_load'] = False
            submitted = True
    with col3:
        if st.button("Reset"):
            st.session_state.page1['is_first_load'] = True

if submitted == False and st.session_state.page1['is_first_load'] == True:
    st.subheader("Please enter the following parameters:")
    st.markdown(
    """
    <ul style="padding-left: 2rem">
    <li>Temperature (°C)</li>
    <li>Soil Moisture (%)</li>
    <li>Light Intensity PAR (µmol/m²/s)</li>
    </ul>
    """, unsafe_allow_html=True)

if submitted == True or st.session_state.page1['is_first_load'] == False:
    st.header("1. Fuzzification")
    fz = FuzzyLogic()

    st.subheader("a. Temperature")
    st.markdown(f"<p class='text'>From the input value {temperature_input}°C, through the predefined membership functions, the fuzzy values ​​are calculated as follows:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_temperature(temperature_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_temperature]]), columns = ("Very cold", "Cold", "Warm", "Hot")))
    st.markdown("<p class='text'>Visualization graph:</p>", unsafe_allow_html=True)
    fig1, ax1 = TemperatureVisualizer(fz.membership_values_of_temperature, temperature_input).plot()
    st.write(fig1)

    st.subheader("b. Soil Moisture")
    st.markdown(f"<p class='text'>From the input value {soil_moisture_input}%, through the predefined membership functions, the fuzzy values ​​are calculated as follows:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_soil_moisture(soil_moisture_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_soil_moisture]]), columns = ("Very dry", "Dry", "Moist", "Very moist")))
    st.markdown("<p class='text'>Visualization graph:</p>", unsafe_allow_html=True)
    fig2, ax2 = SoilMoistureVisualizer(fz.membership_values_of_soil_moisture, soil_moisture_input).plot()
    st.write(fig2)

    st.subheader("c. Light Intensity PAR")
    st.markdown(f"<p class='text'>From the input value {light_intensity_input} µmol/m²/s, through the predefined membership functions, the fuzzy values ​​are calculated as follows:</p>", unsafe_allow_html=True)
    fz.do_fuzzification_of_light_intensity(light_intensity_input)
    st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_light_intensity]]), columns = ("Weak", "Medium", "Strong")))
    st.markdown("<p class='text'>Visualization graph:</p>", unsafe_allow_html=True)
    fig3, ax3 = LightIntensityVisualizer(fz.membership_values_of_light_intensity, light_intensity_input).plot()
    st.write(fig3)

    st.header("2. Fuzzy Inference")
    ok = fz.do_fuzzy_inference()
    if ok == False:
        st.markdown(f"<p class='text'>From the fuzzy values calculated above, applying the defined rules, we conclude:</p>", unsafe_allow_html=True)
        st.markdown("<p class='text center'><b>Should not water the plants in this condition</b></p>", unsafe_allow_html=True)

    else:
        st.markdown(f"<p class='text'>From the fuzzy values calculated above, applying the defined rules, we calculate the fuzzy values for the output watering speed as follows:</p>", unsafe_allow_html=True)
        st.table(pd.DataFrame(np.array([[i for i in fz.membership_values_of_watering_speed]]), columns = ("Very Slow", "Slow", "Fast", "Very Fast")))

        st.header("3. Defuzzification")
        st.markdown(f"<p class='text'>Projecting the computed values from fuzzy inference into the membership function of watering speed, we have:</p>", unsafe_allow_html=True)
        fz.do_defuzzification_of_watering_speed()
        fig4, ax4 = WateringSpeedVisualizer(fz.membership_values_of_watering_speed, fz.crisp_value).plot()
        st.write(fig4)
        st.markdown(f"<p class='text'>Identifying the two maximum points, the beginning and the end are: {fz.max1} and {fz.max2}</p>", unsafe_allow_html=True)
        st.markdown("<p class='text'>Using the centroid method, we determine the output value as:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>({fz.max1} + {fz.max2}) / 2 =  {fz.crisp_value} liters/minute ~ <b>{'{:.10f}'.format(fz.output)} m3/s</b></p>", unsafe_allow_html=True)

   
        