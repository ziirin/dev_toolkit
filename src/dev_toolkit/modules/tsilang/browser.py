import webbrowser

def open_url(url: str) -> bool:
    try:
        webbrowser.open(url)
    except:
        return False
    return True