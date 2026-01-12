import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # from dify_plugin.config.logger_format import plugin_logger_handler
    # logger.addHandler(plugin_logger_handler)
    return logger
