def analyze_cost(current_cost, average_cost):

    if current_cost > average_cost:
        return "High AWS cost detected"

    return "AWS cost is under control"