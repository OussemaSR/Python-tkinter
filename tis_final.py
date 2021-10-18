from tkinter import *
import matplotlib.pyplot as plt
from tkinter import filedialog
from PIL import Image , ImageTk
import tkinter as tk
from pydub import AudioSegment 
import pydub 
from playsound import playsound
from scipy.io.wavfile import write
import pygame
import time
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import ntpath
import wave
from mutagen.mp3 import MP3
import librosa, librosa.display
##from sets import Set

root = Tk()
root.title('MP3 Player')

root.geometry("500x300")
# intialize pygame Mixer
pygame.mixer.init()
# define variable texts (recording status / file name)
fls = StringVar()
fls.set("No File")

fls2 = StringVar()
fls2.set("No Activity")

###################################################################
##### Audio processing functions ####################################

def audio_filter():
    song = song_box.get(ACTIVE)
    song = f'C:/images/song/{song}'

    wav_file = f'{song}.wav'
    sound = pydub.AudioSegment.from_mp3(f'{song}.mp3')
    sound.export(wav_file, format="wav")
    # filterd sound by low  freq-filter
    new = sound.low_pass_filter(3000)
    # filterd sound by low  high-filter

    new1 = new.high_pass_filter(3000)
    
    # increase volume by 6db
    song_6_db_quieter = new1+ 6
    
    song_6_db_quieter.export(f'{song}_Filtered.wav', format="wav")
    
    song_6_db_quieter.export(f'{song}_Filtered.mp3', format="mp3")
    
    # stripping
    base = path_leaf(f'{song}_Filtered.mp3')
    base = os.path.splitext(base)[0]
    song_box.insert(END, base)

    
    signal_wave = wave.open(wav_file, 'r')
    sample_rate = 44100
    o_sig= np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)
    plt.figure(1)
    #  ploting the original sound
    
    plot_a = plt.subplot(221)
    plot_a.set_title("Waveform before filtering") 
    plot_a.plot(o_sig)
    plot_a.set_xlabel('sample rate * time')
    plot_a.set_ylabel('energy')

    plot_b = plt.subplot(222)
    plot_b.set_title("Frequency Spectrum before filtering")
    plot_b.specgram(o_sig, NFFT=1024, Fs=sample_rate, noverlap=900)
    plot_b.set_xlabel('Time')
    plot_b.set_ylabel('Frequency')

    #  ploting the filtrered sound

    signal_wave2 = wave.open(f'{song}_Filtered.wav', 'r')
    sig2 = np.frombuffer(signal_wave2.readframes(sample_rate), dtype=np.int16)

    plot_a = plt.subplot(223)
    plot_a.set_title("Waveform after filtering") 
    plot_a.plot(sig2)
    plot_a.set_xlabel('sample rate * time')
    plot_a.set_ylabel('energy')

    plot_b = plt.subplot(224)
    plot_b.set_title("Frequency Spectrum after filtering")
    plot_b.specgram(sig2, NFFT=1024, Fs=sample_rate, noverlap=900)
    plot_b.set_xlabel('Time')
    plot_b.set_ylabel('Frequency')
    
    plt.show()
    
def audio_comprizion():
    
    song = song_box.get(ACTIVE)
    song = f'C:/images/song/{song}'
    # show file size before comression 
    file_stats = os.stat(f'{song}.mp3')
    print(f'Original File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')
    
    # Read the audio file and set the sampling rate <default=44100>
    song_cmprss = AudioSegment.from_mp3(f'{song}.mp3').set_frame_rate(22050)
    # Export the file to the specified path by bitrate of 32k, here is to directly overwrite the original file.
    song_cmprss.export(f'{song}_Compressed.mp3', format='mp3', bitrate='32k')

    # show file size after comression 
    file_stats2 = os.stat(f'{song}_Compressed.mp3')
    print(f'Compressed File Size in MegaBytes is {file_stats2.st_size / (1024 * 1024)}')
    # stripping
    base = path_leaf(f'{song}_Compressed.mp3')
    base = os.path.splitext(base)[0]
    song_box.insert(END, base)

def audio_nummig():
    # converting mp3 file to wav for treatement
    song = song_box.get(ACTIVE)
    song = f'C:/images/song/{song}' 
    wav_file = f'{song}.wav'
    sample_rate = 44100
    sound = pydub.AudioSegment.from_mp3(f'{song}.mp3')
    sound.export(wav_file, format="wav")
    signal_wave = wave.open(wav_file, 'r')
    sig = np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)

    plt.figure(2)
    plt.title('decimalated signal')
    
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.plot(sig)
    plt.show()
def audio_coding():
    song = song_box.get(ACTIVE)
    song = f'C:/images/song/{song}' 
    file = f'{song}.wav'
    sound = pydub.AudioSegment.from_mp3(f'{song}.mp3')
    sound.export(file, format="wav")
    signal_wave = wave.open(file, 'r')
    i=0
    sample_rate = 44100
    sig = np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)
    sig[:100]
    x=np.arange(1,1602)
    my_list = []
    bin_list = []
    bin_list.append(0)
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    print("binary signal")
    for i in sig[:100]:
        print(np.uint16(i))
        print(get_bin(np.uint16(i), 16))
        b=get_bin(np.uint16(i), 16)
        my_list.append(b)
        for j in b:
            bin_list.append(j)
    plt.figure(3)
    plt.title("Coded First 100 Simples")
    plt.step(x,bin_list)
    plt.xlabel(my_list) 
    plt.grid()
    plt.show()

def audio_tff():
    song = song_box.get(ACTIVE)
    song = f'C:/images/song/{song}' 
    file = f'{song}.wav'
    sound = pydub.AudioSegment.from_mp3(f'{song}.mp3')
    sound.export(file, format="wav")
    base = path_leaf(f'{song}.mp3')
    base = os.path.splitext(base)[0]
    signal,sr = librosa.load(file,sr=44000)

    fft = np.fft.fft(signal)

    magnitude = np. abs(fft)
    frequency = np.linspace(0,sr,len(magnitude))
    plt.figure(4)
    plt.plot(frequency, magnitude)
    plt.title(f'FFT Spectrum of <{base}>')
    plt.xlabel("frequency")
    plt.ylabel("Amplitude")
    plt.show()

##################################################################
##################################################################
    
# mp3 to wav
def mp3_2_wav(cnv3):
   wav_file = f'{cnv3}.wav'
   sound = pydub.AudioSegment.from_mp3(f'{cnv3}.mp3')
   sound.export(wav_file, format="wav")
   os.remove(f'{cnv3}.wav') # delete old mp3 file

# wav to mp3
def wav_2_mp3(cnvw):
      mp3_file = f'{cnvw}.mp3'
      sound = pydub.AudioSegment.from_wav(f'{cnvw}.wav')
      sound.export(mp3_file, format="mp3")
      os.remove(f'{cnvw}.wav') # delete old  wav file
      
##################################################################

    
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# audio file length duration
duration =5
# simple rate
fs = 44100

sd.default.samplerate = fs
sd.default.channels = 2


# play recorded sound function
def add_to_play(): 
    base = path_leaf(fln)
    song_box.insert(END, base)
    rec_root.destroy()
def start_rec() :
    
    fls2.set("recording.....")
      
      # variable to hold recording file
    myrec = sd.rec(int(duration*fs) )
      
    sd.wait()
      #recording audio
    sf.write(f'{fln}.wav' , myrec , fs)
      
     # convert recorded  wav file to mp3
    wav_2_mp3(fln)
    rec_button.config(text = "record",command=startrecord)
    fls2.set("finished recording")
    rec_status_bar.config(text = f' Audio File:      { fls.get()}     Status:     { fls2.get()}    ')
    global  rec_add_button
    rec_add_button = Button(rec_root, text = "add to song box",command = add_to_play)
    rec_add_button.place(x=100, y=20)
    rec_add_button.pack()
# define start record function
def startrecord():
      
      # define default save path
      global fln
      fln = filedialog.asksaveasfilename(initialdir='C:/images/song' ,title="Save Audio File", filetypes=(("Audio File","*.mp3"),("All Files","*.*")))
      fls.set(path_leaf(fln))

      if fls.get()=='':
          print("waiting for file name")
      else:
          rec_status_bar.config(text = f' Audio File:      {fls.get()}     Status:     {fls2.get()}    ')
          rec_button.config(text = "start recording",command=start_rec)    
      

     
# create record song  tab 
def record_song_tab():
   stop()
   global rec_root
   rec_root = Tk()
   rec_root.title('Sound Recorder exe')
   rec_root.geometry("400x200")
   fls.set("No File")
   fls2.set("No Activity")
  
   global rec_controls_frame
   rec_controls_frame = Frame(rec_root)
   rec_controls_frame.pack(pady=35)
   global rec_button 
   rec_button = Button(rec_controls_frame, text = "record",command = startrecord)
   stop_button = Button(rec_controls_frame, text = "stop",command = lambda:exit())

   rec_button.grid(row = 0 , column = 0, padx=10)
   stop_button.grid(row = 0 , column = 1, padx=10)
   global rec_status_bar
   rec_status_bar = Label(rec_root, text ='',bd = 1,relief = GROOVE, anchor =E)
   rec_status_bar.pack(fill = X, side = BOTTOM, ipady = 2)
   rec_status_bar.config(text = f' Audio File:      { fls.get()}     Status:     { fls2.get()}    ')
  
   

# grab song lenght time info

def play_time():
   # grab current song elapsed time
   current_time = pygame.mixer.music.get_pos() / 1000
   # convert time format
   converted_current_time = time.strftime('%M:%S ',time.gmtime(current_time ))
   

   song = song_box.get(ACTIVE)
   song = f'C:/images/song/{song}.mp3'
   # load song with mutagen
   song_mut = MP3(song)
   #get song lenght
   song_length= song_mut.info.length
   converted_song_length = time.strftime('%M:%S ',time.gmtime(song_length ))
   status_bar.config(text = f' Time Elapsed  { converted_current_time}  of  { converted_song_length}    ')


   status_bar.after(1000, play_time)
   
# Add song function
def add_song():
   song = filedialog.askopenfilename(initialdir='C:/images/song', title = "Choose A Song", filetypes=(("mp3 files","*.mp3"),("wav Files","*.wav")))
 # stripping
   base = path_leaf(song)
   base = os.path.splitext(base)[0]
   song_box.insert(END, base)
# Add songs function
def add_many_songs():
  songs = filedialog.askopenfilenames(initialdir='C:/images/song', title = "Choose A Song", filetypes=(("mp3 files","*.mp3"),("wav Files","*.wav"))) # os.getcwd() command for directory access

  # loop thru song list  and stripping
  for song in songs:
       base = path_leaf(song)
       base = os.path.splitext(base)[0]
       song_box.insert(END, base)
# play function
def play():
     song = song_box.get(ACTIVE)
     song = f'C:/images/song/{song}.mp3'
   
     pygame.mixer.music.load(song)
     pygame.mixer.music.play(loops=0)
     # call play time
     play_time()
def stop():
     pygame.mixer.music.stop()
     song_box.selection_clear(ACTIVE)
     # clear status bar
     status_bar.config(text='')
# play the next song
def next_song():
    
   next_one = song_box.curselection()
   next_one = next_one[0]+1
   song = song_box.get(next_one)
   song = f'C:/images/song/{song}.mp3'
   pygame.mixer.music.load(song)
   pygame.mixer.music.play(loops=0)
   # move active bar in palylist
   song_box.selection_clear(0,END)
   song_box.activate(next_one)
   song_box.selection_set(next_one,last=None)
# play the previous song
def prv_song():
   
   next_one = song_box.curselection()
   next_one =next_one[0]-1
   song = song_box.get(next_one)  
   song = f'C:/images/song/{song}.mp3'
   pygame.mixer.music.load(song)
   pygame.mixer.music.play(loops=0)
    # move active bar in palylist
   song_box.selection_clear(0,END)
   song_box.activate(next_one)
   # set active bar
   song_box.selection_set(next_one,last=None)
   

# create global pause variable
global paused
paused = False

# pause and unpause current song
def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True
        
# Create playlist Box
song_box = Listbox(root, bg="black", fg="green", width=80, selectbackground="grey", selectforeground="black")
song_box.pack(pady=20)

# define player control button images 
back_btn_img= PhotoImage(file = 'C:/images/back50.png')
forward_btn_img= PhotoImage(file = 'C:/images/forward50.png')
play_btn_img= PhotoImage(file = 'C:/images/play50.png')
pause_btn_img= PhotoImage(file = 'C:/images/pause50.png')
stop_btn_img= PhotoImage(file = 'C:/images/stop50.png')
# create player controle frame
controls_frame = Frame(root)
controls_frame.pack()

# create player control buttons

back_button = Button(controls_frame, image= back_btn_img, borderwidth=0,command=prv_song )
forward_button = Button(controls_frame, image= forward_btn_img, borderwidth=0,command=next_song)
play_button = Button(controls_frame, image= play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image= pause_btn_img, borderwidth=0,command=lambda: pause(paused))
stop_button = Button(controls_frame, image= stop_btn_img, borderwidth=0,command=stop)


back_button.grid(row=0,column=0, padx=10)
forward_button.grid(row=0,column=1, padx=10)
play_button.grid(row=0,column=2, padx=10)
pause_button.grid(row=0,column=3, padx=10)
stop_button.grid(row=0,column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label ="Add Songs", menu=add_song_menu)

add_song_menu.add_command(label = "Add One Song To Playlist", command=add_song)
#add many song menu
add_song_menu.add_command(label = "Add many songs To Playlist", command=add_many_songs)
# create record menu
record_menu = Menu(my_menu)
my_menu.add_cascade(label ="Record A Song", menu=record_menu)
record_menu.add_command(label = "Record Sound",command = record_song_tab)
# create sound editor menu
audio_processing = Menu(my_menu)
my_menu.add_cascade(label ="Audio Processing", menu=audio_processing)

audio_processing.add_command(label = "Filtering",command = audio_filter)
audio_processing.add_command(label = "Compression",command = audio_comprizion)
audio_processing.add_command(label = "Numerisation",command = audio_nummig)
audio_processing.add_command(label = "Coding",command = audio_coding)
audio_processing.add_command(label = "FFT Application",command = audio_tff)
# create status bar
status_bar = Label(root, text ='',bd = 1,relief = GROOVE, anchor =E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 2)

root.mainloop()
