import pygame
import math
import sys

# ------------------------------------------------------------
# Constants (matching the Java version)
# ------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
G = 0.20
RESTITUTION = 1.0
SIZE = 20
EPS = 1e-8

# ------------------------------------------------------------
# BouncingBox – same physics as the final Java class
# ------------------------------------------------------------
class BouncingBox:
    def __init__(self, x, y, color, vx, vy):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color

    def draw(self, surface):
        half = SIZE / 2.0
        rect = pygame.Rect(int(self.x - half), int(self.y - half), SIZE, SIZE)

        # filled box
        pygame.draw.rect(surface, self.color, rect)
        # cyan outline
        pygame.draw.rect(surface, (0, 255, 255), rect, 3)

        self.advance_frame()

    def advance_frame(self):
        half = SIZE / 2.0
        dt = 1.0

        # ---------- horizontal ----------
        self.x += self.vx * dt
        if self.x - half < 0:
            self.x = half
            self.vx = -self.vx * RESTITUTION
        elif self.x + half > WIDTH:
            self.x = WIDTH - half
            self.vx = -self.vx * RESTITUTION

        # ---------- vertical with at most one analytic collision ----------
        t_floor = self.time_to_floor(dt)
        t_ceil  = self.time_to_ceiling(dt)

        t_hit = dt
        hit_floor = False
        hit_ceil  = False

        if t_floor >= 0.0 and t_floor < t_hit:
            t_hit = t_floor
            hit_floor = True
        if t_ceil >= 0.0 and t_ceil < t_hit:
            t_hit = t_ceil
            hit_ceil = True
            hit_floor = False

        # analytic advance up to impact (or end of frame)
        self.y  += self.vy * t_hit + 0.5 * G * t_hit * t_hit
        self.vy += G * t_hit

        if hit_floor:
            self.y  = HEIGHT - half
            self.vy = -self.vy * RESTITUTION
            rem = dt - t_hit
            if rem > EPS:
                self.y  += self.vy * rem + 0.5 * G * rem * rem
                self.vy += G * rem
        elif hit_ceil:
            self.y  = half
            self.vy = -self.vy * RESTITUTION
            rem = dt - t_hit
            if rem > EPS:
                self.y  += self.vy * rem + 0.5 * G * rem * rem
                self.vy += G * rem

    def time_to_floor(self, max_t):
        half = SIZE / 2.0
        h = HEIGHT - (self.y + half)

        if h <= EPS:
            return 0.0 if self.vy > 0 else -1.0

        disc = self.vy * self.vy + 2.0 * G * h
        if disc < 0.0:
            return -1.0

        t = (-self.vy + math.sqrt(disc)) / G
        return t if 0.0 <= t <= max_t else -1.0

    def time_to_ceiling(self, max_t):
        half = SIZE / 2.0
        h = self.y - half

        if h <= EPS:
            return 0.0 if self.vy < 0 else -1.0

        disc = self.vy * self.vy - 2.0 * G * h
        if disc < 0.0:
            return -1.0

        t = (-self.vy - math.sqrt(disc)) / G
        return t if 0.0 <= t <= max_t else -1.0

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Cubes")
    clock = pygame.time.Clock()

    boxes = [
        BouncingBox(150, 150, (0, 0, 255),    1.7,  1.5),   # blue
        BouncingBox(400, 300, (0, 255, 255),  0.0,  0.0),   # cyan
        BouncingBox(100, 200, (0, 255, 0),   -2.0,  1.0),   # green
        BouncingBox(200, 100, (255, 0, 0),    1.0, -1.0),   # red
        BouncingBox(250,  50, (255, 165, 0), -4.0, -1.0),   # orange
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))          # black background

        for box in boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()