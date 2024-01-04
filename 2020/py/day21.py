#!/usr/bin/env python3
from collections import namedtuple, defaultdict, Counter

Food = namedtuple('Food', ['ingredients', 'allergens'])

def part1(foods):
    all_ingredients = set.union(*(f.ingredients for f in foods))
    all_allergens = set.union(*(f.allergens for f in foods))
    cantbe = defaultdict(set)
    for ingredient in all_ingredients:
        for allergen in all_allergens:
            for food in foods:
                if ingredient not in food.ingredients and allergen in food.allergens:
                    cantbe[ingredient].add(allergen)
                    break
    clean = set(ingredient for ingredient, allergens in cantbe.items() if allergens == all_allergens)

    c = Counter(i for f in foods for i in f.ingredients)

    # remove clean ingredients (in place) for part 2
    for i in range(len(foods)):
        foods[i] = Food(foods[i].ingredients-clean, foods[i].allergens)

    return sum(c[i] for i in clean)

def part2(foods):
    from itertools import permutations
    all_ingredients = list(set.union(*(f.ingredients for f in foods)))
    all_allergens = list(set.union(*(f.allergens for f in foods)))
    # brute force is only 8! permutations
    for perm in permutations(range(len(all_allergens))):
        conflict = False
        for i, a in enumerate(perm):
            ingredient = all_ingredients[i]
            allergen = all_allergens[a]
            for food in foods:
                if allergen in food.allergens and ingredient not in food.ingredients:
                    conflict = True
                    break
            if conflict: break
        if not conflict:
            break
    resolved = {all_allergens[a]: all_ingredients[i] for i, a in enumerate(perm)}
    return ','.join(resolved[k] for k in sorted(resolved))

def parse_input(lines):
    foods = []
    for line in lines:
        ingredients, allergens = line[:-1].split('(contains')
        ingredients = set(map(str.strip, ingredients.split()))
        allergens = set(map(str.strip, allergens.split(',')))
        foods.append(Food(ingredients, allergens))
    return foods

def run_tests():
    test_input = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".strip().split('\n')
    foods = parse_input(test_input)
    assert part1(foods) == 5

if __name__ == '__main__':
    run_tests()
    with open(__file__[:-3] + '-input.dat') as infile:
        test_input = infile.read().strip().split('\n')
    foods = parse_input(test_input)
    print(f"Part 1: {part1(foods)}")
    print(f"Part 2: {part2(foods)}")
