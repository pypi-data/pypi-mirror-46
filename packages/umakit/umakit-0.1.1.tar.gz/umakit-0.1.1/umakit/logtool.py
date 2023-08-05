# -*- coding: utf-8 -*-

from datetime import datetime

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

class LogTool():
    
    def __init__(self, file=None, log=[], dtime={}, timelog=True):
        self.log = log
        self.file = file
        self.dtime = dtime
        self.timelog = timelog
    
    def _reset(self):
        self.log = []
        self.dtime = {}

    def _diff_dtime(self, index):
        if not self.dtime[index]:
            return None
        start, end = self.dtime[index]
        hours, minutes, seconds = convert_timedelta(end - start)
        return hours, minutes, seconds
    
    def add(self, message, timelog=False):
        if self.timelog or timelog:
            now = datetime.now()
            msg = "[{}] {}".format(
                    now.strftime('%Y-%m-%d %H:%M:%S'), message)
        self.log.append(msg)
        return msg
        
    def savepoint(self, index):
        now = datetime.now()
        if index in self.dtime:
            self.dtime[index].append(now)
        else:
            self.dtime[index] = [now]
        
        if len(self.dtime[index]) > 2:
            self.dtime[index].pop(0)        
        return now.strftime('%Y-%m-%d %H:%M:%S')
        
    def duration(self, index):
        hours, minutes, seconds = self._diff_dtime(index)
        return "{}:{}:{}".format(hours, minutes, seconds)

    def summary(self):
        msg = "\n".join(self.log)
        return msg

    def add_savepoint(self, message, index, timelog=False):
        msg = self.add(message, timelog=timelog)
        self.savepoint(index)
        return msg
    
    def add_duration(self, index):
        duration = self.duration(index)
        self.add("Duration: {}".format(duration))
        return duration
    
    def to_txt(self, path):
        content = self.summary()
        with open(path, "w") as file:
            file.write(content)