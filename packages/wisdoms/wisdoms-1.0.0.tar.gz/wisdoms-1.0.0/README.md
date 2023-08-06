[TOC]

# 天智信达的库

## 用法
1. 此库作为git项目管理，凡是修改完后应及时通知到开发团队
2. 需要使用库中的方法，使用pip install,这时候就可以在项目中引用库中的方法
3. 引用的方法举例：

----------------------------------------------------------

- #### generation - 更新库

_Make sure you installed setuptools and wheel._

_Important: You must modify the version of the package in setup.py and delete folders (build, dist, egg-info)_

> python setup.py sdist bdist_wheel

- #### upload - 上传代码

Install twine before doing this(qays:鱼和熊掌不可兼得）
> twine upload dist/*

------------------------------------------------------------

- #### install - 安装
> pip install wisdoms

- #### find the latest package of wisdoms - 发现最新版本
> pip list --outdated

- #### upgrade - 升级到最新包
> pip install wisdoms --upgrade


## packets usage:

- #### auth.py:

``` python

    # 权限验证
    from wisdoms.auth import permit

    host ={'AMQP_URI': "amqp://guest:guest@localhost"}

    auth = permit(host)

    class A:
        @auth
        def func():
            pass
```

- #### config.py

``` python

    # 读取yml配置
    from wisdoms.config import c

    # gains item of YML config
    print(c.get('name'))

    # transforms class into dict
    d = c.to_dict()
    print(d['name'])

```

- #### commons package

``` python

    # 返回执行后的状态码
    from wisdoms.commons import revert, codes, success

    def func():
        # do something

        # revert(codes.code) or revert(number)
        # return revert(1)
        return revert(codes.ERROR)

    def foo():
        # return revert(code, data, desc)
        return revert(codes.SUCCESS, {'data':'data'},'返回成功描述信息')

    def done():
        # simplified revert where success execute
        # return success(data) or success()
        return success()
```

- #### util.py
``` python

    # 多个字符串连接成路径
    from wisdoms.utils import joint4path

    print(joint4path('abc','dac','ccc'))

    # $: abc/dac/ccc

    # ------------------------------------------------------------------
    # 对象转字典
    from wisdoms.utils import o2d

    o2d(obj)

    # ------------------------------------------------------------------
    # 捕获异常装饰器
    from wisdoms.utils import func_exception
    
    ex = func_exception(codes.WARNING)

    @ex
    def func():
        pass
        
        
    # ------------------------------------------------------------------
    # 捕获异常类装饰器
    from wisdoms.utils import cls_exception
    
    # ex为方法装饰器
    xpt_cls = cls_exception(ex)
    
    @xpt_cls
    class A:
        name = 'a'
    
        def __init__(self, param):
            self.desc = param
    
        def func1(self, param):
            return self.desc + param
    
        @classmethod
        def func2(cls, param):
            print(cls)
            print('func2', param)
            raise Exception('func2 error')
    
        @staticmethod
        def func3(param):
            print('func3', param)
            raise Exception('func3 error')
    
    aa = A('param')
    # 注意： 该装饰器的静态方法和类方法必须用实例调用
    print(aa.func1('1111111'))
    print(aa.func2('2222222'))
    print(aa.func3('3333333'))

```

- #### ms.py
``` python

    from wisdoms.ms import ms_base

    MsBase = ms_base(config)

    class A(MsBase):
        pass

    # -----------------------------------------------
    from wisdoms.ms import closure_crf

    crf = closure_crf(config('ms_host'))
```

- #### pg_db.py
``` python

    from wisdoms.pg_db import session_exception

    se = session_exception(session)

    @se
    def func():    
        # raise exception extend SqlalChemyError
        pass

    # ------------------------------------------------------------------
    # session 增删改查表基础类，已经实现增删改查通用方法，直接继承就能使用
    from wisdoms.db import repo_ref

    RepoBase = repo_ref(session)

    class FooRepo(RepoBase):
        """
        common add, delete, update, get(include search) function finished
        """
        pass

    # Foo is the model of table
    foo = FooRepo(Foo)

    # you can do follow list
    foo.add({'name':'name','desc':'desc',...})
    foo.update(id,{'name':'rename','desc':'redesc',...})
    foo.delete(id)

    foo.get() # return list of all objects
    foo.get(id) # return a object
    foo.get(None,name ='name',...}) # return list of objects what you search


```


## 如何设计包
- 顶级包：wisdom，代表天智，智慧
- 现阶段的约定：采用一级包的方式
- 不同的功能放在不同的文件（模块）即可做好方法的分类