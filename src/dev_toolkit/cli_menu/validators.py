from datetime import datetime
from ..misc.util import translate
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
        
class RemainingTimeValidator(NoEmptyValidator):
    VALID_UNITS = [
        'd',
        'w',
        'm',
        'y'
    ]
    def validate(self, doc) -> None:
        super().validate(doc)
        if not doc.text[:-1].isnumeric():
            raise ValidationError(message='Invalid format.')
        unit = doc.text[-1:]
        if unit not in RemainingTimeValidator.VALID_UNITS:
            raise ValidationError(message=f'Invalid units "{unit}".')

    def value_to_str(value: str) -> str:
        if not value[:-1].isnumeric():
            return ''
        time = int(value[:-1])
        unit = value[-1:]
        if unit not in RemainingTimeValidator.VALID_UNITS:
            return ''
        
        full_unit_str = ''
        if unit == 'd':
            full_unit_str = 'day'
        elif unit == 'w':
            full_unit_str = 'week'
        elif unit == 'm':
            full_unit_str = 'month'
        elif unit == 'y':
            full_unit_str = 'year'
            
        full_unit_str = full_unit_str if time == 1 else f'{full_unit_str}s'
        full_unit_str = translate(full_unit_str)
        return f'{time} {full_unit_str}.'