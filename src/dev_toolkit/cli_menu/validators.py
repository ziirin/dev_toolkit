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

class DayMonthValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        values = str(doc.text).split('/')
        if len(values) != 2 or not values[0].isnumeric() or not values[1].isnumeric():
            raise ValidationError(message='Invalid date.')

class FirstDayOfWeekValidator(DayMonthValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        values = str(doc.text).split('/')
        try:
            date = datetime.now().replace(day=int(values[0]), 
                                          month=int(values[1]))
        except Exception as e:
            raise ValidationError(message=str(e))
        if not date.weekday() == 0:
            raise ValidationError(message='Thats not a Monday date.')
        
class ProjectNameValidator(NoEmptyValidator):
    VALID_INPUTS = [
        'Núcleo',
        'Lasts',
        '3D+',
        'Traducciones',
        'General'
    ]
    def validate(self, doc) -> None:
        super().validate(doc)
        if not doc.text in ProjectNameValidator.VALID_INPUTS:
            raise ValidationError(message=f'"{doc.text}" is not a valid project.')
        
class FileOrFolderValidator(NoEmptyValidator):
    def validate(self, doc) -> None:
        super().validate(doc)
        if not Path(doc.text).exists():
            raise ValidationError(message=f'File or folder not found: "{doc.text}".')
        
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
        