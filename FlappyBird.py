import pygame #biblioteca usada para criacao de jogos em python
import os #biblioteca para integrar o codigo com os arquivos do computador (imgs)
import random #biblioteca para gerar valores aleatorios (usado na geracao dos canos)

SCREEN_HEIGH = 800
SCREEN_WIDTH = 300

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bd.png')))
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMGS_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONT_SCORE = pygame.font.SysFont('Arial', 50)


Class Bird:
    IMGS = IMGS_BIRD
    #animacoes de rotacao
    ROTATE_MAX = 25
    ROTATE_SPEED = 20
    ANIMATION_TIME = 5
    
    #construtor
    def __init__(self, x, y):
        self.x = x #posicao eixo x
        self.y = y #posicao eixo y
        self.angle = 0 #angulo de rotacao
        self.speed = 0 #velocidade (vertical - eixo y)
        self.height = self.y #altura
        self.time = 0 #tempo de duracao da animacao de movimento 
        self.num_img = 0 #numero da imagem atual do vetor de imagens do passaro
        self.img = self.IMGS[0] #imagem atual

    def jump(self):
        self.speed = -10.5 #velocidade negativa para subir, pois está indo para cima no eixo y (eixo y é invertido na lógica do programa)
        self.time = 0 #tempo para calculo do deslocamento (displacement)
        self.height = self.y
        
    def move(self):
        #calcular deslocamento 
        self.time += 1 #essa funcao eh executada a cada 1 unidade de tempo do jogo (cada frame)
        displacement = 1.5 * (self.time**2) + self.speed * self.time # S = So + VoT + (AT^2)/2
        
        #restringir deslocamento, nao permite que o passaro acelere infinitamente para baixo ou para cima
        if displacement > 16:
            displacement = 16 #deslocamento maximo de 16 pixels
        elif displacement < 0:
            displacement -= 2
            
        self.y += displacement #apos os calculos, deslocar de fato o passaro
        
        #angulo do passaro
        if displacement < 0 or self.y < (self.height + 50): #caso esteja deslocando para cima, estara com o angulo maximo
            if self.angle < self.ROTATE_MAX:
                self.angle = self.ROTATE_MAX
        
        else: #caso contrario, sera subtraido o "rotate speed"
            if self.angle > -90:    
                self.angle -= self.ROTATE_SPEED 
    
    def draw(self):
        #definir qual imagem do passaro usar
        self.num_img += 1
        
        #altera a imagem do passaro a cada 5 tempos/frames para gerar a animacao de bate asa
        if self.num_img < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.num_img < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.num_img < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.num_img < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.num_img >= self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.num_img = 0
            
        #caso o passaro esteja caindo, nao havera animacao de "bater asa"
        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.num_img = self.ANIMATION_TIME*2 
        
        #desenhar imagem
        
        
        
        
        
Class Pipe:
    pass

Class Base:
    pass