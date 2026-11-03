import asyncio
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KOEX GAMING")
clock = pygame.time.Clock()

BG = (10, 13, 21)
PANEL = (19, 25, 38)
WHITE = (239, 243, 250)
MUTED = (145, 157, 177)
LIME = (200, 255, 66)
CYAN = (99, 230, 226)
RED = (244, 83, 105)
ORANGE = (255, 173, 77)

font_big = pygame.font.Font(None, 72)
font_title = pygame.font.Font(None, 48)
font_mid = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 22)

def text(surf, value, font, color, pos, center=False):
    image = font.render(str(value), True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surf.blit(image, rect)

def button(surf, rect, label, active=True):
    color = LIME if active else (45, 54, 70)
    pygame.draw.rect(surf, color, rect, border_radius=6)
    image = font_mid.render(label, True, BG if active else MUTED)
    surf.blit(image, image.get_rect(center=rect.center))

def draw_background():
    screen.fill(BG)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (17, 23, 35), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (17, 23, 35), (0, y), (WIDTH, y))

def menu():
    draw_background()
    text(screen, "KOEX", font_big, LIME, (WIDTH//2, 76), True)
    text(screen, "G A M I N G   /   A R C A D E", font_small, MUTED, (WIDTH//2, 123), True)
    text(screen, "CHOOSE YOUR GAME", font_title, WHITE, (WIDTH//2, 185), True)
    names = [
        ("1", "NEON RACER", "Dodge traffic and beat your distance"),
        ("2", "SNAKE", "Eat, grow, and avoid your tail"),
        ("3", "PONG", "Play paddle against the computer"),
        ("4", "BREAKOUT", "Break every brick with the ball"),
        ("5", "BLOCK DODGER", "Avoid the falling blocks"),
    ]
    for i, (key, name, desc) in enumerate(names):
        y = 235 + i * 65
        rect = pygame.Rect(155, y, 490, 54)
        pygame.draw.rect(screen, PANEL, rect, border_radius=6)
        pygame.draw.rect(screen, (48, 59, 78), rect, 1, border_radius=6)
        text(screen, key, font_mid, LIME, (176, y+14))
        text(screen, name, font_mid, WHITE, (220, y+7))
        text(screen, desc, font_small, MUTED, (220, y+31))
    text(screen, "PRESS 1–5 TO PLAY  •  ESC DURING A GAME TO RETURN HERE", font_small, MUTED, (WIDTH//2, 578), True)

def end_screen(title, score, hint="Press ENTER to play again  •  ESC for menu"):
    screen.fill(BG)
    text(screen, title, font_big, LIME, (WIDTH//2, 220), True)
    text(screen, f"SCORE  {score}", font_title, WHITE, (WIDTH//2, 300), True)
    text(screen, hint, font_small, MUTED, (WIDTH//2, 370), True)

def new_racer():
    return {"player": pygame.Rect(382, 475, 36, 62), "traffic": [], "spawn": 0,
            "speed": 5.0, "score": 0, "over": False, "road_offset": 0}

def racer_update(g, dt):
    keys = pygame.key.get_pressed()
    p = g["player"]
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: p.x -= int(360*dt)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: p.x += int(360*dt)
    p.x = max(245, min(519, p.x))
    g["spawn"] += dt
    g["speed"] = min(12, 5 + g["score"] / 450)
    if g["spawn"] > max(.38, .95 - g["score"]/3000):
        lane = random.choice([270, 350, 430, 510])
        g["traffic"].append(pygame.Rect(lane, -75, 34, 58))
        g["spawn"] = 0
    for car in g["traffic"][:]:
        car.y += int(g["speed"]*60*dt)
        if car.top > HEIGHT:
            g["traffic"].remove(car)
            g["score"] += 10
        if p.colliderect(car):
            g["over"] = True
    g["road_offset"] = (g["road_offset"] + int(g["speed"]*60*dt)) % 70

def racer_draw(g):
    screen.fill((13, 25, 28))
    pygame.draw.rect(screen, (42, 49, 62), (225, 0, 350, HEIGHT))
    pygame.draw.rect(screen, (205, 210, 220), (225, 0, 5, HEIGHT))
    pygame.draw.rect(screen, (205, 210, 220), (570, 0, 5, HEIGHT))
    for y in range(-70, HEIGHT, 70):
        yy = (y + g["road_offset"]) % (HEIGHT+70) - 35
        pygame.draw.rect(screen, (222, 226, 235), (338, yy, 5, 34))
        pygame.draw.rect(screen, (222, 226, 235), (455, yy, 5, 34))
    for car in g["traffic"]:
        pygame.draw.rect(screen, RED, car, border_radius=7)
        pygame.draw.rect(screen, (255, 165, 175), (car.x+7, car.y+8, 20, 12), border_radius=3)
    p = g["player"]
    pygame.draw.rect(screen, LIME, p, border_radius=7)
    pygame.draw.rect(screen, (238, 255, 193), (p.x+7, p.y+8, 22, 15), border_radius=3)
    text(screen, f"DISTANCE  {g['score']}", font_mid, WHITE, (20, 18))
    text(screen, f"SPEED  {int(g['speed']*20)}", font_small, LIME, (20, 52))

def new_snake():
    return {"body": [(10, 10), (9, 10), (8, 10)], "dir": (1, 0),
            "food": (15, 10), "timer": 0, "score": 0, "over": False}

def snake_update(g, dt):
    g["timer"] += dt
    if g["timer"] < max(.075, .14 - g["score"]*.001): return
    g["timer"] = 0
    dx, dy = g["dir"]
    head = (g["body"][0][0]+dx, g["body"][0][1]+dy)
    if head[0] < 0 or head[0] >= 25 or head[1] < 0 or head[1] >= 18 or head in g["body"][:-1]:
        g["over"] = True
        return
    g["body"].insert(0, head)
    if head == g["food"]:
        g["score"] += 10
        while True:
            food = (random.randrange(25), random.randrange(18))
            if food not in g["body"]:
                g["food"] = food
                break
    else:
        g["body"].pop()

def snake_draw(g):
    screen.fill(BG)
    ox, oy, cell = 150, 90, 20
    pygame.draw.rect(screen, PANEL, (ox-4, oy-4, 508, 368), border_radius=5)
    for x, y in g["body"]:
        pygame.draw.rect(screen, LIME, (ox+x*cell, oy+y*cell, 18, 18), border_radius=4)
    fx, fy = g["food"]
    pygame.draw.circle(screen, RED, (ox+fx*cell+9, oy+fy*cell+9), 7)
    text(screen, f"SCORE  {g['score']}", font_mid, WHITE, (20, 20))

def new_pong():
    return {"p": pygame.Rect(70, 260, 14, 90), "cpu": pygame.Rect(716, 260, 14, 90),
            "ball": pygame.Rect(393, 293, 16, 16), "vx": 270, "vy": 190,
            "score": 0, "cpu_score": 0, "over": False}

def pong_update(g, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]: g["p"].y -= int(390*dt)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: g["p"].y += int(390*dt)
    g["p"].y = max(0, min(HEIGHT-g["p"].height, g["p"].y))
    b, cpu = g["ball"], g["cpu"]
    target = b.centery - cpu.height//2
    cpu.y += max(-300*dt, min(300*dt, target-cpu.y))
    b.x += int(g["vx"]*dt); b.y += int(g["vy"]*dt)
    if b.top <= 0 or b.bottom >= HEIGHT: g["vy"] *= -1
    if b.colliderect(g["p"]) and g["vx"] < 0:
        g["vx"] *= -1.04
    if b.colliderect(cpu) and g["vx"] > 0:
        g["vx"] *= -1.04
    if b.left < 0:
        g["cpu_score"] += 1; g["ball"].center = (400, 300); g["vx"] = 270
    if b.right > WIDTH:
        g["score"] += 1; g["ball"].center = (400, 300); g["vx"] = -270
    if g["score"] >= 5 or g["cpu_score"] >= 5: g["over"] = True

def pong_draw(g):
    screen.fill(BG)
    for y in range(0, HEIGHT, 28): pygame.draw.rect(screen, (65, 76, 96), (398, y, 4, 14))
    pygame.draw.rect(screen, LIME, g["p"], border_radius=4)
    pygame.draw.rect(screen, CYAN, g["cpu"], border_radius=4)
    pygame.draw.ellipse(screen, WHITE, g["ball"])
    text(screen, f"{g['score']}     {g['cpu_score']}", font_title, WHITE, (400, 35), True)
    text(screen, "YOU: W/S OR ↑/↓", font_small, MUTED, (25, 20))

def new_breakout():
    bricks = [pygame.Rect(115+c*96, 95+r*30, 82, 20) for r in range(4) for c in range(6)]
    return {"p": pygame.Rect(345, 535, 110, 12), "ball": pygame.Rect(395, 510, 14, 14),
            "vx": 250, "vy": -260, "bricks": bricks, "score": 0, "over": False, "win": False}

def breakout_update(g, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: g["p"].x -= int(420*dt)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: g["p"].x += int(420*dt)
    g["p"].x = max(0, min(WIDTH-g["p"].width, g["p"].x))
    b = g["ball"]
    b.x += int(g["vx"]*dt); b.y += int(g["vy"]*dt)
    if b.left <= 0 or b.right >= WIDTH: g["vx"] *= -1
    if b.top <= 0: g["vy"] *= -1
    if b.colliderect(g["p"]) and g["vy"] > 0:
        g["vy"] *= -1
        offset = (b.centerx-g["p"].centerx)/(g["p"].width/2)
        g["vx"] = offset*330
    for brick in g["bricks"][:]:
        if b.colliderect(brick):
            g["bricks"].remove(brick); g["vy"] *= -1; g["score"] += 10; break
    if b.top > HEIGHT: g["over"] = True
    if not g["bricks"]: g["over"] = True; g["win"] = True

def breakout_draw(g):
    screen.fill(BG)
    colors = [LIME, CYAN, (151, 126, 255), RED]
    for i, brick in enumerate(g["bricks"]):
        pygame.draw.rect(screen, colors[(brick.y//30-3)%4], brick, border_radius=3)
    pygame.draw.rect(screen, WHITE, g["p"], border_radius=6)
    pygame.draw.ellipse(screen, LIME, g["ball"])
    text(screen, f"SCORE  {g['score']}", font_mid, WHITE, (20, 20))

def new_dodger():
    return {"p": pygame.Rect(382, 510, 36, 36), "blocks": [], "timer": 0,
            "score": 0, "speed": 220, "over": False}

def dodger_update(g, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: g["p"].x -= int(390*dt)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: g["p"].x += int(390*dt)
    g["p"].x = max(0, min(WIDTH-g["p"].width, g["p"].x))
    g["timer"] += dt
    g["score"] += int(dt*10)
    g["speed"] = min(600, 220+g["score"]*1.5)
    if g["timer"] > max(.25, .8-g["score"]*.002):
        x = random.randint(0, WIDTH-28)
        g["blocks"].append(pygame.Rect(x, -30, random.randint(22, 42), random.randint(22, 42)))
        g["timer"] = 0
    for block in g["blocks"][:]:
        block.y += int(g["speed"]*dt)
        if block.top > HEIGHT: g["blocks"].remove(block)
        elif block.colliderect(g["p"]): g["over"] = True

def dodger_draw(g):
    draw_background()
    pygame.draw.rect(screen, LIME, g["p"], border_radius=5)
    for block in g["blocks"]:
        pygame.draw.rect(screen, RED, block, border_radius=4)
    text(screen, f"SURVIVAL  {g['score']}", font_mid, WHITE, (20, 20))

factories = {1: new_racer, 2: new_snake, 3: new_pong, 4: new_breakout, 5: new_dodger}
updates = {1: racer_update, 2: snake_update, 3: pong_update, 4: breakout_update, 5: dodger_update}
drawers = {1: racer_draw, 2: snake_draw, 3: pong_draw, 4: breakout_draw, 5: dodger_draw}
titles = {1: "NEON RACER", 2: "SNAKE", 3: "PONG", 4: "BREAKOUT", 5: "BLOCK DODGER"}

game_id = 0
game = None
game_over = False
running = True

async def main():
    global game_id, game, game_over, running
    while running:
        dt = min(clock.tick(60) / 1000, 0.04)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_id == 0:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                        game_id = int(event.unicode)
                        game = factories[game_id]()
                        game_over = False
                elif event.key == pygame.K_ESCAPE:
                    game_id = 0
                    game = None
                    game_over = False
                elif game_over and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    game = factories[game_id]()
                    game_over = False
                elif game_id == 2 and not game_over:
                    dirs = {pygame.K_UP:(0,-1), pygame.K_w:(0,-1), pygame.K_DOWN:(0,1),
                            pygame.K_s:(0,1), pygame.K_LEFT:(-1,0), pygame.K_a:(-1,0),
                            pygame.K_RIGHT:(1,0), pygame.K_d:(1,0)}
                    if event.key in dirs:
                        nd = dirs[event.key]
                        if nd != (-game["dir"][0], -game["dir"][1]):
                            game["dir"] = nd

        if game_id == 0:
            menu()
        elif game_over:
            if game_id == 4 and game.get("win"):
                end_screen("YOU CLEARED IT", game["score"])
            else:
                end_screen("GAME OVER", game.get("score", 0))
            text(screen, titles[game_id], font_small, MUTED, (WIDTH//2, 420), True)
        else:
            updates[game_id](game, dt)
            drawers[game_id](game)
            if game["over"]:
                game_over = True

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
