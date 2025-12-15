from prompt_toolkit.styles import Style

# ========================================================================

ONE_ATOM_PALETTE = {
    'background': '#282c34',
    'normal_text': '#abb2bf',
    'cyan': '#56b6c2',
    'green': '#98c379',
    'yellow': '#e5c07b',
    'orange': '#d19a66',
    'red': '#e06c75',
    'blue': '#61afef',
    'purple': '#c678dd',
}

ONE_ATOM_THEME = Style.from_dict({
    # --- Console Styles (Global App) ---
    'dialog':                   f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["normal_text"]}',
    'dialog.body':              f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["normal_text"]}',
    # 'dialog.body focused':      f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["normal_text"]}',
    # 'dialog.body padding':      f'bg:{ONE_ATOM_PALETTE["background"]}',
    
    # --- General Prompt (User Input) ---
    # 'prompt':                   f'{ONE_ATOM_PALETTE["normal_text"]}',
    # 'prompt_symbol':            f'{ONE_ATOM_PALETTE["blue"]}',
    # 'prompt_continuation':      f'{ONE_ATOM_PALETTE["blue"]}',

    # # --- Autocompletion (Suggestion/Completion) ---
    # 'completion-menu':                      f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["normal_text"]}',
    # 'completion-menu.completion.current':   f'bg:{ONE_ATOM_PALETTE["blue"]} black',

    # # --- Information Messages / Titles ---
    'title':                  f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["blue"]} bold',
    'label':                  f'{ONE_ATOM_PALETTE["blue"]}',       # General labels
    'text-area':              f'{ONE_ATOM_PALETTE["background"]}',
    
    # # --- Buttons and Interactive Components ---
    'button':                 f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["blue"]}',
    'button.focused':         f'bg:{ONE_ATOM_PALETTE["blue"]} {ONE_ATOM_PALETTE["background"]} underline bold',
    'radiolist':              f'bg:{ONE_ATOM_PALETTE["background"]} {ONE_ATOM_PALETTE["normal_text"]}',
    'radiolist.selected':     f'{ONE_ATOM_PALETTE["yellow"]}',     # Selected radio option

    # --- Syntax Tokens (Example) ---
    # Useful if you use a lexer for code highlighting
    # 'pygments.keyword':       f'bold {ONE_ATOM_PALETTE["purple"]}',
    # 'pygments.name.function': f'{ONE_ATOM_PALETTE["blue"]}',
    # 'pygments.literal.string':f'{ONE_ATOM_PALETTE["green"]}',
    # 'pygments.number':        f'{ONE_ATOM_PALETTE["orange"]}',
    # 'pygments.comment':       f'italic {ONE_ATOM_PALETTE["normal_text"]}'
})