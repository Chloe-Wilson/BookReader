import tkinter as tk
import sqlite3
from selenium import webdriver
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

app = tk.Tk()
app.attributes('-fullscreen', True)
app['bg'] = 'black'

try:
    conn = sqlite3.connect('D:/Books/BookDatabase')
except:
    try:
        conn = sqlite3.connect('//MAIN-DESKTOP/Books/BookDatabase')
    except:
        conn = sqlite3.connect('BookDatabase')
crsr = conn.cursor()

def markRead(title, issue):
    for slave in app.grid_slaves():
        slave.destroy()
    crsr.execute('select * from ' + title + ' where Issue=' + str(issue[0]))
    data = crsr.fetchall()
    if data[0][2] == 1:
        crsr.execute('update ' + title + ' set Read=0 where Issue=' + str(issue[0]))
    else:
        crsr.execute('update ' + title + ' set Read=1 where Issue=' + str(issue[0]))
    openBook(title)

def openIssue(title, issue):
    driver = webdriver.Chrome()
    driver.get(issue[1])
    driver.maximize_window()
    for slave in app.grid_slaves():
        slave.destroy()
    canvas = tk.Canvas(app, bg='black', width=screensize[0] - 20, height=screensize[1])
    canvas.grid(row=0, column=0)
    if issue[2] == 1:
        but = tk.Button(app, font=("Times 20 italic bold", int(50/1080*screensize[1])), bg='green', text='Unread', command=lambda issue=issue, title=title: markRead(title, issue))
    else:
        but = tk.Button(app, font=("Times 20 italic bold", int(50/1080*screensize[1])), text='Read', command=lambda issue=issue, title=title: markRead(title, issue))
    but.configure(width=int(20/1920*screensize[0]), height=int(5/1080*screensize[1]))
    if screensize == (1000, 1500):
        but.configure(width=6, height=1)
    canvas.create_window(screensize[0]/4, screensize[1]/2, window=but)
    app.bind('r', lambda event: markRead(title, issue))
    but = tk.Button(app, font=("Times 20 italic bold", int(50/1080*screensize[1])), text='Back', fg='red', command=lambda: openBook(title))
    app.bind('<Escape>', lambda event: openBook(title))
    but.configure(width=int(20/1920*screensize[0]), height=int(5/1080*screensize[1]))
    if screensize == (1000, 1500):
        but.configure(width=6, height=1)
    canvas.create_window(3*screensize[0]/4, screensize[1]/2, window=but)

def openBook(title):
    for slave in app.grid_slaves():
        slave.destroy()
    app.unbind('r')
    col = 0
    line = 2

    canvas = tk.Canvas(app, bg='black', width=screensize[0] - 20, height=screensize[1])
    butrow = int(10 / 1920 * screensize[0])
    canvas.grid(row=0, column=0)
    scroll_y = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.create_text(screensize[0]/2, 15, font=("Times 20 italic bold", 50), fill="white", text=title)

    crsr.execute('select * from ' + title + ' order by Issue asc')
    for issue in crsr.fetchall():
        if issue[2] == 1:
            but = tk.Button(app, bg='green', wraplength=190, text=issue[0], command=lambda issue=issue, title=title: openIssue(title, issue))
        else:
            but = tk.Button(app, wraplength=190, text=issue[0], command=lambda issue=issue, title=title: openIssue(title, issue))
        but.configure(width=25, height=2)
        canvas.create_window(190 * col, 45 * line, anchor='nw', window=but)
        col += 1
        if col >= butrow:
            col = 0
            line += 1
    but = tk.Button(app, text='Back', fg='red', command=lambda: menu())
    app.bind('<Escape>', lambda event: menu())
    but.configure(width=25, height=2)
    canvas.create_window(190*butrow - 190, 45 * (line + 1), anchor='nw', window=but)
    canvas.configure(scrollregion=canvas.bbox("all"))

def menu():
    for slave in app.grid_slaves():
        slave.destroy()

    col = 0
    line = 0

    canvas = tk.Canvas(app, bg='black', width=screensize[0] - 20, height=screensize[1])
    butrow = int(10 / 1920 * screensize[0])
    canvas.grid(row=0, column=0)
    scroll_y = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll_y.set)

    crsr.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = crsr.fetchall()
    tables = sorted(tables, key=lambda x: x[0])
    for title in tables:
        crsr.execute('select * from ' + title[0] + ' where Read=0')
        exists = crsr.fetchall()
        if exists:
            but = tk.Button(app, wraplength=180, text=title[0], command=lambda title=title[0]: openBook(title))
        else:
            but = tk.Button(app, wraplength=180, bg='green', text=title[0], command=lambda title=title[0]: openBook(title))
        but.configure(width=25, height=2)
        canvas.create_window(190 * col, 45 * line, anchor='nw', window=but)
        col += 1
        if col >= butrow:
            col = 0
            line += 1
    but = tk.Button(app, text='Quit', fg='red', command=lambda: app.destroy())
    app.bind('<Escape>', lambda event: app.destroy())
    but.configure(width=25, height=2)
    canvas.create_window(190*butrow - 190, 45 * (line + 1), anchor='nw', window=but)
    canvas.configure(scrollregion=canvas.bbox("all"))


menu()
app.mainloop()
conn.commit()
conn.close()