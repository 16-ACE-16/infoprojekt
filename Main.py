#Main

from Spiel import *

if __name__ == '__main__':
    app = App()
    app.run()


#-------------------------------------------------- Sound + Icon ----------------------------------------------------
#Importierung aller nötigen Pakete
import pygame, os, sys, random

def path(path): # PyInstaller
    base_path = getattr(sys,"_MEIPASS",os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,path)

#Pygame wird initalisiert
pygame.init()

#Icon für das Spiel
icon = pygame.image.load(path("zusatz/icon.png"))

#---------------------------------- Audio ----------------------------------------------------------------------------
#Überprüfung, ob Sound möglich ist
#try:
#    sound, muted, VOLUME = True, False, 0.3
#    pygame.mixer.init()
#    pygame.mixer.music.set_volume(VOLUME)
#    #Soundeffekte
#    soundeffekte_liste = [] #In die Klammeer mit " " ("Beispiel1", "Beispiel2"), also Auflistung der Soundeffekte
#    soundeffekt = [pygame.mixer.Sound(path(f"zusatz/soundeffekte/{sound}.mp3")) for sound in soundeffekte_liste]
#except: sound = False

#def play_audio(audio=None):
#    if sound:
#       if not audio:
#          #musik = f"zusatz/Musik/{random.randint()}.mp3" #random.randint(1, wie viele Lieder).mp3 - Wählt zufällig eins aus
#          musik = f"zusatz/Musik/untouchablepeter.mp3"
#          pygame.mixer.music.load(path(musik))
#          pygame.mixer.music.play(-1)
#       else: soundeffekt[soundeffekte_liste.index(audio)].play()
#-------------------------------------------------
