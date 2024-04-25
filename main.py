import random
from tkinter import *
import pygame
import os


def generate_random_word():
    file = open('data/nouns.txt', 'r', encoding="utf-8")
    a = file.read().splitlines()
    random_word = random.choice(a).upper()
    random_word = list(random_word)
    while len(random_word) > 12:
        random_word = random.choice(a).upper()
        random_word = list(random_word)
    file.close()
    return random_word


def generate_mask(random_word):
    mask = []
    for i in range(len(random_word)):
        mask.append('_')
    return mask


def guess(random_word, mask):
    win.bind('<Return>', next)
    final_result = random_word
    final_result = list(final_result)
    guessed_list = set()
    letters = set()
    writing_list = set()
    lose_count_list = set()
    writing_x = 0
    writing_y = 0

    lose_count = 15
    lose_count_image = PhotoImage(file=f'data/{lose_count}.png')
    lose_count_label = Label(win, image=lose_count_image, width=50, height=50, borderwidth=0)
    lose_count_label.place(x=60, y=225)

    mask_img = PhotoImage(file='data/mask.png')
    for i in range(len(mask)):
        mask_place = Label(win, image=mask_img, borderwidth=0)
        mask_place.place(x=10 + i*45, y=300)


    if '-' in random_word:
        index = random_word.index('-')
        mask[index] = random_word[index]
        random_word[index] = '*'
        guessed_image = PhotoImage(file=f'data/-.png')
        mask_place = Label(win, image=guessed_image, borderwidth=0)
        mask_place.place(x=10 + index*45, y=300)


    while '_' in mask:

        while True:
            guessing.delete(0, END)           
            enter_letter.wait_variable(waiting)
            guess = guessing.get().upper()
            if len(guess) != 1 or guess not in 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ': 
                continue
            else:
                if guess in letters:
                    continue
                else:
                    if guess not in random_word:
                        lose_count -= 1
                        lose_count_image = PhotoImage(file=f'data/{lose_count}.png')
                        lose_count_list.add(lose_count_image)
                        lose_count_label = Label(win, image=lose_count_image, width=50, height=50, borderwidth=0)
                        lose_count_label.place(x=60, y=225)
                        break
                    else:
                        break
        
        if lose_count == 0:
            win.unbind('<Return>')
            for w in win.winfo_children():
                w.destroy()
            win.geometry('800x500')
            lose_background_image = PhotoImage(file='data/lose_background.png')
            lose_background_label = Label(win, image=lose_background_image)
            lose_background_label.place(x=0, y=0)
            
            go_back = PhotoImage(file='data/go_back.png')
            return_to_main_screen = Button(win, image=go_back, command=main_screen, width=348, height=78, borderwidth=0)
            return_to_main_screen.place(x=205, y=200)

            for i in range(len(final_result)):
                guessed_image = PhotoImage(file=f'data/{final_result[i].upper()}.png')
                guessed_list.add(guessed_image)
                mask_place = Label(win, image=guessed_image, borderwidth=0)
                mask_place.place(x=(400 - len(final_result)*25) + i*45, y=290)
            
        letters.add(guess)

        while guess in random_word:
            index = random_word.index(guess)
            guessed_image = PhotoImage(file=f'data/{random_word[index].upper()}.png')
            guessed_list.add(guessed_image)
            mask_place = Label(win, image=guessed_image, borderwidth=0)
            mask_place.place(x=10 + index*45, y=300)
            mask[index] = random_word[index]
            random_word[index] = '*'
        writing_image = PhotoImage(file=f'data/{guess.upper()}.png')
        writing_list.add(writing_image)
        mask_place = Label(win, image=writing_image, borderwidth=0)
        mask_place.place(x=830 + writing_x*45, y=130 + int(writing_y)*44)
        writing_x += 1
        writing_y += 0.2
        writing_y = round(writing_y, 2)
        if writing_x == 5:
            writing_x = 0
    
    win.unbind('<Return>')

    win.geometry('800x500')
    win1_image = PhotoImage(file='data/win1_background.png')
    win1_label = Label(win, image=win1_image)
    win1_label.place(x=0, y=0)

    go_back = PhotoImage(file='data/go_back.png')
    return_to_main_screen = Button(win, image=go_back, command=main_screen, width=348, height=78, borderwidth=0)
    return_to_main_screen.place(x=205, y=200)

    for i in range(len(final_result)):
        guessed_image = PhotoImage(file=f'data/{final_result[i].upper()}.png')
        guessed_list.add(guessed_image)
        mask_place = Label(win, image=guessed_image, borderwidth=0)
        mask_place.place(x=(400 - len(final_result)*25) + i*45, y=290)
    
    win.mainloop()


def start_game():
    global guessing, enter_letter, waiting
    
    pygame.mixer.music.load('data/game.mp3')
    pygame.mixer.music.play(-1)

    for w in win.winfo_children():
        w.destroy()

    win.geometry('1100x700')
    second_background = PhotoImage(file='data/second_background2.png')
    second_background_label = Label(win, image=second_background)
    second_background_label.place(x=0, y=0)
    
    guessing = Entry(win, font=('Arial', 20), width=8)
    guessing.place(x=205, y=210)

    waiting = IntVar()

    enter_image = PhotoImage(file='data/guess_button.png')
    enter_letter = Button(win, image=enter_image, command=lambda: waiting.set(1), borderwidth=0, relief='solid', width=145, height=38)
    enter_letter.place(x=195, y=170)

    exit_image = PhotoImage(file='data/exit_button.png')
    exiting = Button(win, image=exit_image, width=145, height=38, command=exite, borderwidth=0, relief='solid')
    exiting.place(x=880, y=410)

    a = generate_random_word()
    b = generate_mask(a)
    guess(a, b)


def exite():
    win.destroy()
    os.kill(os.getpid(),9)


def next(event):
    waiting.set(1)


def main_screen():
    global win
    win.geometry('800x500')
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('data/main_menu.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.10)

    for w in win.winfo_children():
        w.destroy()
    
    main_background = PhotoImage(file='data/main_background.png')
    main_background_label = Label(win, image=main_background)
    main_background_label.place(x=0, y=0)

    start_image = PhotoImage(file='data/start_button.png')
    starting = Button(win, image=start_image, width=145, height=38, command=start_game, borderwidth=0, relief='solid')
    starting.place(x=310, y=265)
    
    exit_image = PhotoImage(file='data/exit_button.png')
    exiting = Button(win, image=exit_image, width=145, height=38, command=exite, borderwidth=0, relief='solid')
    exiting.place(x=310, y=315)

    win.mainloop()


win = Tk()
win.geometry('800x500')
win.resizable(width=False, height=False)
win.title('Виселица')


main_screen()
