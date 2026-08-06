"""环境配置 - 所有模块和夹具统一读取。

由 pytest_configure 根据 --env 参数初始化，Jenkins 只需:
    pytest -vs --env=uat
"""
from pathlib import Path
import yaml

# ==================== 项目固定路径 ====================
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "report"
DATA_DIR = BASE_DIR / "data"

for dir_path in [LOG_DIR, REPORT_DIR, DATA_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)


# ==================== 动态环境配置 ====================
_ENV_FILE = BASE_DIR / "config" / "env.yaml"
_env_name: str = "uat"
_env_config: dict = {}


def set_active_env(env_name: str) -> dict:
    """设置当前环境配置。由 pytest_configure 调用。"""
    global _env_name, _env_config
    with open(_ENV_FILE, "r", encoding="utf-8") as f:
        all_configs = yaml.safe_load(f)
    _env_name = env_name
    _env_config = all_configs.get(env_name, {})
    return _env_config


def get(name: str):
    """获取配置项，如 get("base_url")。"""
    return _env_config.get(name)


def get_all() -> dict:
    """获取完整配置。"""
    return _env_config
