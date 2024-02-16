class Meta(type):
    def __call__(cls, *args, **kwargs):
        class_type = kwargs.pop("class_type", None)
        if class_type is not None:
            subclasses = {
                subclass.__name__: subclass for subclass in cls.__subclasses__()
            }
            try:
                return subclasses[class_type](*args, **kwargs)
            except KeyError:
                raise ValueError(f"Invalid class type: {class_type}")
        else:
            return super().__call__(*args, **kwargs)


class A(metaclass=Meta):
    pass


class A1(A):
    pass


class A2(A):
    pass


class A3(A):
    pass


# 动态实例化子类
instance = A(class_type="A1")
print(isinstance(instance, A1))  # 输出: True

instance = A(class_type="A2")
print(isinstance(instance, A2))  # 输出: True

# 错误的类型会抛出异常
try:
    instance = A(class_type="Unknown")
except ValueError as e:
    print(e)  # 输出: Invalid class type: Unknown
