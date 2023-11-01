import pygame

pygame.init()
screen = pygame.display.set_mode((1200,600))
rect = pygame.Rect(100,100,100,100)
running = True
moving = False
offset = (0,0)
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect.collidepoint(event.pos):
                    moving = True
                    mouse_x,mouse_y= event.pos
                    offset = (rect.x - mouse_x, rect.y - mouse_y)
                    print(offset)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving = False
        elif event.type == pygame.MOUSEMOTION:
            if moving: 
                mouse_x,mouse_y= event.pos
                rect.x =  offset[0]+ mouse_x 
                rect.y =  offset[1]+  mouse_y
    pygame.draw.rect(screen,(0,0,0),rect)
        
    pygame.display.update()
pygame.quit()