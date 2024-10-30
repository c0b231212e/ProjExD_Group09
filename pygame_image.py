import os
import sys
import time
import pygame as pg
from random import randint
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



class Block_Rock:
    """障害物(岩)を生成するクラス"""
    def __init__(self, x, y=-200):
        self.image = pg.image.load("fig/block.png")
        self.x = x * 120 + 130  # x座標を180, 300, 420の中からランダムに設定
        self.y = y
        self.speed = 3  # 移動速度を設定
    
    def update(self):
        """障害物の位置を更新する"""
        self.y += self.speed  # 下に移動する
    
    def draw(self, screen):
        """障害物を画面に描画する"""
        screen.blit(self.image, (self.x, self.y))
    
    def is_off_screen(self):
        """障害物が画面の下に出たかを判定する"""
        return self.y > 800  # y座標が800を超えたら画面外と判定
    

class Block_Logg:
    """障害物(丸太)を生成するクラス"""
    def __init__(self, y=-200):  # 初期位置は画面の上に設定
        self.image = pg.image.load("fig/block_log.png")
        self.x = 73   # 丸太のx座標（画面全体を覆うために左端に固定）
        self.y = y  # 丸太の初期y座標
        self.speed = 3  # 丸太が下に移動する速度

    def update(self):
        """丸太の位置を更新する"""
        self.y += self.speed  # 下に移動する

    def draw(self, screen):
        """丸太を画面に描画する"""
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        """丸太が画面の下に出たかを判定する"""
        return self.y > 800  # y座標が800を超えたら画面外と判定


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg2.jpg")
    road_img=pg.image.load("fig/road.jpg")
    human_plasex=0
    human=Human((300,500))
    tmr = 0
    obj_speed = 0
    bg_speed = 1.0 # 初期の速度
    diff_spd = 0.0001 # 加速度
    logg = None
    last_logg_time = time.time()  # 最後に丸太を生成した時刻
    flag_num = 0
    # 複数の障害物を保持するリスト
    blocks = [Block_Rock(randint(0, 2)) for _ in range(3)]  # 初期障害物を3つ生成
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
        bg_y = (obj_speed//2%800) # 背景速度 = roadの1/2
        ro_y = (obj_speed%800)  # 道の速度 デフォルト
            


        screen.blit(bg_img, [0, bg_y]) # 自身に別のSurdaceを貼り付ける
        screen.blit(bg_img, [0, bg_y-800])
        screen.blit(road_img, [75, ro_y])
        screen.blit(road_img, [75, ro_y-800])
        pg.display.update()
        bg_speed += diff_spd # 背景の速度に加速度を足す
        obj_speed += bg_speed # obj_speedに背景の速度を加算する
        clock.tick(200)
        # 現在の時刻を取得
        current_time = time.time()
        # 丸太の生成（既存の丸太がないときに新しい丸太を追加）
        if logg is None and randint(0, 100) < 3:  # 一定確率で新しい丸太を生成
                logg = Block_Logg()
        # 丸太の更新と描画fig/block_log.png
        if logg:
            logg.update()
            logg.draw(screen)
            # 画面外に出たら丸太を削除
            if logg.is_off_screen():
                logg = None

        # 障害物の更新と描画
        for block in blocks:
            block.update()
            block.draw(screen)
        
        # 画面外に出た障害物をリストから削除し、新しい障害物を追加
        blocks = [block for block in blocks if not block.is_off_screen()]
        if len(blocks) < 2 and randint(0, 100) < 3:  # 最大2個の障害物が常に表示されるように
            blocks.append(Block_Rock(randint(0, 2)))


        human_plasey,y_Flag=human.time_(y_Flag)
        human.update(human_plasex,human_plasey,screen)
        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()