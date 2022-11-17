# delibird ：数据库和 Parquet 之间的转换工具

## 功能：

delibird 是一个 python 工具库，帮助在数据库表和 parquet 之间做转换。基于 Python 和 Pyarrow 开发，支持多进程、异步调用

## 主要特性

- 多进程操作：针对表和 parquet，支持 batch 读取和多进程操作
- 支持目录：目录储存了分片的 parquet 文件，一个目录对应一个数据库表
- mock 支持：自定义 schema ，生成 parquet 或数据库表
- 工作流支持：在 yaml 文件定义多个操作，组成工作流执行

## 限制：

- 目前仅支持 postgres  , oracle 数据库

## 安装

### 从源代码安装

```bash
git clone https://gitee.com/lipicoder/delibird.git
cd delibird
pip install -e .
```

### Pypi 安装

```bash
$ python -m build
```

## 使用

输入 delibird 会显示使用方法：

```sh
(.env) % delibird
Usage: delibird [OPTIONS] COMMAND [ARGS]...

  delibird command line interface.

Options:
  -h, --help  Show this message and exit.

Commands:
  mock      Mock data to directory , file, or database.
  parquet   Write or read Parquet file or directory
  workflow  Database and parquet data transform workflow.
```

### mock

一个生成 mock 的 yaml 示例：

```yaml
# mock data workflow

# workflow lists
mocks:
  - name: "mock-to-directory"
    row-number: 2048
    direction: "directory" # directory ,file or  table
    directory: "./datasets/mock_data/mock_stocks"
    columns: {
                # stock code as a type
                "sec_code": "code",  # "600001"
                "date": "date",  # 2022-08-24
                "close": "float",  # 16.87
                "open": "float",  # 16.65
                "high": "float",  # 16.95
                "low": "float",  # 16.55
                "hold": "decimal(10,5)",  # 123.25515
                "time": "timestample(unit=s,tz=Asia/Shanghai)",
                "volume": "int",  # 1530231
                "amount": "int",  # 2571196416
                "memo":"string", # hello
            }

  - name: "mock-to-file"
    row-number: 2048
    direction: "file" # directory, file or table
    filepath: "./datasets/mock_data/mock_stocks.parquet"
    columns: {
                # stock code as a type
                "sec_code": "code",  # "600001"
                "date": "date",  # 2022-08-24
                "close": "float",  # 16.87
                "open": "float",  # 16.65
                "high": "float",  # 16.95
                "low": "float",  # 16.55
                "hold": "decimal(10,5)",  # 123.25515
                "time": "timestample(unit=s,tz=Asia/Shanghai)",
                "volume": "int",  # 1530231
                "amount": "int",  # 2571196416
                "memo":"string", # hello
            }

  - name: "mock-to-table"
    row-number: 204800
    direction: "table" # directory ,file or table
    engine: "postgresql"
    dsn: "postgresql://test:test123@localhost:5432/delibird"
    table-name: "mock_stocks"
    columns: {
                # stock code as a type
                "sec_code": "code",  # "600001"
                "date": "date",  # 2022-08-24
                "close": "float",  # 16.87
                "open": "float",  # 16.65
                "high": "float",  # 16.95
                "low": "float",  # 16.55
                "hold": "decimal(10,5)",  # 123.25515
                # datetime.datetime(2022,10,25).timestamp()
                "time": "timestample(unit=s,tz=Asia/Shanghai)",
                "volume": "int",  # 1530231
                "amount": "int",  # 2571196416
            }

```

```direction```  生成的类型/方向。"directory" 目录，"file" 文件，"table" 数据库表

```columns``` 是 schema 定义。支持标准的 postgres 列数据类型，对应 pyarrow 数据类型。code 数据类型是指沪深股票代码，这个之后会去除

执行这个 mock workflow:

```sh
(.env) % delibird mock tests/yamls/mock_file.yaml
write directory finished
write parquet finished
```

### parquet

从数据库读取表，写入到 parquet，或者是包含 parquet 的目录
或者从 parquet 或者目录读取文件内容，写入到数据库表中

```sh
(.env) % delibird parquet
Usage: delibird parquet [OPTIONS] COMMAND [ARGS]...

  Write or read Parquet file or directory.

Options:
  -h, --help  Show this message and exit.

Commands:
  read   Read parquet file and write to database.
  write  Read from database and write to parquet file.
```

#### **read 操作**

读取文件，写入数据库表
```sh
(.env) % delibird parquet read -h
Usage: delibird parquet read [OPTIONS] PATH ENGINE DSN TABLE_NAME

  Read parquet file, write to database.

  dsn sample:postgresql://user:password@host:port/dbname.

  engine [postgresql/oracle]

Options:
  -h, --help  Show this message and exit.
```

示例如下：

```sh
delibird parquet read datasets/mock_data/mock_stocks.parquet postgresql postgresql://test:test123@localhost:5432/delibird mock_stocks
```

#### **write 操作**:

读取数据库表，生成到**目录**中

```sh
(.env) % delibird parquet write -h
Usage: delibird parquet write [OPTIONS] PATH ENGINE DSN TABLE_NAME

  Read from database and write to parquet file.

  dsn sample:postgresql://user:password@host:port/dbname.

  engine [postgresql/oracle]

Options:
  -s, --batch_size INTEGER
  -h, --help                Show this message and exit.
```

示例如下：

```sh
delibird parquet write datasets/mock_data/mock_stocks_tmp postgresql postgresql://test:test123@localhost:5432/delibird mock_stocks
```

write 也可以支持设置 batch size

```sh
delibird parquet write -s 1024  datasets/mock_data/mock_stocks postgresql postgresql://test:test123@localhost:5432/delibird mock_stocks
```

这样的话，单个文件的最大记录数是1024，在目录下就可以看到有四个文件：

```sh
(.env) % ls datasets/mock_data/mock_stocks
ea6c445914824cae8ef171bbafd3a58f.parquet
604a63ccf14343c39bcc5bc0d1b3907d.parquet
9c7150d9821c46c78054d87ae23d900f.parquet
2ba1952316344b01a2a2f8e6faf41c31.parquet
```

生成为**文件**

```sh
delibird parquet write datasets/mock_data/mock_stocks_tmp.parquet postgresql postgresql://test:test123@localhost:5432/delibird mock_stocks;
```

文件也可以设置 batch size ，主要是为了减少内存占用，提高写入效率

### workflow

建立一个处理的工作流，以 yaml 文件作为流程记录

```sh
(.env) % delibird workflow  -h
Usage: delibird workflow [OPTIONS] YAML_FILE

  Execute yaml workflow.

Options:
  -h, --help  Show this message and exit.
```

示例如下：

```yaml
workflows:
  - name: "read-workflow" # workflow name
    direction: "table" # table or file or directory
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn : "postgresql://test:test123@localhost:5432/delibird"
    read-type: "file" # file or directory
    filepath: "./datasets/mock_data/mock_stocks.parquet" # filepath

  - name: "write-directory-workflow" # workflow name
    direction: "directory"
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn : "postgresql://test:test123@localhost:5432/delibird"
    directory: "./datasets/mock_data/mock_stocks" # directory path
    batch-size: 1024 # batch size

  - name: "write-file-workflow" # workflow name
    direction: "file"
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn : "postgresql://test:test123@localhost:5432/delibird"
    filepath: "./datasets/mock_data/mock_stocks_rewrite.parquet"
```



## 还需要完成的事

- 去除 mock code 类型，提供支持 random 字符串、数字字符串类型

## 依赖

pyarrow >=9.0.0

python >= 3.10

## License

Apache License 2.0

