import pygame,time,os 
from random import *

pygame.init()

red = (255,0,0)
back = (255,247,0)
mw = pygame.display.set_mode((500,500))

clock = pygame.time.Clock()

# необходимые классы
class Area():
    def __init__(self,x=0,y=0,width=10,height=10,color=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self,new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw,self.fill_color,self.rect)
    
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

    def colliderect(self,rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self,filename,x=0,y=0,width=10,height=10):
        Area.__init__(self,x=x,y=y,width=width,height=height,color=None)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image,(width,height))

    def draw(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
# необходимые спрайты
apple = os.path.join(os.getcwd(),'Graphics','apple.png')

head_r = os.path.join(os.getcwd(),'Graphics','head_right.png')
head_l = os.path.join(os.getcwd(),'Graphics','head_left.png')
head_d = os.path.join(os.getcwd(),'Graphics','head_down.png')
head_u = os.path.join(os.getcwd(),'Graphics','head_up.png')

apple = Picture(apple,0, 0, 50, 50)
python = Picture(head_u,200,200, 50, 50)

# глобальные переменные
speed_x = 0
speed_y = 0
end = False
apple_spawned = False
direction = 0
x_k = 100
y_k = 100


while not end :
    apple.fill()
    # создание яблока
    if not apple_spawned or python.rect.colliderect(apple.rect):

        x_k = randint(50,400)
        y_k = randint(50,450)

        apple.rect.x = x_k
        apple.rect.y = y_k

        apple_spawned = True
    # обработка стрелок
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
                speed_x = 5
                speed_y = 0
                python.image = pygame.image.load(head_r) 
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
                speed_x = -5
                speed_y = 0
                python.image = pygame.image.load(head_l)
            if event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
                speed_x = 0
                speed_y = 5
                python.image = pygame.image.load(head_d)
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
                speed_x = 0
                speed_y = -5
                python.image = pygame.image.load(head_u)
    # движение змейки
    python.rect.x += speed_x
    python.rect.y += speed_y
    
    if python.rect.x > 500 or python.rect.x < 0 or python.rect.y > 500 or python.rect.y < 0 :

        end = True

    mw.fill(back)
    python.draw()
    apple.draw()
    pygame.display.update()
    clock.tick(40)