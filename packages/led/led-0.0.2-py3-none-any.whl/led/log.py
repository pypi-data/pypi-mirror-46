import json
import logging
import logging.config
import os
import sys

from led.constants import LED_LOG_CONFIG, LED_LOG_FILE, LED_LOG_LEVEL
from led.error import ExitCode


def get_logging_config(env_log_level='LED_LOG_LEVEL',
                       env_log_config='LED_LOG_CONFIG',
                       env_log_file='LED_LOG_FILE'):
    """Setup logging configuration."""
    value = os.getenv(env_log_config)
    if value:
        log_config_path = value
    else:
        log_config_path = LED_LOG_CONFIG

    try:
        with open(log_config_path, 'rt') as f:
            logging_config = json.load(f)
    except OSError as e:
        print(f"Failed to open led logging configuration file at "
              f"{log_config_path}\nExiting...\n\n")
        sys.exit(ExitCode.EX_NOINPUT)

    value = os.getenv(env_log_file)
    if value:
        led_log_file = value
    else:
        led_log_file = LED_LOG_FILE
    logging_config['handlers']['default_handler']['filename'] = led_log_file

    value = os.getenv(env_log_level)
    if value:
        led_log_level = value
    else:
        led_log_level = LED_LOG_LEVEL
    logging_config['loggers']['led']['level'] = led_log_level

    return logging_config


logging.config.dictConfig(get_logging_config())


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    return logger
