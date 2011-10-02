import math

#todo: how to calculate what my angular velocity should be
# based on what these vectors are?

def calculate_field_to_goal(xy, goal_xy, r):
    alpha = 0.1
    spread = 1000.0
    d = math.sqrt((xy['x'] - goal_xy['x']) ** 2 + (xy['y'] - goal_xy['y']) ** 2)
    theta = math.atan2((goal_xy['y'] - xy['y']) / (goal_xy['x'] - xy['x']))
    if d < r:
        return [0, 0]
    elif r <= d and d <= spread + r:
        return [alpha * (d - r) * math.cos(theta), alpha * (d - r) * math.sin(theta)]
    else:
        return [alpha * spread * math.cos(theta), alpha * spread * math.sin(theta)]
