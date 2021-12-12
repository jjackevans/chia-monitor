from pygtail import Pygtail


class Log:

    def __init__(self, logfile):
        self.logfile = logfile
        self.logfile = ""
        self.latest_timestamp = ""

    def get_latest_logs(self):
        for log_line in Pygtail(self._expanded_log_path, read_from_end=True):
            print(log_line)


