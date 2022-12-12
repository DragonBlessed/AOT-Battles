import pygame
import os
pygame.font.init()
pygame.mixer.init()

# makes new window with resolution
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("AOT Battles")

BROWN = (101, 67, 33)
GREEN = (1, 50, 32)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# sound effects
ROCK_HIT_SOUND = pygame.mixer.Sound(os.path.join('rock_smash.mp3'))
ROCK_FIRE_SOUND = pygame.mixer.Sound(os.path.join('throw.mp3'))


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
ROCK_VEL = 7
MAX_ROCKS = 2


CHARACTER_WIDTH, CHARACTER_HEIGHT = 75, 70

# Adding events
EREN_HIT = pygame.USEREVENT + 1
REINER_HIT = pygame.USEREVENT + 2

# make character with dimensions and rotations
EREN_YEAGER_IMAGE = pygame.image.load(
    os.path.join('attacktitan.png'))
EREN_YEAGER = pygame.transform.rotate(pygame.transform.scale(
    EREN_YEAGER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 360)

REINER_TITAN_IMAGE = pygame.image.load(
    os.path.join('armoredtitan.png'))
REINER_TITAN = pygame.transform.rotate(pygame.transform.scale(
    REINER_TITAN_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 360)

FIELD = pygame.transform.scale(pygame.image.load(os.path.join('field.png')), (WIDTH, HEIGHT))

# screen color
def draw_window(eren, reiner, eren_rocks, reiner_rocks, eren_health, reiner_health):
    WIN.blit(FIELD, (0, 0))
    pygame.draw.rect(WIN, GREEN, BORDER)

    # health
    reiner_health_text = HEALTH_FONT.render("Health: " + str(reiner_health), 1, RED)
    eren_health_text = HEALTH_FONT.render("Health: " + str(eren_health), 1, GREEN)
    WIN.blit(reiner_health_text, (WIDTH - reiner_health_text.get_width() - 10, 10))
    WIN.blit(eren_health_text, (10, 10))


    # posting images
    WIN.blit(EREN_YEAGER, (eren.x, eren.y))
    WIN.blit(REINER_TITAN, (reiner.x, reiner.y))



    for rock in reiner_rocks:
        pygame.draw.rect(WIN, RED, rock)

    for rock in eren_rocks:
        pygame.draw.rect(WIN, YELLOW, rock)

    pygame.display.update()


def eren_movement(keys_pressed, eren):
    if keys_pressed[pygame.K_a] and eren.x - VEL > 0: # left
        eren.x -= VEL
    if keys_pressed[pygame.K_d] and eren.x + VEL + eren.width < BORDER.x: # right
        eren.x += VEL
    if keys_pressed[pygame.K_w] and eren.y - VEL > 0: # up
        eren.y -= VEL
    if keys_pressed[pygame.K_s] and eren.y + VEL + eren.height < HEIGHT - 5: # down
        eren.y += VEL

def reiner_movement(keys_pressed, reiner):
    if keys_pressed[pygame.K_LEFT] and reiner.x - VEL > BORDER.x + BORDER.width: # left
        reiner.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and reiner.x + VEL + reiner.width < WIDTH: # right
        reiner.x += VEL
    if keys_pressed[pygame.K_UP] and reiner.y - VEL > 0: # up
        reiner.y -= VEL
    if keys_pressed[pygame.K_DOWN] and reiner.y + VEL + reiner.height < HEIGHT - 5: # down
        reiner.y += VEL

# rock event
def handle_rocks(eren_rocks, reiner_rocks, eren, reiner):
    for rock in eren_rocks:
        rock.x += ROCK_VEL
        if reiner.colliderect(rock):
            pygame.event.post(pygame.event.Event(REINER_HIT))            
            eren_rocks.remove(rock)
        if rock.x > WIDTH:
            eren_rocks.remove(rock)

    for rock in reiner_rocks:
        rock.x -= ROCK_VEL
        if eren.colliderect(rock):
            pygame.event.post(pygame.event.Event(EREN_HIT))            
            reiner_rocks.remove(rock)
        elif rock.x < 0:
            reiner_rocks.remove(rock)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    # movement of characters
    eren = pygame.Rect(100, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    reiner = pygame.Rect(700, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    eren_rocks = []
    reiner_rocks = []

    reiner_health = 10
    eren_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # end while loop to quit
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                print("Goodbye!")
                pygame.quit()
            
            # firing rocks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(eren_rocks) < MAX_ROCKS:
                    rock = pygame.Rect(
                        eren.x + eren.width, eren.y + eren.height//2 - 2, 10, 5)
                    eren_rocks.append(rock)
                    ROCK_FIRE_SOUND.play() 

                if event.key == pygame.K_RCTRL and len(reiner_rocks) < MAX_ROCKS:
                    rock = pygame.Rect(
                        reiner.x, reiner.y + reiner.height//2 - 2, 10, 5)
                    reiner_rocks.append(rock)
                    ROCK_FIRE_SOUND.play() 
        
            if event.type == REINER_HIT:
                reiner_health -= 1
                ROCK_HIT_SOUND.play()

            if event.type == EREN_HIT:
                eren_health -= 1
                ROCK_HIT_SOUND.play()

        winner_text = ""
        if reiner_health <= 0:
            winner_text = "Eren wins!"

        if eren_health <= 0:
            winner_text = "Reiner wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        print(eren_rocks, reiner_rocks)
        keys_pressed = pygame.key.get_pressed()
        eren_movement(keys_pressed, eren)
        reiner_movement(keys_pressed, reiner)

        handle_rocks(eren_rocks, reiner_rocks, eren, reiner)
        

        
        draw_window(eren, reiner, eren_rocks, reiner_rocks, 
        eren_health, reiner_health)

    main()

# only use in the main file
if __name__ == "__main__":
    main()

