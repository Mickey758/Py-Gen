from flask import Flask,render_template,request,Markup,session
from os import listdir
from random import choice
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "RandomKey" # Change this to a random value that is not easy to guess
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=5) # Rate limiter (The ammount of time a user has to wait before generating another account)

@app.route("/")
def mainpage():
    gens = "" # Make a string for the gens
    for gen in listdir("Accounts"):
        name = gen.lower().replace(".txt","")
        gens += f'<option value="{name}">{name.title()}</option>\n' # Add the gens to the string in html format
    return render_template("index.html",gens=Markup(gens)) # Return the index.html file and the gens

@app.route("/gen")
def get_account():
    if "waiting" in session:
        return "Generating too fast",429 # Return rate limiting text
    gens = [] # Make an array for the list of gens
    for gen in listdir("Accounts"):
        gens.append(gen.lower().replace(".txt","")) # Add the list of gens to the array
    try:
        gen_name = request.args["name"].lower() # Get the account type argument
        if gen_name not in gens:
            return f"An error occured: Gen not found!",404 # Return gen not found error
        else:
            with open(f"Accounts/{gen_name}.txt") as f:
                accounts = f.read().splitlines() # Get the list of accounts as an array
            if len(accounts) == 0:
                return "Out of stock",202 #Return out of stock
            account = choice(accounts) # Get an account from the accounts to give
            new = "" # Make a string for the new accounts
            for line in accounts: # Add the lines except the account to the new stock string
                if line != account:
                    new += f"{line}\n"
            with open(f"Accounts/{gen_name}.txt","w") as f:
                f.write(new) # Write the new stock to the file
            session["waiting"] = "true" # Make a session (acting like a rate limiter (limit the ammount of accounts you can generate in a period of time))
            return account # Return the account
    except Exception as e:
        return f"An error occured: {str(e)}",400 # Return an error

@app.route("/stock")
def get_stock():
    gens = [] #Make an array
    for gen in listdir("Accounts"):
        gens.append(gen.lower().replace(".txt","")) # Add the account types to the array
    try:
        gen_name = request.args["name"].lower() # Get the account type argument
        if gen_name not in gens:
            return f"An error occured: Gen not found!",404 # Return an error code
        else:
            with open(f"Accounts/{gen_name}.txt") as f:
                stock = len(f.read().splitlines()) # Get the stock ammount
            if stock == 0:
                return str(stock),202 # Return no stock
            return str(stock) # Return stock ammount
    except Exception as e:
        return f"An error occured: {str(e)}",400 # Return an error

app.run("0.0.0.0",80) # Run the server (ip,port)