# Notes:

## About `sqlite3.exe`:
- sqlite3 is used in order to run light sql queries on a .db file.
- More about the terminal command-line inputs: [https://www.sqlite.org/cli.html](url) 

# How to deploy to local machine and run application

## Depenedencies
1. Very firstly clone this repository into a directory of your own file.
2. Create a virtual environment for the application: python -m venv venv
3. Activate your virtual environemnt (Linux/Mac)`source venv/bin/activate` (Windows)`venv\Scripts\activate`
3. Run `pip install -r requirements.txt`
4. `flask run` should start the application

## Database:
- If you clone this repository directly, you will be using `finance.db` with the data that has been loaded when the application was being developed and tested.
- Once you clone this repository delete the default `finance.db`.
- And run terminal with command `sqlite3 finance.db`. This will create an instance of a new database which you can use on your own machine.
