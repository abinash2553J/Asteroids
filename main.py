import sys
import pygame
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # 2. Initialize pygame
    pygame.init()
    
    # Create a new clock object and initialize dt to 0.0
    clock = pygame.time.Clock()
    dt = 0.0
    
    # 3. Define screen dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create the updatable, drawable, asteroids, and shots groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Assign the groups to class containers attributes
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    # Instantiate the Player object in the middle of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    # Instantiate the Asteroid Field
    asteroid_field = AsteroidField()
    
    # 4. Create the game loop
    while True:
        # 4.1. Call log_state
        log_state()
        
        # 4.2 & 7. Process the pygame event queue and handle window exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        # Call the .update() method on the updatable group
        updatable.update(dt)
        
        # 4. Collision check step (right after update, before drawing)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
                
            # Check collisions between this asteroid and all active shots
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    # Step 9: Replaced asteroid.kill() with asteroid.split()
                    asteroid.split()
                    shot.kill()
                    break # Stop checking other shots for this asteroid since it's split
                    
        # 4.3. Fill the screen with black
        screen.fill("black")
        
        # Loop over all drawables and .draw() them individually
        for obj in drawable:
            obj.draw(screen)
            
        # 4.4. Refresh the screen
        pygame.display.flip()
        
        # Restrict to 60 FPS and compute delta time
        dt = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()
