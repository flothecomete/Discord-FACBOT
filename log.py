import os
import datetime

class Log():

    def __init__(self, filename) -> None:
        self.filename = "log/"+filename

    def close(self):
        os.rename(self.filename, self.filename.split(".")[0] + " - " + datetime.datetime.now().strftime('%Y%m%d.%H%M') + ".log.bak")

    def begin(self, message):
        with open(self.filename, "a") as f:
            f.write('\n***\t\t***\n')
            f.write(str(datetime.datetime.now()) + " " + message)

    def write(self, message):
        with open(self.filename, "a") as f:
            f.write(str(datetime.datetime.now()) + " " + message)
        