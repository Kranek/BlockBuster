from Entity import Entity


class Collision:
    def __init__(self):
        pass

    @staticmethod
    def rect_vs_rect(obj1, obj2):
        if (obj1.x >= obj2.x + obj2.width or obj1.x + obj1.width <= obj2.y or
                obj1.y >= obj2.y + obj2.height or obj1.y + obj1.height < obj2.y or
                obj2.x >= obj1.x + obj1.width or obj2.x + obj2.width <= obj1.x or
                obj2.y >= obj1.y + obj1.height or obj2.y + obj2.height <= obj1.y):
            return False
        return True

    @staticmethod
    def rect_vs_circle(rect, circle):
        #temp = Entity(circle.x-circle.radius, circle.y-circle.radius, circle.radius*2, circle.radius*2)
        # TODO: fix both the circle representation and its center
        temp = Entity(circle.x, circle.y, circle.radius*2, circle.radius*2)
        return Collision.rect_vs_rect(rect, temp)