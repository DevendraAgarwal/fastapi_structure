"""UtilityHelper Class with Some Useful Common Functions"""

import json
import traceback
from datetime import datetime


class UtilityHelper:
    """UtilityHelper Class with Some Useful Common Functions"""

    @staticmethod
    def get_current_timestamp():
        """Function to Return Current Timestamp

        Returns:
            string: current timestamp
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convert_exception_to_json(exception: Exception):
        """_summary_

        Args:
            exception (_type_): Exception Need to Convert in JSON

        Returns:
            json: JSON Object
        """
        # Extract useful information
        exception_info = {
            "type": type(exception).__name__,
            "message": str(exception),
            "traceback": traceback.format_exc()
        }

        # Convert to JSON (to store in BigQuery as STRING or JSON column)
        return json.dumps(exception_info)
