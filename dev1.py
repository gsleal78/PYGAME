import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 750
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('JetInsper')

# Aqui importamos as imagens e variáveis de dimensões do arquivo definindo_imagens.py
from definindo_imagens import imagens, variaveis_dimensoes,texto_inicial,fonte_moeda

# Carrega os sons do jogo
pygame.mixer.music.load('assets/snd/Jetpack Joyride OST 🎼🎹 - Main Theme.mp3')
pygame.mixer.music.set_volume(0.4)
coin_sound = pygame.mixer.Sound('assets/snd/Mario Som Moedas ♪ 🔥🤑Olhe A Descrição 🤑🔥.mp3')
eletric_sound = pygame.mixer.Sound('assets/snd/Electric Zap 001 Sound Effect (mp3cut.net).mp3')

game_started = False  # Define o estado inicial do jogo como False

clock = pygame.time.Clock()
FPS = 60

background_i = imagens["background_i"]
logo = imagens["logo"]
background = imagens["TESTLAB"]
BARRY = imagens["barry_v_img"]
TIRO = imagens["tiro_img"]
LASER1 = imagens["CHOQUE1_img"]
LASER2 = imagens["CHOQUE2_img"]
LASER_LISTA = [LASER1,LASER2]
moedas_coletadas = 0 

class barry(pygame.sprite.Sprite):
    def __init__(self, img, x, y, moedas_coletadas):  
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y  
        self.rect.bottom = y + 75  
        self.speedx = 0
        self.speedy = 0
        self.last_shot = pygame.time.get_ticks()  
        self.shoot_delay = 75  
        self.shooting = False
        self.moedas_coletadas = moedas_coletadas  # A quantidade de moedas coletadas é passada como parâmetro

        # Criar uma máscara de colisão precisa
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0
        if self.shooting and pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.shoot()

    def shoot(self):
        new_bullet = tiro(TIRO, self.rect.bottom+75, self.rect.centerx)  
        all_sprites.add(new_bullet)  
        all_bullets.add(new_bullet)  
        self.last_shot = pygame.time.get_ticks()

class tiro(pygame.sprite.Sprite): 
    def __init__(self,img, bottom, centerx): 
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = 15

    def update(self): 
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  
            self.kill()  

all_sprites = pygame.sprite.Group()
voando = barry(BARRY, 50,750, moedas_coletadas)  # Passando moedas_coletadas como parâmetro
all_sprites.add(voando)
all_bullets = pygame.sprite.Group()

class Moeda(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5  # Movimento para a esquerda
        if self.rect.right < 0:  # Se a moeda sair completamente da tela
            self.kill()  # Remover a moeda
        
        if pygame.sprite.collide_mask(self, voando):
            voando.moedas_coletadas += 1  # Aumenta a contagem de moedas
            self.kill()  # Remove a moeda
            coin_sound.play()
num_conjuntos = 1
all_moedas = pygame.sprite.Group()

# Função para criar um novo conjunto de moedas
def criar_moedas():
    for _ in range(num_conjuntos):
        # Posição aleatória do centro do grupo de moedas
        center_x = random.randint(WIDTH, WIDTH + 200)
        center_y = random.randint(100 + 3*variaveis_dimensoes["MOEDAS_HEIGHT"], HEIGHT - 100 - 3*variaveis_dimensoes["MOEDAS_HEIGHT"])

        # Calcula as posições das moedas em torno do centro
        positions = [
            (center_x - 20, center_y - 20),
            (center_x + 20, center_y - 20),
            (center_x - 20, center_y + 20),
            (center_x + 20, center_y + 20),
            (center_x - 20 - variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x + 20 + variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x - 20 - variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
            (center_x + 20 + variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
            (center_x - 20 - 2*variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x + 20 + 2*variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x - 20 - 2*variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
            (center_x + 20 + 2*variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
            (center_x - 20 - 3*variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x + 20 + 3*variaveis_dimensoes["MOEDAS_WIDTH"], center_y - 20),
            (center_x - 20 - 3*variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
            (center_x + 20 + 3*variaveis_dimensoes["MOEDAS_WIDTH"], center_y + 20),
        ]

        # Verificar se alguma posição coincide com a posição do laser
        for laser in lasersprite:
            for pos in positions:
                if laser.rect.collidepoint(pos):
                    break
            else:
                continue
            break
        else:
            # Criando as moedas nas posições calculadas
            for pos in positions:
                moeda = Moeda(imagens["MOEDAS_img"], *pos)
                all_moedas.add(moeda)

# Variável para controlar o tempo para criar novas moedas
criar_moedas_timer = pygame.time.get_ticks()

class Laser(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200)
        self.rect.bottom = random.randint(100+variaveis_dimensoes["CHOQUE_HEIGHT"], HEIGHT)

        # Criar uma máscara de colisão precisa
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 5  # Movimento para a esquerda
        if self.rect.right < 0:  # Se o laser sair completamente da tela
            self.kill()  # Remover o laser

        # Verificar colisão com as moedas
        colisoes = pygame.sprite.spritecollide(self, all_moedas, False)
        if colisoes:
            for colisao in colisoes:
                colisao.kill()  # Remover a moeda

        # Verificar colisão com o Barry
        if pygame.sprite.collide_mask(self, voando):
            game_started = False  # Parar o jogo se houver colisão
            pygame.quit()
            quit()

lasersprite = pygame.sprite.Group()

# Função para criar um novo laser
def criar_laser(): 
    LASER = random.choice(LASER_LISTA)
    laser = Laser(LASER)
    lasersprite.add(laser)
     
# Variável para controlar o tempo para criar novos lasers
criar_laser_timer = pygame.time.get_ticks()

# Variável para controlar a posição x do fundo
background_x = 0

# Loop principal do jogo
pygame.mixer.music.play(loops=-1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_RETURN:  # Se o jogo ainda não começou e a tecla de espaço for pressionada
                game_started = True  # Começa o jogo
            elif game_started:
                if event.key == pygame.K_SPACE:
                    all_sprites.remove(voando)
                    BARRY = imagens["barry_a_img"]
                    voando = barry(BARRY, voando.rect.x, voando.rect.y, voando.moedas_coletadas)  # Passando moedas_coletadas como parâmetro
                    all_sprites.add(voando)
                    voando.shooting = True
                    voando.speedy = 10

        elif event.type == pygame.KEYUP:
            if game_started and event.key == pygame.K_SPACE:
                all_sprites.remove(voando)
                BARRY = imagens["barry_v_img"]
                voando = barry(BARRY, voando.rect.x, voando.rect.y, voando.moedas_coletadas)  # Passando moedas_coletadas como parâmetro
                all_sprites.add(voando)
                voando.shooting = False
                voando.speedy -= 10 # Reduz a velocidade vertical

    if not game_started:  # Se o jogo não começou, continua na tela inicial
        window.blit(background_i, (0, 0))
        window.blit(logo, (WIDTH / 2 - logo.get_width() / 2, HEIGHT/2 - logo.get_height() + 100 ))
        window.blit(texto_inicial["texto_renderizado1"], (WIDTH // 2 - texto_inicial["texto_renderizado1"].get_width() // 2, texto_inicial["posicao_y_linha1"]+200))
        window.blit(texto_inicial["texto_renderizado2"], (WIDTH // 2 - texto_inicial["texto_renderizado2"].get_width() // 2, texto_inicial["posicao_y_linha2"]+220))
        pygame.display.update()
        clock.tick(FPS)
        continue  # Volta ao início do loop para verificar eventos

    # Verificar se é hora de criar um novo conjunto de moedas
    if pygame.time.get_ticks() - criar_moedas_timer > 3000:  # 3000 milissegundos = 3 segundos
        criar_moedas()
        criar_moedas_timer = pygame.time.get_ticks()

    # Verificar se é hora de criar um novo laser
    if pygame.time.get_ticks() - criar_laser_timer > 5000:  # 5000 milissegundos = 5 segundos
        criar_laser()
        criar_laser_timer = pygame.time.get_ticks()

    # Atualize a posição do personagem
    all_sprites.update()

    # Atualize a posição x do fundo para movê-lo para a esquerda
    background_x -= 5

    # Verifique se o fundo original saiu completamente da tela
    if background_x <= -WIDTH:
        background_x = 0

    # Desenhe o fundo duas vezes para criar o efeito de loop infinito
    window.blit(background, (background_x, 0))
    window.blit(background, (background_x + WIDTH, 0))

    all_moedas.update()  
    all_moedas.draw(window)  
    lasersprite.update()  
    lasersprite.draw(window)  
    all_sprites.draw(window)   

    text_surface = fonte_moeda.render("{:05d}".format(voando.moedas_coletadas), True, (10, 10, 10))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2,  10)
    window.blit(text_surface, text_rect)

    pygame.display.update()  
    clock.tick(FPS)
pygame.quit()
