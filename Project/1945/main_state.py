# -*- conding: utf-8 -*-
import gfw
from pico2d import *
from player import Player
from bullet import LaserBullet
from score import Score
import gobj
import enemy_gen
import life_gauge
from background import VertScrollBackground
from hp import *

canvas_width = 720
canvas_height = 960

def enter():
    gfw.world.init(['bg', 'enemy', 'bullet', 'player', 'ui', 'particle', 'boss'])

    bgSky = VertScrollBackground('StageBack.bmp')
    bgSky.speed = 30
    gfw.world.add(gfw.layer.bg, bgSky)

    global bgm
    bgm = load_music(gobj.res('/bgm.mp3'))
    bgm.set_volume(32)
    bgm.repeat_play()

    global effectSound
    effectSound = load_wav(gobj.res('/SEwav.wav'))
    effectSound.set_volume(96)

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    global hp
    hp = hp(player.life)
    gfw.world.add(gfw.layer.ui, hp)

    global score
    score = Score(canvas_width - 20, canvas_height - 50)
    gfw.world.add(gfw.layer.ui, score)


    global font
    font = gfw.font.load(gobj.RES_DIR + '/segoeprb.ttf', 40)

    global emenyCnt
    life_gauge.load()

def check_enemy(e):
    if gobj.collides_box(player, e):
        player.life -= 1
        hp.life -=1
        effectSound.play()

        print('Player Collision', e)
        e.remove()
        return

    for b in gfw.gfw.world.objects_at(gfw.layer.bullet):
        if gobj.collides_box(b, e):
            # print('Collision', e, b)
            dead = e.decrease_life(b.power)
            if dead:
                score.score += e.level * 10
                e.remove()
            b.remove()
            return

def update():
    gfw.world.update()
    enemy_gen.update()

    for e in gfw.world.objects_at(gfw.layer.enemy):
        check_enemy(e)

def draw():
    global myScore
    if player.life < 0:
        gfw.world.draw()
        font.draw(200, canvas_height // 2, 'Game Over')
        font.draw(200, canvas_height // 2 - 50, 'Your Score is %d' % myScore)
    else:
        gfw.world.draw()
        font.draw(20, canvas_height - 45, 'Wave: %d' % enemy_gen.wave_index)
        myScore = score.score


def handle_event(e):
    global player
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
