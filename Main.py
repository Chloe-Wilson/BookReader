import tkinter as tk
import os
from PIL import Image, ImageTk
import Global as g


app = tk.Tk()
app.attributes('-fullscreen', True)
app['bg'] = 'black'
global img

def next(manga, issue, event=None):
    try:
        if g.page < len(os.listdir('D:/Books/' + manga + '/' + issue + '/')) - 1:
            g.page += 1
            g.pages.delete('img')
            g.imraw = Image.open('D:/Books/' + manga + '/' + issue + '/' + str(g.page) + '.jpg')
            w, h = g.imraw.size
            if int((1000 / h) * w) > 1560:
                g.imraw = g.imraw.resize((1560, int((1560 / w) * h)))
            else:
                g.imraw = g.imraw.resize((int((1000 / h) * w), 1000))
            g.img = ImageTk.PhotoImage(g.imraw)
            g.pages.create_image(780, 500, image=g.img, tags='img')

            g.pageDisplay.delete(1.0, 'end')
            g.pageDisplay.insert(1.0, str(g.page) + '/' + str(len(os.listdir('D:/Books/' + manga + '/' + issue + '/')) - 1), 'center')
    except Exception as e:
        print(e)

def last(manga, issue, event=None):
    try:
        if g.page > 1:
            g.page -= 1
            g.pages.delete('img')
            g.imraw = Image.open('D:/Books/' + manga + '/' + issue + '/' + str(g.page) + '.jpg')
            w, h = g.imraw.size
            if int((1000 / h) * w) > 1560:
                g.imraw = g.imraw.resize((1560, int((1560 / w) * h)))
            else:
                g.imraw = g.imraw.resize((int((1000 / h) * w), 1000))
            g.img = ImageTk.PhotoImage(g.imraw)
            g.pages.create_image(780, 500, image=g.img, tags='img')

            g.pageDisplay.delete(1.0, 'end')
            g.pageDisplay.insert(1.0, str(g.page) + '/' + str(len(os.listdir('D:/Books/' + manga + '/' + issue + '/')) - 1), 'center')
    except Exception as e:
        print(e)


def back(manga, event=None):
    for slave in app.grid_slaves():
        slave.destroy()
    openManga(manga)


def read(manga, issue, lastPage, event=None):
    for slave in app.grid_slaves():
        slave.destroy()
    f = open('D:/Books/' + manga + '/' + issue + '/Done.txt', 'r')
    if f.read() == 'Read':
        file = open('D:/Books/' + manga + '/' + issue + '/Done.txt', 'w')
        file.write('')
        file.close()
    else:
        file = open('D:/Books/' + manga + '/' + issue + '/Done.txt', 'w')
        file.write('Read')
        file.close()
    f.close()
    openIssue(manga, issue, lastPage)


def openIssue(manga, issue, lastPage = 1):
    g.page = lastPage
    for slave in app.grid_slaves():
        slave.destroy()

    but = tk.Button(app, text='Back', fg='red', command=lambda manga=manga: back(manga))
    but.configure(width=25, height=2)
    but.grid(row=1, column=0, sticky='sw')
    f = open('D:/Books/' + manga + '/' + issue + '/Done.txt', 'r')
    if f.read() == 'Read':
        but = tk.Button(app, text='Mark as Unread', fg='green', command=lambda manga=manga, issue=issue: read(manga, issue, g.page))
    else:
        but = tk.Button(app, text='Mark as Read', fg='green', command=lambda manga=manga, issue=issue: read(manga, issue, g.page))
    f.close()
    but.configure(width=25, height=2)
    but.grid(row=1, column=2, sticky='se')
    but = tk.Button(app, text='<-', command=lambda manga=manga, issue=issue: last(manga=manga, issue=issue))
    but.configure(width=25, height=2)
    but.grid(row=0, column=0, sticky='w')
    but = tk.Button(app, text='->', command=lambda manga=manga, issue=issue: next(manga, issue))
    but.configure(width=25, height=2)
    but.grid(row=0, column=2, sticky='e')

    app.bind('<Right>', lambda event, manga=manga, issue=issue: next(manga=manga, issue=issue))
    app.bind('d', lambda event, manga=manga, issue=issue: next(manga=manga, issue=issue))
    app.bind('<Left>', lambda event, manga=manga, issue=issue: last(manga=manga, issue=issue))
    app.bind('a', lambda event, manga=manga, issue=issue: last(manga=manga, issue=issue))
    app.bind('<Escape>', lambda event, manga=manga: back(manga=manga))
    app.bind('r', lambda event, manga=manga, issue=issue: read(manga=manga, issue=issue, lastPage=g.page))

    g.pages = tk.Canvas(app, bg='black', width=1560, height=1000)
    g.imraw = Image.open('D:/Books/' + manga + '/' + issue + '/' + str(g.page) + '.jpg')
    w, h = g.imraw.size
    if int((1000 / h) * w) > 1560:
        g.imraw = g.imraw.resize((1560, int((1560 / w) * h)))
    else:
        g.imraw = g.imraw.resize((int((1000 / h) * w), 1000))
    g.img = ImageTk.PhotoImage(g.imraw)
    g.pages.create_image(780, 500, image=g.img, tags='img')
    g.pages.grid(row=0, column=1)

    g.pageDisplay = tk.Text(app, width=25, height=2)
    g.pageDisplay.grid(row=1, column=1)
    g.pageDisplay.tag_configure('center', justify='center')
    g.pageDisplay.tag_add('center', 1.0, 'end')
    g.pageDisplay.insert(1.0, str(g.page) + '/' + str(len(os.listdir('D:/Books/' + manga + '/' + issue + '/')) - 1), 'center')


def openManga(manga):
    app.unbind('<Right>')
    app.unbind('<Left>')
    app.unbind('a')
    app.unbind('d')
    app.unbind('r')
    try:
        for slave in app.grid_slaves():
            slave.destroy()
    except:
        pass
    col = 0
    line = 0
    folders = os.listdir('D:/Books/' + manga)
    if 'Done.txt' in folders:
        folders.remove('Done.txt')
    folders = sorted(folders, key=lambda x: float(x.split(' ')[len(x.split(' ')) -1]))

    canvas = tk.Canvas(app, bg='black', width=1900, height=1080)
    canvas.grid(row=0, column=0)
    scroll_y = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll_y.set)
    doneBook = True

    for folder in folders:
        if os.path.isfile('D:/Books/' + manga + '/' + folder + '/Done.txt'):
            f = open('D:/Books/' + manga + '/' + folder + '/Done.txt', 'r')
            if f.read() == 'Read':
                but = tk.Button(app, wraplength=190, text=folder, bg='green', command=lambda folder=folder, manga=manga: openIssue(manga, folder))
            else:
                but = tk.Button(app, wraplength=190, text=folder, command=lambda folder=folder, manga=manga: openIssue(manga, folder))
                doneBook = False
            f.close()
        else:
            but = tk.Button(app, wraplength=190, text=folder, bg='red')
        but.configure(width=25, height=2)
        canvas.create_window(190*col, 40*line, anchor='nw', window=but)
        col += 1
        if col >= 10:
            col = 0
            line += 1
    f = open('D:/Books/' + manga + '/Done.txt', 'w+')
    if doneBook:
        f.write('Read')
    else:
        f.write('')
    f.close()
    but = tk.Button(app, text='Back', fg='red', command=lambda: mainMenu())
    app.bind('<Escape>', lambda event: mainMenu())
    but.configure(width=25, height=2)
    canvas.create_window(1710, 40*(line+1), anchor='nw', window=but)
    canvas.configure(scrollregion=canvas.bbox("all"))


def mainMenu(event=None):
    for slave in app.grid_slaves():
        slave.destroy()

    col = 0
    line = 0

    canvas = tk.Canvas(app, bg='black', width=1900, height=1080)
    canvas.grid(row=0, column=0)
    scroll_y = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll_y.set)

    for folder in os.listdir('D:/Books/'):
        if folder != 'desktop.ini':
            if os.path.isfile('D:/Books/' + folder + '/Done.txt'):
                f = open('D:/Books/' + folder + '/Done.txt', 'r')
                if f.read() == 'Read':
                    but = tk.Button(app, wraplength=180, text=folder, bg='green', command=lambda folder=folder: openManga(folder))
                else:
                    but = tk.Button(app, wraplength=180, text=folder, command=lambda folder=folder: openManga(folder))
                f.close()
            else:
                but = tk.Button(app, wraplength=180, text=folder, bg='red')
            but.configure(width=25, height=2)
            canvas.create_window(190 * col, 40 * line, anchor='nw', window=but)
            col += 1
            if col >= 10:
                col = 0
                line += 1
    but = tk.Button(app, text='Quit', fg='red', command=lambda: app.destroy())
    app.bind('<Escape>', lambda event: app.destroy())
    but.configure(width=25, height=2)
    canvas.create_window(1710, 40 * (line + 1), anchor='nw', window=but)
    canvas.configure(scrollregion=canvas.bbox("all"))


mainMenu()
app.mainloop()
