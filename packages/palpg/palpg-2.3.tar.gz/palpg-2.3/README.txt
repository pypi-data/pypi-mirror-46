Wrapper Class around Psycopg2 for PostgreSQL
	In psycopg2 after connecting to the database, for every read execute statement the data needs to be fetched and for evey write execute statement the data needs to be committed. But this class eliminates these requirements and make it simple to read and write to the database.


Files:
	palpg/__init__.py


Installation:
	sudo pip3 install palpg


Usage Examples:
	import palpg
	
	db = palpg.db("host=HOST port=PORT dbname=DBNAME user=USER password=PASSWORD")  ##-connect to the database

	db.read("sql statement")  ##-returns the read data from database with flat=True

	db.read("select item from table", flat=False)  ##-returns the raw read data 
	
	db.read("select item from table where item = %s", (sub1,))  ##-read with string substitution
	
	db.read1("sql statement")  ##-returns the first read data similar to fetchone
	
	db.write("sql statement")  ##-writes the data and commits to the database
	
	db.clear()  #-to reconnect if any transaction error


For other psycopg connection commands use the connection class
	db.conn....
