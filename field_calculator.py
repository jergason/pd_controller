import math

#todo: how to calculate what my angular velocity should be
# based on what these vectors are?

def calculate_field_to_goal(xy, goal_xy, r, s):
    alpha = 0.1
    d = math.sqrt((xy['x'] - goal_xy['x']) ** 2 + (xy['y'] - goal_xy['y']) ** 2)
    theta = math.atan2((goal_xy['y'] - xy['y']) / (goal_xy['x'] - xy['x']))
    if d < r:
        return {'x': 0, 'y': 0}
    elif r <= d and d <= s + r:
        return { 'x': alpha * (d - r) * math.cos(theta), 'y': alpha * (d - r) * math.sin(theta) }
    else:
        return { 'x': alpha * s * math.cos(theta), 'y': alpha * s * math.sin(theta) }
