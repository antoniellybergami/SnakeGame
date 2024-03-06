import pygame, random
from pygame.locals import *

# Funções auxiliares
def on_grid_random(): #posição aleatória 
    x = random.randint(0,59)
    y = random.randint(0,59)
    return (x * 10, y * 10)

def collision(c1, c2): #verifica se a cobra colidiu 
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Macros para controle de movimento.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init() #inicio do jogo
screen = pygame.display.set_mode((600, 600)) #define tamanho de tela
pygame.display.set_caption('Snake') 

#musica de fundo
pygame.mixer.music.set_volume(0.1) 
bgm = pygame.mixer.music.load('Desktop\Trab Multimídia - Antonielly\som.wav')
pygame.mixer.music.play(-1)

#outros sons
gameover_sound = pygame.mixer.Sound('Desktop\Trab Multimídia - Antonielly\derrota.wav')
eating_sound = pygame.mixer.Sound('Desktop\Trab Multimídia - Antonielly\comeu.wav')

#Info da cobra
snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((255,255,255)) #Branco

#info da maça
apple_pos = on_grid_random() #posição inicial da maça
apple = pygame.Surface((10,10)) 
apple.fill((255,0,0)) #vermelho

my_direction = LEFT #direção da cobra

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

#rodar o jogo
game_over = False
while not game_over: #jogo vai ser infinito enquanto n der game over
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

#controle da cobra
        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    #Cobra comer maça 
    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random() #surgir outra maça
        snake.append((0,0)) #aumenta o tamanho da cobra
        eating_sound.play() #toca som
        score = score + 1 #aumenta pontuação
        
    #Checa se a cobra colidiu com as paredes
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0: #verifica as posições das estremidades (parede)
        game_over = True #acaba game
        pygame.mixer.music.stop() 
        gameover_sound.play()
        break
    
    #Checa se a cobra colidiu com ela mesma
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True #acaba game
            break

    if game_over: 
        pygame.mixer.music.stop()
        gameover_sound.play()
        break
    
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
        
    # Faz a cobra se mover.
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])
    
    #tela
    screen.fill((0,50,0)) #fundo
    screen.blit(apple, apple_pos) #oq aparece
    
    #linhas da matriz 
    for x in range(0, 600, 10): # Desenha linhas da grade em x
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10): # Draw linhas da grade em y
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))
    
    score_font = font.render('Pontos: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (600 - 120, 10)
    screen.blit(score_font, score_rect)
    
    for pos in snake:
        screen.blit(snake_skin,pos)

    pygame.display.update() #atualiza oq acontece na tela

#tela de gameover
while True: 
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Fim de Jogo!', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 250)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
