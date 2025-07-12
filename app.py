import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image

# Set page config
st.set_page_config(
    page_title="🌱 Fertilizer Smart Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    /* Main container */
    .main-container {
        padding: 2rem;
    }
    
    /* Input cards - responsive columns */
    @media (min-width: 1200px) {
        .input-columns {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
    }
    @media (max-width: 1199px) and (min-width: 768px) {
        .input-columns {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
    }
    @media (max-width: 767px) {
        .input-columns {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    /* Input boxes */
    .input-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Result cards */
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Value boxes */
    .value-box {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    try:
        class_model = joblib.load('best_classification_model.pkl')
        reg_model = joblib.load('best_regression_model.pkl')
        le = joblib.load('label_encoder.pkl')
        return class_model, reg_model, le
    except Exception as e:
        st.error(f"Error loading model files: {str(e)}")
        st.stop()

class_model, reg_model, le = load_models()

# Fertilizer information
fertilizer_info = {
    "Urea": {"color": "#3498db", "desc": "Nitrogen-rich (46% N) for vegetative growth"},
    "DAP": {"color": "#e74c3c", "desc": "Diammonium phosphate (18-46-0) for root development"},
    "MOP": {"color": "#f39c12", "desc": "Muriate of potash (0-0-60) for fruit quality"},
}

# Sidebar - Navigation
# Sidebar
with st.sidebar:
    st.title("🌾 Navigation")
    st.markdown("""
    Welcome to the Smart Fertilizer Advisor! 
    This tool helps you optimize fertilizer use for maximum crop yield.
    """)
    
    st.markdown("---")
    st.markdown("""
    ### How to Use:
    1. Enter your soil parameters
    2. Click 'Get Recommendation'
    3. View your customized fertilizer plan
    """)
    
    st.markdown("---")
    st.markdown("""
    **📊 Model Information**  
    - Fertilizer Classifier: Random Forest  
    - Application Rate Predictor: Random Forest  
    """)

# Main content
st.title("🌱 Smart Fertilizer Advisor")
st.markdown("""
*Optimize your fertilizer use for maximum crop yield and cost efficiency*
""")

# Input section - Responsive columns
with st.container():
    st.header("📊 Soil Parameter Input")
    
    with st.form("input_form"):
        # Using columns that respond to screen size
        cols = st.columns(3)
        
        with cols[0]:
            with st.container():
                st.markdown('<div class="input-box">', unsafe_allow_html=True)
                st.subheader("Physical Properties")
                moisture = st.text_input("Moisture (%)", value="30.0", 
                                       help="Soil water content (0-100%)")
                temperature = st.text_input("Temperature (°C)", value="25.0",
                                          help="Soil temperature range: 0-50°C")
                st.markdown('</div>', unsafe_allow_html=True)
                
        with cols[1]:
            with st.container():
                st.markdown('<div class="input-box">', unsafe_allow_html=True)
                st.subheader("Chemical Properties")
                ec = st.text_input("EC (µS/cm)", value="300",
                                 help="Electrical conductivity (0-2000 µS/cm)")
                ph = st.text_input("pH Level", value="6.5",
                                 help="Soil acidity/alkalinity (0-14 scale)")
                st.markdown('</div>', unsafe_allow_html=True)
                
        with cols[2]:
            with st.container():
                st.markdown('<div class="input-box">', unsafe_allow_html=True)
                st.subheader("Nutrient Levels")
                n = st.text_input("Nitrogen (N) mg/kg", value="50",
                                help="Available nitrogen (0-500 mg/kg)")
                p = st.text_input("Phosphorus (P) mg/kg", value="50",
                                help="Available phosphorus (0-500 mg/kg)")
                k = st.text_input("Potassium (K) mg/kg", value="50",
                                help="Available potassium (0-500 mg/kg)")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        submit_col1, submit_col2, submit_col3 = st.columns([1,2,1])
        with submit_col2:
            submitted = st.form_submit_button("🚀 Get Fertilizer Recommendation", 
                                            use_container_width=True)

# Results section
if submitted:
    try:
        # Convert and validate inputs
        input_values = [
            float(moisture), float(temperature), float(ec),
            float(ph), float(n), float(p), float(k)
        ]
        
        # Prepare input array
        input_data = np.array([input_values])
        
        # Make predictions
        fert_pred = class_model.predict(input_data)
        kg_pred = reg_model.predict(input_data)
        fert_name = le.inverse_transform(fert_pred)[0]
        
        # Display results
        st.success("Recommendation generated successfully!")
        st.balloons()
        
        # Results in responsive columns
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h2 style="color:{fertilizer_info.get(fert_name, {}).get('color', '#2e7d32')}">
                    Recommended Fertilizer
                    </h2>
                    <div class="value-box">
                        <h1>{fert_name}</h1>
                        <p>{fertilizer_info.get(fert_name, {}).get('desc', '')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        with col2:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h2 style="color:#2e7d32">Application Rate</h2>
                    <div class="value-box">
                        <h1>{kg_pred[0]:.1f} kg/ha</h1>
                        <p>Recommended amount per hectare</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Feature importance visualization
        if hasattr(class_model, 'feature_importances_'):
            with st.container():
                st.markdown("""
                <div class="result-card">
                    <h2>Key Decision Factors</h2>
                """, unsafe_allow_html=True)
                
                features = ['Moisture', 'Temperature', 'EC', 'pH', 'N', 'P', 'K']
                importance = class_model.feature_importances_
                
                fig = px.bar(
                    x=features,
                    y=importance,
                    labels={'x': 'Parameter', 'y': 'Importance'},
                    color=importance,
                    color_continuous_scale='Viridis',
                    height=400
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Input summary table
        with st.container():
            st.markdown("""
            <div class="result-card">
                <h2>Your Input Summary</h2>
            """, unsafe_allow_html=True)
            
            input_df = pd.DataFrame({
                "Parameter": ["Moisture", "Temperature", "EC", "pH", "N", "P", "K"],
                "Value": input_values,
                "Unit": ["%", "°C", "µS/cm", "pH", "mg/kg", "mg/kg", "mg/kg"]
            })
            
            # Responsive table - full width on mobile, compact on desktop
            st.dataframe(
                input_df.style.background_gradient(cmap='Greens', subset=['Value']),
                hide_index=True,
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
    except ValueError:
        st.error("Please enter valid numbers in all fields")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2,1,1])
with footer_col1:
    st.markdown("""
       Smart Fertilizer Advisor 
    Version 1.0
    """)
with footer_col2:
    st.markdown("""
          Smart Fertilizer Advisor
    """)
with footer_col3:
    st.markdown("""
    Smart Fertilizer Advisor
    """)