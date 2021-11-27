import pygame
import random
from time import sleep
import sys


#전역 변수 선언
screen_width = 480
screen_height = 640
bear_width = 53
bear_height = 111
trash1_width = 39
trash1_height = 22
d_count = 0
bear_num = 3

# 게임 초기화
def startGame():
    global screen, clock, bear, ice, trash1

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Save The Earth')
    bear = pygame.image.load('bear.png')
    trash1 = pygame.image.load('trash1.png')
    ice = pygame.image.load('ice.png')
    clock = pygame.time.Clock()

# 화면에 객체 그리기
def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))

# 충돌
def explode():
    pygame.display.update()
    sleep(3)
    runGame()

# 점수 출력
def showScore(count):
    global screen
    font = pygame.font.SysFont('NanumGothic.ttf', 40)
    text = font.render("Score: " + str(count),True, (0, 0, 255))
    screen.blit(text, (0,0))

# 게임 오버
def gameOver():
    global screen
    font = pygame.font.SysFont('NanumGothic.ttf', 60)
    if d_count == 50:
        text = font.render("Misssion Complete!", True, (0, 255, 0))
        screen.blit(text, (screen_width/2-210, screen_height/2-30))
        
    elif bear_num == 0:
        text = font.render("Game Over!",True, (255, 0, 0))
        screen.blit(text, (screen_width/2-150, screen_height/2-30))
    
    pygame.display.update()
    sleep(2)
    runGame()

        
#게임 실행 함수
def runGame():
    global d_count, bear_num

    # 얼음 리스트 생성
    ice_xy = []

    # 곰 좌표
    x = screen_width * 0.40
    y = screen_height * 0.75
    x_change = 0
    
    # 쓰레기 초기 위치
    trash1_x = random.randrange(0, screen_width - trash1_width)
    trash1_y = 0
    trash1_speed = 3
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 3

                elif event.key == pygame.K_RIGHT:
                    x_change += 3

                elif event.key == pygame.K_SPACE:
                    if len(ice_xy) <2:
                        ice_x = x + bear_width/2
                        ice_y = y - bear_height/4
                        ice_xy.append([ice_x,ice_y])

           
        screen.fill((255, 255, 255))


        # 곰 이동 범위 제한
        x += x_change
        if x < 0:
            x = 0
        elif x > screen_width - bear_width:
            x = screen_width - bear_width

        # 충돌 체크
        if y < trash1_y + trash1_height:
            if trash1_x > x and trash1_x < x + bear_width:
               bear_num -= 1
               explode()

        # 게임 오버 조건     
        if bear_num == 0:
            gameOver()
        if d_count == 50:
            gameOver()
                  
           
                
        drawObject(bear, x, y)

        # 얼음 이동
        if len(ice_xy) != 0:
            for i, bxy in enumerate(ice_xy):
                bxy[1] -= 10
                ice_xy[i][1] = bxy[1]

                if bxy[1] < trash1_y:
                    if bxy[0] > trash1_x and bxy[0] < trash1_x + trash1_width:
                        ice_xy.remove(bxy)
                        trash1_x = random.randrange(0, screen_width - trash1_width)
                        trash1_y = 0
                        d_count += 10

              
                if bxy[1] <= 0:
                    try:
                        ice_xy.remove(bxy)
                    except:
                        pass
        if len(ice_xy) != 0:
            for bx, by in ice_xy:
                drawObject(ice, bx, by)

        showScore(d_count)       

        # 쓰레기 이동
        trash1_y += trash1_speed
        if trash1_y > screen_height:
            trash1_y = 0
            trash1_x = random.randrange(0, screen_width - trash1_width)

        drawObject(trash1, trash1_x, trash1_y)   
       
        pygame.display.update()
        clock.tick(60)

    


startGame()
runGame()
