from python_aternos import Client
import tkinter as tk
from PIL import Image, ImageTk
import os
from mcstatus import JavaServer
import time

server = JavaServer.lookup("absolutewonderland.aternos.me:19578")  


root = tk.Tk()
root.title("Starter")
root.geometry("350x300")
root.resizable(False, False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE1PRERESIZE = os.path.join(SCRIPT_DIR, "aternosbutton1.png")
IMAGE2PRERESIZE = os.path.join(SCRIPT_DIR, "aternosbutton2.png")

IMAGE1 = ImageTk.PhotoImage(Image.open(IMAGE1PRERESIZE).resize((170, 73)))
IMAGE2 = ImageTk.PhotoImage(Image.open(IMAGE2PRERESIZE).resize((170, 73)))



# Create the client object
atclient = Client()

# Log in using your Aternos username and password
atclient.login("ItsmeCryo", "in20di18go-alt")

# Access your account and get your list of servers
aternos = atclient.account
servers = aternos.list_servers()

# Select your first server (or loop to find a specific IP)
wland = servers[0]

# Initialize variables
statusresult = None
status = None
countdown_seconds = 10

def update_timer():
    global countdown_seconds
    
    if countdown_seconds > 0:
        # Update text to show remaining time
        global counttext
        counttext = str(countdown_seconds) + " seconds..."
        button.config(text=f"Wait " + str(counttext))
        # Decrease time by 1 second
        countdown_seconds -= 1
        
        # Call this same function again in 1000ms (1 second)
        root.after(1000, update_timer)
    else:
        # Countdown finished, unlock the button and change image
        button.config(text="Ready", state=tk.NORMAL)
        global buttonunlocked
        buttonunlocked = True
        reload_and_update()

def get_server_status():
    global statusresult
    global status
    
    try:
        status = server.status()
        if status.players.online == 0:
            print(f"The server is offline or in standby, Please try to join soon, and if you can't, Try to start the server. ")
            
            statusresult = 2
        else: 
            print(f"The server is online with {status.players.online} players and a latency of {status.latency} ms.")
            statusresult = 1
    except Exception:
        print(f"The server is offline.")
        statusresult = 0
global buttonunlocked
buttonunlocked = False

def unlock_and_change():
    global statusresult
    global status
    # 1. Change to final image
    if statusresult == 0:
        button.config(image=IMAGE2)
        button.image = IMAGE2
        button.config(state=tk.NORMAL)
        button.config(text=f"The server is Offline.")  
    elif statusresult == 1:
        button.config(text=f"Server is online with {status.players.online} players, Please join!!", state=tk.DISABLED)
    else:
        button.config(state=tk.NORMAL)
        button.config(image=IMAGE2)
        button.image = IMAGE2
        button.config(text=f"The server is offline or in standby, Please try to join soon, and if you can't, Try to start the server.", state=tk.NORMAL)

def startup():
    wland.start()
    button.config(text="Starting server...", state=tk.DISABLED)

def reload_and_update():
    if buttonunlocked == False:
        print("Button is locked, waiting for countdown to finish...")
        return
    get_server_status()
    time.sleep(1.5)
    unlock_and_change()


button = tk.Button(root, image=IMAGE1, text="...", compound="top", state=tk.DISABLED, command=lambda: [startup()], width=170, wraplength=170, justify="center")
reloadstatus = tk.Button(root, text="↺", command=reload_and_update)
reloadstatus.pack(pady=10)
root.after(0, update_timer)
button.pack(pady=50)
root.mainloop()
