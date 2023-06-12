#!/usr/bin/python
# -*- coding: latin-1 -*-

# Copyright (c) 2006-2023 Miguel Bazdresch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from curses import *
from math import log
from random import randint

class Cache:
    # cache is a list of sets
    # each set is a dict
    def __init__(self, u, v):
        self.mem = []
        self.v = int(v)
        self.u = int(u)

        for i in range(self.u):
            self.mem.append([])
            for j in range(self.v):
                self.mem[i].append(-1)

    def find(self, set, tag):
        # determine if tag is in set
        for i in range(self.v):
            #update_debug(debug, i, set, tag, self.mem[set][i])
            #debug.getch()
            if self.mem[set][i] == tag:
                # hit
                return 0
        # miss
        self.update(set, tag)
        return 1

    def update(self, set, tag):
        # see if there's an empty line in set
        done = 0
        for i in range(self.v):
            if self.mem[set][i] == -1:
                self.mem[set][i] = tag
                done = 1
                break
        # set is full -- TODO: allow other replacement policies.
        if done == 0:
            # random replacement policy
            rep = randint(0,self.v-1)
            self.mem[set][rep] = tag

def update_title(win, message):
    win.erase()
    win.box()
    win.addstr(1, 2, message, A_REVERSE + A_BOLD)
    win.refresh()

def update_status(win, message1, message2, attrib=A_NORMAL):
    win.erase()
    win.box()
    win.addstr(1, 2, message1, A_REVERSE + A_BOLD)
    win.addstr(' ' + message2, attrib)
    win.refresh()

def update_params(win, M, C, v, k, L, B, u, n, m, s, t):
    undef = 'No definido'
    if M == 0:
        Ms = undef
        mb = ''
    else:
        Ms = str(M)
        mb = 'MB'
    if C == 0:
        Cs = undef
        kb = ''
    else:
        Cs = str(C)
        kb = 'kB'
    if v == 0: vs = undef
    else: vs = str(v)
    if k == 0: ks = undef
    else: ks = str(k)
    if L == 0: Ls = undef
    else: Ls = str(L)
    if B == 0: Bs = undef
    else: Bs = str(B)
    if u == 0: us = undef
    else: us = str(u)
    if m == 0: ms = undef
    else: ms = str(m)
    if n == 0: ns = undef
    else: ns = str(n)
    if s == 0: ss = undef
    else: ss = str(s)
    if t == 0: ts = undef
    else: ts = str(t)
    win.erase()
    win.addstr(1, 2, 'Parámetros', A_BOLD)
    win.addstr(3, 3, 'Mem Princ (M): ' + Ms + mb)
    win.addstr(4, 3, 'Mem Cache (C): ' + Cs + kb)
    win.addstr(5, 3, 'Vías      (v): ' + vs)
    win.addstr(6, 3, 'Bytes/L   (k): ' + ks)
    win.addstr(7, 3, 'Líneas    (L): ' + Ls)
    win.addstr(8, 3, 'Bloques   (B): ' + Bs)
    win.addstr(9, 3, 'Conjuntos (u): ' + us)
    win.addstr(10, 3, 'n            : ' + ns)
    win.addstr(11, 3, 'm            : ' + ms)
    win.addstr(12, 3, 's            : ' + ss)
    win.addstr(13, 3, 't            : ' + ts)
    win.box()
    win.refresh()

def update_results(win, reads, hits, misses, time, block, set, tag):
    undef = 'No definido'
    if reads == 0:
        rs = undef
        hr = undef
        tr = undef
        mr = undef
    else:
        rs = str(reads)
        hr = str(round(float(hits)/float(reads),4))
        tr = str(round(float(time)/float(reads),4))
        mr = str(round(float(misses)/float(reads),4))
    win.erase()
    win.addstr(1, 2, 'Resultados', A_BOLD)
    win.addstr(3, 3, 'Lecturas   : ' + rs)
    win.addstr(4, 3, 'Aciertos   : ' + str(hits))
    win.addstr(5, 3, '% Aciertos : ' + hr)
    win.addstr(6, 3, 'Fallas     : ' + str(misses))
    win.addstr(7, 3, '% Fallas   : ' + mr)
    win.addstr(8, 3, 'Tiempo     : ' + str(time))
    win.addstr(9, 3, 'T Promedio : ' + tr)
    win.addstr(11, 3, 'Bloque     : ' + str(block))
    win.addstr(12, 3, 'Conjunto   : ' + str(set))
    win.addstr(13, 3, 'Etiqueta   : ' + str(tag))
    win.box()
    win.refresh()

def userinput():
    echo()
    update_status(status, 'Status: ', 'Oprima una tecla para comenzar.')
    status.getch()
    update_status(status, 'Configuración: ', 'Tamaño de la memoria principal (MB): ')
    M = status.getstr()
    update_status(status, 'Configuración: ', 'Tamaño de la memoria cache (kB): ')
    C = status.getstr()
    update_status(status, 'Configuración: ', 'Número de vías: ')
    v = status.getstr()
    update_status(status, 'Configuración: ', 'Número de bytes por línea: ')
    k = status.getstr()
    update_status(status, 'Configuración: ', 'Localidad (1=baja, 2=media, 3=alta): ')
    loc = status.getstr()
    noecho()
    return int(M), int(C), int(v), int(k), int(loc)

def calc_params(M, C, v, k):
    L = int(1024*C/k)
    B = int(1024*1024*M/k)
    u = int(L/v)
    n = int(log(M,2)) + 20
    s = int(log(u,2))
    m = int(log(k,2))
    t = n-(s+m)
    return L, B, u, n, m, s, t

def gen_block(oldblock):
    # bootstrap with a random block
    # subsequent blocks are the last one, plus a random quantity that depends on locality
    # TODO: more sophisticated jumping
    if loc == 1:
        # completely random new block
        return randint(0,B-1)
    ch = randint(1,100)
    distance = 0
    # 30% chance of jumping -10 to +10 blocks away
    if loc == 2:
        if ch > 70:
            distance = randint(1,20)-10
            if distance == 0: distance = 1
    # 10% chance of jumping -5 to +5 blocks away
    if loc == 3:
        if ch > 90:
            distance = randint(1,10)-5
            if distance == 0: distance = 1
    newblock = oldblock + distance
    if newblock > B-1: newblock = B-1
    if newblock < 0: newblock = 0
    return newblock

def start():
    reads = 0
    hits = 0
    misses = 0
    time = 0
    c = ''
    bloque = 0
    set = 0
    tag = 0
    update_status(status, 'Oprima: ', "'space': paso a paso, 'i': 10,000 iteraciones, 'q': terminar")
    while c != ord('q'):
        update_results(results, reads, hits, misses, time, bloque, set, tag)
        c = results.getch()
        if c == ord(' '):
            reads += 1
            bloque = gen_block(bloque)
            # from block number, get set and tag
            set = int(bloque % u)
            tag = bloque//u
            incache = cache.find(set, tag)
            if incache == 0:
                hits += 1
                time += TA_CACHE
            else:
                misses += 1
                time += k*(TA_MEM) + TA_CACHE
            continue
        if c == ord('i'):
            reads += 10000
            for i in range(10000):
                bloque = gen_block(bloque)
                # from block number, get set and tag
                set = int(bloque % u)
                tag = bloque//u
                incache = cache.find(set, tag)
                if incache == 0:
                    hits += 1
                    time += TA_CACHE
                else:
                    misses += 1
                    time += k*(TA_MEM) + TA_CACHE
            continue

# initialize screen
scr = initscr()
noecho()
cbreak()

# global variables: access time to memory
TA_MEM = 100  # regular memory
TA_CACHE = 5  # cache memory

# wrap everything to warrant clean exit on error
try:
    # initial memory parameters
    M = 0
    C = 0
    v = 0
    k = 1
    L = 0
    B = 0
    u = 0
    n = 0
    m = 0
    s = 0
    t = 0

    # windows
    title = newwin(3, 80, 0, 0)
    status = newwin(3, 80, 20, 0)
    params = newwin(15, 31, 4, 0)
    results = newwin(15, 31, 4, 40)
    update_title(title, '                      Simulador de Memoria Cache                            ')
    update_params(params, M, C, v, k, L, B, u, n, m, s, t)
    update_results(results, 0, 0, 0, 0, 0, 0, 0)

    # get user input
    M, C, v, k, loc = userinput()

    # calculate parameters
    L, B, u, n, m, s, t = calc_params(M, C, v, k)
    update_params(params, M, C, v, k, L, B, u, n, m, s, t)

    # create cache object
    cache = Cache(u, v)
    # start simulation
    start()

except Exception as ex:
    # on unexpected error, exit cleanly
    nocbreak()
    echo()
    endwin()

finally:
    # finishing touches
    nocbreak()
    echo()
    endwin()
