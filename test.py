import pygame

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Tháp Hà Nội")
clock = pygame.time.Clock()

fix = (60, 570, 300, 30)

class Player:

    def __init__(self, n):
        self.n = n
        self.cot1 = pygame.Rect(200,200,20,400)
        self.cot2 = pygame.Rect(575,200,20,400)
        self.cot3 = pygame.Rect(950,200,20,400)
        self.rects = [pygame.Rect(fix[0]+i*fix[3]/2,fix[1]-i*fix[3],fix[2]-i*fix[3],fix[3]) for i in range(n)]
        self.dragging = [False for i in range(n)] # Biến để kiểm tra xem có đang kéo hình chữ nhật hay không
        self.offset = [(0, 0) for i in range(n)] # Biến để lưu khoảng cách giữa con trỏ chuột và góc trên bên trái của hình chữ nhật
        self.click = 0
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Nếu nhấn chuột trái
                    for i in range(self.n):
                        rect = self.rects[i]
                        if rect.collidepoint(event.pos): # Nếu con trỏ chuột nằm trong hình chữ nhật
                            self.dragging[i] = True # Thiết lập dragging là True
                            self.click = i
                            mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                            self.offset[i] = (rect.x - mouse_x, rect.y - mouse_y) # Tính toán offset
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Nếu thả chuột trái
                    self.dragging[self.click] = False # Thiết lập dragging là False
            elif event.type == pygame.MOUSEMOTION:
                index = self.click
                if self.dragging[index]: # Nếu đang kéo hình chữ nhật
                    mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                    self.rects[index].x = mouse_x + self.offset[index][0] # Cập nhật vị trí x của hình chữ nhật bằng cách cộng offset với vị trí x của chuột
                    self.rects[index].y = mouse_y + self.offset[index][1] # Cập nhật vị trí y của hình chữ nhật bằng cách cộng offset với vị trí y của chuột
        return True

    def draw(self, surface):
        pygame.draw.rect(surface,(255, 0,0),self.cot1)
        pygame.draw.rect(surface,(255, 0,0),self.cot2)
        pygame.draw.rect(surface,(255, 0,0),self.cot3)
        for i in range(self.n):
            pygame.draw.rect(surface, (0, 0, 128), self.rects[i])

player = Player(10)
running = True
while running:
    running = player.handle_events()
    screen.fill((255, 255, 255))
    player.draw(screen)
    pygame.display.update()
    clock.tick(40)
