import os
import sys
import pygame as pg
import random
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Human():
    # delta = {  # 押下キーと移動量の辞書
    #     pg.K_LEFT: (-50, 0),
    #     pg.K_RIGHT: (+50, 0),
    # }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img=pg.transform.flip(img0, True, False)

    def __init__(self,xy:tuple[int, int]):
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.count=0
        self.human_plasey=0

    def update(self, human_plasex:int, human_plasey:int,screen: pg.Surface):
        
        self.rct.move_ip(human_plasex,human_plasey)        
        screen.blit(self.img, self.rct)

    def time_(self,y_Flag):
        if y_Flag[0] == "Default":
            if y_Flag[1] =="Defult":
                self.human_plasey=0
        if y_Flag[0]!="Default":
            if y_Flag[0]=="Active":
                self.count=0
                y_Flag[0]="Nonactive"
            if y_Flag[0]=="Nonactive":
                if self.count>=4:
                    self.human_plasey=0
                    self.count=0
                    y_Flag[0]="Default"
                elif self.count>=3:
                    self.human_plasey=50
                elif self.count>=2:
                    self.human_plasey=0
                elif self.count>=1:
                    self.human_plasey=-50
                self.count+=1
        else:
            if y_Flag[1]=="Active":
                self.count=0
                y_Flag[1]="Nonactive"
            if y_Flag[1]=="Nonactive":
                if self.count>=4:
                    self.human_plasey=0
                    self.count=0
                    y_Flag[1]="Default"
                elif self.count>=3:
                    self.human_plasey=-50
                elif self.count>=2:
                    self.human_plasey=0
                elif self.count>=1:
                    self.human_plasey=50
                self.count+=1
        return self.human_plasey, y_Flag


class Gorilla:
    """
    Dを押すとゴリラが増え
    Aを押すとゴリラが減る関数
    """
    gorira = pg.transform.rotozoom(pg.image.load("fig/gorira.png"), 0, 0.5) # ゴリラのサイズ調整は一番後ろの数字をいじる
    gorira_img=pg.transform.flip(gorira, True, False)
    def __init__(self,xy):
        self.img = __class__.gorira_img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center=xy
        self.gori_y=700

    def update(self,screen,count):
        for i in range(count):
            if i==1:
                self.rct.center=(300,self.gori_y)
            elif i==2:
                self.rct.center=(420,self.gori_y)
            elif i==3:
                self.rct.center=(180,self.gori_y)
            self.gori_y+=0
            screen.blit(self.img,self.rct)
    
class Arrow(pg.sprite.Sprite):
    """
    槍がランダムな列に投げられる
    """
    def __init__(self,xy :tuple[int,int]):
        super().__init__()
        self.vx, self.vy = xy
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/yari.png"),0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.centery = self.vy
        self.rect.centerx = self.vx
        self.spped=10
        self.count=0
    
    def update(self):
        self.arrow_y=-50
        if self.rect.bottom<=0:
            self.kill()
        self.rect.move_ip(0,-self.spped)
        

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    human_plasex=0
    human_plasey=0
    human = Human((300, 500))
    gorira_count=0
    gorira=Gorilla((300,700))
    arrow=pg.sprite.Group()
    tmr = 0
    fly=False
    human_TF=[False,False] # 最初が左　後ろが右
    y_Flag=["Default","Default"]
    while True:
        human_plasex=0
        for event in pg.event.get():
            if event.type == pg.QUIT: return    
            if pg.key.get_pressed():
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                    if human_TF[0] !=True:
                        human_plasex=-120
                        if human_TF[1]==True:
                            human_TF[1]=False
                        else:
                            human_TF[0]=True
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    if human_TF[1] != True:
                        human_plasex=120
                        if human_TF[0]==True:
                            human_TF[0]=False
                        else:
                            human_TF[1]=True
                if event.type == pg.KEYDOWN and event.key == pg.K_d:
                    if gorira_count<=3:
                        gorira_count+=1
                if event.type == pg.KEYDOWN and event.key == pg.K_a:
                    if gorira_count>0:
                        gorira_count-=1
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    if y_Flag[1]=="Default":
                        if y_Flag[0]=="Default":
                            y_Flag[0]="Active"
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    if y_Flag[0]=="Default":
                        if y_Flag[1]=="Default":
                            y_Flag[1]="Active"
                        
        if tmr%10==0:
            arrow_xy=(random.choice([180,300,420]),700)
            arrow.add(Arrow(arrow_xy))
        screen.blit(bg_img, [0, 0])
        human_plasey,y_Flag = human.time_(y_Flag)
        human.update(human_plasex,human_plasey,screen)
        gorira.update(screen,gorira_count)
        arrow.update()
        arrow.draw(screen)
        pg.display.update()
        tmr += 1        
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()