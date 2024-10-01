from .termcolor_files import color_text, LogColor, LogAttr
import logging
from logging.handlers import RotatingFileHandler
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET
import re
import datetime
from pathlib import Path

LOW_DEBUG = 5
logging.addLevelName(LOW_DEBUG, "LODEBUG")

# Utility to strip ANSI codes
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors only to the log level name and numbers in the message."""

    last_log_time = None  # static variable to keep track of the last log time

    def __init__(self, fmt=None, datefmt='%H:%M:%S', style='%'):
        super().__init__(fmt, datefmt, style)

    def formatTime(self, record, datefmt=None):
        ct = datetime.datetime.fromtimestamp(record.created)
        formatted_time = ct.strftime(self.datefmt)

        # Determine the color based on the time difference
        current_time = datetime.datetime.now()
        if ColorFormatter.last_log_time:
            elapsed_time = (current_time - ColorFormatter.last_log_time).total_seconds()
        else:
            elapsed_time = 0  # Default color for the first log

        # Update the last log time
        ColorFormatter.last_log_time = current_time

        # Decide the color based on elapsed time
        if elapsed_time < 3:
            color = LogColor.WHITE
        elif elapsed_time < 30:
            color = LogColor.LIGHT_MAGENTA
        else:
            color = LogColor.RED

        # Apply the color to the timestamp
        colored_time = color_text(formatted_time, color=color)
        return colored_time

    def format(self, record):
        new_record = logging.makeLogRecord(record.__dict__)
        new_record.levelname = f"{new_record.levelname:->7}"
        if len(new_record.levelname) > 7:
            new_record.levelname = new_record.levelname[:7]

        # Apply color to level names (assuming the mappings are correctly set)
        color_map = {
            LOW_DEBUG: LogColor.WHITE,
            logging.DEBUG: LogColor.LIGHT_CYAN,
            logging.INFO: LogColor.GREEN,
            logging.WARNING: LogColor.YELLOW,
            logging.ERROR: LogColor.RED,
            logging.CRITICAL: LogColor.RED
        }
        new_record.levelname = color_text(new_record.levelname, color=color_map.get(new_record.levelno, LogColor.WHITE))

        return super().format(new_record)

class CleanFormatter(logging.Formatter):
    """Formatter that removes ANSI color codes for file logging."""
    def format(self, record):
        record.msg = strip_ansi_codes(record.msg)
        return super().format(record)

standard_file_format_string = '[%(asctime)s] [%(levelname)s] [%(name)s {%(module)s:%(lineno)d}] %(message)s'
standard_stream_format_string = '%(levelname)s %(asctime)s: %(message)s'

class ProjectLogger:

    def __init__(self,
        stream_log_enable = False,
        file_log_enable = False,
        file_logger_name : str = "file_log",
        file_log_level : int = DEBUG,
        file_path : Path = Path("log.log"),
        file_max_size : int = 10 * 1024, # 10kB
        file_backup_count : int = 0,
        stream_logger_name : str = "stream_log",
        stream_log_level : int = INFO,
        file_log_format_string : str = standard_file_format_string,
        stream_log_format_string : str = standard_stream_format_string
    ) -> None:

        self.stream = stream_log_enable
        self.file = file_log_enable

        if self.file:

            if file_path.suffix != ".log":
                file_path = file_path.with_suffix(".log")

            # Setup loggers and handlers
            self.file_logger = logging.getLogger(file_logger_name)
            self.file_logger.setLevel(file_log_level)
            self.file_handler = RotatingFileHandler(file_path, maxBytes=file_max_size, backupCount=file_backup_count)
            self.clean_formatter = CleanFormatter(file_log_format_string)

            self.file_handler.setFormatter(self.clean_formatter)
            self.file_logger.addHandler(self.file_handler)

        if self.stream:
            self.stream_logger = logging.getLogger(stream_logger_name)
            self.stream_logger.setLevel(stream_log_level)

            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(ColorFormatter(stream_log_format_string))
            self.stream_logger.addHandler(self.console_handler)

    def log(
        self,
        level : int,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ) -> None:
        
        file_text = '\n'.join(
            part.strip() for part in [
                file_text_header,
                message,
                file_text_footer
            ] if part is not None
        )

        if self.stream and message is not None:
            self.stream_logger.log(level, message, stacklevel=2)
        
        if self.file:
            self.file_logger.log(level, file_text, stacklevel=2)
    
    def low_debug(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= LOW_DEBUG,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )

    def debug(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= logging.DEBUG,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )
    
    def info(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= logging.INFO,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )

    def warning(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= logging.WARNING,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )
    
    def error(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= logging.ERROR,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )
    
    def critical(
        self,
        message : str,
        file_text_header : str = None,
        file_text_footer : str = None
    ):
        
        self.log(
            level= logging.CRITICAL,
            message= message,
            file_text_header= file_text_header,
            file_text_footer= file_text_footer
        )

class StandardColoring:
    
    @staticmethod
    def num(text : str) -> str:
        return color_text(text, color= LogColor.LIGHT_BLUE, on_color= None, attrs= [])
    
    @staticmethod
    def object(text : str) -> str:
        return color_text(text, color= LogColor.GREEN, on_color= None, attrs= [])
    
    @staticmethod
    def state(text : str) -> str:
        return color_text(text, color= LogColor.MAGENTA, on_color= None, attrs= [])
    
    @staticmethod
    def success(text : str) -> str:
        return color_text(text, color= LogColor.BLACK, on_color= LogColor.GREEN, attrs= [])
    
    @staticmethod
    def failure(text : str) -> str:
        return color_text(text, color= LogColor.WHITE, on_color= LogColor.RED, attrs= [LogAttr.BOLD])

if __name__ == "__main__":

    test_logger = ProjectLogger(stream_log_enable= True, file_log_enable= True)
    sc = StandardColoring

    msg = f"This is a test of the {sc.failure('emergency broadcast system')}"
    test_logger.log(level=INFO, message=msg, file_text_header="This is indeed very important info.")
    test_logger.log(level=DEBUG, message="This is a console message", file_text_header="This is a file message")
    test_logger.log(level=LOW_DEBUG, message="This is for file eyes only")
    test_logger.log(level=WARNING, message= None, file_text_header="Detailed warning information here.")
    test_logger.log(level=ERROR, message= "This is getting serious")
    test_logger.log(level=CRITICAL, message= "Oh... now it's serious...")
