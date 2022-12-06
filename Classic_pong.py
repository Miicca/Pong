import pygame

pygame.init()


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Pong")

#Sounds
point = pygame.mixer.Sound("point.wav")
point.set_volume(0.03)

hit = pygame.mixer.Sound("hit.wav")
hit.set_volume(0.02)

victory = pygame.mixer.Sound("victory.wav")
victory.set_volume(0.03)

#Background music
music = pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)


#FPS-CAP
FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#Paddle width and height
PADDLE_WIDTH, PADDLE_HEIGHT = 8, 85

#Ball radius
BALL_RADIUS = 6

#Score font
SCORE_FONT = pygame.font.SysFont("system", 50)

#Points to win
WINNING_SCORE = 5

#Paddle class
class Paddle:

    COLOR = WHITE
    VEL = 5


    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move (self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset (self):
        self.x = self.original_x
        self.y = self.original_y



#Ball class
class Ball:

    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


#Function that creates the game window
def draw(win, paddles, ball, left_score, right_score):

    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:          
            continue
        
        #Middle line
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()


#Game logic
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        hit.play()
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        hit.play()
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                hit.play()
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                hit.play()

#Paddle fuction
def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


#Main fuction
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        pygame.mixer.music.unpause()
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        #Rightside scores
        if ball.x < 0:
            point.play()
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        
        #Leftside scores
        elif ball.x > WIDTH:
            point.play()
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            pygame.mixer.music.pause()
            win_text = "PLAYER 1 WINS"
        elif right_score >= WINNING_SCORE:
            won = True
            pygame.mixer.music.pause()
            win_text = "PLAYER 2 WINS"
        
        #Win text and sound
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() //2))
            victory.play()
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            
    pygame.quit()

if __name__ == '__main__':
    main()
