import pygame
from LocationModule import *
from Constants import *


class Drawer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.drawdelta_x = 0
        self.drawdelta_y = 0
        
        self.set_location()      

    def set_location(self):
        self.location = self.game.get_location()
        self.main_surface = pygame.Surface(self.location.get_pixel_size())

    def deltax(self, dx):
        self.drawdelta_x += dx

    def deltay(self, dy):
        self.drawdelta_y += dy

    def get_dd_x(self):
        return self.drawdelta_x

    def get_dd_y(self):
        return self.drawdelta_y

    def draw(self, objects):
        self.main_surface.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))
        self.main_surface.blit(self.location.draw(), (0, 0))
        for obj in objects:
            draw_surface = obj.draw()
            if draw_surface:
                self.main_surface.blit(draw_surface, (obj.left, obj.top))
        self.screen.blit(self.main_surface, (-self.drawdelta_x, -self.drawdelta_y))
        GUI_Interface = self.game.get_main_gui().draw()
        self.screen.blit(GUI_Interface, (0, 0))
        pygame.display.flip()

    def update_drawdeltas(self):
        player = self.game.get_main_player()
        
        if player.top - self.get_dd_y() < TOP_DRAW_SIDE:
            self.deltay(player.top - self.get_dd_y() - TOP_DRAW_SIDE)
        if player.bottom - self.get_dd_y() > BOTTOM_DRAW_SIDE:
            self.deltay(player.bottom - self.get_dd_y() - BOTTOM_DRAW_SIDE)
        if player.left - self.get_dd_x() < LEFT_DRAW_SIDE:
            self.deltax(player.left - self.get_dd_x() - LEFT_DRAW_SIDE)
        if player.right - self.get_dd_x() > RIGHT_DRAW_SIDE:
            self.deltax(player.right - self.get_dd_x() - RIGHT_DRAW_SIDE)

class EventHandler:
    def __init__(self, game):
        self.game = game

    def process_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.handle_events(events)
        self.handle_keys(keys)

    def handle_events(self, events):
        for event in events:
            if event.type is pygame.QUIT:
                self.game.close()

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.game.main_player.deltax(-1)
        if keys[pygame.K_RIGHT]:
            self.game.main_player.deltax(1)
        if keys[pygame.K_UP]:
            self.game.main_player.deltay(-1)
        if keys[pygame.K_DOWN]:
            self.game.main_player.deltay(1)


class GUI:
    def __init__(self, game):
        self.game = game

    def get_player_attributes(self):
        player = self.game.get_main_player()
        return (player.get_health(), player.get_mana()), (player.get_max_health(), player.get_max_mana())
    
    def draw(self):
        screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        attrs = self.get_player_attributes()

        indicators = pygame.Surface((SCREEN_SIZE[0] // 10,
                                           SCREEN_SIZE[1] // 20), pygame.SRCALPHA)
        
        size = indicators.get_size()
        
        pygame.draw.rect(indicators, (255, 0, 0),
                         [0, 0, size[0] * attrs[0][0] // attrs[1][0],
                         size[1] // 3])

        pygame.draw.rect(indicators, (0, 0, 255),
                         [0, size[1] // 3 * 2, size[0] * attrs[0][1] // attrs[1][1],
                         size[1] // 3])

        screen.blit(indicators, (30, 30))
        return screen
        