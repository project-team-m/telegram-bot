from datetime import datetime
from os import system


class Log:
    def __init__(self):
        self.log = 'log/log.txt'
        self.action_log = 'log/Actionlog.txt'
        self.error_log = 'log/Errorlog.txt'



    def write_actions_log(self, action):
        self.write_log(action)
        with open(self.action_log, 'a') as log:
            log.write('{}| Time at: {}\n'.format(str(action), datetime.now()))

    def write_error_log(self, error):
        self.write_log(error)
        with open(self.error_log, 'a') as log:
            log.write('{}| Error at: {}\n'.format(str(error), datetime.now()))

    def write_log(self, string):
        with open(self.log, 'a') as log:
            log.write('{}| Time at: {}\n'.format(str(string), datetime.now()))
