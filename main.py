# main.py -- put your code here!

from rubanLeds import RubanLeds
from time import sleep

print('Démarrage LedStick.')
leds = RubanLeds(nb_leds=30, intensity=0.4)    

def anim_cool_clignotante(nb_repet=1):
    for i in range(nb_repet):
        #anim wheel fade in
        leds.fade_wheel()
        leds.fade_off(fadein = False)
        leds.shuffle_wheel()
        leds.fade_off(fadein = False)
                
        #anim random fade out, sans rouge
        leds.fade_random(fadein = False, red=False)
        leds.fade_off()
        leds.shuffle_random(red=False)
        leds.fade_off()

        #anim random fade in, sans vert
        leds.fade_random(green=False)
        leds.fade_off(fadein=False)
        leds.shuffle_random(green=False)
        leds.fade_off(fadein=False)

        #anim random fade out, sans bleu
        leds.fade_random(fadein = False, blue=False)
        leds.fade_off()
        leds.shuffle_random(blue=False)
        leds.fade_off()

def anim_cool_arc_en_ciel(nb_repet=1):
    leds.fade_wheel()
    for i in range(nb_repet):
        leds.rainbow_cycle()

def anim_cool_non_clignotante(nb_repet=1):
    for i in range(nb_repet):
        for j in range(20):
            leds.random_cycle()             #couleurs aléatoires pastel
        for j in range(20):
            leds.random_cycle(red=False)    #couleur aléatoires pastel sans rouge
        for j in range(20):
            leds.random_cycle(green=False)  #couleurs aléatoires pastel sans vert
        for j in range(20):
            leds.random_cycle(blue=False)   #couleurs aléatoires pastel sans bleu
        
def anim_cool_mono_wheel(nb_repet=1):
    for i in range(nb_repet):
        leds.mono_wheel(delay=0.02)

#animation du ruban à l'infini
while True:       
    anim_cool_clignotante(nb_repet=5)
    anim_cool_arc_en_ciel(nb_repet=5)
    anim_cool_non_clignotante(nb_repet=5)
    anim_cool_mono_wheel(nb_repet=5)  

