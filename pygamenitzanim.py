import pygame
import random

pygame.init()
pygame.mixer.init()

# מסך
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("תזוזה טקטונית - גרסה משודרגת")

# צבעים
BLUE = (50, 150, 255)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

# קבצי קול
collision_sound = pygame.mixer.Sound("collision.wav")
eruption_sound = pygame.mixer.Sound("eruption_volcano.wav")
crack_sound = pygame.mixer.Sound("crack.wav")

# כדור הארץ
earth_radius = 250
earth_center = (WIDTH // 2, HEIGHT // 2)

# לוחות
plate_size = (100, 100)
plate1 = pygame.Rect(150, 250, *plate_size)
plate2 = pygame.Rect(550, 250, *plate_size)

# מהירות
plate1_speed = 2
plate2_speed = 2

# רעידות
shake_offset = [0, 0]
shake_timer = 0

# סדקים
cracks = []

# פונקציה לציור סדק זיגזג
def draw_crack(surface, x, y, length=20):
    points = []
    current_x, current_y = x, y
    for i in range(length):
        current_x += random.randint(-2, 2)
        current_y += random.randint(1, 3)
        points.append((current_x, current_y))
    pygame.draw.lines(surface, GRAY, False, points, 2)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
running = True

while running:
    screen.fill((20, 20, 40))  # רקע חלל

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- קלט משתמש ---
    keys = pygame.key.get_pressed()
    # לוח 1 - חצים
    if keys[pygame.K_LEFT]:
        plate1.x -= plate1_speed
    if keys[pygame.K_RIGHT]:
        plate1.x += plate1_speed
    if keys[pygame.K_UP]:
        plate1.y -= plate1_speed
    if keys[pygame.K_DOWN]:
        plate1.y += plate1_speed
    # לוח 2 - WASD
    if keys[pygame.K_a]:
        plate2.x -= plate2_speed
    if keys[pygame.K_d]:
        plate2.x += plate2_speed
    if keys[pygame.K_w]:
        plate2.y -= plate2_speed
    if keys[pygame.K_s]:
        plate2.y += plate2_speed

    # --- התנגשות / התרחקות ---
    if plate1.colliderect(plate2):
        intersection = plate1.clip(plate2)
        # רעידות
        shake_timer = 10
        shake_offset = [random.randint(-5, 5), random.randint(-5, 5)]
        # סאונד
        collision_sound.play()
        eruption_sound.play()
        # האטת מהירות
        plate1_speed = max(1, plate1_speed - 0.5)
        plate2_speed = max(1, plate2_speed - 0.5)
    else:
        # התרחקות → מהירות עולה
        plate1_speed = min(4, plate1_speed + 0.05)
        plate2_speed = min(4, plate2_speed + 0.05)
        # הוספת סדק אקראי על הקרום
        if random.random() < 0.01:
            x = random.randint(earth_center[0] - earth_radius, earth_center[0] + earth_radius)
            y = random.randint(earth_center[1] - earth_radius, earth_center[1] + earth_radius)
            cracks.append((x, y))
            crack_sound.play()

    # --- ציור כדור הארץ עם gradient ---
    earth_pos = (earth_center[0] + shake_offset[0], earth_center[1] + shake_offset[1])
    for r in range(earth_radius, 0, -1):
        color = (
            BLUE[0],
            max(0, BLUE[1] - int((earth_radius - r) * 0.2)),
            max(0, BLUE[2] - int((earth_radius - r) * 0.2))
        )
        pygame.draw.circle(screen, color, earth_pos, r)

    # הוספת צל להיראות יותר תלת-ממדית
    pygame.draw.circle(screen, BLACK, (earth_pos[0] + 10, earth_pos[1] - 10), earth_radius // 4)

    # ציור סדקים
    for c in cracks:
        draw_crack(screen, c[0], c[1])

    # ציור לוחות
    pygame.draw.rect(screen, RED, plate1)
    pygame.draw.rect(screen, RED, plate2)

    # ציור הר געש בעת התנגשות
    if plate1.colliderect(plate2):
        pygame.draw.polygon(screen, BROWN, [
            (intersection.centerx, intersection.top - 30),
            (intersection.left, intersection.bottom),
            (intersection.right, intersection.bottom)
        ])

    # --- הצגת מהירויות על המסך ---
    speed1_text = font.render(f"Plate 1 speed: {plate1_speed:.1f}", True, WHITE)
    speed2_text = font.render(f"Plate 2 speed: {plate2_speed:.1f}", True, WHITE)
    screen.blit(speed1_text, (10, 10))
    screen.blit(speed2_text, (10, 40))

    # עדכון מסך
    pygame.display.flip()

    # עדכון רעידות
    if shake_timer > 0:
        shake_timer -= 1
    else:
        shake_offset = [0, 0]

    clock.tick(60)

pygame.quit()
