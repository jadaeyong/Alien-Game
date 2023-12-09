from dataclasses import dataclass
from designer import *
from random import randint
ROCKET_SPEED = 12
ALIEN_SPEED = 5
SHOOT_LASER_SPEED = 7

set_window_color('black')

@dataclass
class World:
    rocket: DesignerObject
    rocket_speed: int
    keys_held_down: bool
    aliens: list[DesignerObject]
    lasers: list[DesignerObject]
    explosions: list[DesignerObject]
    score: int
    score_counter: DesignerObject
    lives: int
    lives_counter: DesignerObject
   
def create_world() -> World:
    """ Create the world
        Returns a World """
    return World(create_rocket(), 0, False, [], [], [], 0,
                 text("white", "Score: 0", 20, 200, 8), 3, text("white", "Lives: 3", 20, 550, 8))

def create_rocket() -> DesignerObject:
    """ Create the rocket
        Returns a DesignerObject representing a rocket """
    rocket = emoji('rocket')
    rocket.y = get_height() * (8/10)
    rocket.flip_x = True
    rocket.x = get_width() * 1/2
    turn_left(rocket, 45)
    return rocket
   
def move_left(world: World):
    """ Make the rocket move left
        Takes in a World as an argument """
    world.rocket_speed = -ROCKET_SPEED
    world.rocket.flip_x = False

def move_right(world: World):
    """ Make the rocket move right
        Takes in a World as an argument """
    world.rocket_speed = ROCKET_SPEED
    world.rocket.flip_x = True    

def move_rocket(world: World):
    """ Move copter horizontally
        Takes in a World as an argument """
    world.rocket.x += world.rocket_speed
   
def stop_moving_rocket(world: World):
    """ Stop moving the rocket
        Takes in a World as an argument """
    world.rocket.x = world.rocket.x
    world.rocket_speed = 0

def keys_pressed(world: World, key: str):
    """ Rocket will move if keys are pressed
        Takes in a World and a string representing a key as arguments """
    if key == 'left':
        move_left(world)
        world.keys_held_down == True
    if key == 'right':
        move_right(world)
        world.keys_held_down == True

def keys_released(world: World):
    """ Rocket will not move if keys are not pressed
        Takes in a World as an argument """
    stop_moving_rocket(world)
    world.keys_held_down == False
       
def rocket_off_screen(world: World):
    """ If the rocket is moved off-screen, it will wrap around to the other side of the screen
        Takes in a World as an argument """
    if world.rocket.x > get_width():
        world.rocket.x = 0
    elif world.rocket.x < 0:
        world.rocket.x = get_width()
       
def create_alien()-> DesignerObject:
    """ Make a single alien
        Takes in a World as an argument
        Returns a DesignerObject representing an alien """
    alien = emoji('👾')
    alien.y = get_height() - 300
    alien.x = get_width() - 700
    return alien

def move_aliens(world: World):
    """ The aliens move
       Takes in a World as an argument """
    for alien in world.aliens:
        alien.y += ALIEN_SPEED
       
def create_alien()-> DesignerObject:
    """ Make a single alien
        Takes in a World as an argument
        Returns a DesignerObject representing an alien """
    alien = emoji('👾')
    return alien

def aliens_exist(world:World):
    """ Make aliens appear as a group
        Takes in a World as an argument """
    NOT_TOO_MANY_ALIENS = len(world.aliens) < 9
    if NOT_TOO_MANY_ALIENS and len(world.aliens) == 0:
        #alien1
        alien1 = create_alien()
        alien1.x = 100
        alien1.y = 0
        world.aliens.append(alien1)
        #alien2
        alien2 = create_alien()
        alien2.x = 175
        alien2.y = 50
        world.aliens.append(alien2)
        #alien3
        alien3 = create_alien()
        alien3.x = 250
        alien3.y = 0
        world.aliens.append(alien3)
        #alien4
        alien4 = create_alien()
        alien4.x = 325
        alien4.y = -50
        world.aliens.append(alien4)
        #alien5
        alien5 = create_alien()
        alien5.y = -100
        world.aliens.append(alien5)
        #alien6
        alien6 = create_alien()
        alien6.x = 475
        alien6.y = -50
        world.aliens.append(alien6)
        #alien7
        alien7 = create_alien()
        alien7.x = 550
        alien7.y = 0
        world.aliens.append(alien7)
        #alien8
        alien8 = create_alien()
        alien8.x = 625
        alien8.y = 50
        world.aliens.append(alien8)
        #alien9
        alien9 = create_alien()
        alien9.x = 700
        alien9.y = 0
        world.aliens.append(alien9)
       
def move_aliens(world: World):
    """ Aliens move downard
        Takes in a world as an argument """
    for alien in world.aliens:
        alien.y += ALIEN_SPEED
       
def aliens_wrap(world: World):
    """ If an alien goes off-screen it will wrap to the top of the screen
        Takes in a World as an argument """
    for alien in world.aliens:
        if alien.y > get_height():
            alien.y = alien.y-alien.y

def create_laser_beam() -> DesignerObject:
    """ Create a laser beam
        Returns a DesignerObject """
    laser = ellipse("aqua", 10, 30)
    return laser

def shoot_lasers(world: World, key: str):
    """ Create a laser beam when the space bar is pressed
        Takes in a World and a string representing a key as arguments """
    if key == 'space':
        new_laser = create_laser_beam()
        new_laser.y = world.rocket.y
        new_laser.x = world.rocket.x
        world.lasers.append(new_laser)

def move_above(bottom: DesignerObject, top: DesignerObject):
    """ Move bottom object to be above the top object
        Takes in two DesignerObjects as arguments """
    bottom.y = bottom.y - top.height/2
    bottom.x = bottom.x

def make_laser_shoot(world: World):
    """ A laser shoots when prompted
        Takes in a world as an argument """
    for laser in world.lasers:
        move_above(laser, world.rocket)
        laser.y += SHOOT_LASER_SPEED

def destroy_lasers_when_shooting(world: World):
    """ When a laser goes off-screen it is destroyed
        Takes in a world as an argument """
    kept = []
    for laser in world.lasers:
        if laser.y < get_height():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept

def create_rocket_explosion(world: World)-> DesignerObject:
    """ Creates in an explosion at the same position as the rocket
        Takes in a World as an argument """
    explosion = emoji('💥')
    explosion.y = world.rocket.y
    explosion.x = world.rocket.x
    world.explosions.append(explosion)
    return explosion

def collide_alien_rocket(world: World):
    """ If an alien collides with the rocket, an explosion appears, the rocket resets to middle; One life is lost
        Takes in a world as an argument """
    destroyed_aliens = []
    for alien in world.aliens:
        if colliding(alien, world.rocket):
            world.lives = world.lives - 1
            explosion = create_rocket_explosion(world)
            destroyed_aliens.append(alien)
            world.rocket.x = get_width() * 1/2
    world.aliens = filter_from(world.aliens, destroyed_aliens)

def make_explosions_disappear(world: World):
    """ The explosion shrinks and disappears after the rocket collides with an alien
        Takes in a World as an argument """
    index = 0
    for explosion in world.explosions:
        explosion.scale_x -= 0.01
        explosion.scale_y -= 0.01
        if explosion.scale_x < 0.0:
            world.explosions.remove(explosion)

def collide_alien_laser(world: World):
    """ When aliens collide with a laser, both the laser and the alien disappear and the score increases by 1
        Takes in a World as an argument """
    destroyed_aliens = []
    destroyed_lasers = []
    for alien in world.aliens:
        for laser in world.lasers:
            if colliding(alien, laser):
               destroyed_aliens.append(alien)
               destroyed_lasers.append(laser)
               world.score += 1
    world.aliens = filter_from(world.aliens, destroyed_aliens)
    world.lasers = filter_from(world.lasers, destroyed_lasers)
       
def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    new_values = []
    for item in old_list:
        if item not in elements_to_not_keep:
            new_values.append(item)
        else:
            destroy(item)
    return new_values

def update_score(world: World):
    """ Updates a player's score
        Takes in a World as an argument """
    world.score_counter.text = "Score: " + str(world.score)
   
def update_lives(world: World):
    """" Updates the lives a player has
         Takes in a World as an argument """
    world.lives_counter.text = "Lives: " + str(world.lives)
   
def no_lives_left(world:World) -> bool:
    """ Checks if the player has any lives left
        Takes in a World as an argument
        Returns a boolean """
    if world.lives == 0:
        return True
    else:
        return False
   
def show_stats(world:World):
    """ Displays the stats onscreen at the end of the game
        Takes in a World as an argument """
    stats = text("white", "Score: " + str(world.score), 30)
    return stats
   

def flash_game_over(world: World):
    """ When the player has run out of lives, the game stops and a game over screen is shown
        Takes in a world as an argument """
    game_over_message = text("white", "GAME OVER!", 50)
    hide(world.score_counter)
    hide(world.lives_counter)
    stats = show_stats(world)
    change_y(stats, 40)

when("starting", create_world)
when("updating", move_rocket)
when("typing", keys_pressed)
when("done typing", keys_released)
when("updating", rocket_off_screen)
when("updating", aliens_exist)
when("updating", move_aliens)
when("updating", aliens_wrap)
when("typing", shoot_lasers)
when("updating", make_laser_shoot)
when("updating", destroy_lasers_when_shooting)
when("updating", collide_alien_rocket)
when("updating", collide_alien_laser)
when("updating", make_explosions_disappear)
when("updating", update_score)
when("updating", update_lives)
when(no_lives_left, flash_game_over, pause)
start()