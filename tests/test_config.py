from delibird.config import read_config


def test_config():
    """Test read config."""

    filepath = "key.toml"
    config = read_config(filepath)

    # 获取并检查 request 中的 chat 和 model 字段

    spark_config = config.get("spark")
    if not spark_config:
        raise ValueError("spark 配置项不存在")

    v35_config = spark_config.get("v35")

    if not v35_config:
        raise ValueError("spark 配置项不存在")

    version = v35_config.get("version")
    app_id = v35_config.get("app_id")
    api_key = v35_config.get("api_key")
    api_secret = v35_config.get("api_secret")
    url = v35_config.get("url")

    print(
        f"version: {version}, app_id: {app_id}, api_key: {api_key}, api_secret:"
        f" {api_secret}, url: {url}"
    )

    # 检查 spark v35
    assert config["spark"]["v35"]["version"] == "generalv3.5"
