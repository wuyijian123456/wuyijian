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
PARAM_TEMPLATE_DIR = BASE_DIR / "models" / "param_template"

for dir_path in [LOG_DIR, REPORT_DIR, DATA_DIR,PARAM_TEMPLATE_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)


# ==================== 动态环境配置 ====================

def set_active_env(env_name: str) -> dict:
    """设置当前环境配置。由 pytest_configure 调用。"""
    _ENV_FILE = BASE_DIR / "config" / "env.yaml"
    with open(_ENV_FILE, "r", encoding="utf-8") as f:
        all_configs = yaml.safe_load(f)
    _env_config = all_configs.get(env_name, {})
    return _env_config


