import streamlit as st
import os

st.write("Current folder:", os.getcwd())

# ---------------------------
# 🌙 PAGE STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "🏠"

# ---------------------------
# 🧠 MEMORY (CORE DATA)
# ---------------------------
if "eaten" not in st.session_state:
    st.session_state.eaten = 0

if "goal" not in st.session_state:
    st.session_state.goal = 2000

# ---------------------------
# 🌱 PLANT SYSTEM
# ---------------------------
if "plant_level" not in st.session_state:
    st.session_state.plant_level = 0

if "goal_achieved_today" not in st.session_state:
    st.session_state.goal_achieved_today = False

# ---------------------------
# 🎨 STYLE
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

h1, h2, h3, p {
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #262730;
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 🎯 TITLE
# ---------------------------
st.title("🍽️ Weight Gain Tracker")

# ---------------------------
# ⚙️ GOAL INPUT
# ---------------------------
st.session_state.goal = st.number_input(
    "Daily Calorie Goal",
    value=st.session_state.goal
)

# ---------------------------
# 🌱 CHECK GOAL + GROW PLANT
# ---------------------------
if st.session_state.eaten >= st.session_state.goal:
    if not st.session_state.goal_achieved_today:
        st.session_state.plant_level += 1
        st.session_state.goal_achieved_today = True
        st.success("🌱 Your plant grew!")
        st.balloons()

# ---------------------------
# 📄 PAGES
# ---------------------------

if st.session_state.page == "🏠":
    st.header("🏠 Home")
    st.write("Welcome to your tracker 💪")

elif st.session_state.page == "🍜":
    st.header("🍜 Food")

    if st.button("🍜 Noodles (+580)"):
        st.session_state.eaten += 580

    if st.button("🥛 Milk (+150)"):
        st.session_state.eaten += 150

    if st.button("🥣 Cereal (+200)"):
        st.session_state.eaten += 200

    if st.button("💪 Serious Mass (+1250)"):
        st.session_state.eaten += 1250

    st.write("Calories eaten:", st.session_state.eaten)

elif st.session_state.page == "🌱":
    st.header("🌱 Your Plant")

    plants = [
        "🌰 Seed",
        "🌱 Sprout",
        "🌿 Small Plant",
        "🌳 Tree",
        "🌴 Big Tree",
        "🌸 Blooming Plant"
    ]

    level = min(st.session_state.plant_level, len(plants) - 1)

    st.markdown(f"## {plants[level]}")

    st.write("Keep hitting your calorie goal to grow your plant 💪🌱")

elif st.session_state.page == "📈":
    st.header("📈 Progress")

    remaining = st.session_state.goal - st.session_state.eaten

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Eaten", st.session_state.eaten)

    with col2:
        st.metric("Remaining", remaining)

    if remaining > 0:
        st.info(f"You still need {remaining} calories 💪")
    else:
        st.success("You hit your goal 🎉")

# ---------------------------
# 📊 PROGRESS BAR
# ---------------------------
progress = min(st.session_state.eaten / st.session_state.goal, 1.0)

st.subheader("Daily Progress")
st.progress(progress)

# ---------------------------
# 🔁 RESET DAY
# ---------------------------
if st.button("🔁 Reset Day"):
    st.session_state.eaten = 0
    st.session_state.goal_achieved_today = False
    st.success("Day reset!")

# ---------------------------
# 📱 BOTTOM NAVIGATION
# ---------------------------
st.write("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠"):
        st.session_state.page = "🏠"

with col2:
    if st.button("🍜"):
        st.session_state.page = "🍜"

with col3:
    if st.button("🌱"):
        st.session_state.page = "🌱"

with col4:
    if st.button("📈"):
        st.session_state.page = "📈"