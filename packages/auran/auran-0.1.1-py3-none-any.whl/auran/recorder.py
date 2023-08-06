class LogEntry(object):
    def add(self, index, value):
        raise NotImplementedError("Implement this in subclasses")

    def process(self):
        pass

class Log(object):
    entry_factory = LogEntry

    def __init__(self, name):
        self.name = name
        self.entries = []

    def new_entry(self):
        return self.entry_factory()

    def append_new_entry(self, entry):
        self.entries += [entry.process()]

    def get_entries(self):
        return self.entries

class Recorder(object):
    def __init__(self, xp):
        self.logs = {}
        self.log_entries = None
        self.xp = xp

    def add_log(self, log):
        assert(log.name not in self.logs)
        self.logs[log.name] = log

    def start_new_log_entry(self):
#        print("start_new_log_entry")
        if self.log_entries != None:
            self.process_log_entries()
        self.log_entries = {}
        for log_name, log in self.logs.items():
            self.log_entries[log_name] = log.new_entry()

    def process_log_entries(self):
        for log_name, log_entry in self.log_entries.items():
            self.logs[log_name].append_new_entry(log_entry)

    def add(self, log_name, index, value):
        self.log_entries[log_name].add(index, value)

    def display(self):
        for log_name, log in self.logs.items():
#            print(log_name, log.get_entries())
            self.xp.add_display(-1, "recorder." + log_name, log.get_entries())




