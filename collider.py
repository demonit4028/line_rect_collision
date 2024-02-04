def collision_lines(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2 # not 90 deg
    x = ((y3-y1)*(x2-x1)*(x4-x3) + x1*(y2-y1)*(x4-x3) - x3*(y4-y3)*(x2-x1)) / ((y2-y1)*(x4-x3) - (y4-y3)*(x2-x1))
    y = (x-x1)*(y2-y1)/(x2-x1)+y1
    if x3 <= x <= x4 and y3 <= y <= y4 and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return (x,y)

def all_collisions_line_rect(line, rect):
    points = []
    for x in range(2):
        point = collision_lines(line, [rect[0] if x == 0 else rect[2], rect[1], rect[0] if x == 0 else rect[2], rect[3]])
        if point:
            points += [point]
    for y in range(2):
        point = collision_lines(line, [rect[0], rect[1] if y == 0 else rect[3], rect[2], rect[1] if y == 0 else rect[3]])
        if point:
            points += [point]
    return points