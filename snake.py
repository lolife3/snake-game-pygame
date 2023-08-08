import pygame, random, sys
from pygame.math import Vector2



GRID_SIZE = (20, 20)    
CELL_SIZE = 20         
BOARD_SIZE = (GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE)



class Board:
    def __init__(self):
        self.score = 0
        self.score_font = pygame.font.Font(pygame.font.match_font("arial"), size=32)
 

    def draw_score(self):
        screen.fill(color= (189,183,107), rect= ((0, 0), screen.get_size()))
        self.score_text = self.score_font.render(f"Score: {self.score}", True, (255,255,255))
        screen.blit(self.score_text, (50,15))  
        
        
    def draw_board(self,):
        self.playable_area = pygame.draw.rect(screen, (175,175,175), (50,50, BOARD_SIZE[0], BOARD_SIZE[1]))
        
        for x in range(0, BOARD_SIZE[0], 20):
            pygame.draw.line(screen, (200, 200, 200), (x + 50, 50), (x + 50, BOARD_SIZE[1] + 50))
        for y in range(0, BOARD_SIZE[1], 20):
            pygame.draw.line(screen, (200, 200, 200), (50, y + 50), (BOARD_SIZE[0] + 50, y + 50))


class Snake:
    def __init__(self):
        self.x = (BOARD_SIZE[0] + 100) // 2
        self.y = (BOARD_SIZE[1] + 100) // 2
        self.direction = Vector2(0,-20)
        self.body = [Vector2(self.x, self.y), Vector2(self.x, self.y+20), Vector2(self.x, self.y+40),]
        
        self.head_image = pygame.transform.scale(pygame.image.load("./snakehead.png"), (20,20))
        self.body_image = pygame.transform.scale(pygame.image.load("./snakebody.png"), (20,20))
        
        self.rotated_head_image = pygame.transform.scale(pygame.image.load("./snakehead.png"), (20,20))
        
        
    def draw_snake(self):
        for index, block in enumerate(self.body):
            if index == 0:
                screen.blit(self.rotated_head_image, (block.x, block.y))            
            else:
                screen.blit(self.body_image, (block.x, block.y))      
                
                
    def move_snake(self):
        snake_body = self.body[:-1]
        snake_body.insert(0, snake_body[0] + self.direction) 
        self.x = snake_body[0][0]
        self.y = snake_body[0][1]
        self.body = snake_body[:]
              
                
    def update_direction(self, event):
        right, left, up, down = Vector2(20,0), Vector2(-20,0), Vector2(0,-20), Vector2(0,20) 
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    if not self.direction == left:
                        self.rotated_head_image = pygame.transform.rotate(self.head_image, 270)
                        self.direction = right
                        
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                    if not self.direction == right:
                        self.rotated_head_image = pygame.transform.rotate(self.head_image, 90)
                        self.direction = left
                        
                if event.key == pygame.K_UP or event.key == pygame.K_w: 
                    if not self.direction == down:
                        self.rotated_head_image = self.head_image
                        self.direction = up
                        
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.direction == up:
                        self.rotated_head_image = pygame.transform.rotate(self.head_image, 180)
                        self.direction = down     
                        
                    
    def detect_collision(self, apple_pos):
            if self.x < 50 or self.x > BOARD_SIZE[0] + 30:  
                return "gameover"
            if self.y < 50 or self.y > BOARD_SIZE[1] + 30:
                return "gameover"
            
            if self.x == apple_pos[0] and self.y == apple_pos[1]:
                pygame.mixer.music.play()
                return "newapple"
            
            for cell in self.body[1:]:
                if self.x == cell.x and self.y == cell.y:
                    return "gameover"
            

class Apple:
    def __init__(self):
        self.x = 50 + (random.randint(0, GRID_SIZE[0]-1) * CELL_SIZE)
        self.y = 50 + (random.randint(0, GRID_SIZE[1]-1) * CELL_SIZE)
        self.apple_image = pygame.transform.scale(pygame.image.load("./apple.png"), (20,20))
        
    
    def draw_apple(self):
        screen.blit(self.apple_image, (self.x, self.y))
      
        
    def get_pos(self):
        return (self.x, self.y)



def main():    
    pygame.init()
    pygame.mixer.music.load("eating.mp3")
    pygame.mixer.music.set_volume(0.3)
    running = True
    
    global screen, clock
    screen = pygame.display.set_mode((BOARD_SIZE[0]+100, BOARD_SIZE[1]+100))
    clock = pygame.time.Clock()
    
        
    board = Board()        
    snake = Snake()
    apple = Apple()

    
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 250)

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            snake.update_direction(event)
            
            if event.type == SCREEN_UPDATE:
                snake.move_snake()
            
            if event.type == pygame.QUIT:
                sys.exit()
                

        match snake.detect_collision(apple.get_pos()):
            case "gameover":
                break
            
            case "newapple":
                board.score += 1
                snake.body.append(snake.body[-1] + snake.direction)
                apple = Apple()


        board.draw_score() 
        board.draw_board()
        apple.draw_apple()       
        snake.draw_snake()

        pygame.display.flip()
        
    while True:
        screen.fill(color= (189,183,107), rect= ((0, 0), screen.get_size()))
        end_font = pygame.font.Font(pygame.font.match_font("lucidasans"), size=32)
        end_text1 = end_font.render(f"You lost!", True, (255,255,255))
        end_text2 = end_font.render(f"Score: {board.score}", True, (255,255,255))
        end_text3 = end_font.render(f"Press SPACE to play again", True, (255,255,255))
        end_text4 = end_font.render(f"Press ESC to quit", True, (255,255,255))
        screen.blit(end_text1, (50,20)) 
        screen.blit(end_text2, (50,50)) 
        screen.blit(end_text3, (50,120)) 
        screen.blit(end_text4, (50,150)) 

        
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    
        pygame.display.flip()
    
    
    
    
if __name__ == "__main__":
    main()
