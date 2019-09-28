from tkinter import *
import os, webbrowser, World_gen, data, sys
with open("options.txt", "r") as f:
    exec(f.read())

# Command line launcher bypass
if len(sys.argv) > 1:
    worlds = os.listdir("Worlds")
    if sys.argv[1] in worlds:
        import main
        main.main(sys.argv[1])
    else:
        print("World dosn't exist.")

class Window(Frame):
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    def init_window(self):     
        self.master.title("MineBlock 2D Launcher")
        img = PhotoImage(file=os.path.join("Texture Packs", "Default", "5.png"))
        self.master.tk.call('wm', 'iconphoto', root._w, img)
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        # create the file object
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="Game folder", command=self.game_folder)
        menu.add_cascade(label="File", menu=file)

        # create the options object
        options = Menu(menu)
        options.add_command(label="Options", command=O.start)
        options.add_command(label="Reset to defaults", command=O.reset)
        menu.add_cascade(label="Options", menu=options)

        # create the help object
        hel = Menu(menu)
        hel.add_command(label="Readme", command=self.readme)
        hel.add_command(label="Website", command=self.download)
        hel.add_command(label="Changelog", command=self.changelog)
        menu.add_cascade(label="Help", menu=hel)
        
        # New world button
        button = Button(self, text="New World", width=60, command=W.new_world)
        button.place(x=0, y=0)
        
        self.refresh()
        
    def refresh(self):
        worlds = os.listdir("Worlds")
        if len(worlds) >= 1:
            button = Button(self, text=worlds[0][0:-5], width=50, command=lambda: World.start_world(0))
            button.place(x=0, y=50)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(0))
            button.place(x=350, y=50)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=50)
            button = Button(self, width=6)
            button.place(x=350, y=50)
            
        if len(worlds) >= 2:
            button = Button(self, text=worlds[1][0:-5], width=50, command=lambda: World.start_world(1))
            button.place(x=0, y=80)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(1))
            button.place(x=350, y=80)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=80)
            button = Button(self, width=6)
            button.place(x=350, y=80)
            
        if len(worlds) >= 3:
            button = Button(self, text=worlds[2][0:-5], width=50, command=lambda: World.start_world(2))
            button.place(x=0, y=110)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(2))
            button.place(x=350, y=110)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=110)
            button = Button(self, width=6)
            button.place(x=350, y=110)
            
        if len(worlds) >= 4:
            button = Button(self, text=worlds[3][0:-5], width=50, command=lambda: World.start_world(3))
            button.place(x=0, y=140)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(3))
            button.place(x=350, y=140)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=140)
            button = Button(self, width=6)
            button.place(x=350, y=140)
            
        if len(worlds) >= 5:
            button = Button(self, text=worlds[4][0:-5], width=50, command=lambda: World.start_world(4))
            button.place(x=0, y=170)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(4))
            button.place(x=350, y=170)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=170)
            button = Button(self, width=6)
            button.place(x=350, y=170)
            
        if len(worlds) >= 6:
            button = Button(self, text=worlds[5][0:-5], width=50, command=lambda: World.start_world(5))
            button.place(x=0, y=200)
            button = Button(self, text="Delete", width=6, command=lambda: World.delete_world(5))
            button.place(x=350, y=200)
        else:
            button = Button(self, width=50)
            button.place(x=0, y=200)
            button = Button(self, width=6)
            button.place(x=350, y=200)
    def client_exit(self):
        exit()
    def game_folder(self):
        os.startfile(".")
    def readme(self):
        webbrowser.open("file://" + os.path.realpath("Readme.html"))
    def download(self):
        webbrowser.open("http://mineblock2d.ml/")
    def changelog(self):
        webbrowser.open("http://mineblock2d.ml/changelog.html")

class World():
    # Load world
    def start_world(n):
        global root
        root.destroy()
        worlds = os.listdir("Worlds")
        import main
        main.main(worlds[n])
        
        root = Tk()
        root.geometry("400x300")

        global app
        app = Window(root)
        root.mainloop()
                
    # Delete world
    def delete_world(n=None):
        worlds = os.listdir("Worlds")
        global WORLD
        WORLD = worlds[n][0:-5]
            
        W.root = Tk()
        W.root.title("Delete?")
        W.root.geometry("200x100")
        
        label = Label(W.root, text="Are you shure you want to delete \n" + WORLD)
        label.place(x=0, y=10)
        
        Button(W.root, text="Cancel", command=W.root.destroy).place(x=10, y=70)
        Button(W.root, text="Ok",command=W.rm).place(x=160, y=70)
        W.root.mainloop()
    def rm(self):
        W.root.destroy()
        path = os.path.join("Worlds", WORLD + ".json")
        os.remove(path)
        app.refresh()

    # New world
    def new_world(self):
        self.root = Tk()
        self.root.title("New World")
        self.root.geometry("300x100")
        self.root.bind("<Return>", W.create)
        label = Label(self.root, text="World Name")
        label.place(x=10, y=10)
        self.e = Entry(self.root)
        self.e.place(x=160, y=10)

        button = Button(self.root, text="Create", command=W.create)
        button.pack(side=BOTTOM)
        self.root.mainloop()
    def create(self, a=None):
        world = self.e.get() + ".json"
        worlds = os.listdir("Worlds")
        if world not in worlds and world != ".json":
            World_gen.main(world)
            self.root.destroy()
            app.refresh()
        else:
            label = Label(self.root, text="World allredy exists.")
            label.place(x=50, y=30)

class Options(Frame):
    def start(self):
        self.root = Tk()
        self.root.geometry("300x250")    
        self.root.title("MineBlock 2D Settings")

        button = Button(self.root, text="Apply", command=self.apply)
        button.pack(side=BOTTOM)
        
        label = Label(self.root, text="Screen width")
        label.place(x=10, y=10)
        self.width = Entry(self.root)
        self.width.place(x=160, y=10)
        self.width.insert(0, SCREEN_WIDTH)
        label = Label(self.root, text="Screen height")
        label.place(x=10, y=40)
        self.height = Entry(self.root)
        self.height.place(x=160, y=40)
        self.height.insert(0, SCREEN_HEIGHT)

        label = Label(self.root, text="Sky color (R, G, B)")
        label.place(x=10, y=80)
        self.sky = Entry(self.root)
        self.sky.place(x=160, y=80)
        self.sky.insert(0, str(SKY))
        
        label = Label(self.root, text="Skin filename")
        label.place(x=10, y=110)
        self.skin = Entry(self.root)
        self.skin.place(x=160, y=110)
        self.skin.insert(0, SKIN)
        label = Label(self.root, text="Texture pack folder")
        label.place(x=10, y=140)
        self.pack = Entry(self.root)
        self.pack.place(x=160, y=140)
        self.pack.insert(0, PACK)

        root.mainloop()

    def apply(self):
        with open("options.txt", "r") as f:
            opts = f.read().split("\n")
        for i, o in enumerate(opts):
            if len(o) != 0:
                if o.split()[0] == "SCREEN_HEIGHT":
                    opts[i] = "SCREEN_HEIGHT = " + self.height.get()
                if o.split()[0] == "SCREEN_WIDTH":
                    opts[i] = "SCREEN_WIDTH = " + self.width.get()

                if o.split()[0] == "SKY":
                    opts[i] = "SKY = " + self.sky.get()
                    
                if o.split()[0] == "SKIN":
                    opts[i] = 'SKIN = "' + self.skin.get() + '"'
                if o.split()[0] == "PACK":
                    opts[i] = 'PACK = "' + self.pack.get() + '"'
            with open("options.txt", "w") as f:
                f.write("\n".join(opts))

    def reset(self):
        O.root = Tk()
        O.root.title("Reset to defaults?")
        O.root.geometry("200x100")
        
        label = Label(O.root, text="Are you shure you want to reset all \noptions to defaults?")
        label.place(x=0, y=10)
        
        Button(O.root, text="Cancel", command=O.root.destroy).place(x=10, y=70)
        Button(O.root, text="Ok",command=O.reset_options).place(x=160, y=70)
        O.root.mainloop()

    def reset_options(self):
        O.root.destroy()
        with open("options.txt", "w") as f:
                f.write(data.options)
        
       
# Part of main window          
root = Tk()
root.geometry("400x300")

W = World()
O = Options()
app = Window(root)

root.mainloop()
