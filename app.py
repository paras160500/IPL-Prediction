import pickle
import pandas as pd 
import streamlit as st 
import numpy as np 

# Page config
st.set_page_config(
    page_title="IPL Match Predictor",
    page_icon="🏏",
    layout="centered"
)

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

# Load model
try:
    pipe = pickle.load(open('pipe.pkl','rb'))
except:
    st.error("Model file 'pipe.pkl' not found!")
    st.stop()

# Title
st.title('🏏 IPL Match Predictor')
st.write("---")

# Team selection
st.subheader("Select Teams")
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team', teams)

with col2:
    if batting_team:
        available_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Bowling Team', available_teams)
    else:
        bowling_team = st.selectbox('Bowling Team', teams)

st.write("---")

# Match details
st.subheader("Match Details")
selected_city = st.selectbox('Venue', cities)
target = st.number_input('Target Score', min_value=1, max_value=300, value=180)

st.write("---")

# Current situation
st.subheader("Current Match Situation")
col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=0, max_value=300, value=100)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.1, max_value=20.0, value=10.0, step=0.1)
with col5:
    wickets_lost = st.number_input('Wickets Lost', min_value=0, max_value=10, value=3)

st.write("---")

# Prediction
if st.button('Predict Win Probability', type="primary"):
    if batting_team and bowling_team and score >= 0 and overs > 0:
        runs_left = target - score 
        balls_left = 120 - int(overs * 6)
        wickets_remaining = 10 - wickets_lost
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
        
        if balls_left <= 0:
            st.error("Match Over! No balls remaining.")
        elif runs_left <= 0:
            st.success(f"🎉 {batting_team} has already won!")
        else:
            # Create input dataframe
            input_df = pd.DataFrame({
                'batting_team': [batting_team], 
                'bowling_team': [bowling_team],
                'city': [selected_city],
                'runs_left': [runs_left],
                'balls_left': [balls_left],
                'wickets': [wickets_remaining],
                'total_runs_x': [target],
                'crr': [crr],
                'rrr': [rrr]
            })
            
            try:
                # Make prediction
                result = pipe.predict_proba(input_df)
                loss_prob = result[0][0]
                win_prob = result[0][1]
                
                # Display results
                st.write("---")
                st.subheader("Prediction Results")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label=f"{batting_team}",
                        value=f"{round(win_prob * 100)}%",
                        help="Win Probability"
                    )
                
                with col2:
                    st.metric(
                        label=f"{bowling_team}",
                        value=f"{round(loss_prob * 100)}%",
                        help="Win Probability"
                    )
                
                # Match stats
                st.write("---")
                st.subheader("Match Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Runs Needed", runs_left)
                with col2:
                    st.metric("Balls Left", balls_left)
                with col3:
                    st.metric("Current RR", f"{crr:.2f}")
                with col4:
                    st.metric("Required RR", f"{rrr:.2f}")
                
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
    else:
        st.warning("Please fill all required fields!")

# Footer
st.write("---")
st.caption("🏏 IPL Match Predictor - Powered by Machine Learning")