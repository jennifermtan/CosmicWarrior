import math
import config

class Player:
    def __init__(self):
        pass

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        self.spaceship = spaceship

        thrust = True
        left = False
        right = False
        bullet = False
        
        bullet_count = 0
        i = 0
        while i < len(asteroid_ls):
            #Loop asteroids to find the asteroid with the shortest distance
            i = 0
            shortest_distance = asteroid_ls[0] #Set shortest distance to asteroid index 0
            while i < len(asteroid_ls):
                if self.euc_dist(asteroid_ls[i]) < self.euc_dist(shortest_distance): #Find the shortest distance
                    shortest_distance = asteroid_ls[i]
                i += 1

            # i = 0
            # while i < len(asteroid_ls):
            #     if asteroid_ls[i] == shortest_distance:
            #         break
            #     elif (self.direction(asteroid_ls[i]) > 0):
            #         left = True
            #     elif (self.direction(asteroid_ls[i]) > 0):
            #         right = True
            #     i += 1
            
            if -80 < self.direction(shortest_distance) < 80: #Set a range for shooting bullets
                bullet = True
            elif self.direction(shortest_distance) > 0: #Turn left
                left = True
            else: #Turn right
                right = True

        return (thrust, left, right, bullet)

    def euc_dist(self, other):
        dx = abs(self.spaceship.x - other.x)
        dy = abs(self.spaceship.y - other.y)
        
        if dx > (self.spaceship.width / 2): #If difference is bigger than half the width, it is going the wrong way
            dx = self.spaceship.width - dx #Real distance
        if dy > (self.spaceship.height / 2): #If difference is bigger than half the height, it is going the wrong way
            dy = self.spaceship.height - dy #Real distance
        euc_distance = math.sqrt(dx**2 + dy**2)

        return euc_distance

    def direction(self, other): #Find the direction between the spaceship and asteroid
        line = MySpaceObject(self.spaceship.x, self.spaceship.y, 900, 600, self.spaceship.angle, "spaceship", 1) #Creating a query point as a line representation
        line.move_forward() #Move the query point forward to create a line
        return ((other.x - self.spaceship.x) * (line.y - self.spaceship.y) - (other.y - self.spaceship.y) * (line.x - self.spaceship.x)) #Determinant of two vectors with a line representation
    
    def almost_collide(self, other):
        dx = abs(self.spaceship.x - other.x)
        dy = abs(self.spaceship.y - other.y)
        
        if dx > (self.spaceship.width / 2): #If difference is bigger than half the width, it is going the wrong way
            dx = self.spaceship.width - dx #Real distance
        if dy > (self.spaceship.height / 2): #If difference is bigger than half the height, it is going the wrong way
            dy = self.spaceship.height - dy #Real distance
        euc_distance = math.sqrt(dx**2 + dy**2)

        #Check if spaceship collides with asteroid_small
        if (self.spaceship.obj_type == "spaceship" and other.obj_type == "asteroid_small") or (other.obj_type == "spaceship" and self.spaceship.obj_type == "asteroid_small"):
            return euc_distance <= (config.radius[self.spaceship.obj_type] + config.radius[other.obj_type])
        #Check if spaceship collides with asteroid_large
        if (self.spaceship.obj_type == "spaceship" and other.obj_type == "asteroid_large") or (other.obj_type == "spaceship" and self.spaceship.obj_type == "asteroid_large"):
            return euc_distance + 20 <= (config.radius[self.spaceship.obj_type] + config.radius[other.obj_type])

class MySpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.obj_type = obj_type
        self.id = id
        self.radius = config.radius[self.obj_type]

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