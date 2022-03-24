#Spiel

from random import *
import pygame
import sys
import copy
from Grundlegendes import *
from Spieler import *
from Gegner import *


pygame.init()
vec = pygame.math.Vector2

from pygame import mixer
mixer.init()
mixer.music.set_volume(0.4)
mixer.music.load("zusatz/Musik/untouchablepeter.mp3")
mixer.music.play()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = Karte_WIDTH//COLS
        self.cell_height = Karte_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            #elif self.state == 'win':
            #    self.game_over_events()
            #    self.game_over_update()
            #    self.alles_eingesammelt()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ Hilfsfunktionen ##################################
    #Für Texte grundsätzlich:
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('zusatz/Karte.png')
        self.background = pygame.transform.scale(self.background, (Karte_WIDTH, Karte_HEIGHT))

        # walls.txt für Wände öffnen
        # walls-Liste erstellen
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":                             #Wände
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":                           #Sammelobjekte/Coins
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":                           #Spieler
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:          #Gegner in walls.txt
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"


########################### Introfunktionen / Startmenu ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    #800 x 600

    def start_draw(self):
        #self.screen.fill(BLACK) #Hintergrund Startmenü
        self.screen.fill(HINTERGRUND)
        pygame.display.set_caption('PACMAINIAC')    #Titel des Fensters
        #self.draw_text(Wörter, screen, Position, Schriftgroeße, Farbe, Schriftart, Zentriert ?)
        self.draw_text('Leertaste drücken', self.screen, [WIDTH//2, HEIGHT//2-50], 
                        60, (170, 132, 58), Schrift, centered=True)
        self.draw_text('1 Spieler', self.screen, [WIDTH//2, HEIGHT//2+50], 
                        Schriftgroeße, (44, 167, 198), Schrift, centered=True)
        self.draw_text('HIGHSCORE', self.screen, [4, 0],
                        Schriftgroeße, (255, 255, 255), Schrift)
        self.draw_text('Steuerung per Pfeiltasten', self.screen, [300, 150], 
                        Schriftgroeße, (255, 255, 255), Schrift, centered=True)
        self.draw_text('Ein Projekt von Magnus, Benny, Pierre, Alex und Felix', self.screen, [300, 600], 
                        25, (0,0,0), Schrift, centered=True)
        #pacman(100, 200)            #FEHLER !!              Idee: Icon im Startmenu einfügen
        pygame.display.update()

########################### Spielfunktionen ##################################

    def playing_events(self):   #Steuerung
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  #Nach Links
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT: #Nach Rechts
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:    #Nach Oben
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:  #Nach Unten
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):         #Spielscreen oben (Mit aktuellem Score etc.)
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text('Gesammelt: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 18, WHITE, Schrift)                             #Schriftart wechseln
        self.draw_text('HIGHSCORE: 0', self.screen, [WIDTH//2+60, 0], 18, WHITE, Schrift)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255, 0, 255),  #Farbe der Coins        (Ursprünglich: (124, 123, 7) )        xxx
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,        #Größe der Coins
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
            
        

####################### Game over ###################################################################################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    #Wenn Spiel vorbei, kann man mit Space wieder spielen
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   #Wenn Spiel vorbei, mit ESC raus
                self.running = False
            #if event.key == pygame.K_ESCAPE:   #Wenn Spiel vorbei, mit ESC raus
            #    self.running = False

    def game_over_update(self):
        pass
    
    def game_over_draw(self):   #Endmenu
        self.screen.fill(BLACK)
        #losing_text als variable
        #losing_text = random.randint("SCHLECHT!", "BITTER!", "NOOB!", "ANFÄNGER", "RAGEQUIT?")
        quit_text = "Drücke ESC um zu verlassen"
        again_text = "Nochmal? Leertaste!"
        #self.draw_text(losing_text, self.screen, [WIDTH//2, 100],  100, LILA, "zusatz/Oswald-Medium.ttf", centered=True)
        self.draw_text("Verloren!", self.screen, [WIDTH//2, 100],  100, LILA, "zusatz/Oswald-Medium.ttf", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "zusatz/Oswald-Medium.ttf", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "zusatz/Oswald-Medium.ttf", centered=True)
        pygame.display.update()

    def alles_eingesammelt(self):
        if self.current_score == 300:
            self.screen.fill(255,255,255)
            win_text = "Gewonnen"
            win2_text = "Du hast Alles eingesammelt, wow!"
            win3_text = "Nochmal ?"
            self.draw_text(win_text, self.screen [WIDTH//2, HEIGHT//2], 36, (BLACK), "zusatz/Oswald-Medium.ttf", centered=True)
            self.draw_text(win2_text, self.screen [WIDTH//2, HEIGHT//1.6], 25, (BLACK), "zusatz/Oswald-Medium.ttf", centered=True)
            self.draw_text(win3_text, self.screen [WIDTH//2, HEIGHT//1.3], 15, (BLACK), "zusatz/Oswald-Medium.ttf", centered=True)

