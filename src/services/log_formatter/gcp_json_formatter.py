"""GCP Log Formatter"""
from pythonjsonlogger import jsonlogger


class GCPJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter for Google Cloud structured logging.
    Adds severity and contextual fields to each log record.
    """
    def add_fields(self, log_record, record, message_dict):
        """_summary_

        Args:
            log_record (_type_): _description_
            record (_type_): _description_
            message_dict (_type_): _description_
        """
        super().add_fields(log_record, record, message_dict)
        log_record['severity'] = record.levelname
        log_record['logger'] = record.name
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno
