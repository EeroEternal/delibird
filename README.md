# delibird: a transformer between database and Parquet file

## Introduction:

delibird is a python tool library based on Python pyarrow which supports multithread and asynchronous calls. It can help
users transform data between database and Parquet files.

## Features:

- Multithread: support batch reading/writeing and multithread functions an database table and Parquet files.
- Read directory: reading all Parquet files in the giving directory and transform into database. One directory maps to
  one database table.
- Mock data: create Parquet files or database tables in a customized schema.
- Workflow: giving a yaml file including your customized configurations, delibird can create a workflow to execute
  multiple jobs.

## Limits:

- Only support Postgresql DB and Oracle DB by now.

## Installation

### source code

```bash
git clone https://gitee.com/lipicoder/delibird.git
cd delibird
pip install -e .
```

### Pypi

```bash
$ python -m build
```

### pip

```bash
$ pip install delibird
```

## Usage

Input 'delibird' in command line. The usage lint will be displayed.

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

Example:

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
      "memo": "string", # hello
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
      "memo": "string", # hello
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

```direction```  transform to which format. 'directory': a directory path. 'file': a file path. 'table': a database
table name.

```columns``` defination of the database table. Support standard data types of Postgresql or Oracle db, based on which
database you choose. delibird will auto map the database data type to pyarrow row data type. 'code' means stock code,
which would be removed later.

execute mock workflow:

```sh
(.env) % delibird mock tests/yaml/mock_file.yaml
write directory finished
write parquet finished
```

### parquet

Read data in database table and write data into a Parquet file or Parquet files in a directory. Or read data in a
Parquet file or Parquet files in a directory and write data into a database table.

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

#### **parquet read**

Read data in a Parquet file or Parquet files in a directory and write data into a database table.

```sh
(.env) % delibird parquet read -h
Usage: delibird parquet read [OPTIONS] [-e ENGINE] PATH DSN TABLE_NAME

  Read parquet file, write to database.

  dsn sample:postgresql://user:password@host:port/dbname.

  engine [postgresql/oracle]

Options:
  -h, --help  Show this message and exit.
```

Example:

```sh
delibird parquet read datasets/mock_data/mock_stocks.parquet postgresql://test:test123@localhost:5432/delibird mock_stocks -e postgresql
```

#### **parquet write**:

Read data in database table and write data into a Parquet file or Parquet files in a directory.

**directory**.

```sh
(.env) % delibird parquet write -h
Usage: delibird parquet write [OPTIONS]  [-e ENGINE] PATH DSN TABLE_NAME

  Read from database and write to parquet file.

  dsn sample:postgresql://user:password@host:port/dbname.

  engine [postgresql/oracle]

Options:
  -s, --batch_size INTEGER
  -h, --help                Show this message and exit.
```

Example:

```sh
delibird parquet write datasets/mock_data/mock_stocks_tmp postgresql://test:test123@localhost:5432/delibird mock_stocks -e postgresql
```

parquet write supports configuration of batch size

```sh
delibird parquet write -s 1024 -e postgresql datasets/mock_data/mock_stocks postgresql://test:test123@localhost:5432/delibird mock_stocks
```

In this case, the max row number of a single parquet file is 1024, we can see four files in the directory.

```sh
(.env) % ls datasets/mock_data/mock_stocks
ea6c445914824cae8ef171bbafd3a58f.parquet
604a63ccf14343c39bcc5bc0d1b3907d.parquet
9c7150d9821c46c78054d87ae23d900f.parquet
2ba1952316344b01a2a2f8e6faf41c31.parquet
```

**file**

```sh
delibird parquet write -e postgresql datasets/mock_data/mock_stocks_tmp.parquet postgresql://test:test123@localhost:5432/delibird mock_stocks;
```

Consider of reducing the memory usage and speed up the writing efficiency. write file can also support configuration of
batch size.

### workflow

create and exectue a workflow using a yaml configuration file.

```sh
(.env) % delibird workflow  -h
Usage: delibird workflow [OPTIONS] YAML_FILE

  Execute yaml workflow.

Options:
  -h, --help  Show this message and exit.
```

Example:

```yaml
workflows:
  - name: "read-workflow" # workflow name
    direction: "table" # table or file or directory
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn: "postgresql://test:test123@localhost:5432/delibird"
    read-type: "file" # file or directory
    filepath: "./datasets/mock_data/mock_stocks.parquet" # filepath

  - name: "write-directory-workflow" # workflow name
    direction: "directory"
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn: "postgresql://test:test123@localhost:5432/delibird"
    directory: "./datasets/mock_data/mock_stocks" # directory path
    batch-size: 1024 # batch size

  - name: "write-file-workflow" # workflow name
    direction: "file"
    table-name: "mock_stocks" # table name
    engine: "postgresql"
    dsn: "postgresql://test:test123@localhost:5432/delibird"
    filepath: "./datasets/mock_data/mock_stocks_rewrite.parquet"
```

## TODO

- remove 'code' type from delibird mock. add new supported types such as random string and random digit string.

## Dependency

pyarrow >=9.0.0

python >= 3.10

## License

Apache License 2.0

