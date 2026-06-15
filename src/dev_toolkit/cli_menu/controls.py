from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.data_structures import Point

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
            self._selected_index = (self._selected_index - 1) % len(self.values) # max(0, self._selected_index - 1)
            
        @kb.add('down')
        def _(event):
            self._selected_index = (self._selected_index + 1) % len(self.values) # min(len(self.values) - 1, self._selected_index + 1)
            
        @kb.add('right')
        @kb.add('enter')
        def _(event):
            current_value = self.values[self._selected_index][0]
            event.app.exit(result=current_value)
        
        @kb.add('left')
        @kb.add('escape', eager=True)
        def _(event):
            event.app.exit(result=None)
            
        @kb.add('1')
        @kb.add('2')
        @kb.add('3')
        @kb.add('4')
        @kb.add('5')
        @kb.add('6')
        @kb.add('7')
        @kb.add('8')
        @kb.add('9')
        def _(event):
            selected_num = int(event.key_sequence[-1].key)
            if selected_num < len(self.values):
                event.app.exit(result=self.values[selected_num - 1][0])
        
        self.control.key_bindings = merge_key_bindings([self.control.key_bindings, kb])
        
        if hasattr(self, 'control') and isinstance(self.control, FormattedTextControl):
            self.control.show_cursor = False
            
        self.control.get_cursor_position = self._get_cursor_position
            
        
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
    
    def is_focusable(self) -> bool:
        return True

    def reset(self):
        self._selected_index = 0

    def preferred_width(self, max_width):
        return self.control.preferred_width(max_width)

    def preferred_height(self, width, max_width, line_numbers, wrap_lines):
        return self.control.preferred_height(width, max_width, line_numbers, wrap_lines)

    def create_content(self, width, height):
        return self.control.create_content(width, height)
    
    def _get_cursor_position(self):
        return Point(x=0, y=self._selected_index)