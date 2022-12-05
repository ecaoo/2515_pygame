import pygame
from sys import exit
from random import randint, choice

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/player/teemo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect(midbottom = (80, 350))
        self.grav = 0

        self.jump_sound = pygame.mixer.Sound('sounds/teemolaugh.mp3')
        self.jump_sound.set_volume(0.1)

        self.death_sound = pygame.mixer.Sound('sounds/death.mp3')
        self.death_sound.set_volume(0.2)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.grav = -20
            self.jump_sound.play()


    def apply_grav(self):
        self.grav += 1
        self.rect.y += self.grav
        # if player hits the ground they will not fall through
        if self.rect.bottom >= 350:
            self.rect.bottom = 350


    def update(self):
        self.player_input()
        self.apply_grav()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'corki':
            corki_surface = pygame.image.load('sprites/enemy_flying/corki.png').convert_alpha()
            corki_surface = pygame.transform.scale(corki_surface, (75, 75))
            self.image = corki_surface
            y_pos = 275
        
        else:
            teemo_mushroom_surface = pygame.image.load('sprites/enemy_shroom/teemo_shroom.png').convert_alpha()
            teemo_mushroom_surface = pygame.transform.scale(teemo_mushroom_surface, (50, 50))
            self.image = teemo_mushroom_surface
            y_pos = 350
        # set the obstacle spawning position randomly between the range 
        self.rect = self.image.get_rect(midbottom = (randint(1100, 1200), y_pos))
        
    # method to update rectangle speed as the score increases and destroy the enemy off the screen to save memory 
    def update(self):
        self.rect.x -= 6
        self.destroy()
        score = display_score()
        if score >= 5:
            self.rect.x -= 2

        if score >= 10:
            self.rect.x -= 2
        
        if score >= 15:
            self.rect.x -= 2

        if score >= 20:
            self.rect.x -= 3

        if score >= 30:
            self.rect.x -= 2

        if score >= 50:
            self.rect.x -= 2

    # method to destroy enemy off the screen to save memory
    def destroy(self):
        if self.rect.x <= -100:
            self.kill
            
    # function to check score
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}', False, '#483C32')
    score_rect = score_surface.get_rect(center = (450, 50))
    screen.blit(score_surface, score_rect)
    return current_time

    # function to display enemies
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 275:
                screen.blit(corki_surface, obstacle_rect)
                
            else:
                screen.blit(teemo_mushroom_surface,obstacle_rect)
                
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

    # function to detect collision with player
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

    # function to detect collision with sprite
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        death_sound = pygame.mixer.Sound('sounds/death.mp3')
        death_sound.set_volume(0.7)
        death_sound.play()
        return False
    else:
        return True


# Game start and important variables
pygame.init()
screen = pygame.display.set_mode((900, 450))
pygame.display.set_caption('Teemo Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('font/redensek.ttf', 50)
game_state = False
start_time = 0
score = 0

background_music = pygame.mixer.Sound('sounds/lol.mp3')
background_music.set_volume(0.6)
background_music.play(loops = -1)

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# background
sky_surface = pygame.image.load('sprites/night_sky.png').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (1000, 425))
sky_surface = pygame.transform.rotate(sky_surface, (180))

ground_surface = pygame.image.load('sprites/ground.png').convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))

# Enemys
teemo_mushroom_surface = pygame.image.load('sprites/enemy_shroom/teemo_shroom.png').convert_alpha()
teemo_mushroom_surface = pygame.transform.scale(teemo_mushroom_surface, (50, 50))

corki_surface = pygame.image.load('sprites/enemy_flying/corki.png').convert_alpha()
corki_surface = pygame.transform.scale(corki_surface, (75, 75))

obstacle_rect_list = []

# player surface
player_surface = pygame.image.load('sprites/player/teemo.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (65, 65))
player_rect = player_surface.get_rect(midbottom = (80, 350))
player_grav = 0

# Intro screen
player_intro = pygame.image.load('sprites/player/intro_teemo.png').convert_alpha()
player_intro_rec = player_intro.get_rect(center = (525, 400))
player_intro = pygame.transform.scale(player_intro, (250, 250))

game_name = font.render('Teemo Runner', False, '#483C32')
game_name_rect = game_name.get_rect(center = (450, 50))

game_into = font.render('Press space to run!', False, '#483C32')
game_into_rec = game_into.get_rect(center =(450, 400))

# Timer to start at the beginning of the game and set obstacles timer to change as the score increases
def set_obstacle_timer(score):
    if score == 0:
        pygame.time.set_timer(obstacle_timer, 900)

    if score == 5:
        pygame.time.set_timer(obstacle_timer, 850)

    if score == 15:
        pygame.time.set_timer(obstacle_timer, 750)

    if score == 30:
        pygame.time.set_timer(obstacle_timer, 650)

    if score == 50:
        pygame.time.set_timer(obstacle_timer, 500)

    if score == 100:
        pygame.time.set_timer(obstacle_timer, 300)

# starting timer for game
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_grav = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 350:
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = True
                start_time = int(pygame.time.get_ticks() / 1000)
        
        # add a list of enemies
        if event.type == obstacle_timer and game_state:
            obstacle_group.add(Enemy(choice(['teemo_shroom', 'teemo_shroom', 'corki', 'teemo_shroom', 'corki', 'corki', 'teemo_shroom'])))


    if game_state == True:   
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 350))
        score = display_score()
        set_obstacle_timer(score)


        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # collision
        game_state = collision_sprite()
       
        # end game screen
    else:
        screen.fill('#9370DB')
        screen.blit(player_intro, player_intro_rec)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 350)
        player_grav = 0

        score_message = font.render(f'Your Score: {score}', False, '#483C32')
        score_message_rect = score_message.get_rect(center = (450, 400))
        screen.blit(game_name, game_name_rect)
        
        # score message to show when the game ends
        if score == 0:
            screen.blit(game_into, game_into_rec)
        else:
            screen.blit(score_message, score_message_rect)
            

    pygame.display.update()
    clock.tick(80)