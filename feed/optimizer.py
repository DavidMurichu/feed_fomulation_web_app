import numpy as np

from pulp import *

# Input data
ingredients_x = {
    'Maize': {'DM%': 88, 'CP%': 8, 'CF%': 12, 'Ca%': 0.17, 'P%': 0.55, 'ME Kcal/kg': 3000, 'Lysine %': 0.53, 'Methionine %': 0.29, 'min': None, 'max': None, 'cost': 23.189546668256277},
    'Maize bran': {'DM%': 88, 'CP%': 9.4, 'CF%': 13, 'Ca%': 0.04, 'P%': 1.03, 'ME Kcal/kg': 2200, 'Lysine %': 0.18, 'Methionine %': 0.21, 'min': None, 'max': None, 'cost': 21.87697106165995},
    'Maize/cob meal': {'DM%': 88, 'CP%': 7, 'CF%': 8, 'Ca%': 0, 'P%': 0.3, 'ME Kcal/kg': 0, 'Lysine %': 0, 'Methionine %': 0, 'min': 0, 'max': None, 'cost': 12.15409672533318},
    'Rice bran': {'DM%': 88, 'CP%': 13.5, 'CF%': 6.5, 'Ca%': 0.06, 'P%': 1.43, 'ME Kcal/kg': 3000, 'Lysine %': 0.5, 'Methionine %': 0.22, 'min': None, 'max': None, 'cost': 19.744125331958898},
    'Cassava meal': {'DM%': 88, 'CP%': 2.8, 'CF%': 4.0, 'Ca%': 0.3, 'P%': 0.05, 'ME Kcal/kg': 3000, 'Lysine %': 0, 'Methionine %': 0, 'min': None, 'max': None, 'cost': 15.900467964335567},
    'Molasses': {'DM%': 75, 'CP%': 3.0, 'CF%': 0, 'Ca%': 0.75, 'P%': 0.08, 'ME Kcal/kg': 2330, 'Lysine %': 0, 'Methionine %': 0, 'min': None, 'max': None, 'cost': 9.74283188303314},
    'Millet': {'DM%': 88, 'CP%': 10.5, 'CF%': 2.0, 'Ca%': 0.05, 'P%': 0.4, 'ME Kcal/kg': 1392, 'Lysine %': 0.2, 'Methionine %': 0.27, 'min': None, 'max': None, 'cost': 10.501038943788405},
    'Sorghum': {'DM%': 88, 'CP%': 9.0, 'CF%': 2.1, 'Ca%': 0.03, 'P%': 0.28, 'ME Kcal/kg': 3250, 'Lysine %': 0.2, 'Methionine %': 0.12, 'min': None, 'max': 70, 'cost': 21.282265115752498},
    'Fish meal': {'DM%': 88, 'CP%': 60.0, 'CF%': 1.0, 'Ca%': 4.37, 'P%': 2.53, 'ME Kcal/kg': 2310, 'Lysine %': 4.08, 'Methionine %': 3.7, 'min': None, 'max': None, 'cost': 95.35340164406743},
    'Blood meal': {'DM%': 92, 'CP%': 72.9, 'CF%': 1.7, 'Ca%': 0.28, 'P%': 0.22, 'ME Kcal/kg': 1177, 'Lysine %': 7.0, 'Methionine %': 0.9, 'min': None, 'max': None, 'cost': 83.85814098883452},
    'Cotton seed cake': {'DM%': 88, 'CP%': 40.0, 'CF%': 14, 'Ca%': 0.2, 'P%': 1.2, 'ME Kcal/kg': 968, 'Lysine %': 1.6, 'Methionine %': 0.52, 'min': None, 'max': None, 'cost': 48.7539532170818},
    'Soya bean meal': {'DM%': 88, 'CP%': 43.0, 'CF%': 6, 'Ca%': 0.53, 'P%': 0.64, 'ME Kcal/kg': 2800, 'Lysine %': 2.84, 'Methionine %': 0.65, 'min': None, 'max': None, 'cost': 79.64411128049252},
    'Limestone': {'DM%': 98, 'CP%': 0, 'CF%': 0, 'Ca%': 38.0, 'P%': 0, 'ME Kcal/kg': 0, 'Lysine %': 0, 'Methionine %': 0, 'min': None, 'max': None, 'cost': 14.450768262846697},
    'Oyster shells': {'DM%': 98, 'CP%': 0, 'CF%': 0, 'Ca%': 35.0, 'P%': 0, 'ME Kcal/kg': 0, 'Lysine %': 0, 'Methionine %': 0, 'min': None, 'max': None, 'cost': 17.437072492457933},
    'Wheat pollard': {'DM%': 98, 'CP%': 15.0, 'CF%': 0, 'Ca%': 0, 'P%': 0, 'ME Kcal/kg': 0, 'Lysine %': 0.6, 'Methionine %': 0.0, 'min': None, 'max': None, 'cost': 38.212601422729875},
    # 'methionine': {'DM%': 0, 'CP%': 0, 'CF%': 0, 'Ca%': 0, 'P%': 0, 'ME Kcal/kg': 0, 'Lysine %': 0, 'Methionine %': 2, 'min': 0, 'max': 0, 'cost': 0},
}

nutrient_requirements = {
    'DM%': {'min': None, 'max': None},
    'CP%': {'min': 18, 'max': None},
    'CF%': {'min': None, 'max': 7.5},
    'Ca%': {'min': 0.9, 'max': None},
    'ME Kcal/kg': {'min': 3000, 'max': None},
    'Lysine %': {'min': 1.1, 'max': None},
    'Methionine %': {'min': 0.6, 'max': None},
    
}


def feed_fomulate(nutrient_requirements, ingredients_x):
    total_nutrient = {}
    not_satisfied = {}
    selected_ingridients={}

    # Convert data into NumPy arrays
    costs = np.array([ingredients_x[ingredient]['cost'] for ingredient in ingredients_x])


    nutrient_content = np.array([[ingredients_x[ingredient][nutrient] for nutrient in nutrient_requirements] for ingredient in ingredients_x])

    # Define the problem
    prob = LpProblem("Least_Cost_Feed_Formulation", LpMinimize)


    # Define the decision variables (amount of each ingredient)
    amounts = LpVariable.dicts("Amount", ingredients_x, lowBound=0, cat='Continuous')


    # Define the objective function (cost minimization)
    prob += lpSum(costs * [amounts[i] for i in ingredients_x]), "Total_Cost"


    # Add minimum and maximum requirements for each ingredient
    for ingredient in ingredients_x:
        min_amount = ingredients_x[ingredient]['min']
        max_amount = ingredients_x[ingredient]['max']

        # Min constraint
        if min_amount is not None:
            prob += amounts[ingredient] >= (min_amount)/100, f"{ingredient}_min"

        # Max constraint (if not None)
        if max_amount is not None:
            prob += amounts[ingredient] <= (max_amount)/100, f"{ingredient}_max"


    # Add nutrient constraints
    for idx, nutrient in enumerate(nutrient_requirements):
        min_value = nutrient_requirements[nutrient]['min']
        max_value = nutrient_requirements[nutrient]['max']

        # Min constraint
        if min_value is not None:
            prob += lpSum(nutrient_content[:, idx] * [amounts[i] for i in ingredients_x]) >= (min_value), f"{nutrient}_min"

        # Max constraint (if not None)
        if max_value is not None:
            prob += lpSum(nutrient_content[:, idx] * [amounts[i] for i in ingredients_x]) <= (max_value), f"{nutrient}_max"


    prob += lpSum(amounts[i] for i in ingredients_x) == 1, "Total_Quantity_Constraint"


    # Solve the problem
    status = prob.solve(PULP_CBC_CMD(msg=False))



    # Print the optimal amounts of each ingredient for feasible solutions
    for ingredient in ingredients_x:
        if amounts[ingredient].varValue !=0:
            selected_ingridients[ingredient]=round((amounts[ingredient].varValue)*100, 4)

    # Calculate total nutrient values and check if they meet requirements
    for nutrient in nutrient_requirements:
        nutrient_values = np.array([ingredients_x[i][nutrient] * amounts[i].varValue if amounts[i].varValue is not None else 0 for i in ingredients_x])
        total_value = np.sum(nutrient_values)
        # Check if the nutrient values satisfy the requirements
        min_value = nutrient_requirements[nutrient]['min']
        max_value = nutrient_requirements[nutrient]['max']


        if min_value is not None and max_value is not None:
            if min_value <= total_value <= max_value:
                total_nutrient[nutrient] = round(total_value, 4)
            else:
                not_satisfied[nutrient] = total_value
        elif min_value is not None:
            if min_value <= total_value:
                total_nutrient[nutrient] = round(total_value, 4)
            else:
                not_satisfied[nutrient] = total_value
        elif max_value is not None:
            if total_value <= max_value:
                total_nutrient[nutrient] = round(total_value, 4)
            else:
                not_satisfied[nutrient] = total_value




    # return the context with total nutrient values
    
    context = {
        'total_nutrient': total_nutrient,
        'not_satisfied': not_satisfied,
        'status': status,
        'nutrient_requirements':nutrient_requirements,
        'selected_ingridients':selected_ingridients,
        'cost':value(prob.objective)
    }
    return context


# result=feed_fomulate(nutrient_requirements=nutrient_requirements,ingredients_x=ingredients_x)

# print(result)