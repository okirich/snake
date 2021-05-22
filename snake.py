import pygame,time,os 
from random import *

pygame.init()

red = (255,0,0)
back = (255,247,0)
blue = (204,255,255)
white = (255,255,255)
mw = pygame.display.set_mode((500,500))

clock = pygame.time.Clock()


size_block = 50
count_blocks = 100
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

    def redraw(self,nf,w,h):
        self.image = pygame.image.load(nf)
        self.image = pygame.transform.scale(self.image,(w,h))

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
body = Picture(head_u,200,200, 50, 50)
tail = Picture(head_u,200,200, 50, 50)

# глобальные переменные
snake = [python]

speed_x = 0
speed_y = 0
end = False
apple_spawned = False
direction = 0
prev = 0
x_k = 100
y_k = 100

while not end :
    apple.fill()
    if snake[0].rect.colliderect(apple.rect):
        snake.append(tail)

    # создание яблока
    if not apple_spawned or python.rect.colliderect(apple.rect):

        x_k = randint(0,9)*50
        y_k = randint(0,9)*50

        apple.rect.x = x_k
        apple.rect.y = y_k

        apple_spawned = True
    # обработка стрелок
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
                speed_x = 50
                speed_y = 0
                python.redraw(head_r,50,50)
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
                speed_x = -50
                speed_y = 0
                python.redraw(head_l,50,50)
            if event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
                speed_x = 0
                speed_y = 50
                python.redraw(head_d,50,50)
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
                speed_x = 0
                speed_y = -50
                python.redraw(head_u,50,50)
    # движение змейки
    for i in range(len(snake)-1,0,-1):
        snake[i].rect.x = snake[i-1].rect.x
        snake[i].rect.y = snake[i-1].rect.y 
    snake[0].rect.x += speed_x
    snake[0].rect.y += speed_y

    if python.rect.x > 470 or python.rect.x < -20 or python.rect.y > 470 or python.rect.y < -20 :

        end = True

    mw.fill(back)

    # игровое поле

    for row in range(count_blocks):
        for column in range(count_blocks):
            if (row + column)%2 == 0:
                board_color = blue
            else:
                board_color = white
            pygame.draw.rect(mw,board_color,[   0 + column * size_block,\
                                                0 + row * size_block,\
                                                size_block,size_block   ] )
    for elem in snake:
        elem.draw()
    apple.draw()
    pygame.display.update()
    clock.tick(4)