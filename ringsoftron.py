import pygame
import random
import components
import graphics


def titleScreen():
    """Display the game startup screen"""
    key = ''
    lives = 1
    win = graphics.GraphWin('Rings of Tron', 1000, 600)
    win.setBackground('black')
    title = graphics.Image(graphics.Point(500, 50), 'images/title.png')
    lindsay = graphics.Image(graphics.Point(500, 100), 'images/bylindsay.png')
    art = graphics.Image(graphics.Point(500, 550), 'images/artby.png')
    sark = graphics.Image(graphics.Point(250, 400), 'images/sark_swing.png')
    tron = graphics.Image(graphics.Point(750, 400), 'images/tron_swing.png')
    enter = graphics.Image(graphics.Point(500, 460), 'images/enter.png')
    life = graphics.Image(graphics.Point(475, 400), 'images/life.png')
    life1 = graphics.Image(graphics.Point(560, 398), 'images/life1.png')
    life2 = graphics.Image(graphics.Point(560, 398), 'images/life2.png')
    life3 = graphics.Image(graphics.Point(560, 398), 'images/life3.png')
    lifecount = [life1, life2, life3]
    title.draw(win)
    lindsay.draw(win)
    art.draw(win)
    sark.draw(win)
    tron.draw(win)
    life.draw(win)
    life1.draw(win)
    enter.draw(win)
    while True:
        key = win.getKey()
        if key == 'Up':
            if lives < 3:
                lifecount[lives-1].undraw()
                lives += 1
                lifecount[lives-1].draw(win)
        if key == 'Down':
            if lives > 1:
                lifecount[lives-1].undraw()
                lives -= 1
                lifecount[lives-1].draw(win)
        if key == 'Return' or key == 'space':
            break
    win.close()
    return lives


def modeSelect(lives):
    """pick sides, number of games
        return the details for the gameLoop
    """
    # currently fixed, but maybe have players pick tron or sark at start?
    player1 = components.Tron('right', 700, 400, lives)
    player2 = components.Sark('left', 200, 400, lives)
    player1.scalebyheight(100)
    player2.scalebyheight(100)
    return player1, player2


def match_setup():
    """set up matches. For the first match, draw the platforms and
        have them walk out to the rings.  For other matches, have them "beam" in
    """
    platform1 = components.Platform(550, 450)
    platform2 = components.Platform(50, 450)
    platform1.scalebywidth(400)
    platform2.scalebywidth(400)
    ball = components.Ball(500, 150)
    ballstart = random.randint(1, 10)
    if ballstart < 5:
        ball.direction = 1
    else:
        ball.direction = -1
    scoreboard = components.Scoreboard()

    return scoreboard, platform1, platform2, ball


def check_events(done, platform1, platform2, player1, player2):
    """look for events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player2.state = 'crouch'
            if event.key == pygame.K_UP:
                player1.state = 'crouch'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player2.state = 'swing'
            if event.key == pygame.K_UP:
                player1.state = 'swing'
            if event.key == pygame.K_r:
                platform1.remove_ring(player1)
            if event.key == pygame.K_t:
                platform2.remove_ring(player2)


def check_keys(platform1, platform2, player1, player2):
    """Look for pressed keys"""
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        exit()
    if pressed[pygame.K_a]:
        player2.moveleft(platform2)
    if pressed[pygame.K_d]:
        player2.moveright(platform2)
    if pressed[pygame.K_s]:
        player2.state = 'stand'
    if pressed[pygame.K_LEFT]:
        player1.moveleft(platform1)
    if pressed[pygame.K_RIGHT]:
        player1.moveright(platform1)
    if pressed[pygame.K_DOWN]:
        player1.state = 'stand'


def check_collisions(ball, platform1, platform2, player1, player2, scoreboard, sounds):
    """look for collisions between all the sprites"""

    # if ball misses, reset
    if ball.y > 600:
        ball.reset(ball.start_x, ball.start_y)
        player1.state = 'stand'
        player2.state = 'stand'

    # see if ball hits platform
    if ball.y > 500:
        if pygame.sprite.collide_mask(ball, platform1):
            platform1.remove_ring(player1)
            sounds['ring'].play()
            ball.reset(ball.start_x, ball.start_y)
        if pygame.sprite.collide_mask(ball, platform2):
            platform2.remove_ring(player2)
            sounds['ring'].play()
            ball.reset(ball.start_x, ball.start_y)

    # if ball and player
    if ball.y > 450:
        if pygame.sprite.collide_mask(ball, player1):
            ball.speed += 1
            ball.direction = -1
            ball.set_moveX(platform1, platform2)
            ball.set_move(ball.start_x, ball.start_y)
            sounds['glove'].play()
            player1.state = 'swing'
            player2.state = 'stand'
        if pygame.sprite.collide_mask(ball, player2):
            ball.speed += 1
            ball.direction = 1
            ball.set_moveX(platform1, platform2)
            ball.set_move(ball.start_x, ball.start_y)
            sounds['glove'].play()
            player2.state = 'swing'
            player1.state = 'stand'

    # if ball and scoreboard
    if pygame.sprite.collide_rect(ball, scoreboard):
        sounds['top'].play()
        player1.state = 'stand'
        player2.state = 'stand'
        if ball.direction == 1:
            ball.set_move(random.randint(100, 400), 450)
        else:
            ball.set_move(random.randint(600, 900), 450)


def draw_rings(screen, platform1, platform2):
    """Handle placement of ring objects"""
    for ring in platform1.rings:
        screen.blit(ring, (550, 450))
    for ring in platform2.rings:
        screen.blit(ring, (50, 450))


def draw_players(done, screen, player1, player2, rotate_angle):
    """Handle placement of player objects"""
    # Player 1
    if player1.state == 'killed':
        player1.rotate(rotate_angle * -1)
        player1.setY(player1.y + 5)
        if player1.y >= 600:
            player1.lives -= 1
            done = True
        screen.blit(player1.standImg, player1.xy)
    elif player1.state == 'crouch':
        screen.blit(player1.crouchImg, player1.xy)
    elif player1.state == 'swing':
        screen.blit(player1.swingImg, player1.xy)
    else:
        screen.blit(player1.standImg, player1.xy)

    # Player 2
    if player2.state == 'killed':
        player2.rotate(rotate_angle)
        player2.setY(player2.y + 5)
        screen.blit(player2.standImg, player2.xy)
        if player2.y >= 600:
            player2.lives -= 1
            done = True
    if player2.state == 'crouch':
        screen.blit(player2.crouchImg, player2.xy)
    elif player2.state == 'swing':
        screen.blit(player2.swingImg, player2.xy)
    else:
        screen.blit(player2.standImg, player2.xy)
    return done


def draw_scoreboard(screen, scoreboard, player1, player2):
    # draw game stats ( Player scores, game number )
    screen.blit(scoreboard.image, (0, 0))
    p1image = pygame.transform.scale(player1.standOrig, (50, 60))
    p2image = pygame.transform.scale(player2.standOrig, (50, 60))
    p1x = 940
    p2x = 10
    p1lives = player1.lives
    p2lives = player2.lives
    while p1lives > 0:
        screen.blit(p1image, (p1x, 10))
        p1x = p1x - 60
        p1lives -= 1
    while p2lives > 0:
        screen.blit(p2image, (p2x, 10))
        p2x = p2x + 60
        p2lives -= 1


def draw_ball(screen, ball):
    screen.blit(ball.image, (ball.x, ball.y))
    if ball.direction == 1:
        x = ball.x + ball.moveX
    else:
        x = ball.x - ball.moveX
    y = ball.y + ball.moveY
    ball.setXY(x, y)


def gameloop(screen, scoreboard, ball, platform1, platform2, player1, player2, sounds):
    """Main game loop"""

    rotate_angle = 0
    done = False
    clock = pygame.time.Clock()
    while not done:
        check_events(done, platform1, platform2, player1, player2)
        check_keys(platform1, platform2, player1, player2)
        check_collisions(ball, platform1, platform2, player1, player2, scoreboard, sounds)
        # clear screen
        screen.fill((0, 0, 0))
        draw_scoreboard(screen, scoreboard, player1, player2)
        draw_rings(screen, platform1, platform2)
        done = draw_players(done, screen, player1, player2, rotate_angle)
        if player1.state == 'killed' or player2.state == 'killed':
            ball.speed = 0
        draw_ball(screen, ball)
        rotate_angle = rotate_angle + 2
        pygame.display.flip()
        clock.tick(60)
    return False


def endscreen(screen, player1, player2):
    """Display game results (winner)"""
    done = False
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 72)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            exit()
        screen.fill((0, 0, 0))
        if player1.lives > 0:
            player1.scalebyheight(200)
            text = font.render(player1.name + " Wins!", 1, (0, 176, 240))
            screen.blit(player1.swingImg, (350, 250))
        if player2.lives > 0:
            player2.scalebyheight(200)
            text = font.render(player2.name + " Wins!", 1, (0, 176, 240))
            screen.blit(player2.swingImg, (350, 250))
        screen.blit(text, (400, 200))
        pygame.display.flip()
        clock.tick(60)


def main():
    done = False
    pygame.init()
    pygame.mixer_music.load('sounds/title.ogg')
    pygame.mixer_music.play(1)
    lives = titleScreen()
    pygame.mixer_music.stop()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Rings of Tron')
    player1, player2 = modeSelect(lives)
    ring = pygame.mixer.Sound('sounds/ring.wav')
    top = pygame.mixer.Sound('sounds/top.wav')
    glove = pygame.mixer.Sound('sounds/glove.wav')
    sounds = { 'ring': ring, 'top': top, 'glove': glove }

    while player1.lives > 0 and player2.lives > 0:
        scoreboard, platform1, platform2, ball = match_setup()
        gameloop(screen, scoreboard, ball, platform1, platform2, player1, player2, sounds)
        ball.reset(ball.start_x, ball.start_y)
        platform1.reset()
        platform2.reset()
        player1.reset(650, 400)
        player2.reset(150, 400)
        ballstart = random.randint(1, 10)
        if ballstart < 5:
            ball.direction = 1
        else:
            ball.direction = -1
    pygame.mixer_music.load('sounds/endscreen.ogg')
    pygame.mixer_music.play(1)
    endscreen(screen, player1, player2)

if __name__ == '__main__':
    main()
