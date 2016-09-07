#!/usr/bin/env python3
import tkinter as tk
import logging
logging.basicConfig(level=logging.DEBUG)

class App:
    def __init__(self, master, columns=5):
        # Make frame, child of master
        f = tk.Frame(master)
        #Initialize grid to 40px wide columns
        for column in range(columns):
            f.columnconfigure(column,minsize=40)
        f.pack()

        #tk.Button(f,text="4").grid(column=0,row=1)
        
        row, column = 0, 0
        # Loop through buttons and create button
        # with the command which will then be appended to the
        # "command line", with the exception of functions
        for i,(button,buttonInf) in enumerate(buttons):
            tk.Button(f,text=button).grid(column=column,row=row)
            
            logging.info("Button: {} at row {} col {}".format(button,row,column))
            #Create a new row if needed
            if column == columns - 1:
                logging.info("Creating new row at: {}".format(i))
                row += 1
                column = 0
            else:
                column += 1




    def parse_line(self,line):
        return True

    def clear_line(self):
        return True

#Dict of buttons for the calculator
#key is the display text and the value is the value to 
#be appended to the line or the function to be executed
_buttons = [
    ('0',0),
    ('.','.'),
    ('x10','*10'),
    ('Ans','ANS'),
    ('=',App.parse_line),
    ('eh','eh'),
    ('1',1),
    ('2',2),
    ('3',3),
    ('+','+'),
    ('-','-'),
    ('1/x','1/ANS'),
    ('4',4),
    ('5',5),
    ('6',6),
    ('x','*'),
    ('÷','/'),
    ('±','±'), # What to do with this?
    ('7',7),
    ('8',8),
    ('9',9),
    ('(','('),
    (')',')'),
    ('C',App.clear_line),
]
buttons = [
    ('7',7),
    ('8',8),
    ('9',9),
    ('(','('),
    (')',')'),
    ('4',4),
    ('5',5),
    ('6',6),
    ('x','x'),
    ('/','/')

]


        
root = tk.Tk()
app = App(root)
root.mainloop()
