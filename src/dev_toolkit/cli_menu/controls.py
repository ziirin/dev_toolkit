from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.layout.controls import FormattedTextControl

class CustomRadioList(RadioList):
    def __init__(self, values, default = None):
        super().__init__(values, default)
        self.open_char = ''
        self.close_char = ''
        self.selected_char = '→'
        self.unselected_char = ' '
        
        kb = KeyBindings()
        
        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)
            
        @kb.add('down')
        def _(event):
            self._selected_index = min(len(self.values) - 1, self._selected_index + 1)
            
        @kb.add('right')
        @kb.add('enter')
        def _(event):
            current_value = self.values[self._selected_index][0]
            event.app.exit(result=current_value)
        
        @kb.add('left')
        @kb.add('escape', eager=True)
        def _(event):
            event.app.exit(result=None)
        
        self.control.key_bindings = merge_key_bindings([self.control.key_bindings, kb])
        
        if hasattr(self, 'control') and isinstance(self.control, FormattedTextControl):
            self.control.show_cursor = False
            
        
    def _get_text_fragments(self):
        result = []
        for i, (_, label) in enumerate(self.values):
            selected = (i == self._selected_index)
            
            style = 'class:radio-button'
            if i == self._selected_index:
                style += '.selected'
                
            result.append((style, self.open_char))
            if selected:
                result.append((style, self.selected_char))
            else:
                result.append((style, self.unselected_char))
            result.append((style, self.close_char))
            
            result.append(('', ' '))
            result.append(('', str(label)))
            result.append(('', '\n'))
        
        result.pop()
        return result
    