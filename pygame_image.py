import os
import sys
import time
import pygame as pg
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen):
    """
    引数screen
    黒の透過背景にGameOverと出力される関数
    """
    WIDTH, HEIGHT = screen.get_size()  # 画面サイズを取得
    surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(surface, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    surface.set_alpha(128)
    screen.blit(surface, [0, 0])
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("GameOver", True, (255, 255, 255))
    screen.blit(txt, [WIDTH/2 - 190, HEIGHT/2])
    pg.display.update()
    time.sleep(3)

class Human():
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img=pg.transform.flip(img0, True, False)

    def __init__(self,xy:tuple[int, int]):
        super().__init__()
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
                if self.count>=60:
                    self.human_plasey=0
                    self.count=0
                    y_Flag[0]="Default"
                elif self.count>=40:
                    self.human_plasey=3
                elif self.count>=20:
                    self.human_plasey=0
                else:
                    self.human_plasey=-3
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

class Block_Rock(pg.sprite.Sprite):
    def __init__(self, xy):
        super().__init__()
        self.vx, self.vy = xy
        self.image = pg.transform.rotozoom(pg.image.load("fig/block.png"), 0, 1.0)
        self.rect = self.image.get_rect(center=(self.vx, self.vy))
        self.speed = 5  # 誤字を修正

    def update(self):
        self.rect.centery += self.speed  # 下に移動
        if self.rect.top >= 800:
            self.kill()

class Block_Logg(pg.sprite.Sprite):
    def __init__(self, y=-200):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/block_log.png"), 0, 0.8)
        self.rect = self.image.get_rect(center=(300, y))
        self.speed = 3

    def update(self):
        self.rect.centery += self.speed
        if self.rect.top >= 800:
            self.kill()

class Gorilla(pg.sprite.Sprite):
    """
    槍が投げられるときにゴリラが出現する
    """
    def __init__(self,xy):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/gorira.png"), 0, 0.5) # ゴリラのサイズ調整は一番後ろの数字をいじる
        self.vx, self.vy = xy
        self.rect = self.image.get_rect(center=(self.vx, self.vy))
        self.speed = 5
        self.rect.centerx=self.vx
        self.rect.centery=700
        self.count=0

    def update(self):
        self.count+=1
        if self.count>=10:
            self.kill()
            self.count=0

class Arrow(pg.sprite.Sprite):
    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        self.vx, self.vy = xy
        self.image = pg.transform.rotozoom(pg.image.load("fig/yari.png"), 0, 0.2)
        self.rect = self.image.get_rect(center=(self.vx, self.vy))
        self.speed = 5

    def update(self):
        self.rect.centery -= self.speed  # 上に移動
        if self.rect.bottom <= 0:
            self.kill()


class Items(pg.sprite.Sprite):
    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        self.vx, self.vy = xy
        self.image = pg.transform.rotozoom(pg.image.load("fig/coin.png"), 0, 0.1)
        self.rect = self.image.get_rect(center=(self.vx, self.vy))
        self.speed = 5

    def update(self):
        self.rect.centery += self.speed  # 下に移動
        if self.rect.top >= 800:
            self.kill()


class BackGround():
    """
    背景のスクロール速度と道のスクロール速度の
    制御に関するプログラムを記述
    """
    def __init__(self, bg_speed = 1.0, diff_spd = 0.0001):
        """
        bg_speed : 背景速度と道の速度にかかわる変数 float型
        diff_spd : 加速度にかかわる変数 float型
        """
        self.bg_img = pg.image.load("fig/pg_bg2.jpg")
        self.road_img = pg.image.load("fig/road.jpg")
        self.bg_speed = bg_speed # 背景速度と道の速度にかかわる変数
        self.diff_spd = diff_spd # 加速度にかかわる変数
        self.obj_speed = 0 # オブジェクトの速度に関する変数
        self.bg_y = 0
        self.ro_y = 0

    def update(self, screen):
        # 背景と道の速度を更新
        self.bg_speed += self.diff_spd
        self.obj_speed += self.bg_speed

        # 背景と道のスクロール位置を更新
        self.bg_y = (self.bg_y + self.bg_speed / 2) % 800
        self.ro_y = (self.ro_y + self.bg_speed) % 800

        # 画面に画像を描画
        screen.blit(self.bg_img, [0, self.bg_y])
        screen.blit(self.bg_img, [0, self.bg_y - 800])
        screen.blit(self.road_img, [75, self.ro_y])
        screen.blit(self.road_img, [75, self.ro_y - 800])

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    human_plasex=0
    human_plasey=0
    human = Human((300, 500))
    gorira=pg.sprite.Group()
    arrow=pg.sprite.Group()
    coin=pg.sprite.Group()
    load = BackGround()
    block=pg.sprite.Group()
    terr=pg.sprite.Group()
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

        #update群
        load.update(screen)
        if tmr%200==0:
            arrow_xy=(random.choice([180,300,420]),700)
            arrow.add(Arrow(arrow_xy))
            gorira.add(Gorilla(arrow_xy))
        if tmr%50==0:
            coin_xy=(random.choice([180,300,420]),0)
            coin.add(Items(coin_xy))
        if tmr%100==0:
            block_xy=(random.choice([180,300,420]),0)
            block.add(Block_Rock(block_xy))
        if tmr%500==0:
            block.add(Block_Logg())
        arrow.update()
        arrow.draw(screen)
        coin.update()
        coin.draw(screen)
        block.update()
        block.draw(screen)
        terr.update()
        terr.draw(screen)
        gorira.update()
        gorira.draw(screen)
        human_plasey,y_Flag = human.time_(y_Flag)
        human.update(human_plasex,human_plasey,screen)
        pg.display.update()
        tmr += 1
        clock.tick(200)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()