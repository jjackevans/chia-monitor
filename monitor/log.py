from pygtail import Pygtail

from monitor.config import Config


class Log:

    def __init__(self):
        config = Config()
        # self.logfile = logfile
        self.logfile = config.get_log_file()

    def get_latest_logs(self):
        for log_line in Pygtail(self.logfile, read_from_end=True):
            if "eligible for farming" in log_line:
                splitsville = log_line.split(" ")
                plots_loc = splitsville.index("plots") - 1
                proof_loc = splitsville.index("proofs.") - 1
                time_loc = splitsville.index("Time:") + 1
                print(splitsville[plots_loc], splitsville[proof_loc], splitsville[time_loc])


