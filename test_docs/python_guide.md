# Python编程指南

## 什么是Python？

Python是一种高级、解释型、通用的编程语言。它由Guido van Rossum于1991年创建，强调代码的可读性和简洁性。

## Python的特点

1. **简单易学** - Python语法简洁明了，接近自然语言
2. **丰富的库** - 拥有大量的标准库和第三方库
3. **跨平台** - 可在Windows、macOS、Linux等多个平台运行
4. **多范式支持** - 支持面向对象、函数式、过程式编程

## 基础语法

### 变量和数据类型

```python
# 数字
age = 25
price = 19.99

# 字符串
name = "Python"
message = 'Hello, World!'

# 列表
fruits = ["apple", "banana", "cherry"]

# 字典
person = {"name": "Alice", "age": 30}
```

### 控制流

```python
# if语句
if age >= 18:
    print("成年人")
else:
    print("未成年人")

# for循环
for fruit in fruits:
    print(fruit)

# while循环
while count < 10:
    print(count)
    count += 1
```

### 函数定义

```python
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 调用函数
message = greet("Python")
print(message)
```

## 常用库

- **NumPy** - 数值计算
- **Pandas** - 数据分析
- **Matplotlib** - 数据可视化
- **Requests** - HTTP请求
- **Flask/Django** - Web开发

## 最佳实践

1. 遵循PEP 8编码规范
2. 使用虚拟环境管理依赖
3. 编写文档字符串
4. 进行单元测试
