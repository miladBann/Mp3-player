
from tkinter import *
from tkinter import filedialog
from tkinter.font import BOLD
import pygame
import pickle
from tkinter import ttk
import time
from mutagen.mp3 import MP3

# current_song_position = None
current_time = "00:00"
full_song_lenght = "00:00"

window = Tk()
window.title("Milo MP3 Player 🎵")
window.minsize(width=745, height=550)
window.config(padx=20, pady=20)

pygame.mixer.init()
########################################functions##################################


def add_songs():
    songs = filedialog.askopenfilenames(title="Choose Songs", filetypes=(
        ("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))

    for song in songs:
        lista.insert(END, song)


current_time1 = None


def get_song_pos():
    global current_time, full_song_lenght, current_time1

    # get the current song position
    current_pos = pygame.mixer.music.get_pos()
    current_time1 = int(current_pos / 1000)
    current_time = time.strftime("%M:%S", time.gmtime(current_time1))
    time_elapsed.config(
        text=f"time elapsed: {current_time}, out of: {full_song_lenght}")

    crr_song = lista.curselection()
    song = lista.get(crr_song)
    audio = MP3(song)
    song_lenght = audio.info.length

    current_time1 += 1

    if int(scroll.get()) == int(song_lenght):
        time_elapsed.config(
            text=f'Time Elapsed: {current_time}  of  {full_song_lenght}  ')
    elif paused:
        pass
    elif int(scroll.get()) == int(current_time1):
        # Update Slider To position
        slider_position = int(song_lenght)
        scroll.config(to=slider_position, value=int(current_time1))
    else:
        # Update Slider To position
        slider_position = int(song_lenght)
        scroll.config(to=slider_position, value=int(scroll.get()))

        # convert to time format
        converted_current_time = time.strftime(
            '%M:%S', time.gmtime(int(scroll.get())))

        # Output time to status bar
        time_elapsed.config(
            text=f'Time Elapsed: {converted_current_time}  of  {full_song_lenght}  ')

        # Move this thing along by one second
        next_time = int(scroll.get()) + 1
        scroll.config(value=next_time)

    time_elapsed.after(1000, get_song_pos)


def get_song_lenght():
    global full_song_lenght

    # get the song lenght
    crr_song = lista.curselection()
    song = lista.get(crr_song)
    audio = MP3(song)
    song_lenght = audio.info.length
    convert_song_lenght = time.strftime("%M:%S", time.gmtime(song_lenght))
    full_song_lenght = convert_song_lenght
    time_elapsed.config(
        text=f"time elapsed: {current_time}, out of: {full_song_lenght}")

    scroll.config(to=song_lenght)


def play():
    global full_song_lenght
    song_to_play = lista.get(ACTIVE)
    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0)

    current_amount = str(volume_scroll.get() * 100)
    current_volume_amount = current_amount.split(".")[0]
    current_volume.config(text=current_volume_amount)

    # get the song lenght
    get_song_lenght()
    # get song playing position
    get_song_pos()


def scroller(x):
    pygame.mixer.music.set_pos(scroll.get())


def stop_song():
    pygame.mixer.music.stop()

    scroll.config(value=0)


paused = False


def pause_song():
    global paused
    if paused == False:
        pygame.mixer.music.pause()
        paused = True
    elif paused == True:
        pygame.mixer.music.unpause()
        paused = False


def forward():
    current_song = lista.curselection()
    next_song = current_song[0] + 1
    song = lista.get(next_song)

    scroll.config(value=0)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    lista.selection_clear(0, END)
    lista.activate(next_song)
    lista.selection_set(next_song, last=None)

    get_song_lenght()


def backward():
    current_song = lista.curselection()
    before_song = current_song[0] + -1
    song = lista.get(before_song)

    scroll.config(value=0)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    lista.selection_clear(0, END)
    lista.activate(before_song)
    lista.selection_set(before_song, last=None)

    get_song_lenght()


def save():
    file_name = filedialog.asksaveasfilename(
        title="Save Play List", filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*")))

    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name = f"{file_name}.dat"

    stuff = lista.get(0, END)

    output_file = open(file_name, "wb")

    pickle.dump(stuff, output_file)


def clear():
    pygame.mixer.music.stop()
    lista.delete(0, END)


def open_list():
    file_name = filedialog.askopenfilename(title="Open file", filetypes=(
        ("Dat Files", "*.dat"), ("All Files", "*.*")))
    if file_name:

        # delete currently open list
        lista.delete(0, END)

        # open the file
        input_file = open(file_name, "rb")  # rb means write binary

        # load the stuff from the file
        stuff = pickle.load(input_file)

        # output stuff on the screen
        for item in stuff:
            lista.insert(END, item)


def volume(x):
    pygame.mixer.music.set_volume(volume_scroll.get())

    current_amount = str(volume_scroll.get() * 100)
    current_volume_amount = current_amount.split(".")[0]

    current_volume.config(text=current_volume_amount)


#########################################user interface############################
# list
my_frame = Frame(window)
my_frame.place(x=30, y=20)

lista = Listbox(my_frame, font=("Arial", 18, "bold"), width=45, height=11,
                highlightthickness=0, activestyle=None, borderwidth=3, relief="solid")
lista.pack(side="left", fill="both")

my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side="right", fill="both")

lista.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=lista.yview)

# images
play_img = PhotoImage(file="./pics/play.png")
pause_img = PhotoImage(file="./pics/pause.png")
stop_img = PhotoImage(file="./pics/stop.png")
forward_img = PhotoImage(file="./pics/forward.png")
backward_img = PhotoImage(file="./pics/backward.png")

# buttons
play_btn = Button(image=play_img, command=play)
play_btn.place(x=300, y=370)

pause_btn = Button(image=pause_img, command=pause_song)
pause_btn.place(x=420, y=370)

stop_btn = Button(image=stop_img, command=stop_song)
stop_btn.place(x=540, y=370)

forward_btn = Button(image=forward_img, command=forward)
forward_btn.place(x=180, y=370)

backward_btn = Button(image=backward_img, command=backward)
backward_btn.place(x=60, y=370)

# menu
my_menu = Menu(window)
window.config(menu=my_menu)

# add items to the menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=file_menu)

file_menu2 = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Save Play List", menu=file_menu2)

file_menu3 = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Clear List", menu=file_menu3)

# add drop down items to the menu
file_menu.add_command(label="Add Songs to the list", command=add_songs)
file_menu.add_command(label="Open Saved Play List", command=open_list)
file_menu2.add_command(label="Save as", command=save)
file_menu3.add_command(label="Clear list", command=clear)

# volume scroll
volume_scroll = ttk.Scale(
    from_=0, to=1, orient="vertical", length=145, command=volume, value=0.70)
volume_scroll.place(x=655, y=100)


# volume label indicator
current_amount = str(volume_scroll.get() * 100)
current_volume_amount = current_amount.split(".")[0]
current_volume = Label(text=current_volume_amount, font=("Arial", 15, "bold"))
current_volume.place(x=653, y=250)

# normal scroll
scroll = ttk.Scale(from_=0, to=100, orient="horizontal",
                   length=450, command=scroller, value=0)
scroll.place(x=120, y=450)


# time indecator

time_elapsed = Label(
    text=f"time elapsed: {current_time}, out of: {full_song_lenght}", font=("Arial", 16, "bold"))
time_elapsed.place(x=340, y=490)

window.mainloop()
