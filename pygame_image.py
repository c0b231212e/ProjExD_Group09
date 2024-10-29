import os
import sys
import pygame as pg


os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Human:
    """
    障害物を乗り越える人を表示する。
    """
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)
    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.count=0 #人のｙ軸を変更するために必要なcount

    def update(self, human_plasex,human_plasey,screen: pg.Surface):
        
        self.rct.move_ip(human_plasex,human_plasey)
        screen.blit(self.img, self.rct)

    def time_(self,y_Flag):
            """
            ｙ軸を変更する際の動きに使用する
            """
            if y_Flag == "Default":
                self.human_plasey=0
            else:
                if y_Flag=="Active":
                    self.count=0
                    y_Flag="Nonactive"
                if y_Flag=="Nonactive":
                    if self.count==1:
                        self.human_plasey=-50
                    elif self.count==2:
                        self.human_plasey=0
                    elif self.count==3:
                        self.human_plasey=50
                    elif self.count>=4:
                        self.human_plasey=0
                        y_Flag="Default"
                    self.count+=1
            return self.human_plasey, y_Flag



def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    human_plasex=0
    human = Human((300, 500))
    tmr = 0
    human_TF=[False,False]
    y_Flag="Default"

    while True:
        human_plasex=0
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if pg.key.get_pressed():
                if event.type == pg.KEYDOWN and event.key==pg.K_LEFT:
                    if human_TF[0] ==False:
                        human_plasex=-120
                        if human_TF[1]==True:
                            human_TF[1]=False
                        else:
                            human_TF[0]=True
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    if human_TF[1] == False:
                        human_plasex=120
                        if human_TF[0]==True:
                            human_TF[0]=False
                        else:
                            human_TF[1]=True
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    y_Flag="Active"
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    human_plasey=50
        
        screen.blit(bg_img, [0, 0])
        human_plasey,y_Flag=human.time_(y_Flag)
        human.update(human_plasex,human_plasey,screen)
        pg.display.update()
        tmr += 1        
        clock.tick(10)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()