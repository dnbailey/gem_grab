import random

''' Setup '''

''' Globals '''
game_over = False
score = 0
lives = 3
WIDTH = 500
HEIGHT = 700
center_x = WIDTH/2
center_y = HEIGHT/2

''' Start the Music '''
music.play('8bit')

''' Player '''
player = Actor('idle')
player.pos = midbottom=(center_x, HEIGHT - 96)
player.frame = 1
player.speed = 8

def player_run_animation():
    if player.frame < 2:
        player.frame += 0.25
    else:
        player.frame = 1
    
    player.image = f'walk{int(player.frame)}'
    
def player_move():
    player.image = 'idle'
    if keyboard.left and player.left > 0:
        player_run_animation()
        player.x -= player.speed
    elif keyboard.right and player.right < WIDTH:
        player_run_animation()
        player.x += player.speed
        
''' Gems '''
gems = []
number_of_gems = 5

def gem_spawn():
    gems.append(Actor('gem', pos=(random.randint(0, WIDTH), 0)))

def fall(gem):
    if gem.y < 620:
        gem.y += 4

for i in range(number_of_gems):
    clock.schedule(gem_spawn, i)
    
''' Blades '''
blades = []
number_of_blades = 3

def blade_spawn():
  blades.append(Actor('blade', pos=(random.randint(0, WIDTH), 0)))

def drop(blade):
    if blade.y > HEIGHT:
        blade.y = 0 - 64
    blade.angle += 3
    blade.y += 2

for i in range(number_of_blades):
    clock.schedule(blade_spawn, i*5)

''' Game '''
def draw():
    screen.clear()
    screen.fill((0,100,200))

    player.draw()
    
    if not game_over:
        for gem in gems:
            gem.draw()
        
        for blade in blades:
            blade.draw()
    else:
        screen.draw.text("Game Over", center=(center_x, center_y), fontname='mini_square', fontsize=48)
        player.image = 'hit'
        music.fadeout(1.0)
    
    # Draw the Ground
    for i in range(8):
        screen.blit(images.ground, (i*images.ground.get_width(), HEIGHT - images.ground.get_width()))
    
    screen.draw.text(f"Score: {score}", midtop=(center_x, 10), fontname='mini_square', fontsize=32)
    screen.draw.text("Dodge the blades and collect the gems", midbottom=(center_x, 685), fontname='mini_square', fontsize=14)
    

def update():
    global score
    global game_over
    
    if not game_over:
        for gem in gems:
            fall(gem)

            if player.colliderect(gem):
                score += 1
                gem.pos = (random.randint(0, WIDTH), 0)
        
        for blade in blades:
            drop(blade)

            if player.colliderect(blade):
                game_over = True
                        
        player_move()
