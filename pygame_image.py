import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((600, 800))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg2.png")
    #bgr_img = pg.transform.flip(bg_img, True, False)
    road_img = pg.image.load("fig/road.jpg")
    tmr = 0
    bg_speed = 1.0 # 初期の速度
    diff_spd = 0.0001 # 加速度
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        #screen.blit(bg_img, [0, 0])
        #y = (tmr % 800) 
        bg_y = tmr//2%800 # 背景速度 = roadの1/2
        ro_y = tmr%800 # 道の速度 デフォルト
        screen.blit(bg_img, [0, bg_y])
        screen.blit(bg_img, [0, bg_y - 800])
        screen.blit(road_img, [75, ro_y])
        screen.blit(road_img, [75, ro_y-800])
        pg.display.update()
        bg_speed += diff_spd # 背景の速度に加速度を足す
        tmr += bg_speed # tmrに背景の速度を加算する        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()