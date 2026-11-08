import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event  # Make sure this matches your project's logging import

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    # Add the split method exactly inside the Asteroid class block
    def split(self):
        # 1. Immediately kill itself
        self.kill()

        # 2. Check if it's a small asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # 3. Spawn 2 new asteroids
        log_event("asteroid_split")
        
        # Generate random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)

        # Create two new velocities by rotating the current velocity vector
        vector_1 = self.velocity.rotate(random_angle)
        vector_2 = self.velocity.rotate(-random_angle)

        # Compute the new smaller radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Instantiate the two smaller asteroids at the current coordinates
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Make the smaller asteroids fly off 1.2x faster
        asteroid_1.velocity = vector_1 * 1.2
        asteroid_2.velocity = vector_2 * 1.2
