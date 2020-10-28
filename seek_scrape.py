import requests
import collections
import time
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk

def grab_data(new_data, skill, base, clas, loca, date, max_page):
    for crit in skill:
        page = 0
        while page < max_page:
            time.sleep(0.1)
            url = base + crit + '-jobs' + clas + '/in-All-' + loca + '-VIC?daterange=' + str(date) + '&page=' + str(page)
            print(url)
            seek_r = requests.get(url)
            seek_soup = BeautifulSoup(seek_r.text, 'html.parser')
            for i in range(100):
                try:
                    title_box = seek_soup.findAll('a', {'class':'_2iNL7wI'}, {'target':'_self'})[i]
                    title = title_box.text.strip()
                    new_data.append(title) 
                except IndexError:
                    continue
            page += 1

def write_data(new_data):
    old_data = open('seek_data.dat', 'w+')
    for i in range(len(new_data)):
        old_data.write(new_data[i] + '\n')
    old_data.close()

def seperate_strings(new_data, words):
    i = 0
    while i < len(new_data):
        temp = new_data[i].split(' ')
        for j in temp:
            words.append(j.lower())
        i += 1  

def plot_words(words):
    counter = collections.Counter(words)
    #print(counter)
    plt.bar(range(len(counter)), list(counter.values()), align='center')
    plt.xticks(range(len(counter)), list(counter.keys()), rotation=60)
    plt.show()

def open_clas(fname):
    flist = open(fname).readlines()
    return [s.rstrip('\n') for s in flist]

def find_clas(clas_list, word):
    i = 0
    while i < len(clas_list):
        if word.lower() in clas_list[i]:
            print(clas_list[i])
            return '-in-' + clas_list[i]
        else:
            i += 1
    print(word + ' not found. Searching ALL by default.')
    return ''
        
def find_jobs(t_clas, t_skill):
    _base = 'https://www.seek.com.au/'
    _skill = []
    _list = []
    _loca = 'Melbourne'
    _date = 7
    _max_page = 10

    _new_data = []
    _words = []

    _list = open_clas('clas.dat')
    temp = t_clas.get()#input('What classification would you like to search in? ')
    _clas = find_clas(_list, temp)

    temp = t_skill.get()#input('What job do you want to search for? ')
    _skill.append(temp)

    print('Please wait- we need to go slow so as not to wake anything up!')
    grab_data(_new_data, _skill, _base, _clas, _loca, _date, _max_page)
    seperate_strings(_new_data, _words)
    plot_words(_words)
    return _words

root = tk.Tk()

_t_clas = Entry(root)
_t_skill = Entry(root)
_t_clas.pack()
_t_skill.pack()
_t_clas.insert(END, 'classification...')
_t_skill.insert(END, 'skill...')

frame = tk.Frame(root)
frame.pack()

def callback():
    words = find_jobs(_t_clas, _t_skill)

# Run
_b_run = tk.Button(frame, text='Run', command=callback)
_b_run.pack(side=tk.RIGHT)

# Quit
_b_quit = tk.Button(frame, text='Quit', command=quit)
_b_quit.pack(side=tk.RIGHT)

mainloop()

