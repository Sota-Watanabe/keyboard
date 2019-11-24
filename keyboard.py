import mido
import time
import pygame
import sys
import random
import json
from mido import MidiFile, Message
from pygame.locals import *

DEFAULT_KEY = 48
CFILE = "conversion-table.json"
outport = mido.open_output("Piaggero:Piaggero MIDI 1 24:0")
print(outport)
table = None

def main():    
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((400, 330))    # 画面を作成
    pygame.display.set_caption("keyboard event")    # タイトルを作成

    with open(CFILE) as f:
        global table
        table = json.load(f)

    while True:
        screen.fill((0, 0, 0)) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # キーを押したとき
                # ESCキーならスクリプトを終了
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    octave = 0
                    if event.mod & pygame.KMOD_LSHIFT:
                        octave = octave - 1
                    if event.mod & pygame.KMOD_RSHIFT:
                        octave = octave + 1
                    send_midi(pygame.key.name(event.key), octave)
            pygame.display.update()


def send_midi(key, octave):
    num = key2num(key.upper())
    # num = random.randrange(10, 60)
    if num == None:
        return
    num = num + DEFAULT_KEY + 12 * octave
    msg = Message('note_on', note=num, velocity=90)
    outport.send(msg)
    print(msg)



def key2num(key):
    if key in table:
        return table[key]

if __name__ == '__main__':
   main()
   outport.close()