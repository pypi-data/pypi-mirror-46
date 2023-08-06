from sqlalchemy import String, TypeDecorator
from sequence_field.utils import expand
from .error import OrderNumberError
from .constants import SEQUENCE_FIELD_DEFAULT_EXPANDERS, SEQUENCE_FIELD_DEFAULT_TEMPLATE


# 这里面的初始化的时候的部分属性，我研究了好久，也每看出是干啥的来，
class SequenceField(TypeDecorator):
    impl = String

    def __init__(self, *args, **kwargs):
        if kwargs.get('key'):
            self.generator = kwargs.pop('generator')
            # 用来标识唯一的
            self.key = kwargs.pop('key')
            default_template = SEQUENCE_FIELD_DEFAULT_TEMPLATE
            # 用来获取模板
            self.template = kwargs.pop('template', default_template)
            # 用来
            # self.if_missing()
            default_expanders = SEQUENCE_FIELD_DEFAULT_EXPANDERS
            self.params = kwargs.pop('params', {})
            self.expanders = kwargs.pop('expanders', default_expanders)
            self.auto = kwargs.pop('auto', False)
        super(SequenceField, self).__init__(*args, **kwargs)

    def next_value(self):
        count = self.generator.add(key=self.key)
        template = self.template
        params = self.params
        expanders = self.expanders
        return expand(template, count, params, expanders=expanders)

    def process_bind_param(self, value, dialect):
        if self.auto and not value:
            sequence_string = self.next_value()
            return sequence_string
        elif self.auto and isinstance(value, dict):
            if 'param' not in value and not isinstance(value['param'],dict):
                raise OrderNumberError(message="流水号固定字符串格式不正确")
            self.params = value['param']
            if 'key' not in value:
                raise OrderNumberError(message="流水号唯一KEY不正确")
            self.key = value['key']
            sequence_string = self.next_value()
            return sequence_string
        else:
            return value

    def process_result_value(self, value, dialect):
        return value
