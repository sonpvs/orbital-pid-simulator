import pygame
import math
import random

# --- CÁC HẰNG SỐ HỆ THỐNG ---
WIDTH, HEIGHT = 1100, 850
CENTER = [WIDTH // 2, HEIGHT // 2]
G, M_EARTH, DT = 500, 120, 0.1

# Màu sắc
SPACE_BLACK = (5, 5, 12)
EARTH_BLUE  = (0, 150, 255)
STATION_COLOR = (200, 200, 200)
FUEL_COLOR = (255, 50, 50)
UI_GREEN = (0, 255, 150)
SHIP_BODY = (220, 220, 220)
RADAR_BG = (10, 25, 10) # Màu xanh quân đội tối cho radar

class Particle:
    def __init__(self, pos, vel):
        self.pos = list(pos)
        self.vel = [vel[0] + random.uniform(-1, 1), vel[1] + random.uniform(-1, 1)]
        self.life = 200
    def update(self):
        self.pos[0] += self.vel[0] * 0.5
        self.pos[1] += self.vel[1] * 0.5
        self.life -= 15
    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, (self.life, self.life//2, 0), (int(self.pos[0]), int(self.pos[1])), 2)

class SpaceGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = [220.0, 0.0]
        self.vel = [0.0, 16.0]
        self.fuel = 1500.0
        self.particles = []
        self.station_r = 350.0
        self.station_angle = 0.0
        self.station_v = math.sqrt((G * M_EARTH) / self.station_r)
        self.status = "MISSION START"

    def apply_thrust(self, dx, dy, power=0.5):
        if self.fuel > 0:
            self.vel[0] += dx * power
            self.vel[1] += dy * power
            self.fuel -= 1.0
            s_pos = (self.pos[0] + CENTER[0], self.pos[1] + CENTER[1])
            for _ in range(3):
                self.particles.append(Particle(s_pos, [-dx*8, -dy*8]))
            return True
        return False

    def update(self, auto_pilot, manual_thrust):
        x, y = self.pos
        r = math.sqrt(x**2 + y**2)
        if r < 30: 
            self.status = "CRASHED"
            return self.status

        accel_g = -G * M_EARTH / (r**2)
        self.vel[0] += accel_g * (x / r) * DT
        self.vel[1] += accel_g * (y / r) * DT

        self.station_angle += (self.station_v / self.station_r) * DT
        st_x = self.station_r * math.cos(self.station_angle)
        st_y = self.station_r * math.sin(self.station_angle)

        if manual_thrust != [0, 0]:
            self.apply_thrust(manual_thrust[0], manual_thrust[1])
        elif auto_pilot and self.fuel > 0:
            dx_st, dy_st = st_x - x, st_y - y
            dist = math.sqrt(dx_st**2 + dy_st**2)
            if dist < 12:
                self.status = "DOCKING SUCCESS!"
            else:
                self.apply_thrust(dx_st/dist, dy_st/dist, power=0.15)
                self.status = "AUTO-PILOT ACTIVE"

        self.pos[0] += self.vel[0] * DT
        self.pos[1] += self.vel[1] * DT
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)
        return self.status

def draw_spaceship(screen, pos, vel):
    angle = math.atan2(vel[1], vel[0])
    ship_points = [(15, 0), (-10, -8), (-7, 0), (-10, 8)]
    rotated_points = []
    for pt in ship_points:
        rx = pt[0] * math.cos(angle) - pt[1] * math.sin(angle)
        ry = pt[0] * math.sin(angle) + pt[1] * math.cos(angle)
        rotated_points.append((rx + pos[0], ry + pos[1]))
    pygame.draw.polygon(screen, SHIP_BODY, rotated_points)

def draw_radar(screen, game):
    """Vẽ radar thu nhỏ ở góc màn hình"""
    radar_size = 150
    radar_x, radar_y = 20, HEIGHT - radar_size - 20
    radar_center = (radar_x + radar_size // 2, radar_y + radar_size // 2)
    
    # Vẽ khung radar
    pygame.draw.rect(screen, RADAR_BG, (radar_x, radar_y, radar_size, radar_size))
    pygame.draw.rect(screen, UI_GREEN, (radar_x, radar_y, radar_size, radar_size), 2)
    
    # Tỉ lệ thu nhỏ (Scale down)
    scale = radar_size / 1000 # 1000 pixel thực tế = 150 pixel radar
    
    # 1. Trái đất trên radar
    pygame.draw.circle(screen, EARTH_BLUE, radar_center, int(30 * scale) + 1)
    
    # 2. Trạm ISS trên radar (Chấm trắng)
    st_x = game.station_r * math.cos(game.station_angle) * scale
    st_y = game.station_r * math.sin(game.station_angle) * scale
    pygame.draw.circle(screen, STATION_COLOR, (int(radar_center[0] + st_x), int(radar_center[1] + st_y)), 3)
    
    # 3. Phi thuyền trên radar (Chấm vàng)
    sh_x = game.pos[0] * scale
    sh_y = game.pos[1] * scale
    pygame.draw.circle(screen, (255, 215, 0), (int(radar_center[0] + sh_x), int(radar_center[1] + sh_y)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 18)
    game = SpaceGame()
    auto_pilot = False

    while True:
        screen.fill(SPACE_BLACK)
        manual_thrust = [0, 0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: auto_pilot = not auto_pilot
                if event.key == pygame.K_r: game.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:    manual_thrust[1] = -1
        if keys[pygame.K_DOWN]:  manual_thrust[1] = 1
        if keys[pygame.K_LEFT]:  manual_thrust[0] = -1
        if keys[pygame.K_RIGHT]: manual_thrust[0] = 1

        status = game.update(auto_pilot, manual_thrust)

        # Vẽ Trái Đất & Trạm
        pygame.draw.circle(screen, EARTH_BLUE, CENTER, 30)
        st_x = int(game.station_r * math.cos(game.station_angle) + CENTER[0])
        st_y = int(game.station_r * math.sin(game.station_angle) + CENTER[1])
        pygame.draw.rect(screen, STATION_COLOR, (st_x-5, st_y-5, 10, 10))
        
        for p in game.particles: p.draw(screen)
        draw_spaceship(screen, (game.pos[0] + CENTER[0], game.pos[1] + CENTER[1]), game.vel)

        # Vẽ Radar
        draw_radar(screen, game)

        # UI
        ui_lines = [f"FUEL: {int(game.fuel)} kg", f"AUTO-PILOT: {'ON' if auto_pilot else 'OFF'}", f"STATUS: {status}"]
        for i, text in enumerate(ui_lines):
            screen.blit(font.render(text, True, UI_GREEN), (20, 20 + i*25))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()