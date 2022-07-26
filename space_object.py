import math
import config

class SpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.obj_type = obj_type
        self.id = id
        self.radius = config.radius[self.obj_type]

    def turn_left(self):
        if self.obj_type == "spaceship":
            self.angle += config.angle_increment
            if self.angle > 360: #If angle is bigger than 360, return it back to start from 0 degrees
                self.angle -= 360

    def turn_right(self):
        if self.obj_type == "spaceship":
            self.angle -= config.angle_increment
            if self.angle < 0: #If angle is smaller than 0, return it back to start from 360 degrees
                self.angle += 360

    def move_forward(self):
        dx = config.speed[self.obj_type] * math.cos(math.radians(self.angle))
        dy = config.speed[self.obj_type] * math.sin(math.radians(self.angle))

        self.x += dx
        if self.x < 0: #If x coordinate is negative, add to self.width
            self.x += self.width
        elif self.x > self.width: #If x coordinate is bigger than width, minus with self.width
            self.x -= self.width

        self.y -= dy
        if self.y < 0: #If y coordinate is negative, add to self.height
            self.y += self.height
        elif self.y > self.height: #If y coordinate is bigger than height, minus with self.height
            self.y -= self.height

    def get_xy(self):
        return (self.x, self.y)

    def collide_with(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        
        if dx > (self.width / 2): #If difference is bigger than half the width, it is going the wrong way
            dx = self.width - dx #Real distance
        if dy > (self.height / 2): #If difference is bigger than half the height, it is going the wrong way
            dy = self.height - dy #Real distance
        euc_distance = math.sqrt(dx**2 + dy**2)

        #Check if spaceship collides with asteroid_small
        if (self.obj_type == "spaceship" and other.obj_type == "asteroid_small") or (other.obj_type == "spaceship" and self.obj_type == "asteroid_small"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if spaceship collides with asteroid_large
        if (self.obj_type == "spaceship" and other.obj_type == "asteroid_large") or (other.obj_type == "spaceship" and self.obj_type == "asteroid_large"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if bullet collides with asteroid_small
        if (self.obj_type == "bullet" and other.obj_type == "asteroid_small") or (other.obj_type == "bullet" and self.obj_type == "asteroid_small"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if bullet collides with asteroid_large
        if (self.obj_type == "bullet" and other.obj_type == "asteroid_large") or (other.obj_type == "bullet" and self.obj_type == "asteroid_large"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if asteroid_small collides with asteroid_small
        if (self.obj_type == "asteroid_small" and other.obj_type == "asteroid_small"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if asteroid_large collides with asteroid_large
        if (self.obj_type == "asteroid_large" and other.obj_type == "asteroid_large"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        #Check if asteroid_small collides with asteroid_large
        if (self.obj_type == "asteroid_small" and other.obj_type == "asteroid_large") or (other.obj_type == "asteroid_small" and self.obj_type == "asteroid_large"):
            return euc_distance <= (config.radius[self.obj_type] + config.radius[other.obj_type])
        return False

    def __repr__(self):
        return "{} {:.1f},{:.1f},{},{}".format(self.obj_type, self.x, self.y, self.angle, self.id)

