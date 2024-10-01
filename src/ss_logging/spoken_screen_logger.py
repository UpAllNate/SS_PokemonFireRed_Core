from src.ss_logging.project_logger import (
    ProjectLogger,
    standard_stream_format_string,
    standard_file_format_string,
    LOW_DEBUG,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    color_text,
    LogColor,
    LogAttr,
    StandardColoring as sc
)

from pathlib import Path

# Get the directory to the spoken screen repo
current_file_path = Path(__file__)
spoken_screen_dir = current_file_path.parent.parent.parent

# Create the logs directory if it doesn't already
logs_dir = spoken_screen_dir / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

class logger:

    op = ProjectLogger(
        stream_log_enable= True,
        file_log_enable= True,

        stream_logger_name= "ss_op_s",
        stream_log_level= ERROR,

        file_logger_name= "ss_op_f",
        file_log_level= LOW_DEBUG,
        file_path= logs_dir / "log_operations.log",
        file_max_size= 10 * 1024 * 1024,
        file_backup_count= 0
    )

    ui = ProjectLogger(
        stream_log_enable= True,
        stream_logger_name= "ss_ui_s",
        stream_log_level= LOW_DEBUG
    )

if __name__ == "__main__":

    dino_color = lambda text : color_text(text, color= LogColor.LIGHT_MAGENTA, attrs= LogAttr.UNDERLINE)

    logger.ui.info(message= f"This is a {color_text('test', color= LogColor.GREEN, attrs= [LogAttr.BOLD])}")
    logger.ui.info(sc.success("Success"))
    logger.ui.error(message= f"Something is wrong now!!")
    logger.ui.warning(message= f"Uh oh! {sc.num(4)} dinosaurs got out! Catch the {dino_color('stegosauraus')}!")
    logger.op.debug("Test")
    logger.op.critical(f"Big {sc.failure('PROBLEM')}")
