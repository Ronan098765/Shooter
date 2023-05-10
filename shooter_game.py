from pygame import *
from random import randint
from time import time as timer
from time import sleep

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)

win = font2.render('YOU WIN', True, (255, 255, 10))
lose = font2.render('YOU LOSE', True, (180, 0, 0))

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

heals = 10000
score = 0
lost = 0
max_lost = 300
num_fire = 0
rel_time = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global bullets_num
        if self.rect.y < 0:
            self.kill()
            

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
game = True
resolt = True
pause = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
              
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_p:
                pause = True
            if e.key == K_g:
                pause = False
    if pause:
        sleep(1)

    if not finish:
        

        window.blit(background,(0, 0))
        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        heals_text = font2.render(str(heals), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        window.blit(text, (10, 20))
        window.blit(heals_text, (670, 20))
        

        asteroids.update()
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()

        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Перезарядка', 1, (255, 255, 255))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False






        colledes = sprite.groupcollide(monsters, bullets, True, True)
        for c in colledes:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            if sprite.spritecollide(ship, monsters, True):
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
            if sprite.spritecollide(ship, asteroids, True):
                asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)
            heals -= 1


        if heals <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        

        
        display.update()

    time.delay(60)








    


    


































