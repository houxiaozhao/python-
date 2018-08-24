 ## python flask 练习项目
 
 - 新建虚拟环境
 - 安装依赖
 - 路由视图
 - 表单
 - 新建数据库
 - 数据库的添加查询
 - 用户管理api接口
 
 习惯了前后端分离的开发模式对这种后台选渲染的模式非常不习惯,学习flask知识希望可以为前端提供接口
 
 接下来重点应该是rest接口和数据库查询
 
 添加拦截请求的装饰器，把需要认证的api添加该装饰器，可以从请求的headers的Authorization中获取token ,从而解析出该用户id，
	
 添加一个获取自己用户信息的接口作为测试
 
 #### token
 使用pyjwt包来生产token,服务器不存储token
 使用装饰器拦截请求,并解析token,得到用户id和token有效时间
 然后把用户信息放到g.state中,以供接下来使用
 
 ```python

from flask import g
import jwt  
from app.api.error import bad_request

def decoded_token(req):
    def decorator(func):
        def wrapper(*args, **kw):
            if req.headers['Authorization']:
                token = req.headers['Authorization'].split(' ')[1]
                try:
                    data = jwt.decode(bytes(token, encoding="utf8"), Config.SECRET_KEY, algorithms="HS256")
                    g.state = data
                    return func(*args, **kw)
                except Exception as e:
                    print(e)
                    return bad_request(str(e))

        return wrapper

    return decorator
```
![](http://obr4xf51d.bkt.clouddn.com/18-8-24/76216649.jpg)
![](http://obr4xf51d.bkt.clouddn.com/18-8-24/24532827.jpg)