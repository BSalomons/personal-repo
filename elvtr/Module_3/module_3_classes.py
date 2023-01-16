from math import pow, sqrt


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x, self.y}'

    def to_string(self):
        return f'{self.x, self.y}'

    def distance_from_origin(self):
        ans = pow(self.x, 2) + pow(self.y, 2) # x^2 + y^2
        return sqrt(ans)

if __name__ == '__main__':
    pt1 = Point(3, 4)
    print(pt1.to_string(), end='')
    print(f' is {pt1.distance_from_origin()} from the origin.')
    pt0 = Point()
    print(f'point {pt0} is {pt0.distance_from_origin()} from the origin')

