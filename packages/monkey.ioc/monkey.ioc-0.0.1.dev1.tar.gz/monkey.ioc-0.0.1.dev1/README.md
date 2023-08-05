Monkey IOC
=

Simple framework for inversion of control by dependency injection.

Installation guide
-
    pip install monkey.ioc

User guide
-

    from monkey.ioc.core import Registry
    
    registry = Registry()
    registry.load('config.json')
    my_object = registry.get('myObjectID')

