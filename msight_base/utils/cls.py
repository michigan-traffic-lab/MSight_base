def get_class_path(cls):
    module = cls.__module__
    class_name = cls.__name__
    return f"{module}.{class_name}"

def import_class_from_path(path: str):
    module_path, class_name = path.rsplit('.', 1)
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)