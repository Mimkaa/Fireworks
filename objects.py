import pygame as pg
import random
import math
from settings import *
vec=pg.Vector2

class Firework:
    def __init__(self,pos,radius,color):
        self.main_par=Particle(pos,radius,color)
        self.current=0
        self.faders = [Fader(self.main_par.pos, random.randint(1, self.main_par.radius), self.main_par.color) for i
                       in range(100)]






    def update(self,dt):

        if self.main_par.vel.y>=0 and self.current<1:
            self.faders = [Fader(self.main_par.pos, random.randint(5, self.main_par.radius*2), self.main_par.color) for i
                           in range(100)]
            self.angle = (math.pi * 2) / len(self.faders)
            for n,f in enumerate(self.faders):
                    f.diperse(self.angle*n)
            self.main_par.reset()
            self.current+=1



        if self.current==0:
            self.main_par.update(dt)

        elif self.current==1:
            for f in self.faders:
                f.update(dt)

        zeros=[f for f in self.faders if f.radius<=0]
        if len(zeros)==len(self.faders) and self.current==1:
            self.current=0
            self.main_par.vel.x -= random.randint(-5, 5)
            self.main_par.vel.y -= random.randint(5, 17)
            self.main_par.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))


    def draw(self,surf):
        if self.current==0:
            self.main_par.show(surf)
        elif self.current==1:
            for f in self.faders:
                f.show(surf)

class Particle:
    def __init__(self,pos,radius,color):
        self.pos=vec(pos)
        self.radius=radius
        self.acc=vec(0,0)
        self.vel=vec(0,0)
        self.color=color







    def update(self,dt):

        self.acc = vec(0, 10 * dt)
        self.acc.x += self.vel.x * -dt
        self.vel += self.acc
        self.pos+=self.vel


    def reset(self):
        self.vel=vec(0,0)
        self.pos=vec(random.randint(0,WIDTH),random.randint(HEIGHT-50,HEIGHT))


    def show(self,surf):
        pg.draw.circle(surf,self.color,self.pos,self.radius)


class Fader(Particle):
    def __init__(self,pos,radius,color):
        super().__init__(pos,radius,color)
        self.pos=vec(pos)
        self.color=color
    def fade(self):
        self.radius-=abs(self.vel.y)*0.05
    def diperse(self,angle):
        
        vec_add = vec(math.cos(angle), math.sin(angle))
        vec_add = vec_add.normalize()
        if angle>0 and angle<3:
            vec_add.scale_to_length(3+random.randint(0,5))
        else:
            vec_add.scale_to_length(5+random.randint(0,5))
        self.vel+=vec_add
    def update(self,dt):

        self.acc = vec(0, 10 * dt)
        self.acc.x += self.vel.x * -dt
        self.vel += self.acc
        self.pos+=self.vel
        self.fade()


