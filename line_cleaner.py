from vector import Vec2

def cleanup_line(points : list[Vec2]):
    if len(points) < 3:
        return points

    new_points : list[Vec2] = [points[0]]

    i : int = 1
    while i < len(points) - 1:
        p0 = points[i - 1]
        p1 = points[i]
        p2 = points[i + 1]

        if p0.x == p1.x and p1.x == p2.x and p1.y != p2.y:
            new_points.append(p1)
            i += 2
        else:
            new_points.append(p2)
            i += 2

    return new_points
