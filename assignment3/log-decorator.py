# Task 1.
import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        pos_args = args if args else "none"
        kw_args = kwargs if kwargs else "none"

        result = func(*args, **kwargs)

        log_message = (
            f"function: {func_name}\n"
            f"positional parameters: {pos_args}\n"
            f"keyword parameters: {kw_args}\n"
            f"return: {result}\n"
        )

        logger.log(logging.INFO, log_message)
        return result
    return wrapper

@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def return_true(*arg):
    return True

@logger_decorator
def keyword_only(**kwargs):
    return logger_decorator


if __name__ == "__main__":
    say_hello()
    return_true(1, 2, 3)
    keyword_only(name="Tatiana", project="Ada", level="junior")
