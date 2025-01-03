import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

factories = {}
countries = {}
children = []

def parse_input():
    global factories, countries, children
    lines = sys.stdin.read().strip().splitlines()
    
    n, m, t = map(int, lines[0].split())
    
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories[factory_id] = {'country': country_id, 'stock': stock}
    
    for i in range(n + 1, n + m + 1):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries[country_id] = {'max_export': max_export, 'min_delivery': min_delivery, 'current_delivery': 0}
    
    for i in range(n + m + 1, n + m + t + 1):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        factories_list = data[2:]
        children.append({"id": child_id, "country": country_id, "factories": factories_list})
    
    return n, m, t

def solve_lp():
    """
    Solve the Linear Programming problem.
    """
    prob = LpProblem("MerryHanukkah", LpMaximize)

    # Decision variables: x[k] = 1 if child k receives a present, 0 otherwise
    x = {child["id"]: LpVariable(f"x_{child['id']}", cat="Binary") for child in children}

    # Track how many toys are requested from each factory
    factory_usage = {factory_id: lpSum(x[child["id"]]
                                       for child in children if factory_id in child["factories"])
                     for factory_id in factories.keys()}

    # Track how many toys are delivered to each country
    country_delivery = {country_id: lpSum(x[child["id"]]
                                          for child in children if child["country"] == country_id)
                        for country_id in countries.keys()}

    # Track how many toys are exported from each country
    country_exports = {country_id: lpSum(factory_usage[factory_id]
                                         for factory_id in factories
                                         if factories[factory_id]["country"] == country_id)
                       for country_id in countries.keys()}

    # Objective: Maximize the number of satisfied children
    prob += lpSum(x[child["id"]] for child in children), "Maximize satisfied children"

    # Constraint 1: Factory stock limits
    for factory_id, factory in factories.items():
        prob += factory_usage[factory_id] <= factory["stock"], f"Factory_{factory_id}_Stock"

    # Constraint 2: Country export limits
    for country_id, country in countries.items():
        prob += country_exports[country_id] <= country["max_export"], f"Country_{country_id}_MaxExport"

    # Constraint 3: Minimum delivery for each country
    for country_id, country in countries.items():
        prob += country_delivery[country_id] >= country["min_delivery"], f"Country_{country_id}_MinDelivery"

    # Constraint 4: Each child can receive at most one toy
    for child in children:
        prob += x[child["id"]] <= 1, f"Child_{child['id']}_OneToy"

    # Solve the problem
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    # Check if a solution was found
    if prob.status == 1:  # Feasible solution
        return int(prob.objective.value())
    return -1  # Infeasible solution

if __name__ == "__main__":
    n, m, t = parse_input()
    
    if n == 0:
        print(-1)

    elif t == 0:
        print(0)

    else:
        result = solve_lp()
        print(result)
