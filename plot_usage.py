#!/usr/bin/python

###############
### IMPORTS ###
###############

import re
import matplotlib as mb
mb.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy
import time
from multiprocessing import cpu_count as cores
from os.path import expanduser
import os

time.ctime()

############
### VARS ###
############
home = expanduser("~")
DATAFILE=home+'/.usagelog'
OUTPUTDIR=os.path.dirname(os.path.abspath(__file__))
FIGURE_WIDTH=20
FIGURE_HEIGHT=11
PRINT_DEBUG=0
PRINT_ERROR_DEBUG=0
CPU_TRESHOLD=1.0
MEM_TRESHOLD=1.0
COLOR_RGB = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
              (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
              (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
              (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
              (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(COLOR_RGB)):
    r, g, b = COLOR_RGB[i]
    COLOR_RGB[i] = (r / 255., g / 255., b / 255.)

def drawcpu(procs):
    fig = plt.figure()
    proc,l_proc="",""
    total_cpu=[]
    first_cpu=True
    for row in procs:
        ts,cpu=[],[]
        for chunk in row:
            chunk=chunk.split()
            proc=chunk[0]
            ts.append(mdate.epoch2num(float(chunk[1])))
            cpu.append(float(chunk[2])/cores())
        if numpy.mean(cpu)>=CPU_TRESHOLD:
            simpledraw(ts, cpu, proc, fig, "CPU Usage", "cpu")
    print "Figure cpu.png created in " + OUTPUTDIR

# TODO
# def drawtotalcpu(procs):
# def drawtotalmem(procs):


def drawmem(procs):
    fig = plt.figure()
    proc,l_proc="",""
    total_mem=[]
    first_mem=True
    for row in procs:
        ts,mem=[],[]
        for chunk in row:
            chunk=chunk.split()
            proc=chunk[0]
            ts.append(mdate.epoch2num(float(chunk[1])))
            mem.append(float(chunk[3]))
        if numpy.mean(mem) >= MEM_TRESHOLD:
            simpledraw(ts, mem, proc, fig, "MEM Usage", "mem")
    print "Figure mem.png created in " + OUTPUTDIR

def simpledraw(x,y,proc,fig,title,ofilename):
    ax = fig.add_subplot(111)
    ax.set_ylim([0,100])
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%d-%m-%y %H:%M:%S'))
    plt.title(title)
    ax.set_ylabel('Usage (%)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=50)
    fig.set_size_inches(FIGURE_WIDTH, FIGURE_HEIGHT)
    fig.hold(True)
    col = COLOR_RGB[numpy.random.randint(0,10,1)]
    ax.plot_date(x, y, label=proc, ls='-', marker='o', c=col)
    ax.fill_between(x, y, 0, color=col, alpha=0.2)
    ax.legend(loc='best')

    fig.tight_layout()
    plt.savefig(ofilename+".png")


def dg(msg):
    if PRINT_DEBUG == 1:
        print msg.rstrip('\n')



############
### MAIN ###
############
f=open(DATAFILE,'r')
proc,procs=[],[]

num=0
l_chunk=""
for line in sorted(f):
    num+=1
    cnum=0
    barsplit=re.split('\ ',line)
    dg("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Line #{0} |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(str(num)))
    dg(line)
    for chunk in barsplit:
        cnum+=1
        new_entry=line.replace("\n","")
        if cnum==1:
            if chunk==l_chunk:
                dg("    Same process #{0}: {1}".format(str(cnum), str(chunk)))
                proc.append(new_entry)
                l_chunk==chunk
            else:
                dg("    New process #{0}: {1}".format(str(cnum), str(chunk)))
                l_chunk=chunk
                proc=[]
                proc.append(new_entry)
                procs.append(proc)
f.close()
dg("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| File Parsed |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

drawcpu(procs)
drawmem(procs)

