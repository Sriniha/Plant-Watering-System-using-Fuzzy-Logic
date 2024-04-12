import streamlit as st
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy.control.visualization import FuzzyVariableVisualizer

# Initialize st.session_state.page1 if it doesn't exist
if 'page1' not in st.session_state:
    st.session_state.page1 = {'is_first_load': True, 'temperature': 20.0, 'soil_moisture': 50.0, 'light_intensity': 500.0}

# Set up the Streamlit page configuration and title
st.set_page_config(page_title='Automatic Plant Watering System', page_icon=r"C:\Users\91709\Downloads\watering-system-master\watering-system-master\images\logo.png")
st.image(image=r"C:\Users\91709\Downloads\watering-system-master\watering-system-master\images\logo.png", width=100)
st.title('Automatic Plant Watering System')

# Define CSS styles for Streamlit components
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

# Sidebar section for input parameters
with st.sidebar:
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

    # Input fields for temperature, soil moisture, and light intensity
    st.title("Input Parameters")
    temperature_input = st.number_input("**Temperature (°C):**", min_value=-20.0, max_value=50.0, step=0.1, value=st.session_state.page1['temperature'], key='temperature_input_value', on_change=submit_temperature)
    soil_moisture_input = st.number_input("**Soil Moisture (%):**", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.page1['soil_moisture'], key='soil_moisture_input_value', on_change=submit_soil_moisture)
    light_intensity_input = st.number_input("**Light Intensity PAR (µmol/m²/s):**", min_value=0.0, max_value=1000.0, step=0.1, value=st.session_state.page1['light_intensity'], key='light_intensity_input_value', on_change=submit_light_intensity)

    # Buttons for submitting and resetting input values
    col1, col2, col3 = st.columns([1, 0.5, 0.477])
    with col1:
        if st.button("Submit"):
            st.session_state.page1['is_first_load'] = False
            submitted = True
    with col3:
        if st.button("Reset"):
            st.session_state.page1['is_first_load'] = True

# Custom method to get the figure for fuzzy variable visualization
def get_fig(self, sim):
    fig, ax = FuzzyVariableVisualizer(self).view(sim)
    return fig

ctrl.Consequent.get_fig = get_fig

# Define fuzzy input and output variables
temperature = ctrl.Antecedent(np.arange(-20, 50.01, 0.01), 'Temperature')
soil_moisture = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'Soil Moisture')
light_intensity = ctrl.Antecedent(np.arange(0, 1000.01, 0.01), 'Light Intensity')
watering_speed = ctrl.Consequent(np.arange(0, 12.01, 0.01), 'Watering Speed', defuzzify_method='centroid')

# Define fuzzy membership functions for input variables
temperature['Very Cold'] = fuzz.trapmf(temperature.universe, [-20, -20, 5, 10])
temperature['Cold'] = fuzz.trapmf(temperature.universe, [5, 10, 15, 20])
temperature['Warm'] = fuzz.trapmf(temperature.universe, [15, 20, 25, 30])
temperature['Hot'] = fuzz.trapmf(temperature.universe, [25, 30, 51, 51])

soil_moisture['Very Dry'] = fuzz.trapmf(soil_moisture.universe, [0, 0, 25, 35])
soil_moisture['Dry'] = fuzz.trapmf(soil_moisture.universe, [25, 35, 45, 55])
soil_moisture['Moist'] = fuzz.trapmf(soil_moisture.universe, [45, 55, 65, 75])
soil_moisture['Very Moist'] = fuzz.trapmf(soil_moisture.universe, [65, 75, 101, 101])

light_intensity['Weak'] = fuzz.trapmf(light_intensity.universe, [0, 0, 300, 400])
light_intensity['Medium'] = fuzz.trapmf(light_intensity.universe, [300, 400, 700, 800])
light_intensity['Strong'] = fuzz.trapmf(light_intensity.universe, [700, 800, 1001, 1001])

# Define fuzzy membership functions for output variable
watering_speed['Very Slow'] = fuzz.trapmf(watering_speed.universe, [0, 0, 2, 3])
watering_speed['Slow'] = fuzz.trapmf(watering_speed.universe, [2, 3, 5, 6])
watering_speed['Fast'] = fuzz.trapmf(watering_speed.universe, [5, 6, 8, 9])
watering_speed['Very Fast'] = fuzz.trapmf(watering_speed.universe, [8, 9, 12, 12])
# watering_speed.view()

rule1 = ctrl.Rule(temperature['Very Cold'] & soil_moisture['Very Dry'] & light_intensity['Strong'], watering_speed['Very Slow'])
rule2 = ctrl.Rule(temperature['Cold'] & soil_moisture['Very Dry'] & light_intensity['Weak'], watering_speed['Fast'])
rule3 = ctrl.Rule(temperature['Cold'] & soil_moisture['Very Dry'] & light_intensity['Medium'], watering_speed['Fast'])
rule4 = ctrl.Rule(temperature['Cold'] & soil_moisture['Very Dry'] & light_intensity['Strong'], watering_speed['Very Fast'])
rule5 = ctrl.Rule(temperature['Cold'] & soil_moisture['Dry'] & light_intensity['Weak'], watering_speed['Slow'])
rule6 = ctrl.Rule(temperature['Cold'] & soil_moisture['Dry'] & light_intensity['Medium'], watering_speed['Slow'])
rule7 = ctrl.Rule(temperature['Cold'] & soil_moisture['Dry'] & light_intensity['Strong'], watering_speed['Fast'])
rule8 = ctrl.Rule(temperature['Cold'] & soil_moisture['Moist'] & light_intensity['Medium'], watering_speed['Very Slow'])
rule9 = ctrl.Rule(temperature['Cold'] & soil_moisture['Moist'] & light_intensity['Strong'], watering_speed['Slow'])
rule10 = ctrl.Rule(temperature['Warm'] & soil_moisture['Very Dry'] & light_intensity['Weak'], watering_speed['Very Fast'])
rule11 = ctrl.Rule(temperature['Warm'] & soil_moisture['Very Dry'] & light_intensity['Medium'], watering_speed['Very Fast'])
rule12 = ctrl.Rule(temperature['Warm'] & soil_moisture['Very Dry'] & light_intensity['Strong'], watering_speed['Very Fast'])
rule13 = ctrl.Rule(temperature['Warm'] & soil_moisture['Dry'] & light_intensity['Weak'], watering_speed['Fast'])
rule14 = ctrl.Rule(temperature['Warm'] & soil_moisture['Dry'] & light_intensity['Medium'], watering_speed['Fast'])
rule15 = ctrl.Rule(temperature['Warm'] & soil_moisture['Dry'] & light_intensity['Strong'], watering_speed['Very Fast'])
rule16 = ctrl.Rule(temperature['Warm'] & soil_moisture['Moist'] & light_intensity['Weak'], watering_speed['Slow'])
rule17 = ctrl.Rule(temperature['Warm'] & soil_moisture['Moist'] & light_intensity['Medium'], watering_speed['Slow'])
rule18 = ctrl.Rule(temperature['Warm'] & soil_moisture['Moist'] & light_intensity['Strong'], watering_speed['Fast'])
rule19 = ctrl.Rule(temperature['Hot'] & soil_moisture['Very Dry'] & light_intensity['Weak'], watering_speed['Very Fast'])
rule20 = ctrl.Rule(temperature['Hot'] & soil_moisture['Very Dry'] & light_intensity['Medium'], watering_speed['Very Fast'])
rule21 = ctrl.Rule(temperature['Hot'] & soil_moisture['Very Dry'] & light_intensity['Strong'], watering_speed['Very Fast'])
rule22 = ctrl.Rule(temperature['Hot'] & soil_moisture['Dry'] & light_intensity['Weak'], watering_speed['Fast'])
rule23 = ctrl.Rule(temperature['Hot'] & soil_moisture['Dry'] & light_intensity['Medium'], watering_speed['Fast'])
rule24 = ctrl.Rule(temperature['Hot'] & soil_moisture['Dry'] & light_intensity['Strong'], watering_speed['Very Fast'])
rule25 = ctrl.Rule(temperature['Hot'] & soil_moisture['Moist'] & light_intensity['Weak'], watering_speed['Slow'])
rule26 = ctrl.Rule(temperature['Hot'] & soil_moisture['Moist'] & light_intensity['Medium'], watering_speed['Fast'])
rule27 = ctrl.Rule(temperature['Hot'] & soil_moisture['Moist'] & light_intensity['Strong'], watering_speed['Fast'])

watering_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                     rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
                                     rule21, rule22, rule23, rule24, rule25, rule26, rule27])
watering = ctrl.ControlSystemSimulation(watering_system)

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
    watering.input['Temperature'] = temperature_input
    watering.input['Soil Moisture'] = soil_moisture_input
    watering.input['Light Intensity'] = light_intensity_input

    st.subheader("Results calculated using skfuzzy library:")
    print("skfuzzy:")

    try:
        watering.compute()

        watering_speed.defuzzify_method = 'mom'
        watering = ctrl.ControlSystemSimulation(watering_system)
        watering.input['Temperature'] = temperature_input
        watering.input['Soil Moisture'] = soil_moisture_input
        watering.input['Light Intensity'] = light_intensity_input
        watering.compute()
        print(f"Mean of Maximum ({watering_speed.defuzzify_method})", end = ": ")
        print(round(watering.output['Watering Speed'], 2))
        st.markdown("<p class='text'>Using the Mean of Maximum method, the determined output is:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>{'{:.2f}'.format(round(watering.output['Watering Speed'], 2))} liters/minute ~ <b>{'{:.10f}'.format(round(watering.output['Watering Speed'], 2) / 60000)} m3/s</b></p>", unsafe_allow_html=True)
        fig1 = watering_speed.get_fig(sim=watering)
        st.write(fig1)

        watering_speed.defuzzify_method = 'centroid'
        watering = ctrl.ControlSystemSimulation(watering_system)
        watering.input['Temperature'] = temperature_input
        watering.input['Soil Moisture'] = soil_moisture_input
        watering.input['Light Intensity'] = light_intensity_input
        watering.compute()
        print(f"Centroid ({watering_speed.defuzzify_method})", end = ": ")
        print(round(watering.output['Watering Speed'], 2))
        st.markdown("<p class='text'>Using the centroid method, the determined output is:</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='text center'>{'{:.2f}'.format(round(watering.output['Watering Speed'], 2))} liters/minute ~ <b>{'{:.10f}'.format(round(watering.output['Watering Speed'], 2) / 60000)} m3/s</b></p>", unsafe_allow_html=True)
        fig2 = watering_speed.get_fig(sim=watering)
        st.write(fig2)
      
    except ValueError:
        st.markdown(f"<p class='text'>Based on the fuzzy values computed, and applying the defined rules, the conclusion is:</p>", unsafe_allow_html=True)
        st.markdown("<p class='text center'><b>It is not advisable to water the plant in this condition</b></p>", unsafe_allow_html=True)
        print("Crisp output cannot be calculated!")
    submitted = False
    print("___________________________________________")