import pygame
import random
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Constants - FASTER GAMEPLAY
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CARD_WIDTH = 160
CARD_HEIGHT = 200
CARD_MARGIN = 20
ROWS = 3
COLS = 4
REVEAL_TIME = 1800  # Faster - reduced from 2500
CARD_RADIUS = 25
ANIMATION_SPEED = 15  # Faster animations

# Disney-style magical colors
WITCH_COLORS = [
    ((255, 20, 147), "Rose Spell"),      # Deep Pink
    ((138, 43, 226), "Purple Magic"),   # Blue Violet
    ((0, 191, 255), "Sky Potion"),      # Deep Sky Blue
    ((50, 205, 50), "Forest Brew"),     # Lime Green
    ((255, 165, 0), "Pumpkin Glow"),    # Orange
    ((255, 215, 0), "Golden Charm"),    # Gold
]

# Night theme colors
NIGHT_SKY_START = (25, 25, 80)
NIGHT_SKY_END = (60, 25, 100)
MOON_COLOR = (255, 255, 220)
STAR_COLOR = (255, 255, 255)
CASTLE_COLOR = (40, 40, 80)
CASTLE_LIGHT = (255, 255, 150)
WITCH_HAT = (75, 0, 130)
WITCH_DRESS = (138, 43, 226)
WITCH_SKIN = (255, 220, 177)
FAIRY_COLORS = [(255, 192, 203), (173, 216, 230), (144, 238, 144), (255, 215, 0)]

class Moon:
    def __init__(self):
        self.x = WINDOW_WIDTH - 150
        self.y = 100
        self.radius = 40
        self.glow_intensity = 0
    
    def update(self):
        self.glow_intensity = 0.3 + 0.2 * math.sin(pygame.time.get_ticks() * 0.003)  # Faster
    
    def draw(self, screen):
        # Draw moon glow
        glow_radius = int(self.radius + 20 * self.glow_intensity)
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_color = (*MOON_COLOR, int(30 * self.glow_intensity))
        pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))
        
        # Draw moon
        pygame.draw.circle(screen, MOON_COLOR, (int(self.x), int(self.y)), self.radius)
        
        # Draw moon craters
        pygame.draw.circle(screen, (240, 240, 200), (int(self.x - 10), int(self.y - 8)), 5)
        pygame.draw.circle(screen, (240, 240, 200), (int(self.x + 8), int(self.y + 5)), 3)
        pygame.draw.circle(screen, (240, 240, 200), (int(self.x - 5), int(self.y + 12)), 4)

class TangleCastle:
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.width = int(250 * scale)
        self.height = int(180 * scale)
        self.window_glow = 0
        
    def update(self):
        self.window_glow = 0.5 + 0.3 * math.sin(pygame.time.get_ticks() * 0.004)
    
    def draw(self, screen):
        # Main castle foundation
        foundation = pygame.Rect(self.x, self.y + self.height - 40, self.width, 40)
        pygame.draw.rect(screen, (30, 30, 60), foundation)
        
        # Main castle body - Tangled style with curves
        main_body = pygame.Rect(self.x + 30, self.y + 60, self.width - 60, self.height - 60)
        pygame.draw.rect(screen, CASTLE_COLOR, main_body)
        
        # Curved castle walls
        for i in range(5):
            curve_x = self.x + 30 + i * (self.width - 60) // 4
            curve_height = int(20 * math.sin(i * 0.8) * self.scale)
            curve_rect = pygame.Rect(curve_x, self.y + 60 - curve_height, 
                                   (self.width - 60) // 4, self.height - 60 + curve_height)
            pygame.draw.rect(screen, (50, 50, 90), curve_rect)
        
        # Multiple towers - Tangled style
        towers = [
            # Left tower - tall and thin
            {'x': self.x - 10, 'y': self.y - 20, 'w': int(50 * self.scale), 'h': int(100 * self.scale)},
            # Right tower - medium
            {'x': self.x + self.width - 40, 'y': self.y - 10, 'w': int(45 * self.scale), 'h': int(80 * self.scale)},
            # Center tower - tallest (Rapunzel's tower)
            {'x': self.x + self.width//2 - 25, 'y': self.y - 60, 'w': int(50 * self.scale), 'h': int(140 * self.scale)},
            # Left-center tower
            {'x': self.x + 60, 'y': self.y - 30, 'w': int(40 * self.scale), 'h': int(90 * self.scale)},
            # Right-center tower
            {'x': self.x + self.width - 100, 'y': self.y - 25, 'w': int(42 * self.scale), 'h': int(85 * self.scale)},
        ]
        
        # Draw towers with Tangled-style details
        for i, tower in enumerate(towers):
            # Tower body
            tower_rect = pygame.Rect(tower['x'], tower['y'], tower['w'], tower['h'])
            pygame.draw.rect(screen, CASTLE_COLOR, tower_rect)
            
            # Tower decorative bands
            for band in range(3):
                band_y = tower['y'] + band * tower['h'] // 3
                pygame.draw.rect(screen, (60, 60, 120), 
                               (tower['x'], band_y, tower['w'], 3))
            
            # Conical roof - Tangled style
            roof_height = int(25 * self.scale)
            roof_points = [
                (tower['x'] + tower['w']//2, tower['y'] - roof_height),
                (tower['x'] - 5, tower['y']),
                (tower['x'] + tower['w'] + 5, tower['y'])
            ]
            pygame.draw.polygon(screen, (80, 40, 120), roof_points)
            
            # Roof decorative elements
            pygame.draw.circle(screen, (120, 80, 160), 
                             (tower['x'] + tower['w']//2, tower['y'] - roof_height), 4)
            
            # Tower windows with magical glow
            window_count = max(2, tower['h'] // 30)
            for w in range(window_count):
                window_y = tower['y'] + 20 + w * (tower['h'] - 40) // window_count
                window_x = tower['x'] + tower['w']//2 - 6
                
                # Special glowing window for center tower (Rapunzel's)
                if i == 2 and w == window_count - 1:  # Top window of center tower
                    # Rapunzel's glowing window
                    glow_intensity = self.window_glow
                    window_color = (255, 255, 150, int(200 * glow_intensity))
                    
                    # Window glow effect
                    glow_surf = pygame.Surface((24, 24), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surf, window_color, (12, 12), 12)
                    screen.blit(glow_surf, (window_x - 6, window_y - 6))
                    
                    # Bright window
                    pygame.draw.rect(screen, (255, 255, 200), (window_x, window_y, 12, 16))
                    
                    # Hair flowing from window (Rapunzel's hair)
                    hair_points = []
                    for h in range(8):
                        hair_x = window_x + 6 + math.sin(pygame.time.get_ticks() * 0.002 + h) * 3
                        hair_y = window_y + 16 + h * 8
                        hair_points.append((hair_x, hair_y))
                    
                    if len(hair_points) > 1:
                        pygame.draw.lines(screen, (255, 215, 0), False, hair_points, 3)
                else:
                    # Regular windows
                    pygame.draw.rect(screen, CASTLE_LIGHT, (window_x, window_y, 12, 16))
                
                # Window frame
                pygame.draw.rect(screen, (100, 100, 140), (window_x - 1, window_y - 1, 14, 18), 2)
        
        # Castle gate
        gate_width = int(40 * self.scale)
        gate_height = int(50 * self.scale)
        gate_x = self.x + self.width//2 - gate_width//2
        gate_y = self.y + self.height - gate_height
        
        # Gate arch
        pygame.draw.rect(screen, (20, 20, 40), (gate_x, gate_y, gate_width, gate_height))
        pygame.draw.arc(screen, (20, 20, 40), (gate_x, gate_y - gate_width//2, gate_width, gate_width), 0, math.pi, gate_width//4)
        
        # Gate details
        pygame.draw.rect(screen, (60, 60, 100), (gate_x + 5, gate_y + 10, gate_width - 10, gate_height - 10))
        
        # Decorative flags on towers
        for i, tower in enumerate(towers):
            if i % 2 == 0:  # Every other tower gets a flag
                flag_x = tower['x'] + tower['w']//2
                flag_y = tower['y'] - int(25 * self.scale)
                flag_points = [
                    (flag_x, flag_y),
                    (flag_x + 15, flag_y + 5),
                    (flag_x + 12, flag_y + 12),
                    (flag_x, flag_y + 8)
                ]
                pygame.draw.polygon(screen, (160, 80, 200), flag_points)

class FlyingFairy:
    def __init__(self):
        self.x = random.uniform(-50, WINDOW_WIDTH + 50)
        self.y = random.uniform(100, 400)
        self.speed = random.uniform(1.0, 2.5)  # Faster
        self.bob_speed = random.uniform(0.008, 0.015)  # Faster bobbing
        self.bob_amplitude = random.uniform(15, 25)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.uniform(-0.3, 0.3)
        self.color = random.choice(FAIRY_COLORS)
        self.wing_beat = 0
        self.trail = []
        self.size = random.uniform(0.8, 1.2)
        
    def update(self):
        # Move fairy
        self.x += self.speed * self.direction_x
        self.y += self.direction_y + math.sin(pygame.time.get_ticks() * self.bob_speed) * 0.5
        
        # Wing beating animation - faster
        self.wing_beat = pygame.time.get_ticks() * 0.02
        
        # Reverse direction at edges
        if self.x < -100 or self.x > WINDOW_WIDTH + 100:
            self.direction_x *= -1
            self.y = random.uniform(100, 400)
        
        if self.y < 50 or self.y > WINDOW_HEIGHT - 100:
            self.direction_y *= -1
        
        # Add to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:  # Shorter trail for performance
            self.trail.pop(0)
    
    def draw(self, screen):
        # Draw fairy trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(100 * (i / len(self.trail)))
            if alpha > 0:
                trail_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                trail_color = (*self.color, alpha)
                pygame.draw.circle(trail_surf, trail_color, (3, 3), 3)
                screen.blit(trail_surf, (int(trail_x - 3), int(trail_y - 3)))
        
        # Fairy body
        body_x, body_y = int(self.x), int(self.y)
        body_size = int(4 * self.size)
        
        # Wings - animated
        wing_offset = math.sin(self.wing_beat) * 3
        wing_color = (*self.color, 150)
        
        # Wing surfaces
        wing_surf = pygame.Surface((16, 12), pygame.SRCALPHA)
        
        # Left wing
        left_wing_points = [
            (8 - wing_offset, 6),
            (2, 2 + wing_offset),
            (0, 8),
            (4, 10 - wing_offset)
        ]
        pygame.draw.polygon(wing_surf, wing_color, left_wing_points)
        
        # Right wing
        right_wing_points = [
            (8 + wing_offset, 6),
            (14, 2 + wing_offset),
            (16, 8),
            (12, 10 - wing_offset)
        ]
        pygame.draw.polygon(wing_surf, wing_color, right_wing_points)
        
        screen.blit(wing_surf, (body_x - 8, body_y - 6))
        
        # Fairy body (glowing)
        glow_surf = pygame.Surface((body_size * 3, body_size * 3), pygame.SRCALPHA)
        glow_color = (*self.color, 80)
        pygame.draw.circle(glow_surf, glow_color, (body_size * 3 // 2, body_size * 3 // 2), body_size * 3 // 2)
        screen.blit(glow_surf, (body_x - body_size * 3 // 2, body_y - body_size * 3 // 2))
        
        # Fairy core
        pygame.draw.circle(screen, self.color, (body_x, body_y), body_size)
        pygame.draw.circle(screen, (255, 255, 255), (body_x, body_y), body_size // 2)

class FlyingWitch:
    def __init__(self):
        self.x = -100
        self.y = 200
        self.speed = 2.0  # Faster
        self.bob_offset = 0
        self.direction = 1
        self.size = 1.0
    
    def update(self):
        # Move witch across screen - faster
        self.x += self.speed * self.direction
        
        # Reverse direction when reaching edges
        if self.x > WINDOW_WIDTH + 100:
            self.direction = -1
            self.y = random.uniform(150, 300)
        elif self.x < -100:
            self.direction = 1
            self.y = random.uniform(150, 300)
        
        # Bobbing motion - faster
        self.bob_offset = math.sin(pygame.time.get_ticks() * 0.008) * 10
    
    def draw(self, screen):
        current_y = self.y + self.bob_offset
        
        # Witch body parts
        head_x = int(self.x)
        head_y = int(current_y)
        
        # Broomstick
        broom_length = 60
        broom_start = (head_x - 30, head_y + 20)
        broom_end = (head_x - 30 + broom_length, head_y + 25)
        pygame.draw.line(screen, (139, 69, 19), broom_start, broom_end, 4)
        
        # Broom bristles
        for i in range(8):
            bristle_x = broom_end[0] - 15 + i * 2
            bristle_y = broom_end[1] + random.randint(-5, 5)
            pygame.draw.line(screen, (205, 133, 63), 
                           (bristle_x, bristle_y), (bristle_x + 10, bristle_y + 8), 2)
        
        # Witch dress
        dress_points = [
            (head_x - 15, head_y + 10),
            (head_x + 15, head_y + 10),
            (head_x + 20, head_y + 40),
            (head_x - 20, head_y + 40)
        ]
        pygame.draw.polygon(screen, WITCH_DRESS, dress_points)
        
        # Witch head
        pygame.draw.circle(screen, WITCH_SKIN, (head_x, head_y), 12)
        
        # Witch hat
        hat_points = [
            (head_x, head_y - 25),
            (head_x - 12, head_y - 8),
            (head_x + 12, head_y - 8)
        ]
        pygame.draw.polygon(screen, WITCH_HAT, hat_points)
        
        # Hat brim
        pygame.draw.ellipse(screen, WITCH_HAT, (head_x - 15, head_y - 12, 30, 8))
        
        # Witch hair
        pygame.draw.circle(screen, (139, 69, 19), (head_x - 8, head_y - 2), 4)
        pygame.draw.circle(screen, (139, 69, 19), (head_x + 8, head_y - 2), 4)
        
        # Eyes
        pygame.draw.circle(screen, (255, 255, 255), (head_x - 4, head_y - 2), 2)
        pygame.draw.circle(screen, (255, 255, 255), (head_x + 4, head_y - 2), 2)
        pygame.draw.circle(screen, (0, 0, 0), (head_x - 4, head_y - 2), 1)
        pygame.draw.circle(screen, (0, 0, 0), (head_x + 4, head_y - 2), 1)
        
        # Smile
        pygame.draw.arc(screen, (255, 100, 100), (head_x - 6, head_y + 2, 12, 8), 0, math.pi, 2)
        
        # Magic sparkles around witch
        for i in range(5):
            sparkle_x = head_x + random.randint(-30, 30)
            sparkle_y = int(current_y) + random.randint(-20, 20)
            sparkle_size = random.randint(2, 4)
            color = random.choice([(255, 215, 0), (255, 192, 203), (173, 216, 230)])
            
            # Draw sparkle as a star
            self.draw_sparkle(screen, sparkle_x, sparkle_y, sparkle_size, color)
    
    def draw_sparkle(self, screen, x, y, size, color):
        # Draw a simple 4-pointed star
        points = [
            (x, y - size),
            (x + size//2, y - size//2),
            (x + size, y),
            (x + size//2, y + size//2),
            (x, y + size),
            (x - size//2, y + size//2),
            (x - size, y),
            (x - size//2, y - size//2)
        ]
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)

class MagicalSparkle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(1, 4)
        self.life = random.uniform(40, 80)  # Faster lifecycle
        self.max_life = self.life
        self.twinkle_speed = random.uniform(0.08, 0.2)  # Faster twinkling
        self.drift_x = random.uniform(-0.5, 0.5)
        self.drift_y = random.uniform(-1.2, -0.4)  # Faster drift
        self.color = random.choice([
            (255, 255, 255), (255, 215, 0), (255, 192, 203),
            (173, 216, 230), (144, 238, 144), (221, 160, 221)
        ])
    
    def update(self):
        self.x += self.drift_x
        self.y += self.drift_y
        self.life -= 1.5  # Faster decay
        return self.life > 0
    
    def draw(self, screen):
        if self.life <= 0:
            return
        
        alpha = int(255 * (self.life / self.max_life))
        twinkle = abs(math.sin(pygame.time.get_ticks() * self.twinkle_speed))
        size = int(self.size * twinkle * (self.life / self.max_life))
        
        if size > 0:
            sparkle_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            
            # Draw cross pattern for sparkle
            pygame.draw.line(sparkle_surf, color_with_alpha, 
                           (size * 2 - size, size * 2), (size * 2 + size, size * 2), 2)
            pygame.draw.line(sparkle_surf, color_with_alpha, 
                           (size * 2, size * 2 - size), (size * 2, size * 2 + size), 2)
            
            screen.blit(sparkle_surf, (int(self.x - size * 2), int(self.y - size * 2)))

def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rectangle with rounded corners"""
    if radius <= 0:
        pygame.draw.rect(surface, color, rect)
        return
    
    radius = min(radius, rect.width // 2, rect.height // 2)
    
    rounded_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    pygame.draw.rect(rounded_surf, color, (radius, 0, rect.width - 2*radius, rect.height))
    pygame.draw.rect(rounded_surf, color, (0, radius, rect.width, rect.height - 2*radius))
    
    pygame.draw.circle(rounded_surf, color, (radius, radius), radius)
    pygame.draw.circle(rounded_surf, color, (rect.width - radius, radius), radius)
    pygame.draw.circle(rounded_surf, color, (radius, rect.height - radius), radius)
    pygame.draw.circle(rounded_surf, color, (rect.width - radius, rect.height - radius), radius)
    
    surface.blit(rounded_surf, rect.topleft)

class FloatingParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)  # Faster movement
        self.vy = random.uniform(-4, -1)
        self.color = color
        self.life = 60  # Shorter life for performance
        self.max_life = 60
        self.size = random.uniform(3, 8)
        self.rotation = 0
        self.rotation_speed = random.uniform(-8, 8)  # Faster rotation
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # Faster gravity
        self.rotation += self.rotation_speed
        self.life -= 1.5  # Faster decay
        return self.life > 0
    
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            
            # Draw a simple star
            center = size
            points = []
            for i in range(10):
                angle = i * math.pi / 5 + math.radians(self.rotation)
                if i % 2 == 0:
                    radius = size * 0.8
                else:
                    radius = size * 0.4
                x = center + radius * math.cos(angle)
                y = center + radius * math.sin(angle)
                points.append((x, y))
            
            if len(points) >= 3:
                pygame.draw.polygon(particle_surf, color_with_alpha, points)
            
            screen.blit(particle_surf, (int(self.x - size), int(self.y - size)))

class Card:
    def __init__(self, x, y, color_data, index):
        self.target_x = x
        self.target_y = y
        self.x = x
        self.y = y + 150
        self.color, self.color_name = color_data
        self.index = index
        self.is_revealed = False
        self.is_matched = False
        self.reveal_time = 0
        self.flip_progress = 0
        self.scale = 0.5
        self.target_scale = 1.0
        self.hover = False
        self.entrance_delay = index * 60  # Faster entrance
        self.entrance_complete = False
        self.glow_intensity = 0
        self.sparkles = []
    
    def update(self):
        # Faster entrance animation
        if not self.entrance_complete:
            if pygame.time.get_ticks() > self.entrance_delay:
                self.y += (self.target_y - self.y) * 0.18  # Faster
                self.scale += (self.target_scale - self.scale) * 0.18
                if abs(self.y - self.target_y) < 2 and abs(self.scale - self.target_scale) < 0.02:
                    self.y = self.target_y
                    self.scale = self.target_scale
                    self.entrance_complete = True
        
        # Faster hover effect
        target_scale = 1.08 if self.hover and not self.is_matched else 1.0
        self.target_scale += (target_scale - self.target_scale) * 0.25  # Faster
        
        # Faster glow effect for matched cards
        if self.is_matched:
            self.glow_intensity = 0.5 + 0.3 * math.sin(pygame.time.get_ticks() * 0.008)  # Faster
            # More frequent sparkles
            if random.random() < 0.15:
                rect = self.get_rect()
                self.sparkles.append(MagicalSparkle(
                    rect.centerx + random.uniform(-rect.width//3, rect.width//3),
                    rect.centery + random.uniform(-rect.height//3, rect.height//3)
                ))
        
        # Update sparkles
        self.sparkles = [s for s in self.sparkles if s.update()]
        
        # Faster flip animation
        if self.is_revealed or self.is_matched:
            self.flip_progress = min(1.0, self.flip_progress + 0.18)  # Faster
        else:
            self.flip_progress = max(0.0, self.flip_progress - 0.18)
    
    def draw(self, screen, font, title_font):
        if not self.entrance_complete and pygame.time.get_ticks() < self.entrance_delay:
            return
        
        # Calculate card dimensions with scale
        width = int(CARD_WIDTH * self.target_scale)
        height = int(CARD_HEIGHT * self.target_scale)
        
        # Card position (centered)
        card_x = int(self.x - width // 2 + CARD_WIDTH // 2)
        card_y = int(self.y - height // 2 + CARD_HEIGHT // 2)
        
        # Draw glow effect for matched cards
        if self.is_matched and self.glow_intensity > 0:
            glow_size = int(20 * self.glow_intensity)
            glow_surf = pygame.Surface((width + glow_size * 2, height + glow_size * 2), pygame.SRCALPHA)
            glow_color = (*self.color, int(50 * self.glow_intensity))
            glow_rect = pygame.Rect(glow_size, glow_size, width, height)
            draw_rounded_rect(glow_surf, glow_color, glow_rect, CARD_RADIUS + glow_size//2)
            screen.blit(glow_surf, (card_x - glow_size, card_y - glow_size))
        
        # Draw shadow with rounded corners
        shadow_offset = 5
        shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(0, 0, width, height)
        draw_rounded_rect(shadow_surf, (0, 0, 0, 80), shadow_rect, CARD_RADIUS)
        screen.blit(shadow_surf, (card_x + shadow_offset, card_y + shadow_offset))
        
        # Card rectangle
        card_rect = pygame.Rect(card_x, card_y, width, height)
        
        # Flip effect
        original_width = width
        if self.flip_progress > 0:
            flip_width = int(width * abs(math.cos(self.flip_progress * math.pi)))
            card_rect.width = max(1, flip_width)
            card_rect.x = card_x + (width - card_rect.width) // 2
        
        # Determine card color and content
        if self.flip_progress > 0.5 and (self.is_revealed or self.is_matched):
            # Show color side with gradient
            gradient_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            for i in range(card_rect.height):
                ratio = i / card_rect.height
                r = int(self.color[0] * (1 - ratio * 0.3))
                g = int(self.color[1] * (1 - ratio * 0.3))
                b = int(self.color[2] * (1 - ratio * 0.3))
                pygame.draw.line(gradient_surf, (r, g, b), (0, i), (card_rect.width, i))
            
            # Apply rounded corners to gradient
            temp_rect = pygame.Rect(0, 0, card_rect.width, card_rect.height)
            final_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            draw_rounded_rect(final_surf, (255, 255, 255), temp_rect, CARD_RADIUS)
            final_surf.blit(gradient_surf, (0, 0), special_flags=pygame.BLEND_MULT)
            screen.blit(final_surf, card_rect)
            
            # Draw border with rounded corners
            border_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            border_rect = pygame.Rect(0, 0, card_rect.width, card_rect.height)
            pygame.draw.rect(border_surf, (255, 255, 255), border_rect, 4, border_radius=CARD_RADIUS)
            screen.blit(border_surf, card_rect)
            
            # Draw magical symbol (crystal/gem)
            if card_rect.width > 40:
                center_x, center_y = card_rect.center
                gem_size = min(card_rect.width, card_rect.height) // 6
                self.draw_gem(screen, center_x, center_y - 20, gem_size, (255, 255, 255))
                
                # Draw color name
                text = font.render(self.color_name, True, (255, 255, 255))
                text_rect = text.get_rect(center=(center_x, center_y + 40))
                shadow_text = font.render(self.color_name, True, (0, 0, 0))
                screen.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
                screen.blit(text, text_rect)
        else:
            # Show back side with magical pattern
            gradient_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            card_back_color = (60, 40, 120)
            for i in range(card_rect.height):
                ratio = i / card_rect.height
                r = int(card_back_color[0] * (1 - ratio * 0.2))
                g = int(card_back_color[1] * (1 - ratio * 0.2))
                b = int(card_back_color[2] * (1 - ratio * 0.2))
                pygame.draw.line(gradient_surf, (r, g, b), (0, i), (card_rect.width, i))
            
            # Apply rounded corners
            temp_rect = pygame.Rect(0, 0, card_rect.width, card_rect.height)
            final_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            draw_rounded_rect(final_surf, (255, 255, 255), temp_rect, CARD_RADIUS)
            final_surf.blit(gradient_surf, (0, 0), special_flags=pygame.BLEND_MULT)
            screen.blit(final_surf, card_rect)
            
            # Draw border
            border_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            border_rect = pygame.Rect(0, 0, card_rect.width, card_rect.height)
            pygame.draw.rect(border_surf, (150, 120, 200), border_rect, 4, border_radius=CARD_RADIUS)
            screen.blit(border_surf, card_rect)
            
            # Draw magical pattern (moon and stars)
            if card_rect.width > 40:
                center_x, center_y = card_rect.center
                
                # Draw crescent moon
                moon_radius = 15
                pygame.draw.circle(screen, (255, 255, 200), (center_x, center_y - 10), moon_radius)
                pygame.draw.circle(screen, card_back_color, (center_x + 8, center_y - 10), moon_radius - 2)
                
                # Draw stars around
                star_positions = [
                    (center_x - 25, center_y - 25),
                    (center_x + 25, center_y - 25),
                    (center_x - 30, center_y + 15),
                    (center_x + 30, center_y + 15),
                    (center_x, center_y + 30)
                ]
                
                for star_x, star_y in star_positions:
                    self.draw_star(screen, star_x, star_y, 4, (255, 255, 200))
        
        # Draw sparkles
        for sparkle in self.sparkles:
            sparkle.draw(screen)
    
    def draw_gem(self, screen, x, y, size, color):
        """Draw a magical gem/crystal"""
        points = [
            (x, y - size),
            (x + size//2, y - size//2),
            (x + size, y),
            (x + size//2, y + size//2),
            (x, y + size),
            (x - size//2, y + size//2),
            (x - size, y),
            (x - size//2, y - size//2)
        ]
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)
            inner_points = [(px + (x-px)*0.3, py + (y-py)*0.3) for px, py in points]
            pygame.draw.polygon(screen, (255, 255, 255), inner_points)
    
    def draw_star(self, screen, x, y, size, color):
        """Draw a 5-pointed star"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.4
            px = x + radius * math.cos(angle - math.pi / 2)
            py = y + radius * math.sin(angle - math.pi / 2)
            points.append((px, py))
        
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)
    
    def get_rect(self):
        width = int(CARD_WIDTH * self.target_scale)
        height = int(CARD_HEIGHT * self.target_scale)
        return pygame.Rect(
            int(self.x - width // 2 + CARD_WIDTH // 2),
            int(self.y - height // 2 + CARD_HEIGHT // 2),
            width, height
        )
    
    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos) and self.entrance_complete

class EnhancedDisneyWitchGame:
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("🌙 Enhanced Disney Witch's Magical Memory 🧙‍♀️")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 56)
        self.big_font = pygame.font.Font(None, 84)
        
        # Game objects
        self.moon = Moon()
        
        # Multiple Tangled-style castles
        self.castles = [
            TangleCastle(WINDOW_WIDTH - 350, WINDOW_HEIGHT - 220, 1.2),  # Main large castle
            TangleCastle(WINDOW_WIDTH - 600, WINDOW_HEIGHT - 180, 0.8),  # Medium castle
            TangleCastle(50, WINDOW_HEIGHT - 160, 0.6),                  # Small left castle
            TangleCastle(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 140, 0.5),  # Tiny right castle
        ]
        
        self.witch = FlyingWitch()
        
        # Multiple flying fairies
        self.fairies = []
        for _ in range(6):  # 6 fairies flying around
            self.fairies.append(FlyingFairy())
        
        self.cards = []
        self.revealed_cards = []
        self.matched_pairs = 0
        self.total_pairs = (ROWS * COLS) // 2
        self.game_won = False
        self.floating_particles = []
        self.background_sparkles = []
        self.score = 0
        self.moves = 0
        
        # Initialize background sparkles
        for _ in range(100):  # More sparkles for magical atmosphere
            self.background_sparkles.append(MagicalSparkle(
                random.uniform(0, WINDOW_WIDTH),
                random.uniform(0, WINDOW_HEIGHT)
            ))
        
        self.setup_cards()
    
    def setup_cards(self):
        """Create and shuffle cards with faster entrance"""
        colors_needed = (ROWS * COLS) // 2
        selected_colors = WITCH_COLORS[:colors_needed]
        
        card_data = []
        for color_data in selected_colors:
            card_data.extend([color_data] * 2)
        
        random.shuffle(card_data)
        
        # Calculate starting position to center the grid properly
        total_width = COLS * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN
        total_height = ROWS * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN
        
        screen_rect = self.screen.get_rect()
        start_x = (screen_rect.width - total_width) // 2
        start_y = (screen_rect.height - total_height) // 2 + 40
        
        # Create card objects
        self.cards = []
        index = 0
        for row in range(ROWS):
            for col in range(COLS):
                x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                color_data = card_data[index]
                card = Card(x, y, color_data, index)
                self.cards.append(card)
                index += 1
    
    def handle_card_click(self, pos):
        """Handle clicking on a card"""
        if len(self.revealed_cards) >= 2:
            return
        
        for card in self.cards:
            if card.is_clicked(pos) and not card.is_revealed and not card.is_matched:
                card.is_revealed = True
                card.reveal_time = pygame.time.get_ticks()
                self.revealed_cards.append(card)
                
                if len(self.revealed_cards) == 2:
                    self.moves += 1
                break
    
    def update_revealed_cards(self):
        """Update the state of revealed cards - FASTER"""
        current_time = pygame.time.get_ticks()
        
        if len(self.revealed_cards) == 2:
            if all(current_time - card.reveal_time >= REVEAL_TIME for card in self.revealed_cards):
                card1, card2 = self.revealed_cards
                
                if card1.color == card2.color:
                    # Cards match
                    card1.is_matched = True
                    card2.is_matched = True
                    self.matched_pairs += 1
                    self.score += 250  # Higher score
                    
                    # Create more celebration particles
                    for card in [card1, card2]:
                        rect = card.get_rect()
                        for _ in range(30):  # More particles
                            self.floating_particles.append(FloatingParticle(
                                rect.centerx + random.uniform(-50, 50),
                                rect.centery + random.uniform(-50, 50),
                                card.color
                            ))
                    
                    # Check if game is won
                    if self.matched_pairs == self.total_pairs:
                        self.game_won = True
                        # Massive victory particles explosion
                        for _ in range(200):
                            self.floating_particles.append(FloatingParticle(
                                WINDOW_WIDTH // 2 + random.uniform(-400, 400),
                                WINDOW_HEIGHT // 2 + random.uniform(-400, 400),
                                random.choice([color for color, _ in WITCH_COLORS])
                            ))
                else:
                    # Cards don't match
                    card1.is_revealed = False
                    card2.is_revealed = False
                
                self.revealed_cards = []
    
    def update_hover(self, mouse_pos):
        """Update hover effects"""
        for card in self.cards:
            card.hover = card.is_clicked(mouse_pos) and not card.is_matched and not card.is_revealed
    
    def draw_night_sky_background(self):
        """Draw magical night sky with gradient"""
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(NIGHT_SKY_START[0] + (NIGHT_SKY_END[0] - NIGHT_SKY_START[0]) * ratio)
            g = int(NIGHT_SKY_START[1] + (NIGHT_SKY_END[1] - NIGHT_SKY_START[1]) * ratio)
            b = int(NIGHT_SKY_START[2] + (NIGHT_SKY_END[2] - NIGHT_SKY_START[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Draw more twinkling stars
        for i in range(150):  # More stars
            star_x = (i * 137) % WINDOW_WIDTH
            star_y = (i * 211) % (WINDOW_HEIGHT // 2)
            twinkle = abs(math.sin(pygame.time.get_ticks() * 0.005 + i))  # Faster twinkling
            if twinkle > 0.6:  # More frequent twinkling
                size = int(2 + twinkle * 3)
                pygame.draw.circle(self.screen, STAR_COLOR, (star_x, star_y), size)
    
    def update_background_effects(self):
        """Update all background magical effects"""
        # Update moon
        self.moon.update()
        
        # Update all castles
        for castle in self.castles:
            castle.update()
        
        # Update flying witch
        self.witch.update()
        
        # Update all fairies
        for fairy in self.fairies:
            fairy.update()
        
        # Update existing sparkles
        self.background_sparkles = [s for s in self.background_sparkles if s.update()]
        
        # Add new sparkles more frequently
        if len(self.background_sparkles) < 100:
            for _ in range(3):  # Add multiple sparkles at once
                self.background_sparkles.append(MagicalSparkle(
                    random.uniform(0, WINDOW_WIDTH),
                    random.uniform(0, WINDOW_HEIGHT)
                ))
        
        # Update floating particles
        self.floating_particles = [p for p in self.floating_particles if p.update()]
    
    def draw_background_effects(self):
        """Draw all background magical effects"""
        # Draw all castles first (behind everything)
        for castle in self.castles:
            castle.draw(self.screen)
        
        # Draw moon
        self.moon.draw(self.screen)
        
        # Draw background sparkles
        for sparkle in self.background_sparkles:
            sparkle.draw(self.screen)
        
        # Draw all flying fairies
        for fairy in self.fairies:
            fairy.draw(self.screen)
        
        # Draw flying witch
        self.witch.draw(self.screen)
        
        # Draw floating particles
        for particle in self.floating_particles:
            particle.draw(self.screen)
    
    def draw_ui(self):
        """Draw Disney-style user interface"""
        # Title with magical glow effect
        title_text = self.title_font.render("🌙 Enhanced Disney Witch's Magic 🧙‍♀️", True, (255, 215, 0))
        title_shadow = self.title_font.render("🌙 Enhanced Disney Witch's Magic 🧙‍♀️", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        
        # Draw title with glow
        for offset in [(4, 4), (2, 2)]:
            self.screen.blit(title_shadow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        self.screen.blit(title_text, title_rect)
        
        # Stats panel with Disney styling
        stats_y = 100
        stats = [
            f"🔮 Spell Pairs: {self.matched_pairs}/{self.total_pairs}",
            f"⭐ Magic Moves: {self.moves}",
            f"✨ Enchant Score: {self.score}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (255, 255, 255))
            shadow_text = self.font.render(stat, True, (0, 0, 0))
            self.screen.blit(shadow_text, (22, stats_y + i * 30 + 2))
            self.screen.blit(text, (20, stats_y + i * 30))
        
        # Instructions
        if not self.game_won and self.matched_pairs == 0:
            instruction = "🌟 Cast spells by matching magical gem pairs! 🌟"
            text = self.font.render(instruction, True, (255, 255, 255))
            shadow_text = self.font.render(instruction, True, (0, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.screen.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
            self.screen.blit(text, text_rect)
    
    def draw_win_screen(self):
        """Draw Disney-style magical victory screen"""
        if not self.game_won:
            return
        
        # Semi-transparent magical overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 25, 80, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Victory message with Disney sparkle effect
        win_text = self.big_font.render("🎆 MAGICAL MASTERY! 🎆", True, (255, 215, 0))
        win_shadow = self.big_font.render("🎆 MAGICAL MASTERY! 🎆", True, (75, 0, 130))
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        
        # Draw with multiple shadow layers for glow effect
        for offset in [(6, 6), (4, 4), (2, 2)]:
            self.screen.blit(win_shadow, (win_rect.x + offset[0], win_rect.y + offset[1]))
        self.screen.blit(win_text, win_rect)
        
        # Stats with Disney emojis
        final_score = self.font.render(f"🌟 Final Enchantment Score: {self.score}", True, (255, 255, 255))
        moves_text = self.font.render(f"✨ Total Magical Moves: {self.moves}", True, (255, 255, 255))
        
        score_rect = final_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        moves_rect = moves_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        
        # Draw shadows
        final_score_shadow = self.font.render(f"🌟 Final Enchantment Score: {self.score}", True, (0, 0, 0))
        moves_text_shadow = self.font.render(f"✨ Total Magical Moves: {self.moves}", True, (0, 0, 0))
        self.screen.blit(final_score_shadow, (score_rect.x + 2, score_rect.y + 2))
        self.screen.blit(moves_text_shadow, (moves_rect.x + 2, moves_rect.y + 2))
        
        self.screen.blit(final_score, score_rect)
        self.screen.blit(moves_text, moves_rect)
        
        # Restart instruction
        restart_text = self.font.render("🧙‍♀️ Press R to cast again or ESC to return to reality 🧙‍♀️", True, (255, 255, 255))
        restart_shadow = self.font.render("🧙‍♀️ Press R to cast again or ESC to return to reality 🧙‍♀️", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_shadow, (restart_rect.x + 2, restart_rect.y + 2))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the magical adventure"""
        self.cards = []
        self.revealed_cards = []
        self.matched_pairs = 0
        self.game_won = False
        self.floating_particles = []
        self.score = 0
        self.moves = 0
        
        # Reset fairies
        self.fairies = []
        for _ in range(6):
            self.fairies.append(FlyingFairy())
        
        self.setup_cards()
    
    def handle_resize(self):
        """Handle window resize for proper centering"""
        global WINDOW_WIDTH, WINDOW_HEIGHT
        WINDOW_WIDTH, WINDOW_HEIGHT = self.screen.get_size()
        self.setup_cards()
        
        # Update castle and moon positions
        self.castles = [
            TangleCastle(WINDOW_WIDTH - 350, WINDOW_HEIGHT - 220, 1.2),
            TangleCastle(WINDOW_WIDTH - 600, WINDOW_HEIGHT - 180, 0.8),
            TangleCastle(50, WINDOW_HEIGHT - 160, 0.6),
            TangleCastle(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 140, 0.5),
        ]
        self.moon.x = WINDOW_WIDTH - 150
    
    def run(self):
        """Main Disney magical game loop - FASTER"""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_won:
                        self.restart_game()
                    elif event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                        self.handle_resize()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game_won:
                        self.handle_card_click(event.pos)
            
            # Update game state
            self.update_hover(mouse_pos)
            self.update_revealed_cards()
            self.update_background_effects()
            
            # Update cards
            for card in self.cards:
                card.update()
            
            # Draw everything
            self.draw_night_sky_background()
            self.draw_background_effects()
            
            # Draw cards
            for card in self.cards:
                card.draw(self.screen, self.font, self.title_font)
            
            # Draw UI
            self.draw_ui()
            self.draw_win_screen()
            
            pygame.display.flip()
            self.clock.tick(75)  # Faster frame rate
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = EnhancedDisneyWitchGame()
    game.run()
