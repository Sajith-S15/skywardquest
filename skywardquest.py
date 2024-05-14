
#import pygame library
import pygame

#importing data
import World_data as WD
import asyncio
#import pygame.locals , which gives easy access keys
from pygame.locals import *
from pygame import mixer
import pygame.locals

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
#initialize pygame library
pygame.init()

clock = pygame.time.Clock()
fps = 60

#setting up screen in px
screen_height = 700
screen_width = 1000


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Skyward Quest')

#load images
bg_img = pygame.image.load('img/game_back.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
game_name = pygame.image.load('img/GameName.png')

#load sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1,0.0,5000)
coin_sound = pygame.mixer.Sound('img/coin.wav')
coin_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('img/jump.wav')
jump_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('img/game_over.wav')
game_over_sound.set_volume(0.5)

win_sound = pygame.mixer.Sound('img/win.wav')
win_sound.set_volume(0.5)

#define font
font_score = pygame.font.SysFont('Roboto 100',38)
font1 = pygame.font.SysFont('Arial 500',70)
font2 = pygame.font.SysFont('Jersey 300',70)

#define game variables 
tile_size = 40
game_over = 0
world_data = []
main_menu = True
level = 1
max_levels = 8
score = 0

#define colors
white = (255,255,255)
blue=(0, 0, 128)

def draw_grid():
	for line in range(0, 25):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

def draw_text(text,font,text_col,x,y):
     img = font.render(text,True,text_col)
     screen.blit(img,(x,y))


#function to reset level
def reset_level(level):
      player.reset(100,screen_height-95)
      blob_group.empty()
      lava_group.empty()
      exit_group.empty()

      if level:
            if level == 1:
                  world_data = (WD.world_data1)
            elif level == 2:
                  world_data = (WD.world_data2)
            elif level == 3:
                  world_data = (WD.world_data3)
            elif level == 4:
                  world_data = (WD.world_data4)
            elif level == 5:
                  world_data = (WD.world_data5)
            elif level == 6:
                  world_data = (WD.world_data6)
            elif level == 7:
                  world_data = (WD.world_data7) 
            elif level == 8:
                  world_data = (WD.world_data8) 
      world = World(world_data)

      return world


class Button():
     def __init__(self,x,y,image):
          self.image = image
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
          self.clicked = True

     def draw(self):
          action = False
          #get mouse position
          pos = pygame.mouse.get_pos()


          #check mouse hover
          if self.rect.collidepoint(pos):
               if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked == True

          if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False
          
          #draw button
          screen.blit(self.image , self.rect)

          return action
       

class Player:
      def __init__(self,x,y):  
            self.reset(x,y)

      def update(self,game_over):
            dx=0
            dy=0
            walk_cooldown = 3

            if game_over == 0:
                  #get key presses
                  key = pygame.key.get_pressed()
                  if key[pygame.K_SPACE] and self.jump == False and self.in_air == False:
                        jump_sound.play()
                        self.vel_y = -15
                        self.jump = True
                  if key[pygame.K_SPACE] == False:
                        self.jump = False
                  if key[pygame.K_LEFT]:
                        dx -= 5 
                        self.counter += 1
                        self.direction = -1
                  if key[pygame.K_RIGHT] or key[pygame.K_5]:
                        dx += 5
                        self.counter += 1
                        self.direction = 1
                  if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
                        self.counter = 0
                        self.index = 0
                        if self.direction == 1:    
                              self.image = self.image_right[self.index]
                              if self.direction == -1:
                               self.image = self.image_left[self.index] 
                  
                  #handle animation
                  
                  if self.counter >= walk_cooldown:
                        self.counter = 0
                        self.index += 1
                        if self.index >= len(self.image_right):
                          self.index = 0
                        if self.direction == 1:    
                          self.image = self.image_right[self.index]
                        if self.direction == -1:
                          self.image = self.image_left[self.index]  
                  

                  #add gravity
                  self.vel_y += 1
                  if self.vel_y > 10:
                        self.vel_y = 10
                  dy += self.vel_y

            

                  #check for collisions
                  self.in_air = True
                  for tile in world.tile_list:
                  
                        # check for collisions in x direction
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y , self.width , self.height):
                              dx  = 0

                        # check for collisions in y direction
                        if tile[1].colliderect(self.rect.x , self.rect.y + dy , self.width , self.height):
                              #check if below ground , when jumping
                              if self.vel_y < 0:
                                    dy = tile[1].bottom - self.rect.top
                                    self.vel_y = 0
                              #check if above ground , when falling
                              elif self.vel_y >= 0:
                                    dy = tile[1].top - self.rect.bottom
                                    self.vel_y = 0
                                    self.in_air = False
                  #check for collision with enemies
                  if pygame.sprite.spritecollide(self,blob_group,False):
                        game_over = -1
                        game_over_sound.play()

                  #check for collision with lava
                  if pygame.sprite.spritecollide(self,lava_group,False):
                       game_over = -1
                       game_over_sound.play()

                  #check collision with exit
                  if pygame.sprite.spritecollide(self,exit_group,False):
                       game_over = 1
                       win_sound.play()

                  #update player co-ordinates
                  self.rect.x += dx
                  self.rect.y += dy
            elif game_over == -1:
                 self.image = self.dead_image
                 draw_text('GAME OVER!',font1,blue,(screen_width//2) - 150,100)
                 if self.rect.y > 180:
                  self.rect.y -= 5

            #draw player on screen
            screen.blit(self.image,self.rect)
            # pygame.draw.rect(screen,(255,255,255),self.rect,1)

            return game_over

      def reset(self,x,y):
            self.image_right = []
            self.image_left = []
            self.index = 0
            self.counter = 0
            for num in range(1,5):
                  img_right = pygame.image.load(f"img/guy{num}.png")
                  img_right = pygame.transform.scale(img_right,(35,70))
                  img_left = pygame.transform.flip(img_right,True,False)
                  self.image_right.append(img_right)
                  self.image_left.append(img_left)
            self.dead_image = pygame.image.load('img/demo-ghost.png')
            self.image = self.image_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jump = False
            self.direction = 0
            self.in_air = True



class World:
      def __init__(self,data):
            self.tile_list = []
            #load images
            dirt_img = pygame.image.load('img/demo-wall.png')
            grass_img = pygame.image.load('img/demo-grass1.png')
            row_count = 0
            for row in data:
                  col_count=0
                  for tile in row:
                        if tile == 1:
                              img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                              img_rect = img.get_rect()
                              img_rect.x = col_count * tile_size
                              img_rect.y = row_count * tile_size
                              tile = (img,img_rect)
                              self.tile_list.append(tile)
                        if tile == 2:
                              img = pygame.transform.scale(grass_img,(tile_size,tile_size))
                              img_rect = img.get_rect()
                              img_rect.x = col_count * tile_size
                              img_rect.y = row_count * tile_size
                              tile = (img,img_rect)
                              self.tile_list.append(tile)

                        if tile == 3:
                             blob = Enemy(col_count * tile_size , row_count * tile_size)
                             blob_group.add(blob)

                        if tile == 6:
                             lava = Lava(col_count * tile_size , row_count * tile_size+20)
                             lava_group.add(lava)

                        if tile == 7:
                             coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                             coin_group.add(coin)

                        if tile == 8:
                             exit = Exit(col_count * tile_size , row_count * tile_size-20)
                             exit_group.add(exit)
                        col_count += 1
                  row_count+=1

      def draw(self):
            for tile in self.tile_list:
                  screen.blit(tile[0],tile[1])
                  # pygame.draw.rect(screen,(255,255,255),tile[1],1)

class Enemy(pygame.sprite.Sprite):
      def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self) 
         self.image = pygame.image.load('img/blob.png')
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y
         self.move_direction = 1
         self.counter = 0

      def update(self):
          self.rect.x += self.move_direction
          self.counter += 1
          if abs(self.counter) > 32:
               self.move_direction *= -1
               self.counter *= -1

class Platform(pygame.sprite.Sprite):
      def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self) 
         image = pygame.image.load('img/platform.png')

class Lava(pygame.sprite.Sprite):
      def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self) 
         image = pygame.image.load('img/demo-lava.png')
         self.image = pygame.transform.scale(image, (tile_size,tile_size//2))
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y   


class Coin(pygame.sprite.Sprite):
      def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self) 
         image = pygame.image.load('img/coin.png')
         self.image = pygame.transform.scale(image, ((tile_size // 2)+5 ,(tile_size//2+5)))
         self.rect = self.image.get_rect()
         self.rect.center = (x,y)

class Exit(pygame.sprite.Sprite):
      def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self) 
         image = pygame.image.load('img/demo-exit4.png')
         self.image = pygame.transform.scale(image, (tile_size,int(tile_size*1.5)))
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y  



player = Player(100,screen_height-95)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing score
screen_coin = Coin(tile_size//2 , tile_size//2)
coin_group.add(screen_coin)

#load in level data and create world
if level:
            if level == 1:
                  world_data = (WD.world_data1)
            elif level == 2:
                  world_data = (WD.world_data2)
            elif level == 3:
                  world_data = (WD.world_data3)
            elif level == 4:
                  world_data = (WD.world_data4)
            elif level == 5:
                  world_data = (WD.world_data5)
            elif level == 6:
                  world_data = (WD.world_data6)
            elif level == 7:
                  world_data = (WD.world_data7) 
            elif level == 8:
                  world_data = (WD.world_data8) 
world = World(world_data)

#button instances
restart_button = Button(screen_width //2 - 50 , screen_height //2 + 100, restart_img)
start_button = Button(screen_width //2 - 350 , screen_height //2 , start_img )
exit_button = Button(screen_width //2 + 100 , screen_height //2, exit_img )
#set up condition for run until user quits
running = True

# Define an async function to run the Pygame loop
async def main():
    
    global main_menu,world,game_over,score,level
    # Initialize Pygame
    pygame.mixer.pre_init(44100,-16,2,512)
    mixer.init()
    pygame.init()
    
    # Set up Pygame variables and objects
    
    running = True
    while running:
        clock.tick(fps)
        screen.blit(bg_img, (0, 0))

        if main_menu:
            screen.blit(game_name,(200,20))
            # Draw and handle main menu
            if exit_button.draw():
                running = False
            if start_button.draw():
                main_menu = False
        else:
            world.draw()
            
            if game_over == 0:
                blob_group.update()

                # Update score
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 1
                    coin_sound.play()
                draw_text('X '+str(score), font_score, white, tile_size, 5)
                draw_text('Level '+str(level), font_score, white, tile_size+850, 5)
                draw_text('SKYWARD QUEST',font_score,white,(screen_width//2)-100,5)
            blob_group.draw(screen)
            lava_group.draw(screen)
            coin_group.draw(screen)
            exit_group.draw(screen)
            game_over = player.update(game_over)

            if game_over == -1:
                if restart_button.draw():
                    world = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

            # Player has completed
            if game_over == 1:
                # Reset game and go to the next level
                level += 1
                if level <= max_levels:
                    # Reset level
                    world = []
                    world = reset_level(level)
                    game_over = 0
                else:
                    draw_text('YOU WIN!', font1, blue, screen_width//2-(100),100)
                    draw_text('Score : '+ str(score), font_score, blue, screen_width//2 - (50),5)
                    if restart_button.draw():
                        level = 1
                        world = []
                        world = reset_level(level)
                        game_over = 0
                        score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        await asyncio.sleep(0)  # Allow other asyncio tasks to run

# Run the Pygame loop within an asyncio event loop
asyncio.run(main())



