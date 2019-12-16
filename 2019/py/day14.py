#/usr/bin/env python3
from collections import defaultdict
import math

def parse_recipe(recipe):
    reactions = {}
    for line in recipe.strip().split('\n'):
        def parse_amounts(s):
            fields = s.strip().split()
            return (fields[1], int(fields[0]))

        ingreds, product = line.split('=>')
        product = parse_amounts(product)
        ingreds = [parse_amounts(i) for i in ingreds.split(',')]
        reactions[product[0]] = {'qty': product[1], 'reactants': ingreds}
    return reactions

def calc_ore_cost(reactions, fuel_to_create=1, debug=False):
    def debug_print(s=''):
        if debug:
            print(s)
    ore_counter = 0
    stock = defaultdict(int)

    deficits = [('FUEL', -fuel_to_create)]
    while deficits:
        debug_print("stock: {}".format([i for i in stock.items() if i[1] < 0]))
        for product, deficit_amt in deficits:
            debug_print("need {}x of {}".format(-deficit_amt, product))
            num_reactions = math.ceil(-deficit_amt/reactions[product]['qty'])
            debug_print("running {}x reaction {}".format(num_reactions,
                                                         reactions[product]))
            product_qty = num_reactions * reactions[product]['qty']
            debug_print("producing {}x of {}".format(product_qty, product))
            stock[product] += product_qty
            assert product_qty >= -deficit_amt
            # assert stock[product] <= reactions[product]['qty']
            for reactant in reactions[product]['reactants']:
                reactant_qty = reactant[1] * num_reactions
                if reactant[0] == 'ORE':
                    ore_counter += reactant_qty
                else:
                    stock[reactant[0]] -= reactant_qty
                debug_print("  consuming {}x of {}".format(reactant_qty,
                                                           reactant[0]))
        deficits = [item for item in stock.items() if item[1] < 0]
        debug_print()
    return ore_counter

def calc_max_fuel(reactions, est_ore_per_fuel, ore_reserves=1000000000000):
    fuel = ore_reserves // est_ore_per_fuel
    ore_cost = calc_ore_cost(reactions, fuel_to_create=fuel)
    while ore_cost < ore_reserves:
        fuel += int(fuel * 0.5)
        ore_cost = calc_ore_cost(reactions, fuel_to_create=fuel)

    count = 0
    bracket = [(fuel, ore_cost), (0, 0)]
    while bracket[0][0] - bracket[1][0] > 1:
        fuel = (bracket[0][0] - bracket[1][0]) // 2 + bracket[1][0]
        ore_cost = calc_ore_cost(reactions, fuel_to_create=fuel)
        if ore_cost > ore_reserves:
            bracket[0] = (fuel, ore_cost)
        else:
            bracket[1] = (fuel, ore_cost)
    return bracket[1][0]

recipe = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
assert cost == 31

recipe = """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
assert cost == 165

recipe = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
assert cost == 13312
fuel = calc_max_fuel(reactions, cost)
assert fuel == 82892753

recipe = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
assert cost == 180697
fuel = calc_max_fuel(reactions, cost)
assert fuel == 5586022

recipe = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
assert cost == 2210736
fuel = calc_max_fuel(reactions, cost)
assert fuel == 460664

with open('day14.dat') as f:
    recipe = f.read()
reactions = parse_recipe(recipe)
cost = calc_ore_cost(reactions)
print("part 1: {}".format(cost))

fuel = calc_max_fuel(reactions, cost)
print("part 2: {}".format(fuel))
assert fuel == 6216589

