
from application import app,manager
from flask_script import Server
import www
from  jobs.launcher import runJob

##web server
manager.add_command( "runserver", Server( host='192.168.137.1',port=app.config['SERVER_PORT'],use_debugger = True ,use_reloader = True) )

#job entrance
manager.add_command('runjob', runJob() )

def main():
    manager.run()

if __name__ == '__main__':
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()
