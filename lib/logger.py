import datetime, os


class write_log:
    def __init__(self, log_file: str = None) -> None:
        self.log_file = log_file

    def write(self, log_info: str) -> None:
        if self.log_file is not None:
            self.log_info = log_info
            self.time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            os.system(f"echo '{self.time}|{self.log_info}' >> {self.log_file}")
