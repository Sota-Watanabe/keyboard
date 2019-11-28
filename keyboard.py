import mido
import time
import pygame
import sys
import random
import json
from mido import MidiFile, Message
from pygame.locals import *

DEFAULT_KEY = 48
FILE_list = ["like-piano.json", "lowson-demo.json"]

mode = 0
long_sound = False
outport = mido.open_output("Piaggero:Piaggero MIDI 1 20:0")
print(outport)
table_list = []

def main():
    global mode, long_sound
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((400, 330))    # 画面を作成
    pygame.display.set_caption("keyboard event")    # タイトルを作成

    set_table()

    while True:
        screen.fill((0, 0, 0)) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # キーを押したとき
                # ESCキーならスクリプトを終了
                if event.key == K_ESCAPE:
                    long_sound = not long_sound
                elif event.key == K_F1:
                    mode = 0
                elif event.key == K_F2:
                    mode = 1
                else:
                    octave = 0
                    if mode == 0:
                        if event.mod & pygame.KMOD_LSHIFT:
                            octave = octave - 1
                        if event.mod & pygame.KMOD_RSHIFT:
                            octave = octave + 1
                        key = pygame.key.name(event.key)
                    elif mode == 1:
                        key = pygame.key.name(event.key)
                        if event.mod & pygame.KMOD_SHIFT:
                            key = key.upper()
                    # print(octave)
                    send_midi(key, octave, "down")
            elif event.type == KEYUP:
                send_midi(key, octave, "up")
            pygame.display.update()


def send_midi(key, octave, move):
    # print(long_sound)
    num = key2num(key)
    # num = random.randrange(10, 60)
    if num == None:
        return
    num = num + DEFAULT_KEY + 12 * octave
    if move == "down":
        msg = Message('note_on', note=num, velocity=90)
        outport.send(msg)
    elif move=="up" and long_sound == False:
        msg = Message('note_off', note=num, velocity=0)
        outport.send(msg)
        msg = Message('note_on', note=num, velocity=0)
        outport.send(msg)


def key2num(key):
    if key in table_list[mode]:
        # print(key)
        return table_list[mode][key]

def set_table():
    for file in FILE_list:
        with open(file) as f:
            global table_list
            table_list.append(json.load(f))

if __name__ == '__main__':
   main()
   outport.close()