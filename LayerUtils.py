'''
For now we're defining custom helper functions here

NOTE: __all__ affects the from <module> import * behavior only. Members that are not mentioned in __all__ are still accessible from outside the module and can be imported with from <module> import <member>
'''

__all__ = ['EmptyLayerName']

class EmptyLayerName(Exception):
   """Raised when the Layer doesn't have a name"""
   print("Layers need names such as Q(s,a), V(s), pi(s)")
   pass
