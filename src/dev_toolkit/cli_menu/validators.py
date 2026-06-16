from pathlib import Path
from prompt_toolkit.validation import Validator, ValidationError

from src.dev_toolkit.config.app_config import APP_CONFIG

class NoEmptyValidator(Validator):
    def validate(self, doc) -> None:
        if not doc.text:
            raise ValidationError(message='Required value.')

class NumberValidator(NoEmptyValidator):
    def __init__(self, allow_empty: bool = False) -> None:
        super().__init__()
        self.allow_empty = allow_empty
        
    def validate(self, doc) -> None:
        doc_text_str = str(doc.text)
        is_err = (doc_text_str != '' and not str(doc.text).isnumeric())
        is_err |= (doc_text_str == '' and not self.allow_empty)
        if is_err:
            raise ValidationError(message='Not a number.')
             
class FileValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        if not Path(doc.text).is_file():
            raise ValidationError(message=f'File not found: "{doc.text}".')
        
class FolderValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        if not Path(doc.text).is_dir():
            raise ValidationError(message=f'Folder not found: "{doc.text}".')
                
class FileOrFolderValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        if not Path(doc.text).exists():
            raise ValidationError(message=f'File or folder not found: "{doc.text}".')
        
class NotFileOrFolderValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        if Path(doc.text).exists():
            raise ValidationError(message=f'File or folder already exists: "{doc.text}".')
        
class BoolValidator(NoEmptyValidator):
    TRUE_VALUES = [
        '1',
        'y',
        't',
        'yes',
        'true'
    ]
    FALSE_VALUES = [
        '0',
        'n',
        'f',
        'no',
        'false'
    ]
    def validate(self, doc) -> None:
        super().validate(doc)
        if not doc.text.lower() in BoolValidator.TRUE_VALUES and \
           not doc.text.lower() in BoolValidator.FALSE_VALUES:
            raise ValidationError(message=f'"{doc.text}" is not a valid input.')

class TaskNameValidator(NoEmptyValidator):
    def validate(self, doc):
        super().validate(doc)
        for task in APP_CONFIG.get('tasks', []):
            if doc.text == task['name']:
                raise ValidationError(message=f'Following task already exist: "{doc.text}".')