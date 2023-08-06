## Flask-Douwa 使用说明

### 安装
```
pip install Flask-Douwa -i https://pypi.python.org/simple
```
**注意**  
- 请使用pipy源安装
- 随时关注更新,使用最新的Flask-Douwa
------

### 使用

导入Douwa
```
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
from flask_douwa import Douwa
```
**注意**
- linux操作系统需要在导入Douwa之前为操作系统配置环境变量,这是Douwa里面的一个扩展包需要的

**在flask实例中注册Douwa**
```
douwa = Douwa()

douwa.init_app(app)
```

### ID 生成器
生成分布式系统全局唯一的ID

在flask的配置中加入
```
    GENERATORID_IP = os.getenv('GENERATORID_IP') or "122.237.100.158:5001"
```
**在model层直接引用**
```
from app import db,douwa

order_id = db.Column(db.String(50), primary_key=True, unique=True, default=douwa.generator_id)
```
**注意**  
- 在引用ID生成器时,要douwa.generator_id,不要使用douwa.generator_id()

### 权限相关
在flask的配置中加入redis相关配置,要从redis中读取用户,用户组,用户权限的相关信息
```
REDIS_HOST = os.getenv('REDIS_HOST') or '47.100.21.215'
REDIS_PORT = int(os.getenv('REDIS_PORT', 0)) or 50204
REDIS_DB = os.getenv('REDIS_DB') or '0'
```
在视图类和或者视图函数中应用装饰器实现用户认证,权限判定  

**视图类**
```
from flask_douwa.decorators import permission, authorization

class UserListView(Source):
    method_decorators = [permission('用户列表权限'), authorization]

    def post():
        pass
    def get():
        pass

```
**注意**
- 采用flask_restful时候可以采用method_decorators来给 post get put 等方法一次性加上装饰器
- 注意装饰器的顺序 先写权限的,再写认证的

**路由函数**

```
from flask_douwa.decorators import permission, authorization

@app.route('/users/', methods=['GET'])
@authorization
@permission('用户列表')
@error
def users():
    pass
```
**注意**
- 装饰器的顺序
- 加上error装饰器

### 复杂规则单号生成
引入自定义的SequenceField字段,并且在model中应用

sequence_field已经集成到flask_douwa中采用如下方式应用到模块中

```
from app import db
from sequence_field.fields import SequenceField

class Test(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sequence = db.Column(SequenceField(length=50, key='sequence.name',
                                template='%Y%m%d{code}%NNNNN',
                                params={'code': 'bom'},
                                expanders=[
                                    'sequence_field.expanders.NumericExpander',
                                    'sequence_field.expanders.TimeExpander',
                                    'sequence_field.expanders.ParameterExpander',
                                ],
                                auto=True,
                                ))
```
```
>>> a=Test()
>>> db.session.add(a)
>>> db.session.commit()
>>> a.sequence
'20171214bom00001'
```
**注意**
- 在数据库中会生成名为sequence的表这是用于序列计算用的
### SequenceField参数说明
#### 必选参数
- 限定字段长度
```
length=50
```

- 是否自动生成SequenceField字段,一般设置为True,若为False则无法生成sequence字符串
```
auto=True
```

- key,序列关键字 ,必传参数,这是序列值存储在
sequence数据表中的依据，SequenceField根据该数据表记录该序列的当前值，计算该序列的下一个值,系统中不同的SequenceField该参数不能重复。
```
key='sequence.name'
```

- template,  params,  expanders 三个参数具体确定SequencField字符串的具体内容
```
template='%Y%m%d{code}%NNNNN',
params={'code':'bom'},
expanders=[
    'sequence_field.expanders.NumericExpander',
    'sequence_field.expanders.TimeExpander',
    'sequence_field.expanders.ParameterExpander',
],
```
  + 其中TimeExpandeer 作用于%Y%m%d 获取当前时间,并且将年月日格式化到SequenceField字符串中
  + NumericExpander作用于 %NNNNN 以N的个数为位数标准生成SequenceField字符串中的数字序列部分,可以改变N的个数以改变数字序列部分的个数
  + ParameterExpander 作用于{code}部分 将params键值对中的值格式化到SequenceField中对应的params参数的键的位置

- 以上三个参数都有默认值,默认值为
```
template='%N',
params={},
expanders=[
    'sequence_field.expanders.NumericExpander',
    'sequence_field.expanders.TimeExpander',
    'sequence_field.expanders.ParameterExpander',
],
```
  **注意**
  - 可以不写expanders

#### 详细使用示例
1. 改变template顺序
```
template='{code}%NNNNN%Y%m%d',
```
```
>>> a=TestModel()
>>> db.session.add(a)
>>> db.session.commit()
>>> a.sequence
'bom0000120171023'
```

2. 去除时间成分,同理也可以去除其他成分
```
template='{code}%NNNNN'
```
```
>>> b=TestModel3()
>>> db.session.add(b)
>>> db.session.commit()
>>> b.sequence
'bom00001'
```
3. 传入动态字符串 保证在每次构建的时候实现sequence 定制
```
>>> c=Test()
>>> c.sequence=({'code':'hello'})
>>> db.session.add(c)
>>> db.session.commit()
>>> c.sequence
20171214hello00001
>>> d=Test()
>>> d.sequence=({'code':'world'})
>>> db.session.add(d)
>>> db.session.commit()
>>> d.sequence
20171214world00001
```
