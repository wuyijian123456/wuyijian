import yaml
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent
# 日志目录
LOG_DIR = BASE_DIR / "logs"
# 报告目录
REPORT_DIR = BASE_DIR / "report"
# 测试数据目录
DATA_DIR = BASE_DIR / "data"

# 创建目录（不存在则创建）
for dir_path in [LOG_DIR, REPORT_DIR, DATA_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# 读取环境配置
def load_env_config():
    env_file = BASE_DIR / "config" / "env.yaml"
    with open(env_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

env_config = load_env_config()
ACTIVE_ENV = env_config.get("active", "test")
BASE_URL = env_config[ACTIVE_ENV]["base_url"]
TIMEOUT = env_config[ACTIVE_ENV]["timeout"]
DB_CONFIG = env_config[ACTIVE_ENV]["mysql"]
# 默认请求头
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

# 数据库配置（按需启用）
# MYSQL_CONFIG = env_config[ACTIVE_ENV].get("mysql", {})