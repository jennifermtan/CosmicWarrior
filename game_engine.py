import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def import_state(self, game_state_filename):
        try:
            f = open(game_state_filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open {}".format(game_state_filename))
        
        fixed_game_variables = ["width", "height", "score", "spaceship", "fuel"]
        
       #Loop through the first 5 lines of game_state_file to check if there is "width", "height", "score", "spaceship", "fuel"
        line_num = 0
        i = 0
        while i < 5: 
            line = f.readline()
            line_num += 1
            if line == "\n": #If line is empty, skip it
                continue
            elif line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")

            word = line.split()[0]
            if len(line.split()) != 2: #Check if fixed game variable has a value pair
                raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != fixed_game_variables[i]: #Check if word is the expected key from fixed_game_variables
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))

            value = line.split()[1]
            if word == "spaceship": #Check if spaceship values is float, float, int, int
                value = value.split(",")
                for j in range(0, 2):
                    if not (value[j].isnumeric() == False and "." in value[j]): #Check if the first two values is a float
                        raise ValueError("Error: invalid data type in line {}".format(line_num))
                for j in range(2, 4):
                    if value[j].isnumeric() == False: #Check if the last two values is a int
                        raise ValueError("Error: invalid data type in line {}".format(line_num))
            else:
                if value.isnumeric() == False: #Check if the other fixed game variable value is an int
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            
            if word == "width":
                self.width = int(value)
            elif word == "height":
                self.height = int(value)
            elif word == "score":
                self.score = int(value)
            elif word == "fuel":
                self.ori_fuel = int(value) #Set original fuel value
                self.fuel = int(value)
            elif word == "spaceship":
                self.spaceship = SpaceObject(float(value[0]), float(value[1]), self.width, self.height, int(value[2]), word, int(value[3]))
   
            i += 1

        while True:
            asteroids_count_line = f.readline()
            line_num += 1 
            if asteroids_count_line == "\n": #If line is empty, skip it
                continue
            elif asteroids_count_line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")
            
            word = asteroids_count_line.split()[0]
            if len(asteroids_count_line.split()) != 2: #Check if asteroids_count has a value pair
                    raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "asteroids_count": #Check for asteroids_count
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))

            value = asteroids_count_line.split()[1]
            if value.isnumeric() == False: #Check if asteroids_count value is an int
                raise ValueError("Error: invalid data type in line {}".format(line_num))
            self.asteroids_count = int(value)
            break

        #Loop the number of asteroids_count to check for asteroids
        self.asteroids_ls = [] #Store the asteroids in a list
        i = 0 
        while i < int(self.asteroids_count):
            line = f.readline()
            line_num += 1
            if line == "\n": #If line is empty, skip it
                continue
            elif line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")
            
            word = line.split()[0]
            if len(line.split()) != 2: #Check if asteroid has a value pair
                raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "asteroid_large" and word != "asteroid_small": #Check if key is asteroid_large or asteroid_small
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))
        
            value = line.split()[1]
            value = value.split(",")
            for j in range(0, 2):
                if not (value[j].isnumeric() == False and "." in value[j]): #Check if the first two values is a float
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            for j in range(2, 4):
                if value[j].isnumeric() == False: #Check if the last two values is an int
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            asteroid = SpaceObject(float(value[0]), float(value[1]), self.width, self.height, int(value[2]), word, int(value[3]))
            self.asteroids_ls.append(asteroid)
            i += 1

        while True:
            bullets_count_line = f.readline()
            line_num += 1
            if bullets_count_line == "\n": #If line is empty, skip it
                continue
            elif bullets_count_line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")
            
            word = bullets_count_line.split()[0]
            if len(bullets_count_line.split()) != 2: #Check if bullets_count has a value pair
                    raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "bullets_count": #Check for bullets_count
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))

            value = bullets_count_line.split()[1]
            if value.isnumeric() == False: #Check if bullets_count value is an int
                raise ValueError("Error: invalid data type in line {}".format(line_num))
            self.bullets_count = int(value)
            self.bullets_move_count = [0 for x in range (self.bullets_count)] #Set initial move count for each bullet
            break

        #Loop the number of bullets_count to check for bullets
        i = 0
        self.bullets_ls = [] #Store the bullets in a list
        while i < int(self.bullets_count):
            line = f.readline()
            line_num += 1
            if line == "\n": #If line is empty, skip it
                continue
            elif line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")

            word = line.split()[0]
            if len(line.split()) != 2: #Check if bullet has a value pair
                raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "bullet": #Check if key is bullet
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))

            value = line.split()[1]
            value = value.split(",")
            for j in range(0, 2):
                if not (value[j].isnumeric() == False and "." in value[j]): #Check if the first two values is a float
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            for j in range(2, 4):
                if value[j].isnumeric() == False: #Check if the last two values is an int
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            bullet = SpaceObject(float(value[0]), float(value[1]), self.width, self.height, int(value[2]), word, int(value[3]))
            self.bullets_ls.append(bullet)
            i += 1

        while True:
            upcoming_asteroids_line = f.readline()
            line_num += 1
            if upcoming_asteroids_line == "\n": #If line is empty, skip it
                continue
            elif upcoming_asteroids_line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")
            
            word = upcoming_asteroids_line.split()[0]
            if len(upcoming_asteroids_line.split()) != 2: #Check if upcoming_asteroids_count has a value pair
                    raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "upcoming_asteroids_count": #Check for upcoming_asteroids_count
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))
            
            value = upcoming_asteroids_line.split()[1]
            if value.isnumeric() == False: #Check if upcoming_asteroids_count value is an int
                raise ValueError("Error: invalid data type in line {}".format(line_num))
            self.upcoming_asteroids_count = int(value)
            break

        #Loop the number of upcoming_asteroids to check for upcoming asteroids
        i = 0
        self.upcoming_asteroids_ls = [] #Store the upcoming asteroids in a list
        while i < int(self.upcoming_asteroids_count):
            line = f.readline()
            line_num += 1
            if line == "\n": #If line is empty, skip it
                continue
            elif line == "": #If reach end of file without all variables, file is incomplete
                raise ValueError("Error: game state incomplete")

            word = line.split()[0]
            if len(line.split()) != 2: #Check if upcoming_asteroid has a value pair
                raise ValueError("Error: expecting a key and value in line {}".format(line_num))
            if word != "upcoming_asteroid_large" and word != "upcoming_asteroid_small": #Check if key is upcoming_asteroid_large or upcoming_asteroid_small
                raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))
            
            value = line.split()[1]
            value = value.split(",")
            for j in range(0, 2):
                if not (value[j].isnumeric() == False and "." in value[j]): #Check if the first two values is a float
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            for j in range(2, 4):
                if value[j].isnumeric() == False: #Check if the last two values is an int
                    raise ValueError("Error: invalid data type in line {}".format(line_num))
            obj_type_upcoming = word[9:]
            upcoming_asteroids = SpaceObject(float(value[0]), float(value[1]), self.width, self.height, int(value[2]), obj_type_upcoming, int(value[3]))
            self.upcoming_asteroids_ls.append(upcoming_asteroids)
            i += 1

        #Raise unexpected key if the file still has lines when it's supposed to end
        if f.readline() != "":
            line_num += 1
            raise ValueError("Error: unexpected key: {} in line {}".format(word, line_num))

        f.close()

    def export_state(self, game_state_filename):
        f = open(game_state_filename, "w")
        f.write("width {}\n".format(self.width)) #Width
        f.write("height {}\n".format(self.height)) #Height
        f.write("score {}\n".format(self.score)) #Score
        f.write(str(self.spaceship) + "\n") #Spaceship
        f.write("fuel {}\n".format(self.fuel))
        f.write("asteroids_count {}\n".format(len(self.asteroids_ls)))

        i = 0
        while i < len(self.asteroids_ls):
            f.write(str(self.asteroids_ls[i]) + "\n")
            i += 1
        
        f.write("bullets_count {}\n".format(len(self.bullets_ls)))

        i = 0
        while i < len(self.bullets_ls):
            f.write(str(self.bullets_ls[i]) + "\n")
            i += 1
        
        self.upcoming_asteroids_ls
        f.write("upcoming_asteroids_count {}\n".format(len(self.upcoming_asteroids_ls)))
        i = 0
        while i < len(self.upcoming_asteroids_ls):
            if "upcoming_" not in self.upcoming_asteroids_ls[i].obj_type:
                self.upcoming_asteroids_ls[i].obj_type = "upcoming_" + self.upcoming_asteroids_ls[i].obj_type
            f.write(str(self.upcoming_asteroids_ls[i]) + "\n")
            i += 1
        
        f.close()

    def run_game(self):
        self.id = 0 #Set bullet id
        fuel_warning_count = [True, True, True] #Set fuel warning if it has been printed

        while True:
            # 1. Receive player input
            player_input = self.player.action(self.spaceship, self.asteroids_ls, self.bullets_ls, self.fuel, self.score)
            
            # 2. Process game logic
            #Manoeuvre the spaceship as per the Player's input
            if player_input[1] == True: #Counterclockwise rotation (turn left)
                self.spaceship.turn_left()
            if player_input[2] == True: #Clockwise rotation (turn right)
                self.spaceship.turn_right()
            if player_input[0] == True: #Main thruster (move forward)
                self.spaceship.move_forward()
            
            #Update positions of asteroids by calling move_forward() for each asteroid
            i = 0
            while i < len(self.asteroids_ls):
                self.asteroids_ls[i].move_forward()
                i += 1
            
            #Launch new bullet
            if player_input[3] == True: #Fire bullet
                if self.fuel < config.shoot_fuel_threshold: #If fuel is less than the minimum fuel to shoot bullet constant, do not launch the bullet
                    print("Cannot shoot due to low fuel")
                else:
                    bullet = SpaceObject(self.spaceship.x, self.spaceship.y, self.width, self.height, self.spaceship.angle, "bullet", self.id) #Launch a new bullet
                    self.fuel -= config.bullet_fuel_consumption #Deduct fuel if bullet is launched
                    self.id += 1 #Increase unique ID of bullet
                    self.bullets_ls.append(bullet)
                    self.bullets_move_count.append(0)

            #Remove expired bullets
            i = 0
            while i < len(self.bullets_ls):
                if self.bullets_move_count[i] == config.bullet_move_count:
                    del self.bullets_ls[i]
                    del self.bullets_move_count[i]
                    i -= 1
                i += 1
                
            #Update positions of bullets
            i = 0
            while i < len(self.bullets_ls): #Update positions of bullets on map
                self.bullets_ls[i].move_forward()
                self.bullets_move_count[i] += 1
                i += 1
            
            #Deduct fuel for spaceship
            self.fuel -= config.spaceship_fuel_consumption


            #Print fuel warning threholds
            fuel_per = (self.fuel / self.ori_fuel) * 100 #Fuel percentage
            if fuel_per <= config.fuel_warning_threshold[2] and fuel_warning_count[2]:
                print("{}% fuel warning: {} remaining".format(config.fuel_warning_threshold[2], self.fuel))
                fuel_warning_count[2] = False
            elif fuel_per <= config.fuel_warning_threshold[1] and fuel_warning_count[1]:
                print("{}% fuel warning: {} remaining".format(config.fuel_warning_threshold[1], self.fuel))
                fuel_warning_count[1] = False
            elif fuel_per <= config.fuel_warning_threshold[0] and fuel_warning_count[0]:
                print("{}% fuel warning: {} remaining".format(config.fuel_warning_threshold[0], self.fuel))
                fuel_warning_count[0] = False

            #Detect collisions
            #Small asteroids and bullets
            i = 0
            collide = False
            while i < len(self.asteroids_ls):
                j = 0
                while j < len(self.bullets_ls):
                    if self.asteroids_ls[i].collide_with(self.bullets_ls[j]) == True:
                        if self.asteroids_ls[i].obj_type == "asteroid_small": #Bullet with small asteroid
                            self.score += config.shoot_small_ast_score
                            print("Score: {} \t [Bullet {} has shot asteroid {}]".format(self.score, self.bullets_ls[j].id, self.asteroids_ls[i].id))
                        elif self.asteroids_ls[i].obj_type == "asteroid_large": #Bullet with large asteroid
                            self.score += config.shoot_large_ast_score
                            print("Score: {} \t [Bullet {} has shot asteroid {}]".format(self.score, self.bullets_ls[j].id, self.asteroids_ls[i].id))
                        del self.asteroids_ls[i]
                        del self.bullets_ls[j]
                        del self.bullets_move_count[j]
                        i -= 1
                        j -= 1
                        collide = True
                    j += 1
                i += 1

            #Spaceship and asteroid
            i = 0
            while i < len(self.asteroids_ls):
                if self.spaceship.collide_with(self.asteroids_ls[i]): #Spaceship and asteroid
                    self.score += config.collide_score
                    print("Score: {} \t [Spaceship collided with asteroid {}]".format(self.score, self.asteroids_ls[i].id))
                    del self.asteroids_ls[i]
                    collide = True
                    i -= 1
                i += 1
            
            #Replenish asteroids using the first available asteroid from upcoming asteroids
            if collide == True and 0 < len(self.upcoming_asteroids_ls): 
                self.asteroids_ls.append(self.upcoming_asteroids_ls[0])
                print("Added asteroid {}".format(self.upcoming_asteroids_ls[0].id))
                del self.upcoming_asteroids_ls[0]

            # 3. Draw the game state on screen using the GUI class
            self.GUI.update_frame(self.spaceship, self.asteroids_ls, self.bullets_ls, self.score, self.fuel)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            if self.fuel == 0:
                break
            # - no more asteroids are available
            if len(self.upcoming_asteroids_ls) == 0:
                print("Error: no more asteroids available")
                break

        # Display final score
        self.GUI.finish(self.score)

    # You can add additional methods if required