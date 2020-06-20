# ledStick

Tutoriel complet sur https://www.papsdroid.fr/post/ledstick

## contrôle d'un ruban de leds RGB avec une PYBStick26
 
 ![deco](git_docs/LedStick_decors.jpg) 
 
 Source du projet d'animation d'un ruban de Leds RGB neopixels avec un micro-contrôleur  MicroPython PYBStick26.
 
 ## prototype sur breadboard
 ![fritzing](git_docs/LedStick_fritzing.jpg) 

>**Attention!** le ruban est très fragile: ne pas se tromper avec les voltages (alimentation 5v) et avec les polarités, sinon il est mort direct.

Pour animer le ruban de leds: recopier les 3 fichiers sur le lecteur PYBFLASH qui apparaît lorsque vous branchez la PYBStick26 sur un port USB de votre ordinateur.
* main.py, 
* rubanLeds.py 
* ws2812.py (cette bilbiothèque a été conçue par MCHobby)  

 Déconnectez la PYBStick26, puis branchez l'alimentation Jack DC 5v: le ruban de leds s'anime immédiatement.
 
 ## carte d'extension pour la PYBStick26
 ![Kicad](git_docs/LedStick_Kicad_shcema.png) 
 ![Kicad](git_docs/kicad_LedStick_3D.png) 
  
 Pour fabriquer la carte d'extension chez n'importe quel fabriquant de PCB: utilisez les fichiers GERBER zippés (GERBER_LedStick_v1.1.zip)

Guide de montage sur: https://www.papsdroid.fr/post/ledstick

