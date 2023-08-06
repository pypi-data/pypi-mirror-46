import datetime
import os

class Logger:
    """Class to handle logging messages to console & to logfile"""

    def __init__(self, log_dir='hemnes-logs', log_to_console=True):
        """Default Logger constructor.

        The constructor will create the log_dir if it does not already exist

        Args:
            log_dir (str): path to logfile directory, defaults to hemnes-logs
        """
        self.__time = datetime.datetime.now().strftime('%m-%d-%H:%M:%S')
        self.__to_console = log_to_console
        self.__path = 'hemnes-%s.log' % (self.__time)
        self.__log_dir = log_dir
        if not os.path.exists(log_dir): os.mkdir(log_dir) # create the log dir
        self.__full_path = '%s/%s' % (self.__log_dir, self.__path)
        self.__logfile = open(self.__full_path, 'a+')

    def log(self, message, new_section=False):
        """Logs a message.

        Args:
            message (str): log message
            new_section (bool): True if the message starts a new section, False otherwise
        """
        if self.__to_console: print(message)
        section_div = '============================================\n'
        log_string = '%s\n' % (message) if not new_section else '%s%s%s' % (section_div, message, section_div)
        self.__logfile.write(log_string)

    def close(self):
        """Closes logfile and any other open resources."""
        if self.__to_console: print('see full logs at %s' % (self.__full_path))
        if not self.__logfile.closed: self.__logfile.close()
