from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection
from .validators import phone_validator

class MessageSerializer(serializers.Serializer):
    phone_num = serializers.CharField(label="手机号", validators=[phone_validator, ])
    # 还可以使用钩子函数校验
    # def phone_validator(self,value):
    #     if not re.match(r"^(1[3|4|5|6|7|8|9]\d{9}$)", value):
    #         raise ValidationError("手机格式错误")

class LoginSerializer(serializers.Serializer):
    """校验手机号是否合法
    校验验证码，redis
    -无验证码
    -有验证码输入错误
    -有验证码输入成功
    """
    phone_num = serializers.CharField(label="手机号", validators=[phone_validator, ])
    phoneCode = serializers.CharField(label="短信验证码")

    def validate_phoneCode(self, value):
        if len(value) != 4:
            raise ValidationError('短信格式错误')
        phone_num = self.initial_data.get('phone_num')
        conn = get_redis_connection('default')
        redis_code = conn.get(phone_num)
        if not redis_code:
            raise ValidationError('验证码过期')
        if value != redis_code.decode('utf-8'):
            raise ValidationError('验证码错误')
        return value