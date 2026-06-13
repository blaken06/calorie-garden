import streamlit as st
import json
import os
import random
import datetime

import datetime





quotes = [
    "Small steps every day turn into big changes 🌱",
    "You don’t need motivation, you need consistency 💪",
    "Future you is built by what you do today",
    "One meal at a time, one win at a time",
    "Progress, not perfection",
    "Your body listens to what you feed it",
    "Discipline beats motivation every time 🔥",
    "Keep going — you’re closer than you think",
    "Tiny habits build big transformations",
]


today = datetime.date.today()

if "quote_day" not in st.session_state:
    st.session_state.quote_day = today
    st.session_state.quote = random.choice(quotes)

elif st.session_state.quote_day != today:
    st.session_state.quote_day = today
    st.session_state.quote = random.choice(quotes)






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
    st.markdown(f"""
> 💭 *{st.session_state.quote}*
""")

    st.header("🏠 Home")
    st.write("Welcome to your tracker 💪")

    if st.button("New motivation 🔁"):
        st.session_state.quote = random.choice(quotes)
        st.rerun()



elif st.session_state.page == "🍜":
    st.header("🍜 Food")

    # ---------------------------
    # ⚡ QUICK ADD BUTTONS
    # ---------------------------
    st.subheader("Quick add")

    if st.button("+100 calories"):
        st.session_state.eaten += 100
        save_data()

    if st.button("+250 calories"):
        st.session_state.eaten += 250
        save_data()

    if st.button("+500 calories"):
        st.session_state.eaten += 500
        save_data()

    # ---------------------------
    # ✍️ CUSTOM FOOD INPUT
    # ---------------------------
    st.subheader("Custom food")

    food_name = st.text_input("Food name (optional)")
    calories = st.number_input("Calories", min_value=1)

    if st.button("Add food"):
        st.session_state.eaten += calories
        save_data()

        if food_name:
            st.success(f"Added {food_name} (+{calories})")
        else:
            st.success(f"Added food (+{calories})")

    # ---------------------------
    # 📊 DISPLAY
    # ---------------------------
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