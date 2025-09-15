import pygame
import pickle
import random

pygame.init()
pygame.font.init()

class Window():
    width = 1280
    height = 720
    fps = 60

class Game():
    run = True
    pause = True
    start = True

class Pipe():
    width = 100
    height = 150
    speed = 16
    count = 0
    count1 = 0
    p1_x = 0
    p1_y = 0
    count2 = -Window.width/3
    p2_x = 0
    p2_y = 0
    count3 = -2 * Window.width/3
    p3_x = 0
    p3_y = 0
    colors = [pygame.Color(255,0,0),pygame.Color(0,255,0),pygame.Color(0,0,255),pygame.Color(0,0,0)]
    p1_color = ''
    p2_color = ''
    p3_color = ''

screen = pygame.display.set_mode(size=(Window.width,Window.height), flags=(pygame.FULLSCREEN | pygame.SCALED))


clock = pygame.time.Clock()
class DT():
    dt = clock.tick(Window.fps)/1000

class Player():
    x_pos = Window.width/20
    y_pos = Window.height/2
    rad = 25
    g = 1750
    j = -500
    v = j
    color = pygame.Color((255,255,255))
    rect = pygame.Rect(x_pos-rad, y_pos-rad, rad * 2, rad * 2)
    score = 0
    h_score = 0
    l_score = 0

try:
    with open("flappysave.pkl", "rb") as f:
        Player.h_score = pickle.load(f)
except:
    Player.h_score = 0

def main():
    print(random.choice(Pipe.colors))
    while Game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.run  = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.pause = True
                if event.key == pygame.K_SPACE:
                    jump()
                    
            
        if Game.pause == True:
            pause()
    
        gravity()
        boarder()


        pygame.Surface.fill(screen, (0,128,255))
        pipe()
        score()
        pygame.draw.circle(screen, Player.color, (Player.x_pos,Player.y_pos) ,Player.rad)
        pygame.display.flip()
        clock.tick(Window.fps)
    
def pause():
    option = 1
    while Game.pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.run = False
                Game.pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.pause = False
                if event.key == pygame.K_DOWN:
                    if option < 2:
                        option += 1
                if event.key == pygame.K_UP:
                    if option > 1:
                        option -= 1
                if event.key == pygame.K_SPACE:
                    if option == 1:
                        Game.pause = False
                        Game.start = False
                    if option == 2:
                        Game.run = False
                        Game.pause = False

        pygame.Surface.fill(screen, (100,100,100))

        option1_x = 50
        option1_y = 2*Window.height/20
        option2_x = 50
        option2_y = 10*Window.height/20
        
        pygame.draw.rect(screen, (0,0,0), (option1_x,option1_y,200,50))
        pygame.draw.rect(screen, (0,0,0), (option2_x,option2_y,200,50))
        if option == 1:
            pygame.draw.rect(screen, (255,255,255), (option1_x,option1_y,200,50), width=2)
        if option == 2:
            pygame.draw.rect(screen, (255,255,255), (option1_x,option2_y,200,50), width=2)

        if Game.start == True:
            text1 = "Start"
        elif Game.pause == False:
            text1 = ""
        else:
            text1 = "Resume"
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_surface1 = font.render(text1, True, (255,255,255))
        screen.blit(text_surface1, dest=(option1_x+10,option1_y+10))
        text_surface2 = font.render("Exit", True, (255,255,255))
        screen.blit(text_surface2, dest=(option2_x+10,option2_y+10))


        h_score = (f"Best: {str(Player.h_score)}")
        l_score = (f"Last: {str(Player.l_score)}")
        font2 = pygame.font.Font(pygame.font.get_default_font(), 100)
        text_surface3 = font2.render(h_score, True, (255,255,255))
        screen.blit(text_surface3, dest=(12*Window.width/20,Window.height/20))
        text_surface4 = font2.render(l_score, True, (255,255,255))
        screen.blit(text_surface4, dest=(12*Window.width/20,10*Window.height/20))
        
        pygame.display.flip()
        clock.tick(Window.fps)


def jump():
    Player.v = Player.j

def gravity():
    Player.v += Player.g * DT.dt
    if Player.v > -Player.j * 2:
        Player.v = -Player.j * 2
    Player.y_pos += Player.v * DT.dt

def boarder():
    if Player.y_pos > Window.height - Player.rad:
        end()
    if Player.y_pos < -2 * Player.rad:
        Player.y_pos = -2 * Player.rad

def end():
    Game.start = True
    Game.pause = True
    Player.x_pos = Window.width/20
    Player.y_pos = Window.height/2
    Pipe.speed = 16
    Pipe.count = 0
    Pipe.count1 = 0
    Pipe.p1_x = 0
    Pipe.p1_y = 0
    Pipe.count2 = -Window.width/3
    Pipe.p2_x = 0
    Pipe.p2_y = 0
    Pipe.count3 = -2*Window.width/3
    Pipe.p3_x = 0
    Pipe.p3_y = 0
    Player.l_score = int(Player.score/13)
    if Player.l_score > Player.h_score:
        Player.h_score = Player.l_score
    Player.score = 0
    jump()

def pipe():
    if Pipe.p1_x + 100 <= 0:
        Pipe.p1_x, Pipe.p1_y, Pipe.count1, Pipe.p1_color = new_pipe()
    Pipe.p1_x = Window.width - Pipe.count1    

    if Pipe.p2_x + 100 <= 0:
        Pipe.p2_x, Pipe.p2_y, Pipe.count2, Pipe.p2_color = new_pipe()
    Pipe.p2_x = Window.width - Pipe.count2

    if Pipe.p3_x + 100 <= 0:
        Pipe.p3_x, Pipe.p3_y, Pipe.count3, Pipe.p3_color = new_pipe()
    Pipe.p3_x = Window.width - Pipe.count3

    if Pipe.count >= Window.width + 100:
        Pipe.speed = 4
        draw_pipe(Pipe.p1_x,Pipe.p1_y,Pipe.p1_color)
    if Pipe.count >= Window.width + Window.width/3 + 100:
        draw_pipe(Pipe.p2_x,Pipe.p2_y,Pipe.p2_color)
    if Pipe.count >= Window.width + 2 * Window.width/3 + 100:
        draw_pipe(Pipe.p3_x,Pipe.p3_y,Pipe.p3_color)
    else:
        Pipe.count += Pipe.speed

    Pipe.count1 += Pipe.speed
    Pipe.count2 += Pipe.speed
    Pipe.count3 += Pipe.speed

def new_pipe():
    y_pos = random.randint(int(Window.height/20), int(19*Window.height/20 - 150))
    x_pos = Window.width
    color = random.choice(Pipe.colors)
    return x_pos, y_pos, 0, color

def draw_pipe(pipe_x,pipe_y,color_val):
    top_pipe = 0
    top_length = pipe_y
    bottom_pipe = pipe_y + Pipe.height
    bottom_length = Window.height - bottom_pipe

    color_val = (0,255,0)

    top_rect = pygame.Rect(pipe_x,top_pipe-2*Player.rad,Pipe.width,top_length+2*Player.rad)
    bottom_rect = pygame.Rect(pipe_x,bottom_pipe,Pipe.width,bottom_length)
    pygame.draw.rect(screen,color_val, (pipe_x,top_pipe,Pipe.width,top_length))
    pygame.draw.rect(screen,color_val, (pipe_x,bottom_pipe,Pipe.width,bottom_length))

    line = pygame.Rect(pipe_x+Pipe.width, -100, 1, Window.height+100)

    Player.rect = pygame.Rect(Player.x_pos-Player.rad, Player.y_pos-Player.rad, Player.rad * 2, Player.rad * 2)
    #pygame.draw.rect(screen,(0,0,0),(int(Player.x_pos-Player.rad), int(Player.y_pos-Player.rad), int(Player.rad*2),int(Player.rad*2)))

    
    if Player.rect.colliderect(top_rect):
        end()
    if Player.rect.colliderect(bottom_rect):
        end()

    if Player.rect.colliderect(line):
        Player.score += 1

def score():
    text = str(int(Player.score/13))
    font = pygame.font.Font(pygame.font.get_default_font(), 100)
    text_surface1 = font.render(text, True, (255,255,255))
    screen.blit(text_surface1, dest=(2*Window.width/20,Window.height/20))




if __name__ == "__main__":
    main()
    with open("flappysave.pkl", "wb") as f:
        pickle.dump(Player.h_score, f)

    pygame.quit()