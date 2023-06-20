import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
enn_lst = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:  #こうかとんに着弾したか判定
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_go = pg.image.load("ex02/fig/8.png")
    kk_img_go = pg.transform.rotozoom(kk_img_go, 0, 2.0)
    kk_img_f = pg.transform.flip(kk_img, True, False)
    enn = pg.Surface((20,20))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_1 = pg.transform.rotozoom(kk_img, 315, 1.0)
    kk_img_2 = pg.transform.rotozoom(kk_img, 0, 1.0)
    kk_img_3 = pg.transform.rotozoom(kk_img, 45, 1.0)
    kk_img_4 = pg.transform.rotozoom(kk_img_f, 270, 2.0)
    kk_img_5 = pg.transform.rotozoom(kk_img_f, 315, 2.0)
    kk_img_6 = pg.transform.rotozoom(kk_img_f, 0, 2.0)
    kk_img_7 = pg.transform.rotozoom(kk_img_f, 45, 2.0)
    kk_img_8 = pg.transform.rotozoom(kk_img_f, 90, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    tmr_go = 0
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    enn_rct = enn.get_rect()
    enn_rct.center = x, y
    vx, vy = +5, +5
    kk_img_lst = [kk_img_1, kk_img_2, kk_img_3, kk_img_4, kk_img_5, kk_img_6, kk_img_7, kk_img_8, kk_img_go]
    kk_mv_xy = [[-5, -5], [-5, 0], [-5, +5], [0, +5], [+5, +5], [+5, 0], [+5, -5], [0, -5]]
    accs = [a for a in range(1, 11)]


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(enn_rct):  #ゲームオーバーの設定
            screen.blit(kk_img_lst[9], kk_rct)
            print("ゲームオーバー")
            return
        
        key_lst = pg.key.get_pressed()  #キーに対応したこうかとんの動き
        sum_mv = [0,0]
        for k, mv in enn_lst.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        for i in range(8):  #向きごとのこうかとんの表示
            if kk_mv_xy[i] == sum_mv:
                kk_img = kk_img_lst[i]

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  #爆弾の加速
        enn_rct.move_ip(avx, avy)
        yoko, tate = check_bound(enn_rct)  #画面のはみ出し対策
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(enn, enn_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()