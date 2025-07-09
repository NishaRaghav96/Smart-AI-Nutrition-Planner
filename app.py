# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from pulp import LpMaximize, LpProblem, LpVariable, lpSum
# import random
# import uuid
# from streamlit_lottie import st_lottie
# import json

# # ------------- LOTTIE ANIMATION FUNCTION -------------
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# # Load dataset
# df = pd.read_csv("categorized_dishes.csv")
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
# df.rename(columns={
#     'Dish Name': 'dish',
#     'Calories (kcal)': 'calories',
#     'Protein (g)': 'protein',
#     'Type': 'type'
# }, inplace=True)
# df['type'] = df['type'].str.strip().str.lower()
# df['dish'] = df['dish'].str.title()

# # BMR calculator
# def get_targets(weight, age, gender, goal):
#     gender = gender.lower()
#     weight, age = float(weight), int(age)
#     bmr = 10 * weight + 6.25 * (170 if gender == "male" else 160) - 5 * age + (5 if gender == "male" else -161)
#     calories = bmr * 1.4 + (-300 if goal == "Weight Loss" else 300 if goal == "Muscle Gain" else 0)
#     protein = weight * (1.5 if goal == "Muscle Gain" else 1.2 if goal == "Maintain" else 1.0)
#     return round(calories, 2), round(protein, 2)

# # Optimization
# def build_optimized_meal(cal_limit, protein_limit, available_df, max_dishes=4):
#     df_av = available_df.reset_index(drop=True)
#     n = len(df_av)
#     model = LpProblem("MealPlan", LpMaximize)
#     x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
#     random_weights = [random.uniform(0.9, 1.1) for _ in range(n)]
#     model += lpSum(df_av.loc[i, 'protein'] * random_weights[i] * x[i] for i in range(n))

#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) <= cal_limit + 100
#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) >= cal_limit - 50
#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) >= protein_limit - 5
#     model += lpSum(x[i] for i in range(n)) <= max_dishes

#     soup_salad = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['soup', 'salad']]
#     bev_des = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['beverage', 'dessert']]
#     if soup_salad:
#         model += lpSum(x[i] for i in soup_salad) <= 1
#     if bev_des:
#         model += lpSum(x[i] for i in bev_des) <= 1

#     model.solve()
#     chosen = [i for i in range(n) if x[i].varValue == 1]
#     return df_av.loc[chosen]

# # --- Streamlit Config ---
# st.set_page_config(page_title="Smart AI Nutrition Planner", layout="centered", page_icon="🥗")

# # --- Custom CSS Styling ---
# st.markdown("""
# <style>
# body {
#     background: linear-gradient(to right, #fff3e0, #ffe0b2);
#     font-family: 'Segoe UI', sans-serif;
# }
# h1, h2, h3 {
#     color: #e65100;
#     font-weight: 700;
# }
# input, select, textarea {
#     border: 2px solid #ccc !important;
#     border-radius: 8px !important;
# }
# .stButton > button {
#     background-color: #ef6c00;
#     color: white;
#     border-radius: 10px;
#     padding: 0.6rem 1.2rem;
#     font-weight: bold;
#     border: none;
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: #d84315;
#     transform: scale(1.02);
# }
# .block-container {
#     padding-top: 2rem;
# }
# .meal-card {
#     background: #fffdf9;
#     border-left: 6px solid #ff9800;
#     padding: 15px;
#     margin-bottom: 16px;
#     border-radius: 8px;
#     box-shadow: 0 4px 10px rgba(255, 152, 0, 0.1);
# }
# @keyframes fadeInUp {
#   from {opacity: 0; transform: translateY(20px);}
#   to {opacity: 1; transform: translateY(0);}
# }
# div[data-testid="stAppViewContainer"] > div:first-child {
#     animation: fadeInUp 1s ease-out;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Optional Lottie Animation (load your JSON file) ---
# lottie_path = "healthy.json"  # Make sure this file is in your directory
# try:
#     lottie_json = load_lottie(lottie_path)
#     st_lottie(lottie_json, speed=1, height=200, key="healthy_anim")
# except:
#     st.markdown("🥦 _Your AI nutrition planner_")

# # --- Form UI ---
# st.title("🥗 Smart AI Nutrition Planner")

# with st.form("nutrition_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
#         gender = st.selectbox("Gender", ["Male", "Female"])
#         preference = st.selectbox("Preference", ["Vegetarian", "Non-Vegetarian"])
#     with col2:
#         age = st.number_input("Age", min_value=10, max_value=100, step=1)
#         goal = st.selectbox("Goal", ["Weight Loss", "Maintain", "Muscle Gain"])

#     submitted = st.form_submit_button("Generate Meal Plan")

# # --- Generate & Show Results ---
# if submitted:
#     preference_clean = preference.lower()
#     target_cals, target_prot = get_targets(weight, age, gender, goal)

#     st.markdown("### 🔍 Your Personalized Nutrition Targets")
#     st.info(f"""
#     **Goal:** {goal}  
#     **Gender:** {gender}  
#     **Age:** {age}  
#     **Target Calories:** {target_cals} kcal  
#     **Target Protein:** {target_prot} g
#     """)

#     meal_split = {'Breakfast': 0.2, 'Lunch': 0.4, 'Dinner': 0.4}
#     seed = uuid.uuid4().int & (1 << 32) - 1
#     filtered = df[df['type'] == preference_clean].sample(frac=1, random_state=seed)
#     used = set()

#     def pick_meal(portion):
#         avail = filtered[~filtered['dish'].isin(used)]
#         meal = build_optimized_meal(target_cals * portion, target_prot * portion, avail)
#         used.update(meal['dish'].tolist())
#         return meal

#     st.markdown("### 🍽️ Your Daily Meal Plan")
#     for meal_name in meal_split.keys():
#         portion = meal_split[meal_name]
#         meal_df = pick_meal(portion)
#         total_cal = round(meal_df['calories'].sum(), 2)
#         total_prot = round(meal_df['protein'].sum(), 2)

#         with st.container():
#             st.markdown(f"<div class='meal-card'><h3>{meal_name} — {total_cal} kcal, {total_prot} g Protein</h3>", unsafe_allow_html=True)
#             if not meal_df.empty:
#                 st.table(meal_df[['dish', 'calories', 'protein']].rename(columns={
#                     'dish': 'Dish',
#                     'calories': 'Calories (kcal)',
#                     'protein': 'Protein (g)'
#                 }))
#             else:
#                 st.warning("No dishes found for this meal.")
#             st.markdown("</div>", unsafe_allow_html=True)




# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from pulp import LpMaximize, LpProblem, LpVariable, lpSum
# import random
# import uuid
# from streamlit_lottie import st_lottie
# import json

# # ------------- LOTTIE ANIMATION FUNCTION -------------
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# # Load dataset
# df = pd.read_csv("categorized_dishes.csv")
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
# df.rename(columns={
#     'Dish Name': 'dish',
#     'Calories (kcal)': 'calories',
#     'Protein (g)': 'protein',
#     'Type': 'type'
# }, inplace=True)
# df['type'] = df['type'].str.strip().str.lower()
# df['dish'] = df['dish'].str.title()

# # BMR calculator
# def get_targets(weight, age, gender, goal):
#     gender = gender.lower()
#     weight, age = float(weight), int(age)
#     bmr = 10 * weight + 6.25 * (170 if gender == "male" else 160) - 5 * age + (5 if gender == "male" else -161)
#     calories = bmr * 1.4 + (-300 if goal == "Weight Loss" else 300 if goal == "Muscle Gain" else 0)
#     protein = weight * (1.5 if goal == "Muscle Gain" else 1.2 if goal == "Maintain" else 1.0)
#     return round(calories, 2), round(protein, 2)

# # Optimization
# def build_optimized_meal(cal_limit, protein_limit, available_df, max_dishes=4):
#     df_av = available_df.reset_index(drop=True)
#     n = len(df_av)
#     model = LpProblem("MealPlan", LpMaximize)
#     x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
#     random_weights = [random.uniform(0.9, 1.1) for _ in range(n)]
#     model += lpSum(df_av.loc[i, 'protein'] * random_weights[i] * x[i] for i in range(n))

#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) <= cal_limit + 100
#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) >= cal_limit - 50
#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) >= protein_limit - 5
#     model += lpSum(x[i] for i in range(n)) <= max_dishes

#     soup_salad = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['soup', 'salad']]
#     bev_des = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['beverage', 'dessert']]
#     if soup_salad:
#         model += lpSum(x[i] for i in soup_salad) <= 1
#     if bev_des:
#         model += lpSum(x[i] for i in bev_des) <= 1

#     model.solve()
#     chosen = [i for i in range(n) if x[i].varValue == 1]
#     return df_av.loc[chosen]

# # --- Streamlit Config ---
# st.set_page_config(page_title="Smart AI Nutrition Planner", layout="centered", page_icon="🥗")

# # --- Custom CSS Styling ---
# st.markdown("""
# <style>
# body {
#     background: linear-gradient(to right, #fff3e0, #ffe0b2);
#     font-family: 'Segoe UI', sans-serif;
# }
# h1, h2, h3 {
#     color: #e65100;
#     font-weight: 700;
# }
# input, select, textarea {
#     border: 2px solid #ccc !important;
#     border-radius: 8px !important;
# }
# .stButton > button {
#     background-color: #ef6c00;
#     color: white;
#     border-radius: 10px;
#     padding: 0.6rem 1.2rem;
#     font-weight: bold;
#     border: none;
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: #d84315;
#     transform: scale(1.02);
# }
# .block-container {
#     padding-top: 2rem;
# }
# .meal-card {
#     background: #fffdf9;
#     border-left: 6px solid #ff9800;
#     padding: 15px;
#     margin-bottom: 16px;
#     border-radius: 8px;
#     box-shadow: 0 4px 10px rgba(255, 152, 0, 0.1);
# }
# @keyframes fadeInUp {
#   from {opacity: 0; transform: translateY(20px);}
#   to {opacity: 1; transform: translateY(0);}
# }
# div[data-testid="stAppViewContainer"] > div:first-child {
#     animation: fadeInUp 1s ease-out;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Optional Lottie Animation (load your JSON file) ---
# lottie_path = "healthy.json"  # Make sure this file is in your directory
# try:
#     lottie_json = load_lottie(lottie_path)
#     st_lottie(lottie_json, speed=1, height=200, key="healthy_anim")
# except:
#     st.markdown("🥦 _Your AI nutrition planner_")

# # --- Form UI ---
# st.title("🥗 Smart AI Nutrition Planner")

# with st.form("nutrition_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
#         gender = st.selectbox("Gender", ["Male", "Female"])
#         preference = st.selectbox("Preference", ["Vegetarian", "Non-Vegetarian"])
#     with col2:
#         age = st.number_input("Age", min_value=10, max_value=100, step=1)
#         goal = st.selectbox("Goal", ["Weight Loss", "Maintain", "Muscle Gain"])

#     submitted = st.form_submit_button("Generate Meal Plan")

# # --- Generate & Show Results ---
# if submitted:
#     preference_clean = preference.lower()
#     target_cals, target_prot = get_targets(weight, age, gender, goal)

#     st.markdown("### 🔍 Your Personalized Nutrition Targets")
#     st.info(f"""
#     **Goal:** {goal}  
#     **Gender:** {gender}  
#     **Age:** {age}  
#     **Target Calories:** {target_cals} kcal  
#     **Target Protein:** {target_prot} g
#     """)

#     meal_split = {'Breakfast': 0.2, 'Lunch': 0.4, 'Dinner': 0.4}
#     seed = uuid.uuid4().int & (1 << 32) - 1
#     filtered = df[df['type'] == preference_clean].sample(frac=1, random_state=seed)
#     used = set()

#     def pick_meal(portion):
#         avail = filtered[~filtered['dish'].isin(used)]
#         meal = build_optimized_meal(target_cals * portion, target_prot * portion, avail)
#         used.update(meal['dish'].tolist())
#         return meal

#     st.markdown("### 🍽️ Your Daily Meal Plan")
#     for meal_name in meal_split.keys():
#         portion = meal_split[meal_name]
#         meal_df = pick_meal(portion)
#         total_cal = round(meal_df['calories'].sum(), 2)
#         total_prot = round(meal_df['protein'].sum(), 2)

#         with st.container():
#             st.markdown(f"<div class='meal-card'><h3>{meal_name} — {total_cal} kcal, {total_prot} g Protein</h3>", unsafe_allow_html=True)
#             if not meal_df.empty:
#                 st.table(meal_df[['dish', 'calories', 'protein']].rename(columns={
#                     'dish': 'Dish',
#                     'calories': 'Calories (kcal)',
#                     'protein': 'Protein (g)'
#                 }))
#             else:
#                 st.warning("No dishes found for this meal.")
#             st.markdown("</div>", unsafe_allow_html=True)




# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from pulp import LpMaximize, LpProblem, LpVariable, lpSum
# import uuid
# from streamlit_lottie import st_lottie
# import json

# # ------------- LOTTIE ANIMATION FUNCTION -------------
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# # Load dataset
# df = pd.read_csv("categorized_dishes.csv")
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
# df.rename(columns={
#     'Dish Name': 'dish',
#     'Calories (kcal)': 'calories',
#     'Protein (g)': 'protein',
#     'Type': 'type'
# }, inplace=True)
# df['type'] = df['type'].str.strip().str.lower()
# df['dish'] = df['dish'].str.title()

# # BMR calculator
# def get_targets(weight, age, gender, goal):
#     gender = gender.lower()
#     weight, age = float(weight), int(age)
#     bmr = 10 * weight + 6.25 * (170 if gender == "male" else 160) - 5 * age + (5 if gender == "male" else -161)
#     calories = bmr * 1.4 + (-300 if goal == "Weight Loss" else 300 if goal == "Muscle Gain" else 0)
#     protein = weight * (1.5 if goal == "Muscle Gain" else 1.2 if goal == "Maintain" else 1.0)
#     return round(calories, 2), round(protein, 2)

# # Optimization function (with strict calorie and protein limits)
# def build_optimized_meal(cal_limit, protein_limit, available_df, max_dishes=4):
#     df_av = available_df.reset_index(drop=True)
#     n = len(df_av)
#     model = LpProblem("MealPlan", LpMaximize)

#     x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]

#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n))  # Objective: Maximize protein

#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) <= cal_limit + 50
#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) >= cal_limit - 50

#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) <= protein_limit + 5
#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) >= protein_limit - 5

#     model += lpSum(x[i] for i in range(n)) <= max_dishes

#     # Optional: limit desserts/beverages/salads
#     if 'Category' in df_av.columns:
#         soup_salad = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['soup', 'salad']]
#         bev_des = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['beverage', 'dessert']]
#         if soup_salad:
#             model += lpSum(x[i] for i in soup_salad) <= 1
#         if bev_des:
#             model += lpSum(x[i] for i in bev_des) <= 1

#     model.solve()
#     chosen = [i for i in range(n) if x[i].varValue == 1]
#     return df_av.loc[chosen]

# # --- Streamlit Config ---
# st.set_page_config(page_title="Smart AI Nutrition Planner", layout="centered", page_icon="🥗")

# # --- Custom CSS Styling ---
# st.markdown("""
# <style>
# body {
#     background: linear-gradient(to right, #fff3e0, #ffe0b2);
#     font-family: 'Segoe UI', sans-serif;
# }
# h1, h2, h3 {
#     color: #e65100;
#     font-weight: 700;
# }
# input, select, textarea {
#     border: 2px solid #ccc !important;
#     border-radius: 8px !important;
# }
# .stButton > button {
#     background-color: #ef6c00;
#     color: white;
#     border-radius: 10px;
#     padding: 0.6rem 1.2rem;
#     font-weight: bold;
#     border: none;
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: #d84315;
#     transform: scale(1.02);
# }
# .block-container {
#     padding-top: 2rem;
# }
# .meal-card {
#     background: #fffdf9;
#     border-left: 6px solid #ff9800;
#     padding: 15px;
#     margin-bottom: 16px;
#     border-radius: 8px;
#     box-shadow: 0 4px 10px rgba(255, 152, 0, 0.1);
# }
# @keyframes fadeInUp {
#   from {opacity: 0; transform: translateY(20px);}
#   to {opacity: 1; transform: translateY(0);}
# }
# div[data-testid="stAppViewContainer"] > div:first-child {
#     animation: fadeInUp 1s ease-out;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Optional Lottie Animation (load your JSON file) ---
# lottie_path = "healthy.json"  # Put this file in the same folder
# try:
#     lottie_json = load_lottie(lottie_path)
#     st_lottie(lottie_json, speed=1, height=200, key="healthy_anim")
# except:
#     st.markdown("🥦 _Your AI nutrition planner_")

# # --- App Title ---
# st.title("🥗 Smart AI Nutrition Planner")

# # --- User Input Form ---
# with st.form("nutrition_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
#         gender = st.selectbox("Gender", ["Male", "Female"])
#         preference = st.selectbox("Preference", ["Vegetarian", "Non-Vegetarian"])
#     with col2:
#         age = st.number_input("Age", min_value=10, max_value=100, step=1)
#         goal = st.selectbox("Goal", ["Weight Loss", "Maintain", "Muscle Gain"])

#     submitted = st.form_submit_button("Generate Meal Plan")

# # --- Meal Plan Generation ---
# if submitted:
#     preference_clean = preference.lower()
#     target_cals, target_prot = get_targets(weight, age, gender, goal)

#     st.markdown("### 🔍 Your Personalized Nutrition Targets")
#     st.info(f"""
#     **Goal:** {goal}  
#     **Gender:** {gender}  
#     **Age:** {age}  
#     **Target Calories:** {target_cals} kcal  
#     **Target Protein:** {target_prot} g
#     """)

#     # Meal distribution
#     meal_split = {'Breakfast': 0.2, 'Lunch': 0.4, 'Dinner': 0.4}
#     seed = uuid.uuid4().int & (1 << 32) - 1
#     filtered = df[df['type'] == preference_clean].sample(frac=1, random_state=seed)
#     used = set()

#     def pick_meal(portion):
#         avail = filtered[~filtered['dish'].isin(used)]
#         meal = build_optimized_meal(target_cals * portion, target_prot * portion, avail)
#         used.update(meal['dish'].tolist())
#         return meal

#     # Show meals
#     st.markdown("### 🍽️ Your Daily Meal Plan")
#     total_day_cal = 0
#     total_day_prot = 0

#     for meal_name in meal_split.keys():
#         portion = meal_split[meal_name]
#         meal_df = pick_meal(portion)
#         total_cal = round(meal_df['calories'].sum(), 2)
#         total_prot = round(meal_df['protein'].sum(), 2)

#         total_day_cal += total_cal
#         total_day_prot += total_prot

#         with st.container():
#             st.markdown(f"<div class='meal-card'><h3>{meal_name} — {total_cal} kcal, {total_prot} g Protein</h3>", unsafe_allow_html=True)
#             if not meal_df.empty:
#                 st.table(meal_df[['dish', 'calories', 'protein']].rename(columns={
#                     'dish': 'Dish',
#                     'calories': 'Calories (kcal)',
#                     'protein': 'Protein (g)'
#                 }))
#             else:
#                 st.warning("No dishes found for this meal.")
#             st.markdown("</div>", unsafe_allow_html=True)

#     st.success(f"✅ **Total Daily Intake:** {total_day_cal} kcal, {total_day_prot} g Protein")






# import streamlit as st
# import pandas as pd
# from pulp import LpMaximize, LpProblem, LpVariable, lpSum
# import uuid
# from streamlit_lottie import st_lottie
# import json

# # ------------- LOTTIE ANIMATION FUNCTION -------------
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# # Load dataset
# df = pd.read_csv("categorized_dishes.csv")
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
# df.rename(columns={
#     'Dish Name': 'dish',
#     'Calories (kcal)': 'calories',
#     'Protein (g)': 'protein',
#     'Type': 'type'
# }, inplace=True)
# df['type'] = df['type'].str.strip().str.lower()
# df['dish'] = df['dish'].str.title()

# # BMR calculator
# def get_targets(weight, age, gender, goal):
#     gender = gender.lower()
#     weight, age = float(weight), int(age)
#     bmr = 10 * weight + 6.25 * (170 if gender == "male" else 160) - 5 * age + (5 if gender == "male" else -161)
#     calories = bmr * 1.4 + (-300 if goal == "Weight Loss" else 300 if goal == "Muscle Gain" else 0)
#     protein = weight * (1.5 if goal == "Muscle Gain" else 1.2 if goal == "Maintain" else 1.0)
#     return round(calories, 2), round(protein, 2)

# # Optimization function
# def build_optimized_meal(cal_limit, protein_limit, available_df, max_dishes=4):
#     df_av = available_df.reset_index(drop=True)
#     n = len(df_av)
#     model = LpProblem("MealPlan", LpMaximize)
#     x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]

#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n))  # Objective

#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) <= cal_limit + 50
#     model += lpSum(df_av.loc[i, 'calories'] * x[i] for i in range(n)) >= cal_limit - 50

#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) <= protein_limit + 5
#     model += lpSum(df_av.loc[i, 'protein'] * x[i] for i in range(n)) >= protein_limit - 5

#     model += lpSum(x[i] for i in range(n)) <= max_dishes

#     if 'Category' in df_av.columns:
#         soup_salad = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['soup', 'salad']]
#         bev_des = [i for i in range(n) if df_av.loc[i, 'Category'].lower() in ['beverage', 'dessert']]
#         if soup_salad:
#             model += lpSum(x[i] for i in soup_salad) <= 1
#         if bev_des:
#             model += lpSum(x[i] for i in bev_des) <= 1

#     model.solve()
#     chosen = [i for i in range(n) if x[i].varValue == 1]
#     return df_av.loc[chosen]

# # --- Streamlit Config ---
# st.set_page_config(page_title="Smart AI Nutrition Planner", layout="centered", page_icon="🥗")

# # --- Custom CSS Styling ---
# st.markdown("""
# <style>
# body {
#     background: linear-gradient(to right, #fff3e0, #ffe0b2);
#     font-family: 'Segoe UI', sans-serif;
# }
# h1, h2, h3 {
#     color: #e65100;
#     font-weight: 700;
# }
# input, select, textarea {
#     border: 2px solid #ccc !important;
#     border-radius: 8px !important;
# }
# .stButton > button {
#     background-color: #ef6c00;
#     color: white;
#     border-radius: 10px;
#     padding: 0.6rem 1.2rem;
#     font-weight: bold;
#     border: none;
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: #d84315;
#     transform: scale(1.02);
# }
# .block-container {
#     padding-top: 2rem;
# }
# .meal-card {
#     background: #fffdf9;
#     border-left: 6px solid #ff9800;
#     padding: 15px;
#     margin-bottom: 16px;
#     border-radius: 8px;
#     box-shadow: 0 4px 10px rgba(255, 152, 0, 0.1);
# }
# @keyframes fadeInUp {
#   from {opacity: 0; transform: translateY(20px);}
#   to {opacity: 1; transform: translateY(0);}
# }
# div[data-testid="stAppViewContainer"] > div:first-child {
#     animation: fadeInUp 1s ease-out;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Optional Lottie Animation ---
# lottie_path = "healthy.json"
# try:
#     lottie_json = load_lottie(lottie_path)
#     st_lottie(lottie_json, speed=1, height=200, key="healthy_anim")
# except:
#     st.markdown("🥦 _Your AI nutrition planner_")

# # --- Title ---
# st.title("🥗 Smart AI Nutrition Planner")

# # --- User Input Form ---
# with st.form("nutrition_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         weight = st.text_input("Weight (kg)")
#         gender = st.selectbox("Gender", ["Select Gender", "Male", "Female"])
#         preference = st.selectbox("Preference", ["Select Preference", "Vegetarian", "Non-Vegetarian"])
#     with col2:
#         age = st.text_input("Age")
#         goal = st.selectbox("Goal", ["Select Goal", "Weight Loss", "Maintain", "Muscle Gain"])

#     submitted = st.form_submit_button("Generate Meal Plan")

# # --- Meal Plan Generation ---
# # --- Meal Plan Generation ---
# if submitted:
#     if (not weight or not age or
#         gender == "Select Gender" or
#         goal == "Select Goal" or
#         preference == "Select Preference"):
#         st.error("⚠️ Please fill out all fields before generating the meal plan.")
#         st.markdown("🔁 **Try Again**")
#     else:
#         weight = float(weight)
#         age = int(age)
#         preference_clean = preference.lower()

#         target_cals, target_prot = get_targets(weight, age, gender, goal)

#         st.markdown("### 🔍 Your Personalized Nutrition Targets")
#         st.info(f"""
#         **Goal:** {goal}  
#         **Gender:** {gender}  
#         **Age:** {age}  
#         **Target Calories:** {target_cals} kcal  
#         **Target Protein:** {target_prot} g
#         """)

#         meal_split = {'Breakfast': 0.2, 'Lunch': 0.4, 'Dinner': 0.4}
#         seed = uuid.uuid4().int & (1 << 32) - 1
#         filtered = df[df['type'] == preference_clean].sample(frac=1, random_state=seed)
#         used = set()

#         def pick_meal(portion):
#             avail = filtered[~filtered['dish'].isin(used)]
#             meal = build_optimized_meal(target_cals * portion, target_prot * portion, avail)
#             used.update(meal['dish'].tolist())
#             return meal

#         st.markdown("### 🍽️ Your Daily Meal Plan")
#         total_day_cal = 0
#         total_day_prot = 0

#         for meal_name in meal_split.keys():
#             portion = meal_split[meal_name]
#             meal_df = pick_meal(portion)
#             total_cal = round(meal_df['calories'].sum(), 2)
#             total_prot = round(meal_df['protein'].sum(), 2)

#             total_day_cal += total_cal
#             total_day_prot += total_prot

#             with st.container():
#                 st.markdown(f"<div class='meal-card'><h3>{meal_name} — {total_cal} kcal, {total_prot} g Protein</h3>", unsafe_allow_html=True)
#                 if not meal_df.empty:
#                     st.table(meal_df[['dish', 'calories', 'protein']].rename(columns={
#                         'dish': 'Dish',
#                         'calories': 'Calories (kcal)',
#                         'protein': 'Protein (g)'
#                     }))
#                 else:
#                     st.warning("No dishes found for this meal.")
#                 st.markdown("</div>", unsafe_allow_html=True)

#         st.success(f"✅ **Total Daily Intake:** {total_day_cal} kcal, {total_day_prot} g Protein")
#        # Try Again Button to reset everything
#         st.markdown("---")
#         if st.button("🔁 Try Again"):
#             st.session_state.clear()
#             st.experimental_rerun()







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
                    st.table(meal_df[['dish', 'calories', 'protein']].rename(columns={
                        'dish': 'Dish',
                        'calories': 'Calories (kcal)',
                        'protein': 'Protein (g)'
                    }))
                else:
                    st.warning("No dishes found for this meal.")
                st.markdown("</div>", unsafe_allow_html=True)

        st.success(f"✅ **Total Daily Intake:** {total_day_cal} kcal, {total_day_prot} g Protein")

        # ------------ Try Again Button ------------
     # ------------ Try Again Button ------------
        st.markdown("---")
        if st.button("🔁 Try Again"):
            for key in ["weight", "age", "gender", "goal", "preference"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

