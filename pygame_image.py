import os
import sys
import pygame as pg

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
            print(y_Flag)
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

       
    

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    human_plasex=0
    human_plasey=0
    human = Human((300, 500))
    tmr = 0
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
                
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    if y_Flag[1]=="Default":
                        if y_Flag[0]=="Default":
                            y_Flag[0]="Active"
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    if y_Flag[0]=="Default":
                        if y_Flag[1]=="Default":
                            y_Flag[1]="Active"
                        

        screen.blit(bg_img, [0, 0])
        human_plasey,y_Flag = human.time_(y_Flag)
        human.update(human_plasex,human_plasey,screen)
        pg.display.update()
        tmr += 1        
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()