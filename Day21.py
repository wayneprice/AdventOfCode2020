import re
import functools


with open('data/input-day21.txt', 'r') as fp :
    all_ingredients = []
    all_allergens = {}
    for line in fp :
        ingredients_list, allergens_list = re.fullmatch('(.*) \(contains (.*)\)', line.strip()).groups()
        ingredients = ingredients_list.split(' ')
        allergens = allergens_list.split(', ')

        all_ingredients.extend(ingredients)
        for allergen in allergens :
            if allergen in all_allergens :
                all_allergens[allergen] = all_allergens[allergen].intersection(set(ingredients))
            else :
                all_allergens[allergen] = set(ingredients)

ingredients_free_from_allergens = set(all_ingredients)
for ingredients in all_allergens.values() :
    ingredients_free_from_allergens = ingredients_free_from_allergens.difference(ingredients)
print('Free from allergen count:', sum([all_ingredients.count(ingredient) for ingredient in ingredients_free_from_allergens]))

dangerous_ingredients = {}
while all_allergens :
    allergen = next((allergen for allergen, ingredients in all_allergens.items() if len(ingredients) == 1))
    ingredient = list(all_allergens[allergen])[0]
    dangerous_ingredients[ingredient] = allergen
    for allergen, ingredients in all_allergens.items() :
        if ingredient in ingredients:
            ingredients.remove(ingredient)
    all_allergens = { allergen: ingredient for allergen, ingredient in all_allergens.items() if len(ingredient) }

print('Dangerous ingredients sorted by allergen:', ','.join([x[0] for x in sorted(dangerous_ingredients.items(), key = lambda kv: kv[1])]))

