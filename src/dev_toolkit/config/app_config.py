# Defines if JSON file configuration has been already read
_IS_CONFIG_INITIALIZED = False

# This is the default configuration
# This configuration can be changed using config.json
APP_CONFIG = {
    'close_after_success': True,
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