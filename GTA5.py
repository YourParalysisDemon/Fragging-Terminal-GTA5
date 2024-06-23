import keyboard
import time
import tkinter as tk
import webbrowser
import pygame
import pymem.exception
from threading import Thread
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from subprocess import Popen
from time import sleep

# The game were hacking
mem = Pymem("GTA5")
# The dll we write to
module = module_from_name(mem.process_handle, "GTA5.exe").lpBaseOfDll
# static pointer offsets
health_offsets = [0x280]
ap_offsets = [0x54]
laser_offsets = [0x270, 0X8, 0X0, 0X0, 0X48, 0X0, 0X18]
rev_offsets = [0XD0, 0X20, 0X48, 0X0, 0X18]
c4_offsets = [0X0, 0X708]
cops_offsets = [0x620]
tele_offsets = [0X98]
tele_x_offsets = [0x134]
car_health = [0x18, 0x418, 0x3B8, 0x910]
car_engine = [0x910]
x_axis = [0X1A0]
y_axis = [0X134]
z_axis = [0X138]
player_speed = [0x5E0]
speed_offsets = [0xA88]

# AFK Bot
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class input_i(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", input_i)]


def presskey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = input_i()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008, 0, ctypes.pointer(extra))
    x = input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def releasekey(hexkeycode):
    extra = ctypes.c_ulong(0)
    ii_ = input_i()
    ii_.ki = KeyBdInput(0, hexkeycode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# Are functions
def multi_run_god():
    new_thread = Thread(target=god_hack, daemon=True)
    new_thread.start()


def multi_run_speed():
    new_thread = Thread(target=speed, daemon=True)
    new_thread.start()


def multi_run_police():
    new_thread = Thread(target=never_wanted, daemon=True)
    new_thread.start()


def multi_run_ap():
    new_thread = Thread(target=ap_pistol, daemon=True)
    new_thread.start()


def getpointeraddress(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(mem.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset


def walk_bot():
    while True:
        try:
            time.sleep(5)
            presskey(17)
            time.sleep(2)
            releasekey(17)

            presskey(30)
            time.sleep(2)
            releasekey(30)

            presskey(32)
            time.sleep(2)
            releasekey(32)

            presskey(31)
            time.sleep(2)
            releasekey(31)
            time.sleep(5)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def speed():
    addr = getpointeraddress(module + 0x0261C3E8, speed_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x40400000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def tele_airport():
    addr1 = getpointeraddress(module + 0x02962178, z_axis)
    addr2 = getpointeraddress(module + 0x02962178, y_axis)
    addr3 = getpointeraddress(module + 0x02962170, x_axis)
    try:
        mem.write_int(addr1, 0x416d496e)
        mem.write_int(addr2, 0xc5282c8a)
        mem.write_int(addr3, 0xc47d41c1)
    except pymem.exception.MemoryWriteError as e:
        print(f"Error writing memory: {e}")


def tele_airport_desert():
    addr1 = getpointeraddress(module + 0x02962178, z_axis)
    addr2 = getpointeraddress(module + 0x02962178, y_axis)
    addr3 = getpointeraddress(module + 0x02962170, x_axis)
    try:
        mem.write_int(addr1, 0x42287ddf)
        mem.write_int(addr2, 0x454dcd59)
        mem.write_int(addr3, 0x44db3c43)
    except pymem.exception.MemoryWriteError as e:
        print(f"Error writing memory: {e}")


def tele_mountain():
    addr1 = getpointeraddress(module + 0x02962178, z_axis)
    addr2 = getpointeraddress(module + 0x02962178, y_axis)
    addr3 = getpointeraddress(module + 0x02962170, x_axis)
    try:
        mem.write_int(addr1, 0x4446e90b)
        mem.write_int(addr2, 0x45aed521)
        mem.write_int(addr3, 0x43fb1e13)
    except pymem.exception.MemoryWriteError as e:
        print(f"Error writing memory: {e}")


def tele_up():
    addr = getpointeraddress(module + 0x02962178, z_axis)
    if addr is not None:
        try:
            mem.write_int(addr, 0x4446e90b)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def health_hack():
    addr = getpointeraddress(module + 0x028E5A68, car_engine)
    if addr is not None:
        try:
            mem.write_int(addr, 0x57550000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def god_hack():
    addr1 = getpointeraddress(module + 0x01D75178, health_offsets)
    while 1:
        try:
            mem.write_int(addr1, 0x47960000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def never_wanted():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x0)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def goblin_mode():
    addr1 = getpointeraddress(module + 0x02005F58, health_offsets)
    addr2 = getpointeraddress(module + 0x01D70168, player_speed)
    while 1:
        try:
            mem.write_int(addr1, 0x47960000)
            mem.write_int(addr2, + 7)
            if keyboard.is_pressed("space"):
                keyboard.press_and_release("space")
                sleep(0.07)
                continue
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def both():
    addr1 = getpointeraddress(module + 0x02005F58, health_offsets)
    addr2 = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    addr3 = getpointeraddress(module + 0x0295D228, ap_offsets)
    addr4 = getpointeraddress(module + 0x01D70168, player_speed)
    while 1:
        try:
            mem.write_int(addr1, 0x47960000)
            mem.write_int(addr2, 0x0)
            mem.write_int(addr3, 0x7500)
            mem.write_int(addr4, 7)
            if keyboard.is_pressed("space"):
                keyboard.press_and_release("space")
                sleep(0.07)
                continue
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def kill_hack():
    addr = getpointeraddress(module + 0x02005F58, health_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x0)
            pygame.mixer_music.load("music/kys.mp3")
            pygame.mixer_music.play(1)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def laser_hack():
    addr = getpointeraddress(module + 0x0295E190, laser_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x479600000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def revolver_hack():
    addr = getpointeraddress(module + 0x02C83E30, rev_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x300)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def ap_pistol():
    addr = getpointeraddress(module + 0x0204ED80, ap_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x0b10010)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def pistol_hack():
    addr = getpointeraddress(module + 0x0204ED80, ap_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x7500)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def c4_hack():
    addr = getpointeraddress(module + 0x029621D0, c4_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x20)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def remove_cops():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x0)
            pygame.mixer_music.load("music/cops.mp3")
            pygame.mixer_music.play(1)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def five_stars():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x5)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def four_stars():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x4)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def three_stars():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x3)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def two_stars():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x2)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def one_star():
    addr = getpointeraddress(module + 0x0261C3E8, cops_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x1)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


def open_msn():
    webbrowser.open_new("C:/Microsoft/Windows")


def open_calc():
    pygame.mixer_music.load("music/calc.mp3")
    pygame.mixer_music.play(1)
    Popen("calc.exe")


def open_paint():
    Popen("mspaint.exe")


# Music
pygame.init()
pygame.mixer_music.load("music/mod.mp3")
pygame.mixer_music.play(1)

root = tk.Tk()
root.title("Fragging Terminal")
root.geometry("400x460")
root.configure(background='dark red')
root.attributes("-topmost", True)


def show():
    root.deiconify()


def hide():
    root.withdraw()


label1 = tk.Label(master=root, text='Loops', bg='red', fg='black')
label1.grid(row=0, column=0)
button1 = tk.Button(root, text="God Mode", bg='black', fg='white', command=multi_run_god)
button1.grid(row=1, column=0)
button2 = tk.Button(root, text="No Police", bg='black', fg='white', command=multi_run_police)
button2.grid(row=2, column=0)
button3 = tk.Button(root, text="God Mode/No Police", bg='black', fg='white', command=both)
button3.grid(row=3, column=0)
button4 = tk.Button(root, text="AP Pistol", bg='black', fg='white', command=ap_pistol)
button4.grid(row=4, column=0)
button5 = tk.Button(root, text="Drugs?", bg='black', fg='white', command=multi_run_speed)
button5.grid(row=5, column=0)
button6 = tk.Button(root, text="AFK Bot", bg='black', fg='white', command=walk_bot)
button6.grid(row=6, column=0)

label2 = tk.Label(master=root, text='Police Stars', bg='red', fg='black')
label2.grid(row=7, column=0)
button5 = tk.Button(root, text="Five Stars", bg='black', fg='white', command=five_stars)
button5.grid(row=8, column=0)
button6 = tk.Button(root, text="Four Stars", bg='black', fg='white', command=four_stars)
button6.grid(row=9, column=0)
button7 = tk.Button(root, text="Three Stars", bg='black', fg='white', command=three_stars)
button7.grid(row=10, column=0)
button8 = tk.Button(root, text="Two Stars", bg='black', fg='white', command=two_stars)
button8.grid(row=11, column=0)
button9 = tk.Button(root, text="One Star", bg='black', fg='white', command=one_star)
button9.grid(row=12, column=0)
button10 = tk.Button(root, text="Remove Police", bg='black', fg='white', command=remove_cops)
button10.grid(row=13, column=0)
label3 = tk.Label(master=root, text='Misk', bg='red', fg='black')
label3.grid(row=14, column=0)
button11 = tk.Button(root, text="Calculator", bg='black', fg='white', command=open_calc)
button11.grid(row=15, column=0)
button12 = tk.Button(root, text="MSN", bg='black', fg='white', command=open_msn)
button12.grid(row=16, column=0)
button13 = tk.Button(root, text="Paint", bg='black', fg='white', command=open_paint)
button13.grid(row=17, column=0)

label3 = tk.Label(master=root, text='Non Loops', bg='red', fg='black')
label3.grid(row=0, column=2)
button14 = tk.Button(root, text="Vehicle Health", bg='black', fg='white', command=health_hack)
button14.grid(row=1, column=2)
button15 = tk.Button(root, text="Minigun Ammo", bg='black', fg='white', command=laser_hack)
button15.grid(row=2, column=2)
button16 = tk.Button(root, text="Auto Pistol Ammo", bg='black', fg='white', command=pistol_hack)
button16.grid(row=3, column=2)
button17 = tk.Button(root, text="Heavy Revolver Ammo", bg='black', fg='white', command=revolver_hack)
button17.grid(row=4, column=2)
button18 = tk.Button(root, text="KYS", bg='black', fg='white', command=kill_hack)
button18.grid(row=5, column=2)
button19 = tk.Button(root, text="C4", bg='black', fg='white', command=c4_hack)
button19.grid(row=6, column=2)
label1 = tk.Label(master=root, text='Tele options', bg='red', fg='black')
label1.grid(row=7, column=2)
button23 = tk.Button(root, text="Tele up", bg='black', fg='white', command=tele_up)
button23.grid(row=8, column=2)
button21 = tk.Button(root, text="Tele Airport", bg='black', fg='white', command=tele_airport)
button21.grid(row=9, column=2)
button22 = tk.Button(root, text="Tele Desert Airport", bg='black', fg='white', command=tele_airport_desert)
button22.grid(row=10, column=2)
button22 = tk.Button(root, text="Tele Mountain", bg='black', fg='white', command=tele_mountain)
button22.grid(row=11, column=2)
button20 = tk.Button(root, text="Exit", bg='white', fg='black', command=root.destroy)
button20.grid(row=13, column=2)

label4 = tk.Label(master=root, text='Keybinds', bg='red', fg='black')
label4.grid(row=0, column=3)
label4 = tk.Label(master=root, text='C Show GUI', bg='red', fg='black')
label4.grid(row=1, column=3)
label5 = tk.Label(master=root, text='V Hide GUI', bg='red', fg='black')
label5.grid(row=2, column=3)
label6 = tk.Label(master=root, text='F1 KILLS LOOPS', bg='red', fg='black')
label6.grid(row=3, column=3)
label7 = tk.Label(master=root, text='F6 Remove Cops', bg='red', fg='black')
label7.grid(row=4, column=3)
label8 = tk.Label(master=root, text='F5 God Mode', bg='red', fg='black')
label8.grid(row=5, column=3)
label8 = tk.Label(master=root, text='K KYS', bg='red', fg='black')
label8.grid(row=6, column=3)
label8 = tk.Label(master=root, text='H Vehicle Health', bg='red', fg='black')
label8.grid(row=7, column=3)
keyboard.add_hotkey("c", show)
keyboard.add_hotkey("v", hide)
keyboard.add_hotkey("F5", god_hack)
keyboard.add_hotkey("F6", remove_cops)
keyboard.add_hotkey("k", kill_hack)
keyboard.add_hotkey("h", health_hack)

root.mainloop()
