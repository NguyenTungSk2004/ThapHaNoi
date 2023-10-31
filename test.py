import pygame

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Tháp Hà Nội")
clock = pygame.time.Clock()

# các stack chứa nhãn của đĩa
stack1 =[]
stack2 =[]
stack3 =[]

# giá trị của đĩa
stack1_value = {}
stack2_value = {}
stack3_value = {}

class DrawGame:

    def __init__(self, surface):
        self.surface = surface 
    
    def draw_columns(self):
        cot1 = pygame.Rect(200,200,20,400)
        cot2 = pygame.Rect(575,200,20,400)
        cot3 = pygame.Rect(950,200,20,400)
        pygame.draw.rect(self.surface,(255, 0,0),cot1)
        pygame.draw.rect(self.surface,(255, 0,0),cot2)
        pygame.draw.rect(self.surface,(255, 0,0),cot3)

    def draw(self, rect):
        pygame.draw.rect(self.surface, (0, 0, 128), rect)
    
class Player:
    def __init__(self, rect):
        self.rect = rect
        self.dragging = False # Biến để kiểm tra xem có đang kéo hình chữ nhật hay không
        self.offset = (0, 0) # Biến để lưu khoảng cách giữa con trỏ chuột và góc trên bên trái của hình chữ nhật

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Nếu nhấn chuột trái
                rect = self.rect
                if rect.collidepoint(event.pos): # Nếu con trỏ chuột nằm trong hình chữ nhật
                    self.dragging = True # Thiết lập dragging là True
                    mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                    self.offset = (rect.x - mouse_x, rect.y - mouse_y) # Tính toán offset
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Nếu thả chuột trái
                self.dragging = False # Thiết lập dragging là False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging: # Nếu đang kéo hình chữ nhật
                mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                self.rect.x = mouse_x + self.offset[0] # Cập nhật vị trí x của hình chữ nhật bằng cách cộng offset với vị trí x của chuột
                self.rect.y = mouse_y + self.offset[1] # Cập nhật vị trí y của hình chữ nhật bằng cách cộng offset với vị trí y của chuột

def createPlayer(n):
    r = 30
    # layer = [(180, 570, 60, 30)]
    for i in range(n):
        layer = pygame.Rect(180-i*r/2,570-(n-i-1)*r,60+i*r,r)
        stack1.append(str(i))
        stack1_value[stack1[i]] = layer

def process(event):
    if stack1:
        player = Player(stack1_value[stack1[0]])
        player.handle_events(event)

draw = DrawGame(screen)
running = True
createPlayer(10)
print(stack1)
print(stack1_value)
while running:
    screen.fill((255, 255, 255))
    draw.draw_columns()
    length = len(stack1)
    for i in range(length):
        draw.draw(stack1_value[stack1[i]])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else: 
            process(event)

    pygame.display.update()
    clock.tick(40)

pygame.quit()