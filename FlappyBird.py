import pygame #biblioteca usada para criacao de jogos em python
import os #biblioteca para integrar o codigo com os arquivos do computador (imgs)
import random #biblioteca para gerar valores aleatorios (usado na geracao dos canos)

SCREEN_HEIGH = 500
SCREEN_WIDTH = 800

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMG_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMGS_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONT_SCORE = pygame.font.SysFont('Arial', 50)


class Bird:
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
    
    def draw(self, screen):
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
        rotate_img = pygame.transform.rotate(self.img, self.angle) #rotaciona a imagem
        center_img = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotate_img.get_rect(center = center_img)
        screen.blit(rotate_img, rectangle.topleft)
        
    #método para criar uma mascara no pássaro e evitar colisões em que nao houve contato de fato
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
        
        
class Pipe:
    DISTANCE = 200 # distancia entre o cano de cima e o de baixo
    SPEED = 5 # nesse código, o cano que se movimenta para trás, e o pássaro fica parado no eixo y
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.bottom_position = 0
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
        self.PIPE_BOTTOM = IMG_PIPE
        self.overtook = False
        self.define_height()
        
    def define_height(self):
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.PIPE_TOP.get_height()
        self.bottom_position = self.height + self.DISTANCE
        
    def move(self):
        self.x -= self.SPEED
    
    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_position))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom_position))
    
    def colision(self, bird):
        
        # pega a máscara do pássado, cano de cima e cano de baixo, verifica se há uma sobreposição entre elas, e retorna o resultado
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        bottom_distance = (self.x - bird.x, self.bottom_position - round(bird.y))
        
        top_colision = bird_mask.overlap(top_mask, top_distance)
        bottom_colision = bird_mask.overlap(bottom_mask, bottom_distance)
        
        if top_colision or bottom_colision:
            return True
        else:
            return False
        
class Base:
    SPEED = 5
    WIDTH = IMG_BASE.get_width()
    IMG = IMG_BASE
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED
        
        #se saiu da tela
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self, screen):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))
        
def draw_screen(screen, birds, pipes, base, score):
    screen.blit(IMG_BG, (0, 0))
    for bird in birds:
        bird.draw(screen)
        
    for pipe in pipes:
        pipe.draw(screen)
        
    text = FONT_SCORE.render(f"Pontuação: {score}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    
    base.draw(screen)
    pygame.display.update()
    
def main():
    birds = [Bird(230, 250)]
    base = Base(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_HEIGH, SCREEN_WIDTH))
    score = 0
    clock = pygame.time.Clock()
    
    playing = True
    while playing:
        clock.tick(30)
        
        # interação com o jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
        
        # movimento dos objetos
        for bird in birds:
            bird.move()
        base.move()
        
        add_pipe = False
        remove_pipes = []
        
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colision(bird):
                    birds.pop(i)
                
                if not pipe.overtook and bird.x > pipe.x:
                    pipe.overtook = True
                    add_pipe = True 
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for pipe in remove_pipes:
            pipes.remove(pipe)
        
        for i, bird in enumerate(birds):
            if (bird.y + bird.img.get_height()) > base.y or bird.y < 0:
                birds.pop(i)
                
        
        draw_screen(screen, birds, pipes, base, score)
        
        
if __name__ == '__main__':
    main()