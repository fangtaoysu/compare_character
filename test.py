'''
Author: fangtao
Date: 2024-09-08 17:02:51
LastEditors: 18394604239@163.com 18394604239@163.com
LastEditTime: 2024-09-08 18:02:39
FilePath: /compare_character/test.py
Description: 

Copyright (c) 2024 by fangtao, All Rights Reserved. 
'''
from tkinter import *
from tkinter import messagebox
top = Tk()
top.geometry("100x100")
def helloCallBack():
   msg=messagebox.showinfo( "Hello Python", "Hello World")
B = Button(top, text ="Hello", command = helloCallBack)
B.place(x=50,y=50)
top.mainloop()
