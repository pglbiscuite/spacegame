# Space Game
# Music from monBeats at https://twitter.com/monBeatsART // Personal Project
# Art from Kenney.nl

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
JADE = (0, 168, 107)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Game')
clock = pygame.time.Clock()


font_name = pygame.font.match_font('roboto mono bold')
def draw_text(surf, text, size, x, y):
    """The actual Score on the screen."""
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surface, x, y, pct):
    """Drawing the shield bar"""
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 17
    fill = (pct / 100) * BAR_LENGHT
    # Determine the color based on shield percentage
    if pct > 55:
        color = JADE
    elif pct > 30:
        color = YELLOW
    else:
        color = RED

    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    """Drawing Player Lives"""
    for i in range(lives):
        img_rect = img.get_rect()
        #img_rect.x = x + 30 * i
        SPACE_GAP = 13  # pixels between each image
        img_rect.x = x + ((img_rect.width + SPACE_GAP) * i)
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    """The Player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)            // Circle around the ship
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()





    def update(self):
        """Updating the player"""

        #timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # un hide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        """Shooting the bullets."""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image_orig = meteor_img
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)        // Circle around the asteroid
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        """Rotation of the asteroids"""
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center



    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self. rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (10, 42))
        self.radius = 8.5
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    """The Class for Power Ups"""
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.radius = 8.5
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """The Explosion Sprite"""
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosions_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosions_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Game!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Use The Arrow Keys Move and Space to Fire", 27, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any Key to Begin", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Load all Game Graphics
background = pygame.image.load(path.join(img_dir, "starfield2.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange3.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (24,18))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med12.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laserRed162.png")).convert()
laser_img_rect = background.get_rect()
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_med1.png", "meteorBrown_med12.png",
               "meteorBrown_small1.png", "meteorBrown_small2.png","meteorBrown_tiny1.png", "meteorBrown_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosions_animation = {}
explosions_animation['lg'] = []
explosions_animation['sm'] = []
explosions_animation['player'] = []
for i in range(1, 23):
    filename = 'expl_02_{:04d}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosions_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    explosions_animation['sm'].append(img_sm)


# Making another explosion for the player ship
for i in range(1, 31):
    filename2 = 'expl_06_{:04d}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename2)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosions_animation['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()



# Load all Game Sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shoot_sound.set_volume(0.039)
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'lives.wav'))
shield_sound.set_volume(2)
gun_powerup_sound = pygame.mixer.Sound(path.join(snd_dir, 'guns.wav'))
gun_powerup_sound.set_volume(3)
expl_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'fun.wav'))
player_die_sound.set_volume(0.4)
for sound in expl_sounds:
    sound.set_volume(0.3)  # Adjust the volume to your desired level for each sound

pygame.mixer.music.load(path.join(snd_dir, 'monBeats.wav'))
pygame.mixer.music.set_volume(0.55)






pygame.mixer.music.play(loops=-1)
# Game Loop // Events
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process Input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN:         // Not using this method anymore
        #    if event.key == pygame.K_SPACE:
        #        player.shoot()

    # Update
    all_sprites.update()

    # Check to see if a bullet hit a Mob
    hits = pygame.sprite.groupcollide(mobs, bullets , True, True)
    for hit in hits:
        score += (50 - hit.radius)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # Check to see if a mob hit the Player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in  hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check to see if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 25)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            gun_powerup_sound.play()

   # If the Player Died and the Explosion has Finished
    if player.lives == 0 and not death_explosion.alive():
       game_over = True



    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 38, WIDTH / 2, 10 )
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 110, 15, player.lives, player_mini_img)
    # *after drawing everything, flip the display
    pygame.display.flip()


pygame.quit()