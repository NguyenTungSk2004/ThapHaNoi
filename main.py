import pygame
import threading
import time

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Tháp Hà Nội")
clock = pygame.time.Clock()

# Class vẽ
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

    def draw(self,color, rect):
        pygame.draw.rect(self.surface, color, rect)

# Hàm để giải bài toán tháp Hà Nội
DapAn = []
def Giai(n, from_peg, to_peg, aux_peg):
    if n == 1:
        DapAn.append((from_peg, to_peg))
        return
    Giai(n-1, from_peg, aux_peg, to_peg)
    DapAn.append((from_peg, to_peg))
    Giai(n-1, aux_peg, to_peg, from_peg)

# Hàm check hình chữ nhật cao nhất trong stack
def checkTopRect(rect):
    def check(stack, stack_value):
        for i in range(len(stack)): # Duyệt qua các hình chữ nhật trong stack
            if stack_value[stack[i]].rect.colliderect(rect): 
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
    # Hàm check xem rect có nằm trong stack hay không
    def check(stack, stack_value):
        for i in stack:
            if stack_value[i].rect.colliderect(rect):
                return False
        return True

    # nếu không nằm trong stack và va chạm với khung collide thì trả về cột va chạm
    if check(stack1, stack1_value) and rect.colliderect(collide1): 
        if not stack1:
            return 1
        elif stack1_value[stack1[len(stack1)-1]].rect.width > rect.width:
            return 1
    if check(stack2, stack2_value) and rect.colliderect(collide2):
        if not stack2:
            return 2
        elif stack2_value[stack2[len(stack2)-1]].rect.width > rect.width:
            return 2
    if check(stack3, stack3_value) and rect.colliderect(collide3):
        if not stack3:
            return 3
        elif stack3_value[stack3[len(stack3)-1]].rect.width > rect.width:
            return 3
    return -1
# Hàm xử lí va chạm với stack --> di chuyển vào stack
def checkInStack(rect,stack,stack_value,cot):
    def process_stack(stackps,stackps_value):
        for i in range(len(stackps)):
            if stackps_value[stackps[i]].rect.colliderect(rect): # Kiểm tra có đối tượng nào là rect hay không
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
            test = stack_value[stack[length-1]].rect
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
    if stack != stack2:
        # Kiểm tra xem rect có nằm trong stack2 không
        if process_stack(stack2,stack2_value):
            length = len(stack)
            test = stack_value[stack[length-1]].rect
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
    if stack != stack3:
        # Kiểm tra xem rect có nằm trong stack3 không
        if process_stack(stack3,stack3_value):
            length = len(stack)
            test = stack_value[stack[length-1]].rect
            test.x = cot[0] - test.width/2 +10
            test.y = cot[1] - (length-1)*30
            return 
# Khởi tạo đối tượng những cái đĩa 
class Player:
    def __init__(self, rect):
        self.rect = rect
        self.original_pos = (rect.x, rect.y) # Lưu vị trí ban đầu của đĩa
        self.dragging = False # Biến để kiểm tra xem có đang kéo hình chữ nhật hay không
        self.offset = (0, 0) # Biến để lưu khoảng cách giữa con trỏ chuột và góc trên bên trái của hình chữ nhật

    def handle_events(self, event):
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
    def update(self,stack,stack_value,cot):
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

# Hàm tạo danh sách đối tượng ban đầu
def createPlayer(n):
    r = 30
    for i in range(n):
        layer = pygame.Rect(180-i*r/2,570-(n-i-1)*r,60+i*r,r)
        stack1.insert(0, str(i))
        stack1_value[stack1[len(stack1)-1-i]] = Player(layer)
# Hàm thực thi hành động của đối tượng
def process(event, stack,stack_value):
    for i in stack: # Duyệt qua các đối tượng player trong danh sách players
        stack_value[i].handle_events(event) # Gọi phương thức handle_events cho mỗi đối tượng player
# Hàm set giá trị ban đầu
def Factory_Reset():
        global stack1,stack2,stack3,stack1_value,stack2_value,stack3_value,reset_clicked,winGame,increase,decrease,solution
         # các stack chứa nhãn của đĩa
        stack1 =[]
        stack2 =[]
        stack3 =[]
        # giá trị của đĩa
        stack1_value = {}
        stack2_value = {}
        stack3_value = {}
        # Gọi hàm createPlayer và lưu kết quả vào biến players
        winGame = False # Biến check win game
        reset_clicked = False # Biến check đã ấn nút reset
        increase = False # Biến check đã ấn nút tăng
        decrease = False # Biến check đã ấn nút giảm
        solution = False

def veDia():
    # vẽ đĩa
    if len(stack1) != 0:
        for i in stack1:
            draw.draw((0,0,128),stack1_value[i])   
    if len(stack2) !=0:
        for i in stack2:
            draw.draw((0,0,128),stack2_value[i])
    if len(stack3) !=0:
        for i in stack3:
            draw.draw((0,0,128),stack3_value[i])

draw = DrawGame(screen) # Tạo đối tượng vẽ game

# Tạo chữ
font = pygame.font.SysFont("Arial", 32)
textWin = font.render("You win", True, (255, 255, 255), (0, 0, 0))
textReset = font.render("Reset", True, (255, 255, 255), (0, 0, 0))
textGiai = font.render("Solution", True, (255, 255, 255), (0, 0, 0))
tang = font.render("Increase", True, (255, 255, 255), (0, 0, 0))
giam = font.render("Decrease", True, (255, 255, 255), (0, 0, 0))
# Đối tượng các nút
tang_button = pygame.Rect(0,0, 120,50)
giam_button = pygame.Rect(130 ,0, 120,50)
reset_button = pygame.Rect(1100,0, 100,50)
giai_button = pygame.Rect(970,0,120,50)
win = pygame.Rect(460,100,250,100) #Cửa sổ thông báo chiến thắng
# khung va chạm các cột
collide1 = pygame.Rect(165,70,90,280)
collide2 = pygame.Rect(540,70,90,280)
collide3 = pygame.Rect(915,70,90,280)
n = 2
Factory_Reset()
createPlayer(n) # Gọi hàm createPlayer và lưu kết quả vào biến players

running = True
global an,start,end
l = 0
def update_count(): # Định nghĩa một hàm để cập nhật và in ra biến count
    global l # Khai báo biến toàn cục count
    l += 1 # Tăng biến count lên 1
    timer = threading.Timer(1, update_count) # Khởi tạo lại luồng Timer với khoảng thời gian là 1 giây và hàm là update_count
    timer.start() # Bắt đầu luồng Timer

while running:
    # Phần vẽ
    screen.fill((255, 255, 255))
    draw.draw_columns()
    # Nút reset
    draw.draw((0,0,0), reset_button)   
    screen.blit(textReset, (reset_button.x+12,reset_button.y+5))    
    # Nút giải
    draw.draw((0,0,0), giai_button)   
    screen.blit(textGiai, (giai_button.x+12,giai_button.y+5))  
    # Nút increase
    draw.draw((0,0,0), tang_button)   
    screen.blit(tang, (0,10))    
    # nút decrease
    draw.draw((0,0,0), giam_button)   
    screen.blit(giam, (giam_button.x,10))    
    # Phần xử lí sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset_button.collidepoint(event.pos):
                   reset_clicked = True
                if tang_button.collidepoint(event.pos):
                    increase = True
                if giam_button.collidepoint(event.pos):
                    decrease = True
                if giai_button.collidepoint(event.pos):
                    DapAn.clear()
                    Giai(n,collide1,collide3,collide2)
                    an = DapAn[0]
                    l = 0
                    timer = threading.Timer(1, update_count) # Khởi tạo lại luồng Timer với khoảng thời gian là 1 giây và hàm là update_count
                    timer.start() # Bắt đầu luồng Timer
                    start = 0
                    solution = True
        if not reset_clicked and winGame == False: 
            process(event, stack1,stack1_value) # Gọi hàm process với biến stack1_value
            process(event, stack2,stack2_value) # Gọi hàm process với biến stack2_value
            process(event, stack3,stack3_value) # Gọi hàm process với biến stack3_value

    #khi ấn vào nút solution
    if solution:
        if an[0]== collide1 and an[1] == collide2 and len(stack1) !=0:
            index = stack1[len(stack1)-1]
            stack1_value[index].rect.x = an[1].x 
            stack1_value[index].rect.y = an[1].y 
            stack1_value[index].update(stack2,stack2_value,(575,570))
        if an[0]== collide2 and an[1] == collide1 and len(stack2) !=0:
            index = stack2[len(stack2)-1]
            stack2_value[index].rect.x = an[1].x 
            stack2_value[index].rect.y = an[1].y 
            stack2_value[index].update(stack1, stack1_value,(200,570))
        elif an[0]== collide2 and an[1] == collide3 and len(stack2) !=0:
            index = stack2[len(stack2)-1]
            stack2_value[index].rect.x = an[1].x 
            stack2_value[index].rect.y = an[1].y 
            stack2_value[index].update(stack3, stack3_value,(950,570))
        if an[0]== collide3 and an[1] == collide2 and len(stack3) !=0:
            index = stack3[len(stack3)-1]
            stack3_value[index].rect.x = an[1].x 
            stack3_value[index].rect.y = an[1].y 
            stack3_value[index].update(stack2,stack2_value,(575,570))
        elif an[0]== collide1 and an[1] == collide3 and len(stack1) !=0:
            index = stack1[len(stack1)-1]
            stack1_value[index].rect.x = an[1].x 
            stack1_value[index].rect.y = an[1].y 
            stack1_value[index].update(stack3, stack3_value,(950,570))
        if an[0]== collide3 and an[1] == collide1  and len(stack3) !=0:
            index = stack3[len(stack3)-1]
            stack3_value[index].rect.x = an[1].x 
            stack3_value[index].rect.y = an[1].y 
            stack3_value[index].update(stack1, stack1_value,(200,570))
        end = l
        if end == len(DapAn):
            timer.cancel()
            solution = False
        elif (end - start) == 1:
            start = end
            an = DapAn[l]
    veDia()
    
    #Khi ấn vào nút tăng
    if increase and not stack3 and not stack2 and n < 10:
        n +=1
        Factory_Reset()
        players = createPlayer(n) 
    #Khi ấn vào nút decrease
    if decrease and not stack3 and not stack2 and n > 2:
        n -=1
        Factory_Reset()
        players = createPlayer(n) 
    # Khi ấn vào nút reset
    if reset_clicked:
        n=2
        Factory_Reset()
        players = createPlayer(n) 
    # Win Game
    if len(stack3) == n:
        pygame.draw.rect(screen, (0,0,0),win)
        screen.blit(textWin, (win.x + 75, win.y + win.y/2 - 32))
        winGame = True
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
