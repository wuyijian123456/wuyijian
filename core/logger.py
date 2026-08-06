import sys
from loguru import logger
from config.env_config import LOG_DIR

# 清空默认日志配置
logger.remove()

# 配置日志输出：文件 + 控制台
logger.add(
    sink=LOG_DIR / "api_auto_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8"
)

# 控制台日志
logger.add(
    sink=sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO"
)

# 对外暴露logger
log = logger