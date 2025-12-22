from datetime import datetime
from prompt_toolkit.validation import Validator, ValidationError

class DayMonthValidator(Validator):
    def validate(self, doc) -> None:
        values = str(doc.text).split('/')
        if len(values) != 2 or not values[0].isnumeric() or not values[1].isnumeric():
            raise ValidationError(message='Invalid date.')

class FirstDayOfWeekValidator(Validator):
    def validate(self, doc) -> None:
        DayMonthValidator().validate(doc)
        values = str(doc.text).split('/')
        try:
            date = datetime.now().replace(day=int(values[0]), 
                                          month=int(values[1]))
        except Exception as e:
            raise ValidationError(message=str(e))
        if not date.weekday() == 0:
            raise ValidationError(message='Thats not a Monday date.')