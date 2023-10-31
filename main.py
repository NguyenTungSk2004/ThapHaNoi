import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Di chuyển hình chữ nhật")

clock = pygame.time.Clock()

class Player(object):

    def __init__(self):
        self.rect = pygame.rect.Rect((64, 54, 16, 16))
        self.dragging = False # Biến để kiểm tra xem có đang kéo hình chữ nhật hay không
        self.offset = (0, 0) # Biến để lưu khoảng cách giữa con trỏ chuột và góc trên bên trái của hình chữ nhật

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Nếu nhấn chuột trái
                    if self.rect.collidepoint(event.pos): # Nếu con trỏ chuột nằm trong hình chữ nhật
                        self.dragging = True # Thiết lập dragging là True
                        mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                        self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y) # Tính toán offset
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Nếu thả chuột trái
                    self.dragging = False # Thiết lập dragging là False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging: # Nếu đang kéo hình chữ nhật
                    mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                    self.rect.x = mouse_x + self.offset[0] # Cập nhật vị trí x của hình chữ nhật bằng cách cộng offset với vị trí x của chuột
                    self.rect.y = mouse_y + self.offset[1] # Cập nhật vị trí y của hình chữ nhật bằng cách cộng offset với vị trí y của chuột
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 128), self.rect)

player = Player()
running = True
while running:
    running = player.handle_events()
    screen.fill((255, 255, 255))
    player.draw(screen)
    pygame.display.update()
    clock.tick(40)
