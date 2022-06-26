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
    def __init__(self,Owner,Angle=0,Speed=5,Img='pistol'):
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
        

class Item:
    def posinit(self):
        self.Actor.midbottom=Blocks[randint(0,len(Blocks)-1)].Actor.midtop
    def __init__(self,Img):
        self.Actor=Actor(Img)
        self.posinit()
        self.Death=0

    def draw(self):
        self.Actor.draw()

class Heal(Item):
    def __init__(self,Img='heal'):
        super().__init__(Img)

    def up(self):
        for i in Grand:
            if self.Actor.colliderect(i.Actor):
                i.takedmg(-2)
                self.Death=1


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
        self.FD=1 #1-left 0-right
        self.Force=[0,0]
        self.posinit()

        self.Gun=Actor('gun')

    def draw(self):
        if self.FD:
            self.Gun.midright=self.Actor.midleft
        else:
            self.Gun.midleft=self.Actor.midright
            
        self.Gun.draw()
        self.Actor.draw()
        screen.draw.text(str(self.HP),self.Actor.topleft,fontsize=15)

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
                self.FD=1
            if keyboard.d:
                self.Force[0]=3
                self.FD=0
        elif self.Team=='blue':
            if keyboard.left:
                self.Force[0]=-3
                self.FD=1
            if keyboard.right:
                self.Force[0]=3
                self.FD=0

    def keydown(self,key):
        if self.Jump and key==Player.TeamsAndKeys[self.Team]:
            for i in Blocks:
                if abs(self.Actor.x-i.Actor.x)<=30 and abs(self.Actor.bottom-i.Actor.top)<=3:
                    break
            else:
                self.Jump-=1
                self.Actor.image+='_d'
            self.Force[1]=-15

        if key==Player.TeamsAndBullets[self.Team]:
            Bullets.append(Bullet(self,self.FD*180))
    
    def takedmg(self,Dmg):
        self.HP-=Dmg
        if Dmg>0 and self.HP<=0:
            self.Death=1
        if Dmg<0 and self.HP>10:
           self.HP=10
 

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
Items=[Heal()]

Winner=''

def additem():
    if len(Items)<5:
        t=Heal()
        w=1
        while w:
            for i in Items:
                if t.Actor.center==i.Actor.center:
                    t.posinit()
                    break
            else:
                w=0
                Items.append(t)
clock.schedule_interval(additem,6)
                

def draw():
    global Grand,Blocks,Bullets,Winner
    screen.fill((180,180,180))
    for i in Blocks+Grand+Items+Bullets:
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
    for i in Items:
        i.up()
        if i.Death:
            Items.remove(i)
            
    if len(Grand)==1:
        Winner=Grand[0].Team

def on_key_down(key):
    global Winner,Grand
    for i in Grand:
        i.keydown(key)
    if Winner and key==keys.RETURN:
        Winner=''
        Bullets=[]
        blockinit()
        playerinit()
    
    
pgzrun.go()
