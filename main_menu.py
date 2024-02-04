import pygame
import pygame.gfxdraw as gfxdraw
import time
import itertools as ito
import cv2


class TestSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color = None, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if color != None:
            self.color = color
            self.image.fill(color)

class TestGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

def percent(x, y = 0):
    return x * (y / 100)
class Game:
    WIDTH = 1250
    HEIGHT = 700
    FPS = 120
    gameSurfaceVideo = cv2.VideoCapture('main_menu_background.mp4')
    titleMenuGif = cv2.VideoCapture('title_menu.gif')
    mainGameBackgroundGif = cv2.VideoCapture('main_game_background.gif')
    __singleton = False
    @staticmethod
    def percentX(x):
        return Game.WIDTH * (x/100)
    @staticmethod
    def percentY(y):
        return Game.HEIGHT * (y/100)
    def __init__(self):
        if Game.__singleton:
            raise Exception("`Game` class must be initiated just once.")
        super().__init__()
        Game.__singleton = True
    def __init(self):
        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.tick = 0
        self.gameSurfaceWidth = Game.percentX(100)
        self.gameSurfaceHeight = Game.percentY(100)
        self.sideBar = pygame.transform.scale(pygame.image.load('beside_options_copy.png'),(Game.percentX(28.5), Game.HEIGHT))
        self.sideBar_rect = self.sideBar.get_rect()
        self.inMenu = True
        self.inGame = False
        # self.game_surface = pygame.Surface((self.gameSurfaceWidth, self.gameSurfaceHeight)).convert_alpha()
        self.titleMenu = pygame.transform.scale(pygame.image.load('title_menu_copy.png'),(Game.percentX(32.5), percent(self.sideBar_rect.height, 34)))
        self.titleMenu_rect = self.titleMenu.get_rect()
        self.titleMenuPaddingX = Game.percentX(9.5)
        self.titleMenuPaddingY = Game.percentY(5.5)
        self.menuOptions = pygame.Surface((Game.percentX(30),Game.percentY(40))).convert_alpha()
        self.menuOptions_rect = self.menuOptions.get_rect()
        self.menuOptionMaxWidth = percent(self.menuOptions_rect.width, 80)
        menuOptionsTrail = pygame.image.load('option_trail_copy.png').convert_alpha()
        self.menuOptionsTrail_widthPercent = 35
        self.menuOptionsTrail_borderBoxWidth = percent(self.menuOptionMaxWidth, self.menuOptionsTrail_widthPercent)
        self.menuOptionsTrail = pygame.transform.scale(menuOptionsTrail, (percent(self.menuOptionMaxWidth, self.menuOptionsTrail_widthPercent + 10), percent(self.menuOptions_rect.height, 16.5)))
        self.menuOptionsTrail_rect = self.menuOptionsTrail.get_rect()
        settingsOptionImage = pygame.image.load('settings_option_copy.png').convert_alpha()
        howToPlayImage = pygame.image.load('how_to_play_option_copy.png').convert_alpha()
        exitGameOption = pygame.image.load('exit_game_option_copy.png').convert_alpha()
        optionSize = (percent(self.menuOptionMaxWidth, 75), percent(self.menuOptions_rect.height, 21.25))
        self.settingsOptionImage = pygame.transform.scale(settingsOptionImage, optionSize)
        self.settings_rect = self.settingsOptionImage.get_rect()
        self.howToPlayImage = pygame.transform.scale(howToPlayImage, optionSize)
        self.howToPlay_rect = self.howToPlayImage.get_rect()
        self.exitGameOption = pygame.transform.scale(exitGameOption, optionSize)
        self.exit_rect = self.exitGameOption.get_rect()
        self.trailOptionGapX = percent(self.menuOptions_rect.width, 0)
        self.trailOptionGapY = percent(self.menuOptions_rect.height, 2)
        print(self.menuOptionsTrail_rect)
        # self.game_surface.fill((0,0,0,16))
        # self.game_surface_rect = self.game_surface.get_rect()
    def __enter__(self):
        pygame.init()
        self.__init()
        return self
    def __terminate(self):
        pygame.quit()
    def __exit__(self, exc_type, exc_value, traceback):
        self.__terminate()

    def windowEventHandler(self, keys):
        for key in keys:
            if key.type == pygame.QUIT:
                self.running = False
    def menuEventHandler(self):
        keys = pygame.event.get()
        self.windowEventHandler(keys)
        for key in keys:
            match key.type:
                case pygame.KEYDOWN:
                    if key.dict.get('unicode') == 'y':
                        self.inGame = True
                        self.inMenu = False
    def menuRender(self):
        self.menuEventHandler()
        success , video_image = Game.gameSurfaceVideo.read()
        if not success:
            Game.gameSurfaceVideo.set(cv2.CAP_PROP_POS_MSEC, 0)
            success , video_image = Game.gameSurfaceVideo.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH,Game.HEIGHT + Game.percentY(1)))
        self.game_surface.blit(self.sideBar, (0, 0))
        
        # success , gif_image = Game.titleMenuGif.read()
        # if not success:
        #     Game.titleMenuGif.set(cv2.CAP_PROP_POS_MSEC, 0)
        #     success , gif_image = Game.titleMenuGif.read()
        # titleMenu = pygame.transform.scale(pygame.image.frombuffer(gif_image.tobytes(), gif_image.shape[1::-1], "BGR"), (Game.percentX(30), percent(self.sideBar_rect.height, 30)))
        self.screen.blit(self.game_surface, ((Game.WIDTH / 2) - (self.gameSurfaceWidth / 2) + (self.sideBar_rect.width / 1.5) ,0))
        self.surface.blit(self.titleMenu, ((self.sideBar_rect.width / 4) - (self.sideBar_rect.width / 3) + self.titleMenuPaddingX, percent(self.sideBar_rect.height, 8)+ self.titleMenuPaddingY))
        self.surface.blit(self.menuOptions, (0, self.titleMenu_rect.height * 1.66))

        self.menuOptions.blit(self.menuOptionsTrail,(0,0 + percent(self.menuOptions_rect.height, 2.375)))
        self.menuOptions.blit(self.settingsOptionImage,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,0))
        self.menuOptions.blit(self.menuOptionsTrail,(0,self.settings_rect.y + self.settings_rect.height + self.trailOptionGapY + percent(self.menuOptions_rect.height, 2.375)))
        self.menuOptions.blit(self.howToPlayImage,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.trailOptionGapY))
        self.menuOptions.blit(self.menuOptionsTrail,(0,self.settings_rect.y + self.settings_rect.height + self.howToPlay_rect.height + self.trailOptionGapY + (percent(self.menuOptions_rect.height, 2.375) * 2)))
        self.menuOptions.blit(self.exitGameOption,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.howToPlay_rect.height + self.trailOptionGapY + percent(self.menuOptions_rect.height, 2.375)))
    def endRender(self):
        pygame.display.flip()
        self.tick = self.clock.tick(Game.FPS) / 1000
    def gameEventHandler(self):
        keys = pygame.event.get()
        self.windowEventHandler(keys)
        for key in keys:
            match key.type:
                case pygame.KEYDOWN:
                    pass
    def gameRender(self):
        self.gameEventHandler()
        success, video_image = Game.mainGameBackgroundGif.read()
        if not success:
            Game.mainGameBackgroundGif.set(cv2.CAP_PROP_POS_MSEC, 0)
            success, video_image = Game.mainGameBackgroundGif.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH, Game.HEIGHT))
        self.surface.blit(self.game_surface, (0,0))
    def start(self):
        return self.run()
    def run(self):
        while self.running:
            if self.inMenu:
                while self.running and self.inMenu:
                    # self.windowEventHandler()
                    self.menuRender()
                    self.endRender()
            elif self.inGame:
                self.endRender()
                while self.running and self.inGame:
                    self.gameRender()
                    self.endRender()
    @staticmethod
    def _static_run():
        with Game() as game:
            game.start()

if __name__ == '__main__':
    Game._static_run()