import pygame 
from pygame.locals import *
import random


pygame.init()  # Inicializuje (spustí) všetky moduly pygame

clock = pygame.time.Clock()
fps = 60 #rychlosť hry

#velkosť okna
screen_width = 864
screen_height = 768


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird") #nazov okna hry

#definicia fontu pisma
font = pygame.font.SysFont("Bauhaus 93", 60) #velkosť písma

#definicia farby
white = (255,255,255) #RGB samozrejme

#definicie hernych premennych
scroll_speed = 4 #rychlosť pohybu stlpov (ked dam 1, su natlacene na sebe)
flying = False
game_over = False
pipe_gap = 220 #medzera medzi stlpmi
pipe_frequency = 1500 #milisekundy (kolko ms ubehne pokiaľ sa objaví dalsi nový stlp)
last_pipe = pygame.time.get_ticks() - pipe_frequency #vrati pocet ms odkedy pygame.init() bolo zavolané
score = 0 # cislo skore (musi zacinat od nuly)
pass_pipe = False

#loadovanie obrazkov
bg = pygame.image.load("img/bg.png")
button_img = pygame.image.load("img/restart.png")

#funkcia na ukazovanie textu na obrazovke
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# reštart hry 
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100 #vzdialenosť obrazovky za vtakom
    flappy.rect.y = int (screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 2
        self.counter = 0
        for num in range (1,4): #tu mi loaduje obrazky ako animaciu vtaka (1,2,3,1,2,3,...)
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            
        #aplikovanie gravitacie
            self.vel += 0.5 #velkost vysky vyskoku po kliknuti mysou 
            if self.vel > 8: #rychlost padu smerom dole
                self.vel = 8 #rychlost padu (ked dam 80, hned spadne)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)


        if game_over == False:
            #skok
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #ine ako 1 (vtak neskace pri kliku, pada)
                self.clicked = True
                self.vel = -10 #ako vysoko vtak skace
            if pygame.mouse.get_pressed()[0] == 0: #ak 1 a drzim klik, vtak stupa. Ine = pada (pri kliku nejde hore)
                self.clicked = False
                
            #animacia
            self.counter += 1 #rychlost striedania animacii
            flap_cooldown = 5 #cim vacsie cislo, tym dlhsia doba striedania animacii

            if self.counter > flap_cooldown:
                self.counter = 0 #vacsie cislo = rychlejsie mavanie kridlom
                self.index += 1 #vacsie cislo - neanimuje
                if self.index >= len(self.images):
                    self.index = 0 #zacina to nulou
            self.image = self.images[self.index]

    
            #rotacia vtaka
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1.5)  # ako sa vtak naklana pri lete (ked dam 8 tak sa až otáča,..)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) #stupne, ako vtak spadne na zem (pri 10 takmer vodorovne a pri 90 zobakom dole)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # Premenná position určuje, či stlp prichádza zdola alebo zhora
        #pozicia 1 je od vrchu, -1 je od spodu
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)] #(možno) výška stlpu od steny (cim mensie cislo, tym menej stlp vidno) - ###proste zmeni medzeru medzi stlpmi
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    #rychlost scrollu hry - ako postupuju stlpy v hre 
    def update(self):
            self.rect.x  -= scroll_speed
            if self.rect.right < 0: #kedy stlpy zanikaju vlavo - 500 (cca v polke obrazovky)
                self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        
        action = False

        #dostane poziciu myši
        pos = pygame.mouse.get_pos()

        #skontroluje, či je myš na buttone
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:  #1, inak nejde klik button
                action = True



        # nakreslí button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_height / 2)) #prve cislo - vzdialoenost vtaka od laveho boku obrazovky ##druhe kde na zaciatku 1. hry je vtak

bird_group.add(flappy)

#vytvorí reštart button
button = Button(screen_width //2 - 50, screen_height // 2 - 100, button_img) #pozicia buttonu



run = True
while run: 


    clock.tick(fps)

    #nakresli pozadie
    screen.blit(bg, (0,0))

    #nakresli assety na pozadie 
    bird_group.draw(screen)
    pipe_group.draw(screen)

    bird_group.update()


    #kontroluje skore
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1 #pridavanie skore ked prejdem stlp
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #hlada koliziu
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

        
    #skontroluje, či vtak narazil na zem
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generuje nove stlpy
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        
        
        pipe_group.update()

    #skontroluje, či hra skončila a reštartuje hru
    if game_over == True:
        if button.draw():
            game_over = False
            score = reset_game()
            


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
            flying = True


    pygame.display.update()   


pygame.quit()
