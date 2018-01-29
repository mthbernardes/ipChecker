# ipChecker
Check if a IP is from tor or is a malicious proxy 

# Install
<pre>
pip3 install -r dependecies.txt
</pre>

# Configure database Mongo
Edit the file db/db.py, remove the # from lines 7,8 and add a # on line 9
<pre>
7	        username,passwd,host,port = os.getenv('DATABASE_USERNAME'),os.getenv('DATABASE_PASSWORD'),os.getenv('DATABASE_HOST'),os.getenv('DATABASE_PORT')
8	        dalString  = 'mongodb://%s:%s@%s:%s/ipChecker' % (username,passwd,host,port) #uncomment to use mongodb
9	        #dalString  = 'sqlite://ipChecker.db'  #uncomment to use sqlite
</pre>
Set the system variables
DATABASE_USERNAME
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT

# Configure
<pre>
crontab -e
*/5 * * * * /project/path/updateNew.py
</pre>

# Run
hug -f index.py -p 8080
