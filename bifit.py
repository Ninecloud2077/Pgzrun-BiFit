import pgzrun
from random import randint,choice

WIDTH,HEIGHT=1000,400

class Block:
    def __init__(self):
        self.Actor=Actor('block')
        self.Actor.x=randint(self.Actor.width,WIDTH-self.Actor.width)
        self.Actor.y=randint(self.Actor.height,HEIGHT-self.Actor.height)

    def draw(self):
        self.Actor.draw()


class Power:
    def __init__(self,Owner,SRadius,Speed=1,Dmg=0,Force=0,Freeze=0,Color=(0,0,0)):
        self.Owner=Owner
        self.Pos=self.Owner.Actor.center
        self.Team=self.Owner.Team
        self.Radius=0
        self.SRadius=SRadius
        self.Speed=Speed
        self.Dmg=Dmg
        self.Attacked=[]
        self.Force=Force
        self.Freeze=Freeze
        self.Color=Color
        self.Death=0

    def draw(self):
        screen.draw.circle(self.Pos,self.Radius,self.Color)

    def up(self):
        self.Radius+=self.Speed
        if self.Radius>=self.SRadius:
            self.Death=1
            return
        self.collide()

    def collide(self):
        for i in Grand:
            if i not in self.Attacked and i.Team!=self.Owner.Team and i.Actor.distance_to(self.Pos)<=self.Radius:
                i.takedmg(self.Dmg)
                self.force(i)
                if self.Freeze:
                    i.SK['Freeze']+=self.Freeze
                self.Attacked.append(i)

    def force(self,i):
        if self.Pos[0]<i.Actor.x:
            i.Force[0]+=self.Force
        elif self.Pos[0]>i.Actor.x:
            i.Force[0]-=self.Force

        if self.Pos[1]<=i.Actor.y:
            i.Force[1]+=self.Force
        else:
            i.Force[1]-=self.Force


class Pull(Power):
    def __init__(self, Owner, SRadius, Speed=1, Dmg=0, Force=0, Freeze=0, Color=(0, 0, 0)):
        super().__init__(Owner, SRadius, Speed, Dmg, Force, Freeze, Color)
        self.Radius=self.SRadius
    
    def up(self):
        self.Radius-=1
        if not self.Radius:
            self.Death=1
            return
        self.collide()

    def force(self,i):
        if self.Pos[0]<i.Actor.x:
            i.Force[0]-=self.Force
        elif self.Pos[0]>i.Actor.x:
            i.Force[0]+=self.Force

        if self.Pos[1]<=i.Actor.y:
            i.Force[1]-=self.Force
        else:
            i.Force[1]+=self.Force


class BIF:
    def __init__(self,Owner,Img='bif',Radius=200,Speed=3,Force=12,Wait=90,LifeTime=450):
        self.Actor=Actor(Img)
        self.Actor.center=Owner.Actor.center
        self.Owner=Owner
        self.Team=Owner.Team
        self.Radius=Radius
        self.Speed=Speed
        self.Force=12
        self.Wait=Wait
        self.LifeTime=LifeTime
        self.Tick=0
        self.Death=0

    def draw(self):
        self.Actor.draw()

    def up(self):
        self.Tick+=1
        if self.Tick%self.Wait==0:
            Bullets.append(Power(Owner=self,SRadius=self.Radius,Force=self.Force,Speed=self.Speed,Color=(255,212,56)))
        if self.Tick==self.LifeTime:
            self.Death=1
            return
        

class FIT(BIF):
    def __init__(self, Owner, Img='fit', Radius=200, Speed=5, Force=12, Wait=90, LifeTime=450):
        super().__init__(Owner, Img, Radius, Speed, Force, Wait, LifeTime)
    
    def up(self):
        self.Tick+=1
        if self.Tick%self.Wait==0:
            Bullets.append(Pull(Owner=self,SRadius=self.Radius,Force=self.Force,Speed=self.Speed,Color=(13,225,162)))
        if self.Tick==self.LifeTime:
            self.Death=1
            return


class Bullet:
    def __init__(self,Owner,Angle=0,Dmg=1,Speed=5,Img='pistol'):
        self.Actor=Actor(Img,Owner.Actor.center)
        self.Actor.angle=Angle
        self.Dmg=Dmg
        self.Team=Owner.Team
        self.Speed=Speed
        self.Death=0

    def draw(self):
        self.Actor.draw()

    def move(self):
        if self.Actor.angle==0:
            self.Actor.x+=self.Speed
        else:
            self.Actor.x-=self.Speed
        if self.Actor.x<0 or self.Actor.x>WIDTH:
            self.Death=1

    def collide(self):
        for i in Grand:
            if self.Team!=i.Team and self.Actor.colliderect(i.Actor):
                i.takedmg(self.Dmg)
                self.Death=1
                break

    def block(self):
        for i in Blocks:
            if self.Actor.colliderect(i.Actor):
                self.Death=1
                break        
    
    def up(self):
        self.move()
        self.block()
        self.collide()


class IceRocket(Bullet):
    def __init__(self,Owner,Dmg=2,Angle=90,Speed=7,Wait=45,Img='icerocket'):
        super().__init__(Owner,Angle,Dmg,Speed,Img)

        self.Wait=Wait
        
        self.Target=randenemy(self.Team).Actor.x

    def move(self):
        if self.Actor.angle==90:
            self.Actor.y-=self.Speed
            if self.Actor.bottom<=0:
                self.Actor.angle=0
                self.Actor.x=self.Target
            
        elif self.Actor.angle==-90:
            self.Actor.y+=self.Speed

        elif self.Actor.angle==0:
            self.Wait-=1
            if not self.Wait:
                self.Actor.angle=-90

    def block(self):
        if self.Actor.angle!=-90:
            return
        super().block()
        
    def up(self):
        super().up()
        if self.Death:
            Bullets.append(Power(Owner=self,SRadius=100,Speed=3,Dmg=self.Dmg,Force=10,Freeze=60,Color=(63,133,255)))

class DJ:
    def __init__(self,Pos,Img='dj',Speed=5,Lifetime=6):
        self.Actor=Actor(Img,Pos)
        self.Speed=Speed
        self.Lifetime=Lifetime
        self.Death=0
    
    def draw(self):
        self.Actor.draw()
    
    def up(self):
        self.Actor.y+=self.Speed
        self.Lifetime-=1
        if not self.Lifetime:
            self.Death=1
            return


class Item:
    def posinit(self):
        self.Actor.midbottom=Blocks[randint(0,len(Blocks)-1)].Actor.midtop
    def __init__(self,Img='empty'):
        self.Actor=Actor(Img)
        self.posinit()
        self.Death=0

    def draw(self):
        self.Actor.draw()

    def up(self):
        for i in Grand:
            if self.Actor.colliderect(i.Actor):
                self.collide(i)
                self.Death=1
                return

    def collide(self,Target):
        pass


class Heal(Item):
    def __init__(self,Img='heal'):
        super().__init__(Img)

    def collide(self,Target):
        Target.takedmg(-2)


class ShieldItem(Item):
    def __init__(self,Img='shield'):
        super().__init__(Img)

    def collide(self,Target):
        Target.SK['Shield']=180


class IceItem(Item):
    def __init__(self,Img='ice'):
        super().__init__(Img)

    def collide(self,Target):
        Bullets.append(IceRocket(Target))

class BIFItem(Item):
    def __init__(self,Img='bifitem'):
        super().__init__(Img)

    def collide(self,Target):
        Bullets.append(BIF(Target))

class FITItem(Item):
    def __init__(self, Img='fititem'):
        super().__init__(Img)
    
    def collide(self, Target):
        Bullets.append(FIT(Target))


class Player:
    TeamsAndKeys={'red':keys.W, 'blue':keys.UP}
    TeamsAndBullets={'red':keys.SPACE, 'blue':keys.KP_ENTER}
    
    def posinit(self):
        self.Actor.midbottom=Blocks[randint(0,len(Blocks)-1)].Actor.midtop
        
    def skinit(self):
        self.SK={}
        self.SK['Shield']=0
        self.SK['Freeze']=0
        
    def othersinit(self,Team):
        self.Team=Team
        self.Actor=Actor(Team)
        self.HP=10
        self.Death=0
        self.Jump=1
        self.FD=1 #1-left 0-right
        self.Force=[0,0]
        
    def __init__(self,Team):
        self.othersinit(Team)
        self.posinit()
        self.skinit()

        self.Gun=Actor('gun')

    def draw(self):
        if self.SK['Shield']:
            screen.draw.circle(self.Actor.center,8,(63,133,255))
            screen.draw.text(str(round(self.SK['Shield']/60,1)),(self.Actor.left,self.Actor.top-8),fontsize=15,color='blue')
        if self.SK['Freeze']:
            self.Actor.image='freeze'
            screen.draw.text(str(round(self.SK['Freeze']/60,1)),self.Actor.topright,fontsize=15,color='lightblue')
        elif self.Jump:
            self.Actor.image=self.Team
        elif (not self.Jump):
            self.Actor.image=self.Team+'_d'
        
        if self.FD:
            self.Gun.midright=self.Actor.midleft
        else:
            self.Gun.midleft=self.Actor.midright
        self.Gun.draw()
        
        self.Actor.draw()
        
        screen.draw.text(str(self.HP),self.Actor.topleft,fontsize=15)

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
        if self.SK['Freeze']:
            self.SK['Freeze']-=1
            return
        
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

    def skup(self):
        if self.SK['Shield']>0:
            self.SK['Shield']-=1

    def up(self):
        self.move()
        self.keyup()
        self.collide()
        self.skup()

    def keydown(self,key):
        if self.SK['Freeze']:
            return
        if self.Jump and key==Player.TeamsAndKeys[self.Team]:
            for i in Blocks:
                if abs(self.Actor.x-i.Actor.x)<=30 and abs(self.Actor.bottom-i.Actor.top)<=3:
                    break
            else:
                self.Jump-=1
                self.Actor.image+='_d'
                Bullets.append(DJ(self.Actor.midbottom))
            self.Force[1]=-15

        if key==Player.TeamsAndBullets[self.Team]:
            Bullets.append(Bullet(self,self.FD*180))
    
    def takedmg(self,Dmg):
        if self.SK['Shield'] and Dmg>0:
            return
        
        self.HP-=Dmg
        if Dmg>0 and self.HP<=0:
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


def randenemy(Team):
    global Grand
    i=choice(Grand)
    while i.Team==Team:
        i=choice(Grand)
    return i


Bullets=[]
Items=[]

Winner=''

ItemObj=[Heal,ShieldItem,IceItem,BIFItem,FITItem]

def additem():
    global ItemObj
    if len(Items)<5:
        t=choice(ItemObj)()
        w=1
        while w:
            for i in Items:
                if t.Actor.center==i.Actor.center:
                    t.posinit()
                    break
            else:
                w=0
                Items.append(t)
def iteminit():
    clock.schedule_interval(additem,6)
iteminit()
                

def draw():
    global Grand,Blocks,Bullets,Winner
    screen.fill((180,180,180))
    for i in Blocks+Grand+Items+Bullets:
        i.draw()
    if Winner:
        screen.draw.text(Winner+' wins!',(WIDTH*0.25,HEIGHT*0.25),color='yellow',fontsize=100,fontname='baush93')
        screen.draw.text('Main_Enter to Restart',(WIDTH*0.25,HEIGHT*0.5),color='yellow',fontsize=65,fontname='baush93')

def update():
    global Winner,Grand,Bullets,Items
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
        clock.unschedule(additem)
        Items=[]
        Bullets=[]

def on_key_down(key):
    global Winner,Grand,Bullets,Items
    for i in Grand:
        i.keydown(key)
        
    if Winner and key==keys.RETURN:
        Winner=''
        blockinit()
        playerinit()
        iteminit()
    
    
pgzrun.go()
