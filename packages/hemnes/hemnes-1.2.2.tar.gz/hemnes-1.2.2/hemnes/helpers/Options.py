class Options:
    """Class for organizing extra parameters."""

    def __init__(self):
        """Default constructor for Options - sets fields to default values."""
        self.__cdriver_path = None
        self.__csv_dump = None
        self.__json_dump = None
        self.__keywords = None
        self.__log = False
        self.__num_results = None
        self.__sleep_time = 3
        self.__strict = False        
        self.__tag = None
        
    @property
    def cdriver_path(self):
        return self.__cdriver_path

    @cdriver_path.setter
    def cdriver_path(self, path):
        if not isinstance(path, (str)):
            raise ValueError('Options.cdriver_path must be of type (str)')
        self.__cdriver_path = path

    @property
    def csv_dump(self):
        return self.__csv_dump

    @csv_dump.setter
    def csv_dump(self, path):
        if not isinstance(path, (str)):
            raise ValueError('Options.csv_dump must be of type (str)')
        self.__csv_dump = path

    @property
    def json_dump(self):
        return self.__json_dump

    @json_dump.setter
    def json_dump(self, json_dump):
        if not isinstance(json_dump, (str)):
            raise ValueError('Options.json_dump must be of type (str)')
        self.__json_dump = json_dump

    @property
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, keywords):
        if not isinstance(keywords, (set)):
            raise ValueError('Options.keywords must be of type (set)')
        self.__keywords = keywords

    @property
    def log(self):
        return self.__log

    @log.setter
    def log(self, log):
        if not isinstance(log, (bool)):
            raise ValueError('Options.log must be of type (set)')
        self.__log = log

    @property
    def num_results(self):
        return self.__num_results

    @num_results.setter
    def num_results(self, num):
        if not isinstance(num, (int)):
            raise ValueError('Options.num_results must be of type (int)')
        self.__num_results = num

    @property
    def sleep_time(self):
        return self.__sleep_time

    @sleep_time.setter
    def sleep_time(self, time):
        if not isinstance(time, (int)):
            raise ValueError('Options.sleep_time must be of type (int)')
        if time < 0:
            self.__sleep_time = 0
        else:
            self.__sleep_time = time

    @property
    def strict(self):
        return self.__strict

    @strict.setter
    def strict(self, strict):
        if not isinstance(strict, (bool)):
            raise ValueError('Options.strict must be of type (bool)')
        self.__strict = strict

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, tag):
        if not isinstance(tag, (str)):
            raise ValueError('Options.tag must be of type (str)')
        self.__tag = tag


