MENU_ROUTING = {}

def DevTool(menu_path: str) -> any:
    def decorator(func: any) -> any:
        global MENU_ROUTING
        MENU_ROUTING[menu_path] = func
        return func
    return decorator