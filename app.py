import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="2026 World Cup Predictor", layout="wide", page_icon="🏆")

# ==========================================
# 2. DATA STORE
# ==========================================
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Country": ["France 🇫🇷", "Argentina 🇦🇷", "Brazil 🇧🇷", "England 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Spain 🇪🇸", "Portugal 🇵🇹", "Netherlands 🇳🇱", "Germany 🇩🇪"],
        "Stage": ["Winner", "Runner-up", "Semifinal", "Semifinal", "Quarterfinal", "Quarterfinal", "Quarterfinal", "Quarterfinal"],
        "Goals_Per_Game": [2.85, 2.64, 2.38, 2.41, 2.15, 2.22, 2.08, 2.10],
        "Defensive_Index": [0.89, 0.87, 0.81, 0.79, 0.83, 0.84, 0.78, 0.76],
        "Attack_Power": [88, 86, 85, 84, 82, 83, 80, 81],
        "Defense_Stability": [85, 84, 82, 80, 84, 79, 81, 78],
        "Midfield_Control": [87, 85, 86, 83, 88, 82, 80, 82]
    })

df = load_data()

# ==========================================
# 3. APP HEADER
# ==========================================
st.title("⚽ Live World Cup Match Simulator & Analytics Hub")
st.markdown("Predict match outcomes dynamically by adjusting team variables and simulation parameters.")
st.markdown("---")

# ==========================================
# 4. SIDEBAR CONTROL PANEL
# ==========================================
st.sidebar.header("🎛️ Control Panel")

selected_stages = st.sidebar.multiselect(
    "Filter Bracket Stages:", 
    options=["Round of 16", "Quarterfinal", "Semifinal", "The Final", "Winner"], 
    default=["Round of 16", "Quarterfinal", "Semifinal", "The Final", "Winner"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔥 Match Simulation Engine")
team_a_select = st.sidebar.selectbox("Select Team A (Home):", options=df["Country"], index=0)
team_b_select = st.sidebar.selectbox("Select Team B (Away):", options=df["Country"], index=1)

randomness_factor = st.sidebar.slider("Tournament Volatility (Variance):", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
extra_time_allowed = st.sidebar.checkbox("Allow Extra Time & Penalties", value=True)

if team_a_select != team_b_select:
    stats_a = df[df["Country"] == team_a_select].iloc[0]
    stats_b = df[df["Country"] == team_b_select].iloc[0]
    
    perf_index_a = (stats_a["Attack_Power"] * 0.4 + stats_a["Midfield_Control"] * 0.4 + stats_a["Defense_Stability"] * 0.2)
    perf_index_b = (stats_b["Attack_Power"] * 0.4 + stats_b["Midfield_Control"] * 0.4 + stats_b["Defense_Stability"] * 0.2)
    
    noise_a = np.random.normal(0, randomness_factor * 15)
    noise_b = np.random.normal(0, randomness_factor * 15)
    
    goals_a = int(max(0, np.round(((perf_index_a + noise_a) / 30) + np.random.poisson(0.5))))
    goals_b = int(max(0, np.round(((perf_index_b + noise_b) / 30) + np.random.poisson(0.5))))
    
    penalty_winner = None
    if goals_a == goals_b and extra_time_allowed:
        goals_a_ot = np.random.randint(3, 6)
        goals_b_ot = np.random.randint(3, 6)
        while goals_a_ot == goals_b_ot:
            goals_b_ot = np.random.randint(3, 6)
        penalty_winner = team_a_select if goals_a_ot > goals_b_ot else team_b_select

    col1, col2, col3 = st.columns([3, 2, 3])
    with col1:
        st.metric(label=f"🏠 {team_a_select} Expected Performance", value=f"{goals_a} Goals")
    with col2:
        st.markdown("<h3 style='text-align: center; color: gray;'>VS</h3>", unsafe_allow_html=True)
        if goals_a == goals_b and extra_time_allowed:
            st.markdown(f"<p style='text-align: center; font-weight: bold; color: #FFA500;'>Tie after FT<br>🏆 Winner on Pens: {penalty_winner}</p>", unsafe_allow_html=True)
        elif goals_a > goals_b:
            st.markdown(f"<h4 style='text-align: center; color: #10b981;'>🎉 {team_a_select} Wins!</h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4 style='text-align: center; color: #10b981;'>🎉 {team_b_select} Wins!</h4>", unsafe_allow_html=True)
    with col3:
        st.metric(label=f"✈️ {team_b_select} Expected Performance", value=f"{goals_b} Goals")

st.markdown("---")

# ==========================================
# 5. VISUAL BRACKET DISPLAY
# ==========================================
st.markdown("### 🗺️ Full 16-Team Knockout Journey")
st.markdown("Track the entire progression from the Round of 16 through to the crown.")

# Combined Direct HTML Injection - Strictly zero empty lines to prevent markdown spilling
st.markdown("""<style>
    .bracket-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        background: #0f1116;
        padding: 30px 15px;
        border-radius: 15px;
        border: 1px solid #1e293b;
        font-family: 'Inter', sans-serif;
        width: 100%;
        box-sizing: border-box;
    }
    .bracket-round {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 850px;
        flex: 1 1 0%;
        padding: 0 5px;
    }
    .match-box {
        background: #1e293b;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        width: 100%;
        max-width: 175px;
        margin: auto 0;
        z-index: 2;
    }
    .team-row {
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        font-size: 13px;
        color: #f8fafc;
        padding: 3px 0;
    }
    .team-winner {
        color: #10b981 !important;
    }
    .connector-column {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        height: 850px;
        flex: 0.4 1 0%;
    }
    .branch-connector {
        border: 2px solid #273549;
        border-left: none; 
        height: 110px;     
        width: 100%;
        margin: auto 0;
    }
    .branch-connector-small {
        border: 2px solid #273549;
        border-left: none;
        height: 220px;
        width: 100%;
        margin: auto 0;
    }
    .branch-connector-final {
        border-bottom: 2px solid #273549;
        width: 100%;
        height: 2px;
        margin: auto 0;
    }
    .champion-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
        padding: 20px 10px;
        border-radius: 12px;
        border: 2px solid #eab308;
        text-align: center;
        box-shadow: 0 0 25px rgba(234, 179, 8, 0.4);
        width: 100%;
        max-width: 190px;
        margin: auto 0;
    }
    .champion-title {
        color: #eab308;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .champion-name {
        color: #ffffff;
        font-size: 18px;
        font-weight: 900;
    }
</style>
<div class="bracket-container">
    <div class="bracket-round">
        <div class="match-box"><div class="team-row team-winner">France 🇫🇷</div><div class="team-row" style="color:#64748b;">Italy 🇮🇹</div></div>
        <div class="match-box"><div class="team-row team-winner">Portugal 🇵🇹</div><div class="team-row" style="color:#64748b;">USA 🇺🇸</div></div>
        <div class="match-box"><div class="team-row team-winner">Germany 🇩🇪</div><div class="team-row" style="color:#64748b;">Morocco 🇲🇦</div></div>
        <div class="match-box"><div class="team-row team-winner">England 🏴󠁧󠁢󠁥󠁮󠁧󠁿</div><div class="team-row" style="color:#64748b;">Colombia 🇨🇴</div></div>
        <div class="match-box"><div class="team-row team-winner">Argentina 🇦🇷</div><div class="team-row" style="color:#64748b;">Croatia 🇭🇷</div></div>
        <div class="match-box"><div class="team-row team-winner">Spain 🇪🇸</div><div class="team-row" style="color:#64748b;">Uruguay 🇺🇾</div></div>
        <div class="match-box"><div class="team-row team-winner">Brazil 🇧🇷</div><div class="team-row" style="color:#64748b;">Belgium 🇧🇪</div></div>
        <div class="match-box"><div class="team-row team-winner">Netherlands 🇳🇱</div><div class="team-row" style="color:#64748b;">Japan 🇯🇵</div></div>
    </div>
    <div class="connector-column">
        <div class="branch-connector"></div>
        <div class="branch-connector"></div>
        <div class="branch-connector"></div>
        <div class="branch-connector"></div>
    </div>
    <div class="bracket-round">
        <div class="match-box" style="border-left-color: #a855f7;"><div class="team-row team-winner">France 🇫🇷</div><div class="team-row" style="color:#64748b;">Portugal 🇵🇹</div></div>
        <div class="match-box" style="border-left-color: #a855f7;"><div class="team-row team-winner">England 🏴󠁧󠁢󠁥󠁮󠁧󠁿</div><div class="team-row" style="color:#64748b;">Germany 🇩🇪</div></div>
        <div class="match-box" style="border-left-color: #a855f7;"><div class="team-row team-winner">Argentina 🇦🇷</div><div class="team-row" style="color:#64748b;">Spain 🇪🇸</div></div>
        <div class="match-box" style="border-left-color: #a855f7;"><div class="team-row team-winner">Brazil 🇧🇷</div><div class="team-row" style="color:#64748b;">Netherlands 🇳🇱</div></div>
    </div>
    <div class="connector-column">
        <div class="branch-connector-small"></div>
        <div class="branch-connector-small"></div>
    </div>
    <div class="bracket-round">
        <div class="match-box" style="border-left-color: #ec4899;"><div class="team-row team-winner">France 🇫🇷</div><div class="team-row" style="color:#64748b;">England 🏴󠁧󠁢󠁥󠁮󠁧󠁿</div></div>
        <div class="match-box" style="border-left-color: #ec4899;"><div class="team-row team-winner">Argentina 🇦🇷</div><div class="team-row" style="color:#64748b;">Brazil 🇧🇷</div></div>
    </div>
    <div class="connector-column">
        <div class="branch-connector-small" style="height: 440px;"></div>
    </div>
    <div class="bracket-round">
        <div class="match-box" style="border-left-color: #f43f5e;"><div class="team-row team-winner">France 🇫🇷</div><div class="team-row" style="color:#64748b;">Argentina 🇦🇷</div></div>
    </div>
    <div class="connector-column">
        <div class="branch-connector-final"></div>
    </div>
    <div class="bracket-round">
        <div class="champion-box">
            <div class="champion-title">👑 Predicted Champion</div>
            <div class="champion-name">France 🇫🇷</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("---")


# ==========================================
# 6. INTERACTIVE PLOTLY CHART
# ==========================================
st.markdown("### 📊 Attack Velocity vs. Defensive Stability")
fig = px.scatter(df, x="Goals_Per_Game", y="Defensive_Index", text="Country", color="Stage", size_max=60)
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)