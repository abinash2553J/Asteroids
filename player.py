import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS, 
    LINE_WIDTH, 
    PLAYER_TURN_SPEED, 
    PLAYER_SPEED, 
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS
)

class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class constructor (CircleShape)
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize the rotation attribute to 0
        self.rotation = 0
        # Initialize the shot cooldown timer starting at 0
        self.shoot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Override the draw method to render the player as a triangle polygon
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        # If the timer is greater than 0, prevent shooting
        if self.shoot_timer > 0:
            return
            
        # Reset the cooldown timer
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        # Create a new Shot at the player's current position
        shot = Shot(self.position.x, self.position.y)
        # Set the shot's velocity using a base vector of (0, 1)
        # Rotate it in the direction the player is facing and scale by shoot speed
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        # Decrease the shoot timer by dt every frame before handling spacebar input
        self.shoot_timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        
        # Handle spacebar input to fire shots
        if keys[pygame.K_SPACE]:
            self.shoot()
