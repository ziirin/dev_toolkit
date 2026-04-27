from datetime import datetime
from pathlib import Path
from prompt_toolkit.validation import Validator, ValidationError

class NoEmptyValidator(Validator):
    def validate(self, doc) -> None:
        if not doc.text:
            raise ValidationError(message='Required value.')

class NumberValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        if not str(doc.text).isnumeric():
            raise ValidationError(message='Not a number.')
                
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
        