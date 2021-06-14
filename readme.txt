=== lambda-tree源代码

= 运行说明：
需要安装Python3环境，然后在CLI下执行lambda-*的实用程序:

Usage: ./lambda-tree [--dump-ast] <input_file> <output_file>
Usage: ./lambda-interpreter <input_file>
Usage: ./lambda-pack <input_file> <output_file>

Windows下或未添加执行权限时，请使用类似“python3 lambda-xxx”的指令


= 文件说明：
├── lambda-tree	        实用程序：三地址码生成器
├── lambda-interpreter  实用程序：语言解释器
├── lambda-pack         实用程序：字节码打包器
├── syntax              属性文法定义目录
│   ├── CONDITION.py
│   ├── EXPRESSION.py
│   ├── FACTOR.py
│   ├── LINE.py
│   ├── PROGRAM.py
│   ├── SENTENCE.py
│   ├── TERM.py
│   └── __init__.py
├── scanner.py          扫描器程序（实验一）
├── parser.py           解析器程序（实验二/三）
├── ast_execute.py      语法树处理环境（实验三）
└── test*.src           测试源代码
