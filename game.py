from tkinter import *
from time import time

class GameApp:
    TILESIZE = 32
    terrain = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    objects = []
    player_object = None
    time_scale = 1.0
    running = True
    paused = False

    key_codes = [
        [81],   # Left
        [68],   # Right
        [83],   # Down
        [32],   # Jump
        [13],   # Enter
        [27]    # Esc
    ]
    left_pressed = False
    right_pressed = False
    down_pressed = False
    jump_pressed = False
    
    def __init__(self, name = "Game"):
        self.window = Tk()
        self.window.title(name)
        self.window.resizable(0,0)
        
        self.layout = Canvas(self.window, width = 780, height = 780, bg='#c7debc')
        self.layout.pack()
        
        self.window.bind("<ButtonPress-1>", self.mouse1_pressed)
        self.window.bind("<ButtonRelease-1>", self.mouse1_released)
        self.window.bind("<Key>", self.key_pressed)
        self.window.bind("<KeyRelease>", self.key_released)
        for i in range(len(self.terrain)):
            self.layout.create_line(0,i*self.TILESIZE,len(self.terrain[0])*self.TILESIZE,i*self.TILESIZE)
        for i in range(len(self.terrain[0])):
            self.layout.create_line(i*self.TILESIZE,0,i*self.TILESIZE,len(self.terrain)*self.TILESIZE)
        
        
    def mainloop(self):
        delta = 0.0
        while self.running:
            prev_time = time()
            if not self.paused:
                for obj in self.objects:
                    try:
                        obj._update(delta*self.time_scale)
                        if not obj.exists:
                            del obj
                    except:
                        del obj
            try:
                self.layout.update()
            except:
                self.running = False
            delta = time() - prev_time
        for obj in self.objects:
            del obj
        self.window.destroy
    
    def create_player(self):
        if self.player_object is None:
            self.player_object = Player(80,80)
            self.objects.append(self.player_object)

    def mouse1_pressed(self, evt):
        print("clicked at ", evt.x, evt.y)
    def mouse1_released(self, evt):
        pass

    def key_pressed(self, evt):
        if evt.keycode in self.key_codes[0]:
            self.left_pressed = True
        if evt.keycode in self.key_codes[1]:
            self.right_pressed = True
        if evt.keycode in self.key_codes[2]:
            self.down_pressed = True
        if evt.keycode in self.key_codes[3]:
            self.jump_pressed = True
        if evt.keycode in self.key_codes[4]:
            self.create_player()
        if evt.keycode in self.key_codes[5]:
            self.running = False
    
    def key_released(self, evt):
        if evt.keycode in self.key_codes[0]:
            self.left_pressed = False
        if evt.keycode in self.key_codes[1]:
            self.right_pressed = False
        if evt.keycode in self.key_codes[2]:
            self.down_pressed = False
        if evt.keycode in self.key_codes[3]:
            self.jump_pressed = False

class Player:
    GRAVITY = 1.0              # px/s/s
    MAX_SPEED = 12.0          # px/s
    MAX_FALL_SPEED = 9.0      # px/s
    ACCEL = 1.0               # px/s/s
    DECCEL = 5.0              # px/s/s
    MAX_AIR_TIME = 0.7          # s
    
    pos = [0,0]
    tile = [0,0]
    vel = [0,0]
    hitbox = [20,20]
    air_time = 0.0
    prev_jumped = False

    sprite = None
    pos_img = None
    tile_img = None
    exists = True
    
    def __init__(self, start_x, start_y):
        self.tile[0] = (start_x + self.hitbox[0]/2) // Game.TILESIZE
        self.tile[1] = (start_y + self.hitbox[1]/2) // Game.TILESIZE
        self.pos[0] = start_x
        self.pos[1] = start_y
        self.sprite = Game.layout.create_rectangle(0,0,0,0, fill="blue")
        self.pos_img = Game.layout.create_oval(0,0,0,0, fill="red")
        self.tile_img = Game.layout.create_oval(0,0,0,0, fill="green")

    def _update(self, delta):
        if self.vel[1] < self.MAX_FALL_SPEED:
            self.vel[1] += self.GRAVITY * delta

        if Game.left_pressed and self.vel[0] > -self.MAX_SPEED:
            self.vel[0] -= self.ACCEL * delta
        if Game.right_pressed and self.vel[0] < self.MAX_SPEED:
            self.vel[0] += self.ACCEL * delta
        if not (Game.right_pressed or Game.left_pressed):
            if self.vel[0] > 0.0:
                self.vel[0] -= self.DECCEL * delta
            elif self.vel[0] < 0.0:
                self.vel[0] += self.DECCEL * delta
            else:
                self.vel[0] = 0.0

        move_vel = self.move_and_slide(self.vel, delta)
        self.update_pos(move_vel)

    def move_and_slide(self, velocity, delta):
        vel = [0,0]
        vel[0] = velocity[0]
        vel[1] = velocity[1]
        if (self.pos[0]+vel[0])//Game.TILESIZE <= self.tile[0]:
            if self.get_tilemap_collision("x",-1, Game.terrain):
                self.pos[0] = self.tile[0]*Game.TILESIZE
                vel[0] = 0.0
        if (self.pos[0]+self.hitbox[0]+vel[0])//Game.TILESIZE >= self.tile[0]:
            if self.get_tilemap_collision("x",1, Game.terrain):
                self.pos[0] = self.tile[0]*Game.TILESIZE
                vel[0] = 0.0
        if (self.pos[1]+vel[1])//Game.TILESIZE <= self.tile[1]:
            if self.get_tilemap_collision("y",-1, Game.terrain):
                self.pos[1] = self.tile[1]*Game.TILESIZE
                vel[1] = 0.0
        if (self.pos[1]+self.hitbox[1]+vel[1])//Game.TILESIZE >= self.tile[0]:
            if self.get_tilemap_collision("y",1, Game.terrain):
                self.pos[1] = self.tile[1]*Game.TILESIZE
                vel[1] = 0.0
        self.pos[0] += vel[0]
        self.pos[1] += vel[1]
        return vel
    
    def update_pos(self, vel):
        self.tile[0] = (self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE
        self.tile[1] = (self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE
        Game.layout.coords(self.sprite, self.pos[0], self.pos[1], self.pos[0]+self.hitbox[0], self.pos[1]+self.hitbox[1])
        Game.layout.coords(self.pos_img, self.pos[0]-2, self.pos[1]-2, self.pos[0]+2, self.pos[1]+2)
        Game.layout.coords(self.tile_img, self.tile[0]*Game.TILESIZE-2, self.tile[1]*Game.TILESIZE-2, self.tile[0]*Game.TILESIZE+2, self.tile[1]*Game.TILESIZE+2)

    def get_tilemap_collision(self, axis, dir, tilemap):
        col = False
        try:
            if axis == "x":
                col = (tilemap[int((self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE)][int(self.pos[1]//Game.TILESIZE + dir)] > 0) or (tilemap[int((self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE)][int((self.pos[1]+self.hitbox[1])//Game.TILESIZE + dir)] > 0)
            elif axis == "y":
                col = (tilemap[int(self.pos[0]//Game.TILESIZE + dir)][int((self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE)] > 0) or (tilemap[int((self.pos[0]+self.hitbox[0])//Game.TILESIZE + dir)][int((self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE)] > 0)
        except:
            self.exists = False
        return col

Game = GameApp()
Game.mainloop()
del Game