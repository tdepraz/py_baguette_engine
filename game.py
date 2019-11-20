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

    key_codes = []
    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False
    jump_pressed = False
    jump_prev_pressed = False
    esc_pressed = False
    
    def __init__(self, name = "Game"):
        self.window = Tk()
        self.window.title(name)
        self.window.resizable(0,0)
        
        self.layout = Canvas(self.window, width = 780, height = 780, bg='#c7debc')
        self.layout.pack()
        
        self.window.bind("<ButtonPress-1>", self.mouse1_pressed)
        self.window.bind("<ButtonRelease-1>", self.mouse1_released)
        for i in range(len(self.terrain)):
            self.layout.create_line(0,i*self.TILESIZE,len(self.terrain[0])*self.TILESIZE,i*self.TILESIZE)
        for i in range(len(self.terrain[0])):
            self.layout.create_line(i*self.TILESIZE,0,i*self.TILESIZE,len(self.terrain)*self.TILESIZE)
        
        
    def mainloop(self):
        prev_time = time()
        update_time = 0.0
        while self.running:
            delta = time() - prev_time
            update_time += delta
            prev_time = time()
            if delta > 0.0 and not self.paused:
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
        for obj in self.objects:
            del obj
        self.window.destroy

    def mouse1_pressed(self, evt):
        self.player_object = Player(evt.x,evt.y)
        self.objects.append(self.player_object)
        print("clicked at ", evt.x, evt.y)
    
    def mouse1_released(self, evt):
        pass

class Player:
    GRAVITY = 1.0              # px/s/s
    MAX_SPEED = 2.0          # px/s
    MAX_FALL_SPEED = -2.0      # px/s
    ACCEL = 1.0               # px/s/s
    DECCEL = 1.0              # px/s/s
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
        if self.vel[1] > self.MAX_FALL_SPEED:
            self.vel[1] -= self.GRAVITY * delta
        
        self.vel = self.move_and_slide(self.vel)
        self.update_pos()

    def move_and_slide(self, vel):
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
                self.pos[1] = self.tile[1]*Game.TILESIZE + 
                vel[1] = 0.0
        if (self.pos[1]+self.hitbox[1]+vel[1])//Game.TILESIZE >= self.tile[0]:
            if self.get_tilemap_collision("y",1, Game.terrain):
                self.pos[1] = self.tile[1]*Game.TILESIZE
                vel[1] = 0.0
        return vel
    
    def update_pos(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.tile[0] = (self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE
        self.tile[1] = (self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE
        Game.layout.coords(self.sprite, self.pos[0], self.pos[1], self.pos[0]+self.hitbox[0], self.pos[1]+self.hitbox[1])
        Game.layout.coords(self.pos_img, self.pos[0]-2, self.pos[1]-2, self.pos[0]+2, self.pos[1]+2)
        Game.layout.coords(self.tile_img, self.tile[0]*Game.TILESIZE-2, self.tile[1]*Game.TILESIZE-2, self.tile[0]*Game.TILESIZE+2, self.tile[1]*Game.TILESIZE+2)

    def get_tilemap_collision(self, axis, dir, tilemap):
        col = False
        try:
            if axis == "x":
                col = (tilemap[int((self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE + dir)][int(self.pos[1]//Game.TILESIZE)] > 0) or (tilemap[int((self.pos[0]+self.hitbox[0]/2)//Game.TILESIZE + dir)][int((self.pos[1]+self.hitbox[1])//Game.TILESIZE)] > 0)
            elif axis == "y":
                col = (tilemap[int(self.pos[0]//Game.TILESIZE)][int((self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE + dir)] > 0) or (tilemap[int((self.pos[0]+self.hitbox[0])//Game.TILESIZE)][int((self.pos[1]+self.hitbox[1]/2)//Game.TILESIZE + dir)] > 0)
        except:
            self.exists = False
        return col

Game = GameApp()
Game.mainloop()
del Game