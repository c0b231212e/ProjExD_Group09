import os
import sys
import time
import pygame as pg
from random import randint

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    tmr = 0
    logg = None
    last_logg_time = time.time()  # 最後に丸太を生成した時刻
    flag_num = 0

    # 複数の障害物を保持するリスト
    blocks = [Block_Rock(randint(0, 2)) for _ in range(3)]  # 初期障害物を3つ生成

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

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

        pg.display.update()
        clock.tick(200)
        tmr += 1

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()