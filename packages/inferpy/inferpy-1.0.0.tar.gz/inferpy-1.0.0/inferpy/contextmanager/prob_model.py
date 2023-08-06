import functools

# NOTE: This context might be deprecated. Right now, the is_probmodel_building context
# var is not used. Check if this context must be removed in the following days...

# global variable to know if the prob model is being built or not
is_probmodel_building = False


def build_model(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        global is_probmodel_building
        try:
            is_probmodel_building = True
            return f(*args, **kwargs)
        finally:
            is_probmodel_building = False
    return wrapper
