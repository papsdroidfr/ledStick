# classe animation d'un rubans de leds RGB Neopixels
#   Auteur: https://www.papsdroid.fr
#   date: juin 2020
#   version 1.0
#------------------------------------------------------------------------

from ws2812 import NeoPixel
from time import sleep
from random import randrange, randint


class RubanLeds():
    """ Classe d'animation du ruban de leds Neopixels RGB
        /!\ A partir de 9 leds il faut alimenter le ruban en 5v avec une alimentation externe
        dépendance: bibliothèque ws2812.py nécessaire
        usage: leds = RubanLeds(nb_leds, intensity)
            * nb_leds: nombre de leds sur le ruban (8 par défaut). 
            * intensity = intensité des leds 0 à 1 (1 par défaut)
    """
    def __init__(self, nb_leds=8, intensity=1):
        """constructeur de la classe
            nb_leds: nombre de leds du ruban (8 par défaut)
            intensity 0 à 1 (1 par défaut)
        """
        self.pixels = NeoPixel(spi_bus=1, led_count=nb_leds, intensity=intensity )
        self.nb_leds = nb_leds     # nb de leds du rubans
        self.wait_shortms = 0.001  # délais d'attente ultra-court (en secondes)
        self.wait_short = 0.01     # délais d'attente (secondes) courts
        self.wait_long = 0.03      # délais d'attente (secondes) plus long
        self.rgbMIN = 10           # min pour les couleurs au hasard
        self.rgbMAXpastel = 127    # max pour les couleurs au hasard pastel
        self.rgbMAXhigh = 255      # max pour les couleurs au hasard vives

    # méthodes utilisées pour contrôler les animations
    #-------------------------------------------------
        
    def fade_in_out(self, fadein=True):
        """ retourne tuple (start, end, step) pour parcourir les leds du ruban dans un ordre:
              fadein = True : de la 1ère led à la dernière (valeur par défaut)
              fadein = False: de la dernière led à la première
        """
        start, end, step = 0 , self.nb_leds, 1
        if not fadein:
            start, end, step = self.nb_leds-1, -1 , -1
        return (start, end, step)
    
    def wheel(self, pos):
        """ pos = 0 to 255 correspond à une couleur arc en ciel
            transition r - g - b - back to r.
            retourne un tuple (r,g,b)
        """
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)

    def shuffle(self, l):
        """Fisher–Yates shuffle Algorithm : la methode random.shuffle(l) n'existant pas en micropython
            input: l = liste
            retourne la liste l mélangée
        """
        for i in range(len(l)-1, 0, -1): # parcours la liste à l'envers
            j = randint(0, i)            # random index entier dans l'intervalle [0, i]  
            l[i], l[j] = l[j], l[i]      # Swap l[i] avec l[j]
        return l

    # méthodes d'extinction du ruban
    #----------------------------------
    def off(self):
        """ éteint toutes les leds d'un coup """
        self.pixels.fill((0,0,0))
        self.pixels.write()

    def fade_off(self, fadein = True):
        """ éteint toutes les leds une après les autres
             fadein = True pour simuler un fade in en partant de la 1ère led
             fadein = False pour un fade out en partant de la dernière led
        """
        start, end, step = self.fade_in_out(fadein)
        for l in range(start, end, step):
            self.pixels[l] = (0,0,0)
            self.pixels.write()
            sleep(self.wait_short)      

    # méthodes de rendus de couleur d'une led
    #-----------------------------------------
    def pcolor_random(self, pastel=True, red=True, green=True, blue=True):
        """ retourne une couleur (r,g,b) au hasard
            pastel: rendu de couleur pastel(True) ou vives(False)
            red=False: couleur sans rouge
            green=False: couelmur sans vert
            blue=False: couleur sans bleu
        """
        rgbMAX = pastel * self.rgbMAXpastel + (not pastel) * self.rgbMAXhigh
        r,g,b = 0,0,0
        #on évite la combinaison (0,0,0) qui éteint la led ...
        while (r+g+b) <= self.rgbMIN :
            r,g,b = red*randrange(0,rgbMAX), green*randrange(0,rgbMAX), blue*randrange(0,rgbMAX)
        return (r,g,b)
            
    
    def pcolor_wheel(self, id_led):
        """ retourne une couleur (r,g,b) arc-en-ciel selon la position de la led """
        pixel_index = (id_led * 256 // self.nb_leds)
        return  self.wheel(pixel_index & 255) 
                

    # méthodes d'animation du ruban de leds
    #-----------------------------------------------------------------------------------------
    def rainbow_cycle(self):
        """ cycle de couleurs arc-en ciel """
        for j in range(255):
            for i in range(self.nb_leds):
                pixel_index = (i * 256 // self.nb_leds) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.write()
            sleep(self.wait_shortms)

    def random_cycle(self, pastel=True, red=True, green=True, blue=True):
        """ cycle de couleurs aléatoires
                pastel: True/False pour des couleurs pastel ou vives
                red, green, blue = True/False pour activer/désactiver des composantes Rouge, Verte, Bleue
        """
        for l in range(self.nb_leds):
            self.pixels[l] = self.pcolor_random(pastel=pastel, red=red, green=green, blue=blue)
            self.pixels.write()
        sleep(self.wait_long)

    def fade_wheel(self, fadein=True):
        """ anime le ruban de leds avec des couleurs arc-enciel
            fadein = True: fade in depuis la 1ère leds jusqu'à la dernière
            fadein = False: fade out depuis la dernière led jusqu'à la 1ère
        """
        start, end, step = self.fade_in_out(fadein)
        for l in range(start, end, step):
            self.pixels[l] = self.pcolor_wheel(l)
            sleep(self.wait_long)
            self.pixels.write()
        
    def fade_random(self, fadein = True, pastel=True, red=True, green=True, blue=True):
        """ anime le ruban de leds avec un fade-in de couleurs aléatoires
            params: fadein = True pour un Fade-in False Fade-out
            pastel: True/False pour avoir des couleurs pastels ou vives
            red,green,blue : True/False pour activer/désactiver une composante rouge, verte, bleu
        """
        start, end, step = self.fade_in_out(fadein)
        for l in range(start, end, step):
            self.pixels[l] = self.pcolor_random(red=red, green=green, blue=blue)
            sleep(self.wait_long)
            self.pixels.write()
        
    def shuffle_wheel(self):
        """ anime le ruban en allumant les leds au hasard avec couleur arc-en-ciel """
        leds = self.shuffle([i for i in range(self.nb_leds)])
        for l in leds:
            pixel_index = (l * 256 // self.nb_leds)
            self.pixels[l] = self.wheel(pixel_index & 255)
            sleep(self.wait_short)
            self.pixels.write()
    
    def shuffle_random(self, pastel=True, red=True, green=True, blue=True):
        """ anime le ruban en allumant les leds au hasard avec couleur aléatoire """
        leds = self.shuffle([i for i in range(self.nb_leds)])
        for l in leds:
            self.pixels[l] = self.pcolor_random(red=red, green=green, blue=blue)
            sleep(self.wait_short)
            self.pixels.write()

    def mono_wheel(self, fadein = True, delay=0.1):
        """ anime le ruban en allumant toutes les leds de la même couleur
            changmeent de couleur après chaque delay (en secondes)
            en suivant le rythme de couleur arc-en-ciel
            fadin:  True démarre l'animation avec un fade  in de puis la 1er led
                    False: ... depuis la dernière led
        """
        #1ère mise en couleur avec fadein
        start, end, step = self.fade_in_out(fadein)
        for l in range(start, end, step):
            self.pixels[l] = self.pcolor_wheel(0)
            sleep(self.wait_long)
            self.pixels.write()
        #enchainer les couleurs arc-en-ciel pour toutes le leds
        for j in range(255):
            for i in range(self.nb_leds):
                self.pixels[i] = self.wheel(j)
            self.pixels.write()
            sleep(delay)
        
    def mono_color(self, fadein = True, color = (2555,0,0),  delay=0.1):
        """ anime le ruban en allumant tous les leds de la même couleur 'color'
            fadin:  True démarre l'animation avec un fade  in de puis la 1er led
                    False: ... depuis la dernière led
            delay: delay d'attente 
        """
        #mise en couleur avec fadein
        start, end, step = self.fade_in_out(fadein)
        for l in range(start, end, step):
            self.pixels[l] = color
            sleep(self.wait_long)
            self.pixels.write()
        sleep(delay)
