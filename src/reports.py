from functools import wraps


def write_reports(filename=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            file_to_write = filename if filename is not None else "doc_for_reports.txt"
            try:
                result = func(*args, **kwargs)
                with open(file_to_write, "a+", encoding="utf-8") as f:
                    f.write(str(result) + "\n")

            except Exception as e:
                with open(file_to_write, "a+", encoding="utf-8") as f:
                    f.write(f"Произошла ошибка: {str(e)}\n")
                raise
        return inner
    return wrapper

