from tinyec import registry

class Point:
    def __init__(self, x, y, curve = None) -> None:
        self.curve = curve
        self.x = x
        self.y = y
        if curve == None:
            self.on_curve = None
        elif x == None or y == None:
            self.on_curve = None
        else:
            self.on_curve = curve.on_curve(x, y)
        pass
    
    def __add_pt(self, point_1, point_2):
        # INFO: print for DEBUG purposes ONLY!
        # print("ADD pts {} + {}".format(point_1, point_2))
        if point_1 == point_2:
            return self.__double_pt(point_1)
        if point_1 == None:
            return point_2
        elif point_2 == None:
            return point_1
        elif point_1.x == point_2.x and point_1.y != point_2.y:
            return Point(None, None, self.curve)
        
        lambda_f = ((point_2.y - point_1.y) * pow(point_2.x - point_1.x, -1, self.curve.p)) % self.curve.p
        
        x_3 = (lambda_f**2 - point_1.x - point_2.x) % self.curve.p
        y_3 = (lambda_f * (point_1.x - x_3) - point_1.y) % self.curve.p
        
        return Point(x_3, y_3, self.curve)

    def __double_pt(self, point):
        # INFO: print for DEBUG purposes ONLY!
        # print("DOUBLE pt {}".format(point))
        if point == None:
            return Point(None, None, self.curve)
        elif point.y == 0:
            return Point(None, None, self.curve)
        
        lambda_f = ((3*pow(point.x, 2) + self.curve.a) * pow(2 * point.y, -1, self.curve.p)) % self.curve.p
        
        x_3 = (lambda_f**2 - 2*point.x) % self.curve.p
        y_3 = (lambda_f * (point.x - x_3) - point.y) % self.curve.p
        
        return Point(x_3, y_3, self.curve)
    
    def __mul_pt(self, point, multiplier):
        if multiplier == 0:
            return Point(None, None, self.curve)
        elif multiplier == 1:
            return point
        elif multiplier % 2 == 1:
            return self.__add_pt(point, self.__mul_pt(point, multiplier-1))
        else:
            return self.__mul_pt(self.__double_pt(point), multiplier//2)

    def __mul__(self, multiplier):        
        return self.__mul_pt(self, multiplier)
    
    __rmul__ = __mul__
    
    def __str__(self):
        return "P({}, {})".format(self.x, self.y)
    
    def __eq__(self, value):
        try:
            if value == None:
                if self.x == None and self.y == None:
                    return True
                elif self.x == None or self.y == None:
                    raise Exception("ERROR: Point object cannot have coordinate of None type!")
                return False
            else:
                if self.x == value.x and self.y == value.y:
                    return True
                return False
        except:
            return False

class Curve:
    """
    Class defining an elliptic curve with generator G point (if set)
    """    
    def __init__(self, a, b, p = None) -> None:
        self.a = a
        self.b = b
        self.p = p
        pass
    
    def __point_on_curve(self, x, y):
        result = (x**3 + self.a*x + self.b - y**2) % self.p
        if result == 0:
            return True
        else:
            return False
        
    def on_curve(self, x, y):
        return self.__point_on_curve(x, y)
    
    def list_points_over_finite_field(self) -> list:
        try:
            if self.p == None:
                raise Exception("You need to specify parameter p!")
            
            points = []
            
            for x in range(self.p):
                for y in range(self.p):
                    result = self.__point_on_curve(x, y)
                    if result == True:
                        points.append((x, y))
            return points
        except:
            self.p = input("Set value p: ")
            self.p = int(self.p)
            self.list_points_over_finite_field
            
    def set_generator(self, x, y):
        self.G = Point(x, y, self)
        print("Generator set properly to point G({}, {})".format(x, y))
        
# ------- MAIN --------

curr = registry.get_curve('secp192r1')        

curve = Curve(curr.a, curr.b, curr.field.p)
curve.set_generator(curr.g.x, curr.g.y)
print("-- CYCLIC GROUP --")
for it in range(10):
    print(it, curve.G*it)