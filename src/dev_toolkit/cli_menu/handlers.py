from .routing import DevTool

@DevTool('/devtoolkit/tsilang~sil2csv')
def _handle_sil2csv() -> str:
    return ''

@DevTool('/devtoolkit/tsilang~csv2sil')
def _handle_csv2sil() -> str:
    return ''