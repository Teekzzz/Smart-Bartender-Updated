#The code within drinks.py is already comptabile with Python 3, so no syntax changes were needed.
#The only updates to the code were as follows:
#   -The use of namedtuples for better readability and ease of use. These replaced the previous
#    dictionaries being used.
#   -Clear comments have been added to aide those who are not familiar with Python, to provide them
#    the opportunity to easily edit this file themselves.


from collections import namedtuple

# Define a namedtuple 'Drink' with fields 'name' and 'ingredients'
Drink = namedtuple("Drink", ["name", "ingredients"])

# Define a namedtuple 'Ingredient' with fields 'name' and 'value'
Ingredient = namedtuple("Ingredient", ["name", "value"])

# List of drink recipes, each with a name and a dictionary of ingredients and their amounts (in milliliters)
drink_list = [
    Drink("Rum & Coke", {"rum": 50, "coke": 150}),
    Drink("Gin & Tonic", {"gin": 50, "tonic": 150}),
    Drink("Long Island", {"gin": 15, "rum": 15, "vodka": 15, "tequila": 15, "coke": 100, "oj": 30}),
    Drink("Screwdriver", {"vodka": 50, "oj": 150}),
    Drink("Margarita", {"tequila": 50, "mmix": 150}),
    Drink("Gin & Juice", {"gin": 50, "oj": 150}),
    Drink("Tequila Sunrise", {"tequila": 50, "oj": 150})
]

# List of available drink ingredients, each with a name and a value (used for identification)
drink_options = [
    Ingredient("Gin", "gin"),
    Ingredient("Rum", "rum"),
    Ingredient("Vodka", "vodka"),
    Ingredient("Tequila", "tequila"),
    Ingredient("Tonic Water", "tonic"),
    Ingredient("Coke", "coke"),
    Ingredient("Orange Juice", "oj"),
    Ingredient("Margarita Mix", "mmix")
]