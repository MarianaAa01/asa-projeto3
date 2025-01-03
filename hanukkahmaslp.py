import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def parse_input():
    lines = sys.stdin.read().strip().splitlines()
    n, m, t = map(int, lines[0].split())
    
    factories = {}
    countries = {}
    children = []
    children_per_country = {i: 0 for i in range(1, m + 1)}
    
    # Parse countries first
    for i in range(n + 1, n + m + 1):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        max_export = max(0, max_export)
        min_delivery = max(0, min_delivery)
        countries[country_id] = {
            'max_export': max_export, 
            'min_delivery': min_delivery
        }
    
    # Parse factories - include if stock > 0, regardless of country's max_export
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        if stock > 0:  # Only check stock, not max_export
            factories[factory_id] = {'country': country_id, 'stock': stock}
    
    # Parse children
    for i in range(n + m + 1, n + m + t + 1):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        children_per_country[country_id] += 1
        valid_requests = [f for f in data[2:] if f in factories and countries[factories[f]['country']]['max_export'] > 0]
        
        if len(valid_requests) > 0:
            children.append({"id": child_id, "country": country_id, "factories": valid_requests})
    
    return n, t, factories, countries, children, children_per_country

def check_min_delivery_feasibility(countries, children_per_country):
    """Check if minimum delivery requirements can potentially be met"""
    for country_id, country in countries.items():
        if country['min_delivery'] > 0:
            if children_per_country[country_id] < country['min_delivery']:
                return False
    return True

def solve_lp():
    n, t, factories, countries, children, children_per_country = parse_input()
    
    if n == 0:
        return -1
    if t == 0:
        return 0
    
    if not children:
        return 0
    
    # Check if minimum delivery requirements are feasible
    if not check_min_delivery_feasibility(countries, children_per_country):
        return -1

    prob = LpProblem("MerryHanukkah", LpMaximize)
    
    # Decision variables
    x = {}
    for child in children:
        for factory_id in child["factories"]:
            x[f"{child['id']}_{factory_id}"] = LpVariable(
                f"x_{child['id']}_{factory_id}", 
                cat="Binary"
            )
    
    # Objective: Maximize satisfied children
    prob += lpSum(lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                       for factory_id in child["factories"])
                  for child in children)
    
    # Factory stock constraints
    for factory_id, factory in factories.items():
        prob += lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                     for child in children
                     if factory_id in child["factories"]) <= factory["stock"]
    
    # One toy per child
    for child in children:
        prob += lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                    for factory_id in child["factories"]) <= 1
    
    # Country constraints - combine export and min delivery
    for country_id, country in countries.items():
        # Count toys exported from this country
        country_exports = lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                           for child in children
                           for factory_id in child["factories"]
                           if factories[factory_id]["country"] == country_id)
    
        prob += country_exports <= country["max_export"]
    
        # Minimum delivery requirement (ensure it accounts for both max export and min delivery)
        country_deliveries = lpSum(lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                                     for factory_id in child["factories"] )
                                     for child in children
                                     if child["country"] == country_id)
        
        if country["min_delivery"] >= 0:
            prob += country_deliveries >= country["min_delivery"]
    
    solver = PULP_CBC_CMD(msg=False)
    status = prob.solve(solver)
    
    
    if status != 1:
        return -1
    
    return int(round(prob.objective.value()))

if __name__ == "__main__":
    result = solve_lp()
    print(result)
