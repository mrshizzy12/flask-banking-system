from app import create_app
from app import db
from app.models import User, Deposit, Interest, Withdrawal


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Deposit': Deposit,
        'Interest': Interest,
        'withdrawal': Withdrawal,
    }



'''
    --> uncomment the code below if you wish
    --> to use vs code debugger
'''
#if __name__ == '__main__':
    #app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)