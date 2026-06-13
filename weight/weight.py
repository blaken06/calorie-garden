import streamlit as st
import json
import os

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "eaten": 0,
        "goal": 2000,
        "plant_level": 0,
        "goal_achieved_today": False
    }

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "eaten": st.session_state.eaten,
            "goal": st.session_state.goal,
            "plant_level": st.session_state.plant_level,
            "goal_achieved_today": st.session_state.goal_achieved_today
        }, f)


data = load_data()

if "eaten" not in st.session_state:
    st.session_state.eaten = data["eaten"]

if "goal" not in st.session_state:
    st.session_state.goal = data["goal"]

if "plant_level" not in st.session_state:
    st.session_state.plant_level = data["plant_level"]

if "goal_achieved_today" not in st.session_state:
    st.session_state.goal_achieved_today = data["goal_achieved_today"]


# ---------------------------
# 🌙 PAGE STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "🏠"




# ---------------------------
# 🎨 STYLE
# ---------------------------


st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
}
div[data-testid="column"] {
    min-width: 0 !important;
}
button[kind="secondary"] {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)



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

st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap;
}

div[data-testid="stHorizontalBlock"] > div {
    min-width: 0px;
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
new_goal = st.number_input("Daily Calorie Goal", value=st.session_state.goal)

if new_goal != st.session_state.goal:
    st.session_state.goal = new_goal
    save_data()
# ---------------------------
# 🌱 CHECK GOAL + GROW PLANT
# ---------------------------
if st.session_state.eaten >= st.session_state.goal:
    if not st.session_state.goal_achieved_today:
        st.session_state.plant_level += 1
        st.session_state.goal_achieved_today = True
        save_data()
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
        save_data()

    if st.button("🥛 Milk (+150)"):
        st.session_state.eaten += 150
        save_data()

    if st.button("🥣 Cereal (+200)"):
        st.session_state.eaten += 200
        save_data()

    if st.button("💪 Serious Mass (+1250)"):
        st.session_state.eaten += 1250
        save_data()

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
progress = min(st.session_state.eaten / max(st.session_state.goal, 1), 1.0)

st.subheader("Daily Progress")
st.progress(progress)

# ---------------------------
# 🔁 RESET DAY
# ---------------------------
if st.button("🔁 Reset Day"):
    st.session_state.eaten = 0
    st.session_state.goal_achieved_today = False
    save_data()
    st.success("Day reset!")

# ---------------------------
# 📱 BOTTOM NAVIGATION
# ---------------------------
st.write("---")

col1, col2, col3, col4 = st.columns(4, vertical_alignment="center")

with col1:
    if st.button("🏠"):
        st.session_state.page = "🏠"
        st.rerun()
        st.stop()

with col2:
    if st.button("🍜"):
        st.session_state.page = "🍜"
        st.rerun()
        st.stop()

with col3:
    if st.button("🌱"):
        st.session_state.page = "🌱"
        st.rerun()
        st.stop()

with col4:
    if st.button("📈"):
        st.session_state.page = "📈"
        st.rerun()
        st.stop()