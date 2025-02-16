import pygame
from pygame.locals import *
import random
import os
import pygame.freetype

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

GAME_FONT = pygame.freetype.Font(os.path.join(os.getcwd(), "PygameFont.ttf"), 48)

# Character variables
CharacterPos = [500, 400, 100, 100]
TargetY = CharacterPos[1] - 200
Jumping = False
JumpStrength = 20
GravityStrength = 1
CharacterType = 0 # Tells what character sprite needs to be used
Colided = False

# Rock variables
RockPositions = []
DefaultRockPos = [1280, 450, 50, 50]


# Images
image_path = os.path.join(os.getcwd(), "VideoGameBackground.png")
bg = pygame.image.load(image_path)

JumpCharacter_path = os.path.join(os.getcwd(), "SpriteFalling.png")
JumpCharacter = pygame.image.load(JumpCharacter_path)

SpriteRun1_path = os.path.join(os.getcwd(), "SpriteRun1.png")
SpriteRun1 = pygame.image.load(SpriteRun1_path)

SpriteRun2_path = os.path.join(os.getcwd(), "SpriteRun2.png")
SpriteRun2 = pygame.image.load(SpriteRun2_path)

SpriteHurt_Path = os.path.join(os.getcwd(), "SpriteHurt.png")
SpriteHurt = pygame.image.load(SpriteHurt_Path)

Icon_path = os.path.join(os.getcwd(), "The Run of Tuxedo Man.png")
Icon = pygame.image.load(Icon_path)

Banner_Path = os.path.join(os.getcwd(), "Text_Banner.png")
Banner = pygame.image.load(Banner_Path)

colisionDebounce = 0

score = 0

Playing = False

Button_text = "Play"
Top_text = "Score: " + str(score)


while running:
    screen.fill([255, 255, 255])
    screen.blit(bg, (0,0))
    
    pygame.display.set_caption('The Run of Tuxedo Man')
    pygame.display.set_icon(Icon)
    
    # Top Banner and points
    screen.blit(Banner, [340, 50, 680, 200])
    
    
    text_surface, rect = GAME_FONT.render("The Run of Tuxedo Man", (0, 0, 0))
    screen.blit(text_surface, (430, 102))
    
    if Playing:
         text_surface, rect = GAME_FONT.render("Score: " + str(score), (0, 0, 0))
    else:
         text_surface, rect = GAME_FONT.render(Top_text, (0, 0, 0))
    screen.blit(text_surface, (550, 150))
    
    # Play(again) Button
    if not Playing:
         BottomBanner = pygame.transform.scale(Banner, (340, 100))
         screen.blit(BottomBanner, [470, 600, 340, 100])
    
         text_surface, rect = GAME_FONT.render(Button_text, (0, 0, 0))
         screen.blit(text_surface, (540, 630))
    
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if Playing:
                 if not Jumping:
                    Jumping = True
                    JumpStrength = 4
                    GravityStrength = 15
            else:
                 # Play Button Click Detection
                 x, y = pygame.mouse.get_pos()
                 if x > 470 and x < 810:
                      if y > 600 and y < 700:
                           Playing = True
                           Colided = False
                           score = 0

    # Random rock spawning
    if random.randint(1, 150) == 50:
        RockPositions.append(DefaultRockPos.copy())  # Copy to avoid modifying the original list

    # Update and draw rocks
    new_positions = []
    for RockPos in RockPositions:
        RockPos[0] -= 5  # Move rock left
        pygame.draw.rect(screen, (105, 105, 105), RockPos, 0, 25)

        # Keep only rocks that are still visible on screen
        if RockPos[0] + RockPos[2] > 0:
            new_positions.append(RockPos)
            
        # Colisions
        
        if colisionDebounce == 0:
               if RockPos[0] < 400 and RockPos[0] > 300:
                    if CharacterPos[1] > 400:
                         colisionDebounce = 1
                         Colided = True
                         Playing = False
                         Button_text = "Play Again"
                         Top_text = "You Died, Score: " + str(score)
                    if CharacterPos[1] < 400:
                         score += 1
                         colisionDebounce = 1
               
        if colisionDebounce > 0:
          colisionDebounce += 1
          if colisionDebounce >= 40:  # Resets debounce
               colisionDebounce = 0
               
        color = (105, 105, 105)
          
        pygame.draw.rect(screen, color , RockPos, 0, 25)

            

    RockPositions = new_positions  # Update list
    
    

    # Character jump logic
    if Jumping:
        if CharacterPos[1] > TargetY:
            CharacterPos[1] -= JumpStrength
            JumpStrength -= 0.08
            screen.blit(JumpCharacter, CharacterPos) # Jump Sprite Rendering
        else:
            Jumping = False
    elif not Jumping:
         # Character Sprite Rendering
         if not Colided:
              if CharacterType <= 10:
                    screen.blit(SpriteRun1, CharacterPos)
                    CharacterType += 1
              elif CharacterType > 10 and CharacterType < 25:
                    screen.blit(SpriteRun2, CharacterPos)
                    CharacterType += 1
              elif CharacterType >= 25:
                    screen.blit(SpriteRun1, CharacterPos)
                    CharacterType = 0
         if Colided:
              screen.blit(SpriteHurt, CharacterPos)
              Playing = False
          
         
            

    # Gravity effect
    if CharacterPos[1] >= 400:
        Jumping = False
    elif not Jumping and CharacterPos[1] < 400:
        CharacterPos[1] += GravityStrength
        GravityStrength += 0.4



    # Render updated display
    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
