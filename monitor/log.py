from pygtail import Pygtail

from monitor.config import Config


class Log:

    def __init__(self):
        config = Config()
        self.logfile = config.get_log_file()


    # TODO: use regex
    def get_latest_logs(self):
        results = []
        for log_line in Pygtail(self.logfile, read_from_end=True):
            if "eligible for farming" in log_line:
                splitsville = log_line.split(" ")
                plots_loc = splitsville.index("plots") - 1
                proof_loc = splitsville.index("proofs.") - 1
                time_loc = splitsville.index("Time:") + 1
                results.append({"time": splitsville[0], "partials":splitsville[plots_loc], "proofs":splitsville[proof_loc], "latency":splitsville[time_loc] })
        return results

