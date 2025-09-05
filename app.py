import pickle
import pandas as pd 
import streamlit as st 
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="IPL Match Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #e3f2fd, #f3e5f5, #e8f5e8, #fff3e0);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .main-header h1 {
        color: #1976d2;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: #666;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    .team-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .predict-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        border: none;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin: 2rem 0;
        animation: bounceIn 0.8s ease-out;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .team-logo {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    .vs-text {
        font-size: 2rem;
        color: #1976d2;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #1976d2; }
        to { text-shadow: 0 0 20px #1976d2, 0 0 30px #1976d2; }
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #1976d2;
        box-shadow: 0 0 10px rgba(25, 118, 210, 0.3);
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1976d2;
        box-shadow: 0 0 10px rgba(25, 118, 210, 0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-cricket {
        position: absolute;
        color: rgba(25, 118, 210, 0.1);
        animation: float 6s ease-in-out infinite;
        font-size: 2rem;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .success-animation {
        animation: successPulse 0.6s ease-out;
    }
    
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Team logos dictionary (using emoji for now, you can replace with actual image URLs)
team_logos = {
    'Sunrisers Hyderabad': '🌅',
    'Mumbai Indians': '🔵',
    'Royal Challengers Bangalore': '🔴',
    'Kolkata Knight Riders': '⚫',
    'Kings XI Punjab': '🟡',
    'Chennai Super Kings': '🟨',
    'Rajasthan Royals': '💜',
    'Delhi Capitals': '🔷'
}

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

# Add floating cricket elements
st.markdown("""
<div class="floating-elements">
    <div class="floating-cricket" style="top: 10%; left: 10%; animation-delay: 0s;">🏏</div>
    <div class="floating-cricket" style="top: 20%; right: 10%; animation-delay: 1s;">⚾</div>
    <div class="floating-cricket" style="bottom: 30%; left: 15%; animation-delay: 2s;">🏏</div>
    <div class="floating-cricket" style="bottom: 20%; right: 20%; animation-delay: 3s;">⚾</div>
    <div class="floating-cricket" style="top: 50%; left: 5%; animation-delay: 4s;">🏏</div>
</div>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏏 IPL Match Predictor</h1>
    <p>Powered by Advanced Machine Learning | Dream11 Style Experience</p>
</div>
""", unsafe_allow_html=True)

# Load the model
try:
    pipe = pickle.load(open('pipe.pkl','rb'))
except:
    st.error("⚠️ Model file 'pipe.pkl' not found! Please make sure the file is in the same directory.")
    st.stop()

# Team selection section
# st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 🎯 Select Teams")

col1, col2 = st.columns([1, 1])
batting_team, bowling_team = '', ''

with col1:
    st.markdown("#### 🏏 Batting Team")
    batting_team = st.selectbox('Choose the batting team', teams, key='batting')
    if batting_team:
        st.markdown(f"<div style='text-align: center; font-size: 3rem; margin: 1rem 0;'>{team_logos.get(batting_team, '🏏')}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("#### ⚾ Bowling Team") 
    if batting_team:
        available_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Choose the bowling team', available_teams, key='bowling')
        if bowling_team:
            st.markdown(f"<div style='text-align: center; font-size: 3rem; margin: 1rem 0;'>{team_logos.get(bowling_team, '⚾')}</div>", unsafe_allow_html=True)

if batting_team and bowling_team:
    st.markdown(f"<div class='vs-text'>{batting_team} vs {bowling_team}</div>", unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# Match details section
# st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 🏟️ Match Details")

col1, col2 = st.columns([1, 1])
with col1:
    selected_city = st.selectbox('🌍 Select Venue', cities)
with col2:
    target = st.number_input('🎯 Target Score', min_value=1, max_value=300, value=180)

# st.markdown('</div>', unsafe_allow_html=True)

# Current match situation
# st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 📊 Current Match Situation")

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('📈 Current Score', min_value=0, max_value=300, value=100)
with col4:
    overs = st.number_input('⏰ Overs Completed', min_value=0.1, max_value=20.0, value=10.0, step=0.1)
with col5:
    wickets = st.number_input('🎯 Wickets Lost', min_value=0, max_value=10, value=3)

# st.markdown('</div>', unsafe_allow_html=True)

# Live statistics
if score > 0 and overs > 0:
    # st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📈 Live Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1976d2; margin-bottom: 0.5rem;">🎯 Runs Needed</h3>
            <h2 style="color: #333; margin: 0;">{runs_left}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1976d2; margin-bottom: 0.5rem;">⚾ Balls Left</h3>
            <h2 style="color: #333; margin: 0;">{balls_left}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1976d2; margin-bottom: 0.5rem;">📊 Current RR</h3>
            <h2 style="color: #333; margin: 0;">{crr:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1976d2; margin-bottom: 0.5rem;">🎯 Required RR</h3>
            <h2 style="color: #333; margin: 0;">{rrr:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # st.markdown('</div>', unsafe_allow_html=True)

# Predict button with animation
st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
predict_clicked = st.button('🚀 PREDICT WIN PROBABILITY', key='predict_btn')
# st.markdown('</div>', unsafe_allow_html=True)

# Prediction results
if predict_clicked and batting_team and bowling_team and score > 0 and overs > 0:
    # Show loading animation
    with st.spinner('🔮 Analyzing match data and predicting outcomes...'):
        time.sleep(2)  # Simulating processing time for better UX
        
        runs_left = target - score 
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        if balls_left <= 0:
            st.error("⚠️ Match Over! No balls remaining.")
        elif runs_left <= 0:
            st.success(f"🎉 {batting_team} has already won!")
        else:
            input_df = pd.DataFrame({
                'batting_team': [batting_team], 
                'bowling_team': [bowling_team],
                'city': [selected_city],
                'runs_left': [runs_left],
                'balls_left': [balls_left],
                'wickets': [wickets_left],
                'total_runs_x': [target],
                'crr': [crr],
                'rrr': [rrr]
            })
            
            try:
                result = pipe.predict_proba(input_df)
                loss_prob = result[0][0]
                win_prob = result[0][1]
                
                # Display results with animations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="result-card success-animation" style="background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{team_logos.get(batting_team, '🏏')}</div>
                        <h2 style="margin-bottom: 1rem; color: white;">{batting_team}</h2>
                        <h1 style="font-size: 3rem; margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{round(win_prob * 100)}%</h1>
                        <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.9;">Win Probability</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="result-card success-animation" style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa0a0 100%);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{team_logos.get(bowling_team, '⚾')}</div>
                        <h2 style="margin-bottom: 1rem; color: white;">{bowling_team}</h2>
                        <h1 style="font-size: 3rem; margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{round(loss_prob * 100)}%</h1>
                        <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.9;">Win Probability</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Match insights
                # st.markdown('<div class="input-section">', unsafe_allow_html=True)
                st.markdown("### 🎯 Match Insights")
                
                insights = []
                if rrr > crr + 2:
                    insights.append("🔥 Required run rate is significantly higher than current rate")
                elif rrr < crr:
                    insights.append("✅ Batting team is ahead of required run rate")
                
                if wickets_left <= 3:
                    insights.append("⚠️ Limited wickets remaining - pressure situation")
                elif wickets_left >= 7:
                    insights.append("💪 Strong batting depth available")
                
                if balls_left <= 30:
                    insights.append("⏰ Death overs - crucial phase of the match")
                
                for insight in insights:
                    st.markdown(f"- {insight}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Prediction error: {str(e)}")

elif predict_clicked:
    st.warning("⚠️ Please fill all required fields before predicting!")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; background: rgba(255, 255, 255, 0.8); border-radius: 15px;">
    <p style="color: #666; margin: 0;">🏏 IPL Match Predictor | Powered by Machine Learning</p>
    <p style="color: #999; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Made with ❤️ for Cricket Fans</p>
</div>
""", unsafe_allow_html=True)