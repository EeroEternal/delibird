```bash
    tox -e py310-dev -- test_dask
```

```bash
    python -m venv .env
    source .env/bin/activate
    pip install -r requirements-dev.txt

    export PYTHONPATH=$PWD/src:$PYTHONPATH
```

mac install 
```bash
    pip install "psycopg[c]"==3.1.1 
```

or 
```bash
    brew install libpq
    echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
```

centos7 install
```bash
    pip install psycopg-binary
    yum isntall  python3-devel postgresql-devel
```