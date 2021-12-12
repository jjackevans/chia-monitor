from pygtail import Pygtail


class Log:

    def __init__(self):
        # self.logfile = logfile
        self.logfile = "/root/.chia/mainnet/log/debug.log"

    def get_latest_logs(self):
        for log_line in Pygtail(self.logfile, read_from_end=True):
            print(log_line)


