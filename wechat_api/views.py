from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import uuid
from wechat_api.serializer.account import *

class messageCode(APIView):
    def get(self, request, *args, **kwargs):
        # 1.获取手机号
        phone_num = request.query_params.dict().get('phone_num')
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if ser.is_valid():
            print(ser.validated_data)

        else:
            return Response({'status': False, 'message': '手机格式错误'})
        # 3.生成随机验证码

        random_code = str(random.randint(1000, 9999))

        # 4.验证码发送到手机上
        # TODO 使用腾讯云或阿里云服务发送到手机上
        # 5.把验证码+手机号保留（30S过期  ）

        conn = get_redis_connection('default')

        conn.set(phone_num, random_code, ex=30)

        return Response({"status": True, "code": random_code})

class LoginView(APIView):
    """
    1.效验手机号是否合法
    2.效验验证码是否过期 redis
    -无验证码
    -有验证码，输入错误
    -有验证码，输入成功
    3.去数据库中获取用户信息（获取、创建）
    4.将一些信息返回给小程序
    """
    def post(self, request, *args, **kwargs):


        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False})
        from wechat_api import models
        phone_num = ser.validated_data.get('phone_num')



        user_obj,flag=models.UserInfo.objects.get_or_create(phone=phone_num)
        user_obj.token=str(uuid.uuid4())
        user_obj.save()
        return Response({"status":True,"data":{"token":user_obj.token,'phone':phone_num}})