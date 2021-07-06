import pyxel
import math
from random import randint



class Bullet:
    def __init__(self,x,y,to_x,to_y,col):
        self.x = x
        self.y = y
        self.vx = (to_x-x)/(math.sqrt((to_x-x)**2+(to_y-y)**2))
        self.vy = (to_y-y)/(math.sqrt((to_x-x)**2+(to_y-y)**2))
        self.r = 1
        self.speed = 5
        self.exist = True
        self.col = col
    def update(self):
        if self.exist:
            self.x += self.speed*self.vx
            self.y += self.speed*self.vy

    def draw(self):
        if self.exist:
            pyxel.circ(self.x,self.y,1,self.col)

class Player:
    def __init__(self,windoww,windowh):
        self.x = windoww/2
        self.y = windowh/2
        self.vx = 0
        self.vy = 0
        self.hit = False
        self.speed = 1
        self.windoww = windoww
        self.windowh = windowh
        self.skill = 0
        self.skillstate = False
        self.hp = 100
        self.bullets = []
        self.w = 16
        self.h = 16
        self.image = 16

    def update(self): 
        
        #移動
        if pyxel.btn(pyxel.KEY_A) and pyxel.btn(pyxel.KEY_D):
            self.vx = 0
        elif pyxel.btn(pyxel.KEY_A):
            self.vx = -1
        elif pyxel.btn(pyxel.KEY_D):
            self.vx = 1
        else:
            self.vx = 0
        self.x += self.speed*self.vx

        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_W):
            self.vy = 0
        elif pyxel.btn(pyxel.KEY_W):
            self.vy = -1
        elif pyxel.btn(pyxel.KEY_S):
            self.vy = 1
        else:
            self.vy = 0
        self.y += self.speed*self.vy

        if self.x < 0:
            self.x = 0
        if self.x > self.windoww:
            self.x = self.windoww
        if self.y < 0:
            self.y = 0
        if self.y > self.windowh:
            self.y = self.windowh

        #射撃
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.bullets.append(Bullet(self.x,self.y,pyxel.mouse_x,pyxel.mouse_y,9))
        
        if len(self.bullets) > 0:
            for i in range(len(self.bullets)):
                self.bullets[i].update()
        
        if self.vx > 0:
            self.image = 16
        elif self.vx < 0:
            self.image = 32

    def draw(self):
        
        if len(self.bullets)>0:
            for i in range(len(self.bullets)):
                self.bullets[i].draw()
        # pyxel.circ(self.x,self.y,8,3)
        if self.skillstate:
            if pyxel.frame_count%10<5:
                pyxel.blt(self.x-8,self.y-8,0,self.image,0,16,16,11)
        else:
            pyxel.blt(self.x-8,self.y-8,0,self.image,0,16,16,11)
            if self.hit:
                pyxel.blt(self.x-8,self.y-8,0,16,16,16,16,0)
        


class Enemy:
    def __init__(self,windoww,windowh):
        self.windoww = windoww
        self.windowh = windowh
        self.x = randint(0,self.windoww)
        self.y = randint(0,self.windowh)
        self.angle = math.radians(randint(0,359))
        self.vx = math.cos(self.angle)
        self.vy = math.cos(self.angle)
        self.hit = False
        self.speed = 1
        self.hp = 100
        self.image = 0
        self.bullets = []
        self.player_x = 100
        self.player_y = 100
        self.h = 16
        self.predictx = 0
        self.predicty = 0
        self.image = 48

    def update(self):

        
        self.x += self.vx*self.speed
        self.y += self.vy*self.speed

        if self.x < 0:
            self.vx *= -1
            self.x = 0
        if self.x > self.windoww:
            self.vx *= -1
            self.x = self.windoww
        if self.y < 0:
            self.vy *= -1
            self.y = 0
        if self.y > self.windowh:
            self.vy *= -1
            self.y = self.windowh

        if pyxel.frame_count%10 == 0 and randint(1,3) == 1:
            self.angle = math.radians(randint(0,359))
            self.vx = math.cos(self.angle)
            self.vy = math.cos(self.angle)
            self.speed = randint(0,30)/10

        if randint(1,10)>5:
            self.bullets.append(Bullet(self.x,self.y,self.player_x+self.predictx,self.player_y+self.predicty,8))
        
        if len(self.bullets) > 0:
            for i in range(len(self.bullets)):
                self.bullets[i].update()

        
        if self.vx > 0:
            self.image = 48
        elif self.vx < 0:
            self.image = 64

    def draw(self):
        
        if len(self.bullets)>0:
            for i in range(len(self.bullets)):
                self.bullets[i].draw()
        pyxel.blt(self.x-8,self.y-8,0,self.image,0,16,16,11)
        if self.hit:
            pyxel.blt(self.x-8,self.y-8,0,16,16,16,16,0)

        pyxel.line(self.x-8,self.y-10,self.x+8,self.y-10,6)
        pyxel.line(self.x-8,self.y-10,self.x+(16*self.hp//100)-8,self.y-10,5)

class Obstacle:
    def __init__(self,windoww,windowh):
        self.x = randint(0,windoww)
        self.y = randint(0,windowh)
        self.w = 16
        self.h = 16

        

    def draw(self):
        pyxel.blt(self.x,self.y,0,0,0,16,16,11)

class Status:
    def __init__(self,windoww,windowh):
        self.hp = 100
        self.maxhp = 100
        self.skill = 0
        self.windoww = windoww
        self.windowh = windowh

    def draw(self):
        pyxel.rect(150,185,50,15,6)
        pyxel.line(155,195,195,195,13)
        pyxel.rect(155,193,41*self.hp//self.maxhp,2,[8,9,3][self.hp//34])
        pyxel.text(155,193,str(self.hp)+"/"+str(self.maxhp),1)
        if self.skill == 100:
            if pyxel.frame_count%30 <= 15:
                pyxel.text(155,187,str(self.skill)+" Press Q",8)
        else:
            pyxel.text(155,187,str(self.skill),1)
    
        

    
class App:
    def __init__(self):
        self.windoww = 200
        self.windowh = 200
        pyxel.init(self.windoww,self.windowh)
        pyxel.load("assets/my_resource.pyxres")
        self.reset()
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if self.gamestate == 0:
            self.enemy.update()
            #難易度選択
            if pyxel.btnp(pyxel.KEY_W):
                self.difficulty -= 1
                pyxel.play(0,2)
            if pyxel.btnp(pyxel.KEY_S):
                self.difficulty += 1
                pyxel.play(0,2)
            self.difficulty = self.difficulty%3


            if pyxel.btnp(pyxel.KEY_SPACE):
                self.gamestate = 1
                pyxel.play(0,3)
        elif self.gamestate == 1:

            self.killtime += 1
            #Player

            self.player.update()
            #ダメージ判定
            self.player.hit = False
            if not self.player.skillstate:
                for i in self.enemy.bullets:
                    if i.exist and self.player.x-8 <= i.x and i.x <= self.player.x+8 and self.player.y-8 <= i.y and  i.y <= self.player.y + 8:
                        self.player.hp -= 1
                        pyxel.play(0,1)
                        if self.player.skill < 100:
                            self.player.skill += 1
                        self.player.hit = True
                        i.exist = False
            #ゲームオーバー
            if self.player.hp <= 0:
                self.gamestate = 2
                pyxel.play(0,5)
            #障害物接触
            for i in self.obstacles:
                if i.y <= self.player.y and self.player.y <= i.y+16 and i.x - self.player.x < 9 and 0 < i.x - self.player.x:
                    self.player.x = i.x-9 
                if i.y <= self.player.y and self.player.y <= i.y+16 and self.player.x -i.x < 24 and 0 < self.player.x -i.x:
                    self.player.x = i.x+24
                if i.x <= self.player.x and self.player.x <= i.x+16 and i.y - self.player.y < 9 and 0 < i.y - self.player.y:
                    self.player.y = i.y-9
                if i.x <= self.player.x and self.player.x <= i.x+16 and self.player.y -i.y < 24 and 0 < self.player.y -i.y:
                    self.player.y = i.y+24

            #Enemy
            self.enemy.player_x = self.player.x
            self.enemy.player_y = self.player.y
            #予測撃ち
            if self.difficulty == 0:
                self.enemy.predictx = randint(-16,16)
                self.enemy.predicty = randint(-16,16)
            elif self.difficulty == 1:
                self.enemy.predictx = self.player.vx*math.sqrt((self.player.x-self.enemy.x)**2+(self.player.y-self.enemy.y)**2)/5+randint(-16,16)
                self.enemy.predicty = self.player.vy*math.sqrt((self.player.x-self.enemy.x)**2+(self.player.y-self.enemy.y)**2)/5+randint(-16,16)
            elif self.difficulty == 2:
                self.enemy.predictx = self.player.vx*math.sqrt((self.player.x-self.enemy.x)**2+(self.player.y-self.enemy.y)**2)/5
                self.enemy.predicty = self.player.vy*math.sqrt((self.player.x-self.enemy.x)**2+(self.player.y-self.enemy.y)**2)/5
            self.enemy.update()

            self.enemy.hit = False
            for i in self.player.bullets:
                if i.exist and self.enemy.x-8 <= i.x and  i.x <= self.enemy.x + 8 and self.enemy.y - 8 <= i.y and  i.y <= self.enemy.y + 8:
                    if self.difficulty == 0:
                        self.enemy.hp -= 3
                    elif self.difficulty == 1:
                        self.enemy.hp -= 2
                    elif self.difficulty == 2:
                        self.enemy.hp -= 1
                    pyxel.play(0,0)
                    if self.player.skill < 100:
                        self.player.skill += 2
                    self.hit += 1
                    self.enemy.hit = True
                    i.exist = False
            #ゲームクリア
            if self.enemy.hp <= 0:
                #スコアを計算

                #キルタイム
                if self.killtime//30 <= 60:
                    self.timescore = 60 - self.killtime//30
                else:
                    self.timescore = 0
                #被ダメージ

                self.hpscore = self.player.hp

                #命中率

                self.hitscore = int(100*self.hit/len(self.player.bullets))

                self.score = self.timescore + self.hpscore + self.hitscore + self.difficulty*20

                pyxel.play(0,4)

                self.gamestate = 3

            #障害物接触
            for i in self.obstacles:
                if i.y <= self.enemy.y and self.enemy.y <= i.y+16 and i.x - self.enemy.x < 9 and 0 < i.x - self.enemy.x:
                    self.enemy.vx *= -1
                    self.enemy.x = i.x-10
                if i.y <= self.enemy.y and self.enemy.y <= i.y+16 and self.enemy.x -i.x < 24 and 0 < self.enemy.x -i.x:
                    self.enemy.vx *= -1
                    self.enemy.x = i.x+25
                if i.x <= self.enemy.x and self.enemy.x <= i.x+16 and i.y - self.enemy.y < 9 and 0 < i.y - self.enemy.y:
                    self.enemy.vy *= -1
                    self.enemy.y = i.y-10
                if i.x <= self.enemy.x and self.enemy.x <= i.x+16 and self.enemy.y -i.y < 24 and 0 < self.enemy.y -i.y:
                    self.enemy.vy *= -1
                    self.enemy.y = i.y+25

            #障害物に弾が接触したら弾を消す
            for i in self.obstacles:
                for j in self.player.bullets:
                    if i.x <= j.x and i.x+i.w >= j.x and i.y <= j.y and i.y+i.h >= j.y:
                        j.exist = False
                for j in self.enemy.bullets:
                    if i.x <= j.x and i.x+i.w >= j.x and i.y <= j.y and i.y+i.h >= j.y:
                        j.exist = False
            if self.player.skill > 100:
                self.player.skill = 100
            self.status.skill = self.player.skill
            self.status.hp = self.player.hp

            if self.player.skillstate:
                if self.player.skill <= 0:
                    self.player.skillstate = False
                    self.player.speed = 1
                else:
                    self.player.skill -= 1
            else:
                if pyxel.btnp(pyxel.KEY_Q) and self.player.skill == 100:
                    pyxel.play(0,2)
                    self.player.skillstate = True
                    self.player.speed = 2

        elif self.gamestate == 2:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(0,3)
                self.reset()

        elif self.gamestate == 3:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(0,3)
                self.reset()


    def draw(self):
        # 背景
        pyxel.cls(11)

        if self.gamestate == 0:
            self.enemy.draw()
            self.drawshadowtext(5,5,"Nopperi Shooting",5,7)
            if pyxel.frame_count%30 <15:
                pyxel.text(63,150,"Press SPACE to start",5)
            # 難易度表示
            pyxel.text(90,60,"EASY",5)
            pyxel.text(90,90,"NORMAL",5)
            pyxel.text(90,120,"HARD",5)
            pyxel.circ(85,[62,92,122][self.difficulty],2,9)


        elif self.gamestate == 1:
            for i in range(0,(self.windoww//16+1)*16,16):
                for j in range(0,(self.windowh//16+1)*16,16):
                    pyxel.blt(i,j,0,0,16,16,16)
            self.player.draw()
            self.enemy.draw()

            for i in self.obstacles:
                i.draw()

            self.status.draw()
            pyxel.blt(pyxel.mouse_x-2,pyxel.mouse_y-2,0,80,0,7,7,11)

        elif self.gamestate == 2:
            self.drawshadowtext(5,5,"GameOver",5,7)
            if pyxel.frame_count%30 <15:
                pyxel.text(5,20,"Press SPACE to retry",5)

        elif self.gamestate == 3:
            self.drawshadowtext(5,5,"GameClear",5,7)
            pyxel.text(5,30,"HP: "+str(self.hpscore)
                +"\nHit Rate: "+str(self.hitscore)
                +"\nKill Time Bonus: "+str(self.timescore)
                +"\nDifficulty Bonus: "+str(self.difficulty*20),5)
            self.drawshadowtext(5,70,"Your Score: "+str(self.score),5,7)
            if pyxel.frame_count%30 <15:
                pyxel.text(5,150,"Press SPACE to retry",5)

    def reset(self):
        # 場面設定 0タイトル画面 1プレー画面 2ゲームオーバー画面 3クリア画面
        self.gamestate = 0

        self.player = Player(self.windoww,self.windowh)
        self.enemy = Enemy(self.windoww,self.windowh)
        self.obstacles = []
        self.obstacles.clear()
        for i in range(10):
            self.obstacles.append(Obstacle(self.windoww,self.windowh))
        self.status = Status(self.windoww,self.windowh)
        self.difficulty = 0
        self.killtime = 0
        self.hit = 0

    def drawshadowtext(self,x,y,text,maincol,shadowcol):
        pyxel.text(x+1,y,text,shadowcol)
        pyxel.text(x,y,text,maincol)
        


App()