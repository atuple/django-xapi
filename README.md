django rest api ~

only running in django >= 2.0

author: Sai

email: 3030159@qq.com 

## eg

```bash
#models
class Member(models.Model):
    name = models.CharField(max_length=10)
    time = models.DateTimeField()
    
class Order(models.Model):
    member = models.ForeignKey(Member)
    price = models.IntegerField()
    time = models.DateTimeField()
    
# yourapp apix.py
from xapi import xplatform
from xapi.views import *
site = xplatform.new_site("web", "web")
api = site.new_router(title="api_mod_title", path="admin")



@api.register_model(Order)
class OrderApi:
    pass
    
@api.register
class TestGetApi(GetApi):
    title = "my test get api"
    path = "test/get"
    des = """
    use md bash ~~~!
    
    curl 127.0.0.1:8000/test/get
    return {"code": 200, "data": {"hello": "hello world!"}, "msg": "some thing"}
    """    
    def get_context_data(self, **kwargs):        
        ctx = {"hello": "hello world!"}
        return ctx    
        
@api.register
class TestPostApi(PostApi):
    title = "my test post api"
    path = "test"
    des = """
    use md bash ~~~!
    
    """
    #form_class = SomeForm
        
    def get_context_data(self, **kwargs):        
        data = json.loads(self.request.body)
        print(data)
        ctx = {}
        return ctx 
        
@api.register
class OrderListApi(ModelListApi):
    title = "order list"
    path = "order/list"
    model = Order
    display = ["member", "price", "time"]
    des = """
    """
    def model_serializer(self, obj):
        data = super().model_serializer(obj)
        data["idaddone"] = obj.id + 1
        return data
        
@api.register
class OrderCreateApi(ModelCreateApi):
    title = "order add"
    path = "order/add"
    des = """
    
    """
    model = Order
   
@api.register
class OrderCreateApi(ModelDetailApi):
    title = "order add"
    path = "order/add"
    display = ["member", "price", "time"]
    des = """
    """
    model = Order        

    
#urls.py
import xapi
xapi.autodiscover()

urlpatterns = [
    ......
    path('api/', xapi.xplatform.urls),
]

# web docs
open http://localhost:8000/api/docs

