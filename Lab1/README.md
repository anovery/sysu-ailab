# Lab 1 一阶逻辑归结推理

## Content

在给出的test{n}.txt中，以如下格式记录知识库和查询的子句

```
KB:
Clause1
Clause2
...
QUERY:
Clauseq
```

其中

- `clause`均以析取式形式存储。

- 单一谓词子句保存表达式，多谓词子句以元组形式存储并以字符串形式记录。

- `Clauseq`已完成否定转换

另外，实验内容遵循以下标准

- 谓词符号第一个字符采用大写字母，其余字符为英文字符。

- 变量符号以单个小写字母表示。

- 常量符号以多个小写字母表示。

- 否定符号以`~`表示。

## Requirements

1. 实验文件已给出代码文件`main.py`和测试样例`test1.txt`,`test2.txt`,`test3.txt`，需完成的部分为`my_Predicate.py`。

2. `Sentences`类包含的核心内容

- `__init__(self, path)`: 根据传入的文件路径，读取知识库和查询，保存到类内部。

- `resolution()`: 归结当前类存储的知识库，记录每一步的归结结果。

- `reindex()`: 从归结后的最终状态出发，逆序分析`resolution()`中需要用到的步骤，然后按顺序打印步骤。

3. 归结示例

```
(P(x),Q(g(x)))
(R(a),Q(z),~P(aa))

R[1a,2c](x=aa) = (Q(g(aa)),R(aa),Q(z))
```

