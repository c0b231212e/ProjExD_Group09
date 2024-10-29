import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Human:
    # delta = {  # 押下キーと移動量の辞書
    #     pg.K_LEFT: (-60, 0),
    #     pg.K_RIGHT: (+60, 0),
    # }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)
    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, human_plase: list[bool], screen: pg.Surface):
        self.rct.move_ip(human_plase,0)
        screen.blit(self.img, self.rct)

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    human_plase=0
    human = Human((300, 500))
    tmr = 0
    human_TF=[False,False]
    while True:
        human_plase=0
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if pg.key.get_pressed():
                if event.type == pg.KEYDOWN and event.key==pg.K_LEFT:
                    if human_TF[0] ==False:
                        human_plase=-120
                        if human_TF[1]==True:
                            human_TF[1]=False
                        else:
                            human_TF[0]=True
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    if human_TF[1] == False:
                        human_plase=120
                        if human_TF[0]==True:
                            human_TF[0]=False
                        else:
                            human_TF[1]=True



        screen.blit(bg_img, [0, 0])
        human.update(human_plase, screen)
        pg.display.update()
        tmr += 1        
        clock.tick(10)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()