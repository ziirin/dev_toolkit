APP_CONFIG = {
    'close_after_success': False,
    'close_after_err': False,
    'allowed_tools': [
        # Entrypoint
        '/devtoolkit',
        
        # devtoolkit > tsilang
        '/devtoolkit/tsilang',
        '/devtoolkit/tsilang/:sil2csv',
        '/devtoolkit/tsilang/:csv2sil',
        
        # devtoolkit > git
        # '/devtoolkit/git',
        
        # devtoolkit > :kill_rad
        # '/devtoolkit/:kill_rad',
        
        # devtoolkit > :icons_web
        # '/devtoolkit/:icons_web',
        
        # devtoolkit > settings
        # '/devtoolkit/settings'
    ]
}