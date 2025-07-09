import streamlit as st
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import uuid
import json
from streamlit_lottie import st_lottie

# ------------ Load Lottie Animation ------------
def load_lottie(path: str):
    with open(path, "r") as f:
        return json.load(f)

# ------------ Load Dataset ------------
df = pd.read_csv("categorized_dishes.csv")
df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
df.rename(columns={
    'Dish Name': 'dish',
    'Calories (kcal)': 'calories',
    'Protein (g)': 'protein',
    'Type': 'type'
}, inplace=True)
df['type'] = df['type'].str.strip().str.lower()
df['dish'] = df['dish'].str.title()

# ------------ BMR Function ------------
def get_targets(weight, age, gender, goal):
    gender = gender.lower()
    weight, age = float(weight), int(age)
    bmr = 10 * weight + 6.25 * (170 if gender == "male" else 160) - 5 * age + (5 if gender == "male" else -161)
    calories = bmr * 1.4 + (-300 if goal == "Weight Loss" else 300 if goal == "Muscle Gain" else 0)
    protein = weight * (1.5 if goal == "Muscle Gain" else 1.2 if goal == "Maintain" else 1.0)
    return round(calories, 2), round(protein, 2)

# ------------ Meal Optimizer ------------
def build_optimized_meal(cal_limit, protein_limit, available_df, max_dishes=4):
    df_av = available_df.reset_index(drop=True)
    n = len(df_av)
    model = LpProblem("MealPlan", LpMaximize)
    x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
    model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n))
    model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) <= cal_limit + 50
    model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) >= cal_limit - 50
    model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) <= protein_limit + 5
    model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) >= protein_limit - 5
    model += lpSum(x[i] for i in range(n)) <= max_dishes

    if 'Category' in df_av.columns:
        soup_salad = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['soup', 'salad']]
        bev_des = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['beverage', 'dessert']]
        if soup_salad:
            model += lpSum(x[i] for i in soup_salad) <= 1
        if bev_des:
            model += lpSum(x[i] for i in bev_des) <= 1

    model.solve()
    chosen = [i for i in range(n) if x[i].varValue == 1]
    return df_av.loc[chosen]

# ------------ Page Config ------------
st.set_page_config(page_title="Smart AI Nutrition Planner", layout="centered", page_icon="🥗")

# ------------ Styling ------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #fff3e0, #ffe0b2);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #e65100;
    font-weight: 700;
}
input, select, textarea {
    border: 2px solid #ccc !important;
    border-radius: 8px !important;
}
.stButton > button {
    background-color: #ef6c00;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: bold;
    border: none;
    transition: 0.3s ease;
}
.stButton > button:hover {
    background-color: #d84315;
    transform: scale(1.02);
}
.block-container {
    padding-top: 2rem;
}
.meal-card {
    background: #ffe0b2;  /* Orange background */
    border-left: 6px solid #ff9800;
    padding: 15px;
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(255, 152, 0, 0.1);
}
@keyframes fadeInUp {
  from {opacity: 0; transform: translateY(20px);}
  to {opacity: 1; transform: translateY(0);}
}
div[data-testid="stAppViewContainer"] > div:first-child {
    animation: fadeInUp 1s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ------------ Lottie Animation ------------
try:
    lottie_json = load_lottie("healthy.json")
    st_lottie(lottie_json, speed=1, height=200, key="healthy_anim")
except:
    st.markdown("🥦 _Smart Diet Assistant_")

# ------------ App Title ------------
st.title("🥗 Smart AI Nutrition Planner")

# ------------ Input Form ------------
with st.form("nutrition_form"):
    col1, col2 = st.columns(2)
    with col1:
        weight = st.text_input("Weight (kg)", key="weight")
        gender = st.selectbox("Gender", ["Select Gender", "Male", "Female"], key="gender")
        preference = st.selectbox("Preference", ["Select Preference", "Vegetarian", "Non-Vegetarian"], key="preference")
    with col2:
        age = st.text_input("Age", key="age")
        goal = st.selectbox("Goal", ["Select Goal", "Weight Loss", "Maintain", "Muscle Gain"], key="goal")

    submitted = st.form_submit_button("Generate Meal Plan")

# ------------ Submit Logic ------------
if submitted:
    if (not weight or not age or
        gender == "Select Gender" or
        goal == "Select Goal" or
        preference == "Select Preference"):
        st.error("⚠️ Please fill out all fields before generating the meal plan.")
        st.markdown("🔁 **Try Again**")
    else:
        weight = float(weight)
        age = int(age)
        preference_clean = preference.lower()
        target_cals, target_prot = get_targets(weight, age, gender, goal)

        st.markdown("### 🔍 Your Personalized Nutrition Targets")
        st.info(f"""
        **Goal:** {goal}  
        **Gender:** {gender}  
        **Age:** {age}  
        **Target Calories:** {target_cals} kcal  
        **Target Protein:** {target_prot} g
        """)

        meal_split = {'Breakfast': 0.2, 'Lunch': 0.4, 'Dinner': 0.4}
        seed = uuid.uuid4().int & (1 << 32) - 1
        filtered = df[df['type'] == preference_clean].sample(frac=1, random_state=seed)
        used = set()

        def pick_meal(portion):
            avail = filtered[~filtered['dish'].isin(used)]
            meal = build_optimized_meal(target_cals * portion, target_prot * portion, avail)
            used.update(meal['dish'].tolist())
            return meal

        st.markdown("### 🍽️ Your Daily Meal Plan")
        total_day_cal = 0
        total_day_prot = 0

        for meal_name in meal_split:
            portion = meal_split[meal_name]
            meal_df = pick_meal(portion)
            total_cal = round(meal_df['calories'].sum(), 2)
            total_prot = round(meal_df['protein'].sum(), 2)

            total_day_cal += total_cal
            total_day_prot += total_prot

            with st.container():
                st.markdown(f"<div class='meal-card'><h3>{meal_name} — {total_cal} kcal, {total_prot} g Protein</h3>", unsafe_allow_html=True)
                if not meal_df.empty:
                    display_df = meal_df[['dish', 'calories', 'protein']].copy()
                    display_df = display_df.rename(columns={
                        'dish': 'Dish',
                        'calories': 'Calories (kcal)',
                        'protein': 'Protein (g)'
                    })

                    # ✅ Format calories and protein to 2 decimal places
                    display_df['Calories (kcal)'] = display_df['Calories (kcal)'].apply(lambda x: f"{x:.2f}")
                    display_df['Protein (g)'] = display_df['Protein (g)'].apply(lambda x: f"{x:.2f}")

                    # ✅ Reset index and add S.No
                    display_df.reset_index(drop=True, inplace=True)
                    display_df.index = display_df.index + 1
                    display_df.index.name = "S.No"

                    # ✅ Show the table with S.No
                    st.table(display_df)







        st.success(f"✅ **Total Daily Intake:** {total_day_cal} kcal, {total_day_prot} g Protein")

        # ------------ Try Again Button ------------
        st.markdown("---")
        if st.button("🔁 Try Again"):
            for key in ["weight", "age", "gender", "goal", "preference"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
