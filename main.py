from flask import Flask,render_template,request,Markup,session
from os import listdir
from random import choice
from threading import Lock, Thread
from random import randbytes
from time import time,sleep

db_lock = Lock()

app = Flask(__name__)
app.secret_key = randbytes(128).hex()

def get_gens() -> list:
    return [gen.lower().replace(".txt","") for gen in listdir("Accounts")]

def get_ip(request) -> str:
    isCloudflare = request.headers.get('Cf-Connecting-Ip')
    ip = request.remote_addr if not isCloudflare else isCloudflare
    
    return ip

Cooldowns = {} # Array for managing cooldowns
def cooldown_manager():
    while True: # Remove all the ips in the cooldown array if they have expired
        for ip in Cooldowns.copy():
            if Cooldowns[ip] < time():
                Cooldowns.pop(ip)
        
        sleep(0.1) # Have a small delay
Thread(target=cooldown_manager,daemon=True).start() # Start the cooldown_manager thread

@app.route("/")
def mainpage():
    return render_template("index.html",gens=get_gens()) # Display the index.html file and the gens

@app.route("/gen")
def get_account():
    ip = get_ip(request) # Get the user's ip
    if ip in Cooldowns:
        return "Generating too fast",429 # Return rate limiting text
    
    gens = get_gens() # Get the list of gens
    gen_name = request.args.get('name','').lower() # Get the account type argument
    if gen_name not in gens:
        return f"An error occured: Gen not found!",404 # Return gen not found error
    
    with db_lock: # Lock the db to prevent errors
        with open(f"Accounts/{gen_name}.txt",errors='ignore') as f:
            accounts = f.read().splitlines() # Get the list of accounts in the databse
        if not accounts:
            return "Out of stock",202 # Return out of stock error
        account = choice(accounts) # Get an account from the accounts to give
        new = [combo for combo in accounts if combo != account] # Remove the account from the database
        with open(f"Accounts/{gen_name}.txt","w",errors='ignore') as f:
            f.write('\n'.join(new)) # Write the new stock to the file
    
    Cooldowns[ip] = time()+5
    return account # Return the account

@app.route("/stock")
def get_stock():
    gens = get_gens() # Get the list of gens
    gen_name = request.args.get('name','').lower() # Get the account type argument
    if gen_name not in gens:
        return f"An error occured: Gen not found!",404 # Return an error code
    
    with db_lock: # Lock the db to prevent errors
        with open(f"Accounts/{gen_name}.txt",errors='ignore') as f:
            stock = len(f.read().splitlines()) # Get the stock ammount
    if not stock:
        return '0',202 # Return no stock
    
    return str(stock) # Return stock ammount

app.run("0.0.0.0",80) # Run the server (ip,port)