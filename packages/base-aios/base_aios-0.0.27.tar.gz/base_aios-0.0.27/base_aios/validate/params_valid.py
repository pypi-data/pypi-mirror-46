from types import FunctionType

class ParamsValid(object):

    def __init__(self, **args):
        self.v_map = {
            'type': self.validate_type,
            'required': self.validate_required,
            'minlen': self.validate_minlen,
            'maxlen': self.validate_maxlen,
            'max': self.validate_max,
            'min': self.validate_min,
            're': self.validate_re,
            'function': self.validate_function,
            'enum': self.validate_enum
        }
        self.fields = args or {}

    def validate(self, data={}):
        try:
            for field in self.fields:
                rules = self.fields.get(field)
                rules.setdefault('type', str)

                v_data = data.get(field)

                required = rules.get('required')
                if required is None and v_data is None:
                    continue
                for rule in rules:
                    v_rule = rules.get(rule)
                    fn = self.v_map.get(rule)
                    if fn:
                        is_valid, msg = fn(v_rule, field, v_data)
                        if not is_valid:
                            raise Exception('Params verification failed! {}'.format(msg))
                    else:
                        raise Exception('Unknown validation type: [{}]'.format(rule))
            return True, ''
        except Exception as err:
            return False, str(err)

    def validate_type(self, rule, key, value):
        if isinstance(value, rule):
            return True, ''
        else:
            try:
                rule(value)
                return True, ''
            except Exception as err:
                return False, 'Data type does not match: {}'.format(key)

    def validate_required(self, rule, key, value):
        if rule:
            if bool(value):
                return True, ''
            else:
                return False, 'Required items can not be empty: {}'.format(key) 
        else:
            return True, ''

    def validate_minlen(self, rule, key, value):
        if rule <= len(value):
            return True, ''
        else:
            return False, 'Length of the string exceeds the limit: {}'.format(key)

    def validate_maxlen(self, rule, key, value):
        if len(value) <= rule:
            return True, ''
        else:
            return False, 'Length of the string exceeds the limit: {}'.format(key)

    def validate_min(self, rule, key, value):
        if rule <= float(value):
            return True, ''
        else:
            return False, 'Value range exceeds the limit: {}'.format(key)

    def validate_max(self, rule, key, value):
        if float(value) <= rule:
            return True, ''
        else:
            return False, 'Value range exceeds the limit: {}'.format(key)

    def validate_re(self, rule, key, value):
        if rule.match(value):
            return True, ''
        else:
            return False, 'Data format error: {}'.format(key)

    def validate_function(self, rule, key, value):
        if isinstance(rule, FunctionType):
            if rule(value):
                return True, ''
        else:
            return False, 'Callback validate error: {}'.format(key)

    def validate_enum(self, rule, key, value):
        if value in rule:
            return True, ''
        else:
            return False, 'Enum validate error: {}'.format(key)
