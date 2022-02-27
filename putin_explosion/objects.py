import pygame as pg
import random
import math
from settings import *
vec=pg.Vector2

class Firework:
    def __init__(self,pos,radius,color,images):
        self.images = images
        self.main_par=Particle(pos,radius,color,self.images[0])
        self.current=0
        self.faders = [Fader(self.main_par.pos, random.randint(1, self.main_par.radius), self.main_par.color,self.images[-2:]) for i
                       in range(100)]






    def update(self,dt):

        if self.main_par.vel.y>=0 and self.current<1:
            self.faders = [Fader(self.main_par.pos, random.randint(5, self.main_par.radius*2), self.main_par.color,self.images[-2:]) for i
                           in range(100)]
            self.angle = (math.pi * 2) / len(self.faders)
            for n,f in enumerate(self.faders):
                    f.diperse(self.angle*n)
            self.main_par.explosion_coords = self.main_par.pos
            self.bloodstainimg=random.choice(self.images[1:3])
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
            self.main_par.vel.y -= random.randint(5, 14)
            self.main_par.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.main_par.explosion_coords=vec(0,0)


    def draw(self,surf):
        # if self.current == 1:
        #     image=self.bloodstainimg.copy()
        #
        #
        #     surf.blit(image, (self.main_par.explosion_coords.x-image.get_width()//2,self.main_par.explosion_coords.y-image.get_height()//2))
        if self.current==0:
            self.main_par.show(surf)
        elif self.current==1:
            for f in self.faders:
                f.show(surf)


class Particle:
    def __init__(self,pos,radius,color,image):
        self.pos=vec(pos)
        self.radius=radius
        self.acc=vec(0,0)
        self.vel=vec(0,0)
        self.color=color
        self.image=image
        self.explosion_coords=vec(0,0)






    def update(self,dt):

        self.acc = vec(0, 10 * dt)
        self.acc.x += self.vel.x * -dt
        self.vel += self.acc
        self.pos+=self.vel


    def reset(self):
        self.vel=vec(0,0)
        self.pos=vec(random.randint(0,WIDTH),random.randint(HEIGHT-50,HEIGHT))


    def show(self,surf):
        image=pg.transform.scale(self.image,(int(self.image.get_width()*0.2),int(self.image.get_height()*0.2)))
        rect=image.get_rect()
        rect.center = self.pos
        surf.blit(image,rect)
        #pg.draw.circle(surf,self.color,self.pos,self.radius)


class Fader(Particle):
    def __init__(self,pos,radius,color,images):
        super().__init__(pos,radius,color,None)
        self.pos=vec(pos)
        self.color=color
        self.images=images
        choises=[self.images[1]]*20+[self.images[0]]
        self.choise=random.randint(0,len(choises)-1)
        self.image=choises[self.choise]
        self.img_copy=self.image.copy()
        self.angle_intestine_rot=0
    def fade(self):
        self.radius -= abs(self.vel.y) * 0.05
        if self.radius>0 and self.choise<20:

            prop_w=self.radius/self.img_copy.get_width()

            prop_h=self.radius/self.img_copy.get_height()
            image= pg.transform.rotate(self.img_copy, vec(self.vel).angle_to(vec(0, 1)))
            self.image=pg.transform.scale(image,(int(image.get_width()*prop_w),int(image.get_height()*prop_h)))
        elif self.choise==20:
                self.image = pg.transform.rotate(self.img_copy, math.degrees(self.angle_intestine_rot))
    # def rotate_intestine(self):
    #     if self.image!=self.images[1]:
    #         self.image = pg.transform.rotate(self.img_copy,math.degrees(self.angle_intestine_rot))

    def diperse(self,angle):
        
        vec_add = vec(math.cos(angle), math.sin(angle))
        vec_add = vec_add.normalize()
        if angle>0 and angle<3:
            vec_add.scale_to_length(3+random.randint(0,5))
        else:
            vec_add.scale_to_length(5+random.randint(0,5))
        self.vel+=vec_add
    def update(self,dt):
        self.angle_intestine_rot+=0.2

        self.acc = vec(0, 10 * dt)
        self.acc.x += self.vel.x * -dt
        self.vel += self.acc
        self.pos+=self.vel
        self.fade()

    def show(self,surf):
        image=pg.transform.scale(self.image,(int(self.image.get_width()),int(self.image.get_height())))
        rect=image.get_rect()
        rect.center = self.pos
        surf.blit(image,rect)




