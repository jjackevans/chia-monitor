from pygtail import Pygtail

from monitor.config import Config


class Log:

    def __init__(self):
        config = Config()
        # self.logfile = logfile
        self.logfile = config.get_log_file()

    def get_latest_logs(self):
        for log_line in Pygtail(self.logfile, read_from_end=True):
            print(type(log_line))

            if "eligible for farming":
                print(log_line)
                print("test")


