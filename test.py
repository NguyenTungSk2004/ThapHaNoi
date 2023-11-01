import pygame

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Tháp Hà Nội")
clock = pygame.time.Clock()

# Tạo chữ
font = pygame.font.SysFont("Arial", 32)
textWin = font.render("You win", True, (255, 255, 255), (0, 0, 0))
textReset = font.render("Reset", True, (255, 255, 255), (0, 0, 0))
tang = font.render("Increase", True, (255, 255, 255), (0, 0, 0))
giam = font.render("Decrease", True, (255, 255, 255), (0, 0, 0))
tang_click = pygame.Rect(0,0, 120,50)
giam_click = pygame.Rect(130 ,0, 120,50)
win = pygame.Rect(460,100,250,100)
reset = pygame.Rect(1100,0, 100,50)


# các stack chứa nhãn của đĩa
stack1 =[]
stack2 =[]
stack3 =[]

# giá trị của đĩa
stack1_value = {}
stack2_value = {}
stack3_value = {}

# khung va chạm các cột
collide1 = pygame.Rect(165,70,90,280)
collide2 = pygame.Rect(540,70,90,280)
collide3 = pygame.Rect(915,70,90,280)

# Hàm check hình chữ nhật cao nhất trong stack
def checkTopRect(rect):
    def check(stack, stack_value):
        for i in range(len(stack)): # Duyệt qua các hình chữ nhật trong stack
            if stack_value[stack[i]].colliderect(rect): 
                if i == len(stack)-1:
                    return True
        return False
    
    result = check(stack1,stack1_value)
    if result:
        return True
    result = check(stack2,stack2_value)
    if result:
        return True
    result = check(stack3,stack3_value)
    if result:
        return True
    return False

# Hàm check va chạm
def checkCollide(rect):
    def check(stack, stack_value):
        for i in stack:
            if stack_value[i].colliderect(rect):
                return False
        return True

    if check(stack1, stack1_value) and rect.colliderect(collide1):
        if not stack1:
            return 1
        elif stack1_value[stack1[len(stack1)-1]].width > rect.width:
            return 1
    if check(stack2, stack2_value) and rect.colliderect(collide2):
        if not stack2:
            return 2
        elif stack2_value[stack2[len(stack2)-1]].width > rect.width:
            return 2
    if check(stack3, stack3_value) and rect.colliderect(collide3):
        if not stack3:
            return 3
        elif stack3_value[stack3[len(stack3)-1]].width > rect.width:
            return 3
    return -1

def checkInStack(rect,stack,stack_value,cot):
    def process_stack(stackps,stackps_value):
        for i in range(len(stackps)):
            if stackps_value[stackps[i]].colliderect(rect): # Kiểm tra có đối tượng nào là rect hay không
                # Thêm rect vào stack va chạm
                stack.append(stackps[i]) 
                stack_value[stackps[i]] = stackps_value[stackps[i]]
                # Xóa đối tượng rect trong stack chứa nó
                stackps_value.pop(stackps[i])
                stackps.pop(i)
                return True
        return False
    if stack != stack1:
        # Kiểm tra xem rect có nằm trong stack1 không
        if process_stack(stack1,stack1_value):
            length = len(stack)
            test = stack_value[stack[length-1]]
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
    if stack != stack2:
        # Kiểm tra xem rect có nằm trong stack2 không
        if process_stack(stack2,stack2_value):
            length = len(stack)
            test = stack_value[stack[length-1]]
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
    if stack != stack3:
        # Kiểm tra xem rect có nằm trong stack3 không
        if process_stack(stack3,stack3_value):
            length = len(stack)
            test = stack_value[stack[length-1]]
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
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
        self.original_pos = (rect.x, rect.y) # Lưu vị trí ban đầu của đĩa
        self.dragging = False # Biến để kiểm tra xem có đang kéo hình chữ nhật hay không
        self.offset = (0, 0) # Biến để lưu khoảng cách giữa con trỏ chuột và góc trên bên trái của hình chữ nhật

    def handle_events(self, event,x,y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Nếu nhấn chuột trái
                rect = self.rect
                if rect.collidepoint(event.pos): # Nếu con trỏ chuột nằm trong hình chữ nhật
                    # Kiểm tra xem hình chữ nhật có phải là hình chữ nhật trên cùng của một cột hay không
                    top_rect = checkTopRect(rect) 
                    if top_rect: # Nếu hình chữ nhật là hình chữ nhật trên cùng của một cột
                        self.dragging = True # Thiết lập dragging là True
                        mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                        self.offset = (rect.x - mouse_x, rect.y - mouse_y) # Tính toán offset
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Nếu thả chuột trái
                self.dragging = False # Thiết lập dragging là False
                if checkCollide(self.rect) == 1:
                    checkInStack(self.rect,stack1, stack1_value,(200,570))
                    self.original_pos = (self.rect.x, self.rect.y) # Lưu vị trí ban đầu của đĩa
                elif checkCollide(self.rect) == 2:
                    checkInStack(self.rect,stack2, stack2_value,(575,570))
                    self.original_pos = (self.rect.x, self.rect.y) # Lưu vị trí ban đầu của đĩa
                elif checkCollide(self.rect) == 3:
                    checkInStack(self.rect,stack3, stack3_value,(950,570))
                    self.original_pos = (self.rect.x, self.rect.y) # Lưu vị trí ban đầu của đĩa
                elif checkCollide(self.rect) == -1:
                    self.rect.x = self.original_pos[0] # Di chuyển đĩa về vị trí ban đầu
                    self.rect.y = self.original_pos[1] # Di chuyển đĩa về vị trí ban đầu
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging: # Nếu đang kéo hình chữ nhật
                mouse_x, mouse_y = event.pos # Lấy vị trí của con trỏ chuột
                self.rect.x = mouse_x + self.offset[0] # Cập nhật vị trí x của hình chữ nhật bằng cách cộng offset với vị trí x của chuột
                self.rect.y = mouse_y + self.offset[1] # Cập nhật vị trí y của hình chữ nhật bằng cách cộng offset với vị trí y của chuột

def createPlayer(n):
    r = 30
    players = [] # Tạo một danh sách để lưu các đối tượng player
    for i in range(n):
        layer = pygame.Rect(180-i*r/2,570-(n-i-1)*r,60+i*r,r)
        stack1.insert(0, str(i))
        stack1_value[stack1[len(stack1)-1-i]] = layer
        players.insert(0, Player(layer)) # Tạo một đối tượng player cho mỗi hình chữ nhật và thêm vào danh sách players
    return players # Trả về danh sách players

def process(event, players):
    for player in players: # Duyệt qua các đối tượng player trong danh sách players
        player.handle_events(event,player.rect.x,player.rect.y) # Gọi phương thức handle_events cho mỗi đối tượng player

draw = DrawGame(screen)
running = True
n = 2
players = createPlayer(n) # Gọi hàm createPlayer và lưu kết quả vào biến players
winGame = False
reset_clicked = False
increase = False
decrease = False
while running:
    # Phần vẽ
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0,0,0), reset)   
    screen.blit(textReset, (reset.x+12,reset.y+5))    
    pygame.draw.rect(screen, (0,0,0), tang_click)   
    screen.blit(tang, (0,10))    
    pygame.draw.rect(screen, (0,0,0), giam_click)   
    screen.blit(giam, (giam_click.x,10))    
    draw.draw_columns()
    for i in players:
        draw.draw(i)

    # Phần xử lí sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset.collidepoint(event.pos):
                   reset_clicked = True
                if tang_click.collidepoint(event.pos):
                    increase = True
                if giam_click.collidepoint(event.pos):
                    decrease = True
        if not reset_clicked and winGame == False: 
            process(event, players) # Gọi hàm process với biến players

    #Phần tăng số lượng đĩa
    if increase and not stack3 and not stack2 and n < 10:
        n +=1
         # các stack chứa nhãn của đĩa
        stack1 =[]
        stack2 =[]
        stack3 =[]
        # giá trị của đĩa
        stack1_value = {}
        stack2_value = {}
        stack3_value = {}
        # Gọi hàm createPlayer và lưu kết quả vào biến players
        players = createPlayer(n) 
        reset_clicked = False
        winGame = False
        increase = False

    #Phần giảm số lượng đĩa
    if decrease and not stack3 and not stack2 and n > 2:
        n -=1
         # các stack chứa nhãn của đĩa
        stack1 =[]
        stack2 =[]
        stack3 =[]
        # giá trị của đĩa
        stack1_value = {}
        stack2_value = {}
        stack3_value = {}
        # Gọi hàm createPlayer và lưu kết quả vào biến players
        players = createPlayer(n) 
        reset_clicked = False
        winGame = False
        decrease = False

    if reset_clicked:
        n=2
         # các stack chứa nhãn của đĩa
        stack1 =[]
        stack2 =[]
        stack3 =[]
        # giá trị của đĩa
        stack1_value = {}
        stack2_value = {}
        stack3_value = {}
        # Gọi hàm createPlayer và lưu kết quả vào biến players
        players = createPlayer(n) 
        reset_clicked = False
        winGame = False
        crease = False

    # Win Game
    if len(stack3) == n:
        pygame.draw.rect(screen, (0,0,0),win)
        screen.blit(textWin, (win.x + 75, win.y + win.y/2 - 32))
        winGame = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
