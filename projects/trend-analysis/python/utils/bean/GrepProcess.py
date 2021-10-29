class GrepProcess:
    def __init__(self):
        self._user = None
        self._pid = None
        self._cpu = None
        self._mem = None
        self._vsz = None
        self._rss = None
        self._tty = None
        self._stat = None
        self._start = None
        self._time = None
        self._commands = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        self._pid = value

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, value):
        self._cpu = value

    @property
    def mem(self):
        return self._mem

    @mem.setter
    def mem(self, value):
        self._mem = value

    @property
    def vsz(self):
        return self._vsz

    @vsz.setter
    def vsz(self, value):
        self._vsz = value

    @property
    def rss(self):
        return self._rss

    @rss.setter
    def rss(self, value):
        self._rss = value

    @property
    def tty(self):
        return self._tty

    @tty.setter
    def tty(self, value):
        self._tty = value

    @property
    def stat(self):
        return self._stat

    @stat.setter
    def stat(self, value):
        self._stat = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, value):
        self._commands = value

    def __str__(self):
        return " ".join([self.user, self.pid, self.cpu, self.mem, self.vsz, self.rss, self.tty, self.stat, self.start,
                         self.time, " ".join(self._commands)])