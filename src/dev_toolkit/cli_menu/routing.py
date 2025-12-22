BASE_PATH = '/devtoolkit'
MENU_ROUTING = {}

def DevTool(menu_path: str) -> any:
    def decorator(func: any) -> any:
        global MENU_ROUTING
        MENU_ROUTING[BASE_PATH + menu_path] = func
        return func
    return decorator