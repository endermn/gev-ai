from functools import wraps

# import logging
# from services.logger import GevaiLogger

# logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()

# -- INFO logging doesnt work for some reason, needs to be debug


def tools(func):
    print("In decorator")
    @wraps(func)
    def wrapp(self, *args, **kwargs):
        # logger.info("In wrapper")
        # logger.info(f"Tool '{func.__name__}' called with args: {args}, kwargs: {kwargs}")
        result = func(self, *args, **kwargs)
        # logger.info(f"Tool '{func.__name__}' returned: {result}")
        return result
    return wrapp
