To run the PokéDex Application through your database please do as following:



Before doing stp 1-4, it could be a good idea to setup a virtual enviroment for using this.
We had some problems running the on Mac without the venv.

(1)
Make sure that the path to the .csv is correct - From init.sql be aware that the data from the .csv
are retrieved by this:

FROM '/Users/mads/Desktop/Datalogi/DIS/PokeTest/generation1_pokemon.csv'

Make sure that the path to the .csv is changed accordingly to your device with the complete path.

(2)
Next a database has to be created - Please do so via the postgresql as this is how we setup the app.
The database name is up to the user, however make sure that in app.py:

    dbname="todo",
    user="mads",           
    host="localhost",
    port="5432"

The above should me changed accordingly to the users setup ie. dbname = "TADB" etc. The host and port should 
remain as default.

(3)
To initialize your database with the data we need to use for the PokéDex run the following command:
psql -d <YOUR DB NAME> -f init.sql 
This will create tables with data corresponding to the .csv in your database.

(4)
To run the application use this command: python app.py.

Doing the above will result in : 

    * Serving Flask app 'app'
    * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 120-890-013

To acces the app please input this: http://127.0.0.1:5000 in your browser (mostly tested on chrome)
