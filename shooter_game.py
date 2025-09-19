from pygame import *
from random import randint
from time import time as timer
#Background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#fonts
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True,(180, 0 ,0))
font2 = font.SysFont("Arial", 36)


img_back = 'galaxy.jpg'#Game backgr
img_hero = 'rocket.png'#hero
img_enemy = 'ufo.png' #enemy
img_bullet = 'bullet.png' #bullet
img_ast = 'asteroid.png'#asteroid


score = 0 #ship destroyed
lost = 0 #ship missed
goal = 20
max_lost = 10 #lose
life = 3 #life points


#sup clss
class GameSprite(sprite.Sprite):
    #constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #call class(sprite)
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #rectangle
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    #draw char
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#main player
class Player(GameSprite):
    #method control
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #method shoot
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#class Enemy
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost = lost + 1

# Bullet class
class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



#window
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#create sprite
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

#variable game over
finish = False

#main game loop
run = True   # reset by the window close button
rel_time = False  # Flag in charge of reload
num_fire = 0  # variable count shots

run = True# reset by the window close button
while run:
    for i in event.get():
        if i.type == QUIT:
            run = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    if not finish:
        #update background
        window.blit(background, (0, 0))

        #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        #update in a new location
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        #check collide
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        #Lose
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        #Win
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)


    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
             b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
             a.kill()   
        
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)
    #loop executed 0.05 sec
    time.delay(50)

    text_life = font1.render(str(life), 1, life_color)
    window.blit(text_life, (650, 10))

    #write down text on the screen
    text = font2.render('Score: ' + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))

    text_lose = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (10, 50))







    display.update()
    #loop executed 0.05 sec
    time.delay(50)
