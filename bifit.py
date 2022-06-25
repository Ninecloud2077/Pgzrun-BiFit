import pgzrun
from random import randint

WIDTH,HEIGHT=1000,400

class Block:
    def __init__(self):
        self.Actor=Actor('block')
        self.Actor.x=randint(self.Actor.width,WIDTH-self.Actor.width)
        self.Actor.y=randint(self.Actor.height,HEIGHT-self.Actor.height)

    def draw(self):
        self.Actor.draw()

class Bullet:
    def __init__(self,Owner,Img='pistol',Angle=0,Speed=3):
        self.Actor=Actor(Img,Owner.Actor.center)
        self.Actor.angle=Angle
        self.Team=Owner.Team
        self.Speed=Speed
        self.Death=0

    def draw(self):
        self.Actor.draw()

    def up(self):
        if self.Actor.angle==0:
            self.Actor.x+=self.Speed
        else:
            self.Actor.x-=self.Speed

        if self.Actor.x<0 or self.Actor.x>WIDTH:
            self.Death=1
            return
        for i in Grand:
            if self.Team!=i.Team and self.Actor.colliderect(i.Actor):
                i.takedmg(1)
                self.Death=1
                return
        for i in Blocks:
            if self.Actor.colliderect(i.Actor):
                self.Death=1
                return
        

class Player:
    TeamsAndKeys={'red':keys.W, 'blue':keys.UP}
    TeamsAndBullets={'red':keys.SPACE, 'blue':keys.KP_ENTER}
    def posinit(self):
        self.Actor.midbottom=Blocks[randint(0,len(Blocks)-1)].Actor.midtop
    def __init__(self,Team='red'):
        self.Team=Team
        self.Actor=Actor(Team)
        self.HP=10
        self.Death=0
        self.Jump=1
        self.Force=[0,0]
        self.posinit()

    def up(self):
        self.move()
        self.keyup()
        self.collide()

    def collide(self):
        for i in Grand:
            if i.Team!=self.Team and self.Actor.colliderect(i.Actor):
                    if self.Actor.x<=i.Actor.x:
                        self.Actor.x-=10
                    else:
                        self.Actor.x+=10
                    break
        
    def draw(self):
        self.Actor.draw()
        screen.draw.text(str(self.HP),self.Actor.topleft,fontsize=15)
        
    def move(self):
        for i in Blocks:
            if self.Actor.colliderect(i.Actor) and self.Actor.bottom<=i.Actor.bottom:
                if self.Force[1]>=0:
                    self.Force[1]=0
                    self.Actor.bottom=i.Actor.top
                    self.Jump=1
                    if '_d' in self.Actor.image:
                        self.Actor.image=self.Actor.image[:-2]
                break
        else:
            self.Force[1]+=0.65
            
        if self.Force[0]:
            self.Actor.x+=self.Force[0]
            if self.Force[0]>0:
                self.Force[0]-=0.5
            else:
                self.Force[0]+=0.5
        if self.Force[1]:
            self.Actor.y+=self.Force[1]
            if self.Force[1]>0:
                self.Force[1]-=0.5
            else:
                self.Force[1]+=0.5

        if self.Actor.left<0:
            self.Force[0]=0
            self.Actor.left=0
        if self.Actor.right>WIDTH:
            self.Force[0]=0
            self.Actor.right=WIDTH
        if self.Actor.top<0:
            self.Force[1]=0
            self.Actor.top=0
        if self.Actor.bottom>HEIGHT:
            self.Force=[0,0]
            self.posinit()
        
    def keyup(self):
        if self.Team=='red':
            if keyboard.a:
                self.Force[0]=-3
            if keyboard.d:
                self.Force[0]=3
        elif self.Team=='blue':
            if keyboard.left:
                self.Force[0]=-3
            if keyboard.right:
                self.Force[0]=3

    def keydown(self,key):
        if self.Jump and key==Player.TeamsAndKeys[self.Team]:
            self.Force[1]=-15
            for i in Blocks:
                if self.Actor.bottom==i.Actor.top:
                    break
            else:
                self.Jump-=1
                self.Actor.image+='_d'

        if key==Player.TeamsAndBullets[self.Team]:
            Bullets.append(Bullet(self))
    
    def takedmg(self,Dmg):
        self.HP-=Dmg
        if self.HP<=0:
            self.Death=1
            


Blocks=[]
def blockinit():
    global Blocks
    Blocks=[]
    while len(Blocks)<20:
        b=Block()
        for i in Blocks:
            if b.Actor.colliderect(i.Actor):
                break
        else:
            Blocks.append(b)
blockinit()
           
Grand=[]
def playerinit():
    global Grand
    Grand=[Player('red'),Player('blue')]
playerinit()

Bullets=[]

Winner=''

def draw():
    global Grand,Blocks,Bullets,Winner
    screen.fill((180,180,180))
    for i in Grand+Blocks+Bullets:
        i.draw()
    if Winner:
        screen.draw.text(Winner+' wins!',(WIDTH*0.25,HEIGHT*0.25),color='yellow',fontsize=175)
        screen.draw.text('Main_Enter to Restart',(WIDTH*0.25,HEIGHT*0.5),color='yellow',fontsize=80)

def update():
    global Winner,Grand
    for i in Grand:
        i.up()
        if i.Death:
            Grand.remove(i)
    for i in Bullets:
        i.up()
        if i.Death:
            Bullets.remove(i)
    if len(Grand)==1:
        Winner=Grand[0].Team

def on_key_down(key):
    global Winner,Grand
    for i in Grand:
        i.keydown(key)
    if Winner and key==keys.RETURN:
        Winner=''
        playerinit()
        blockinit()

    
pgzrun.go()