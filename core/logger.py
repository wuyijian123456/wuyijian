import sys
from loguru import logger
from config.settings import LOG_DIR

# 清空默认日志配置
logger.remove()

# 配置日志输出：控制台 + 文件
logger.add(
    sink=sys.stdout,  # 控制台输出
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

logger.add(
    sink=LOG_DIR / "api_auto_{time:YYYY-MM-DD}.log",  # 文件输出
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="00:00",  # 每天0点分割日志
    retention="7 days",  # 保留7天
    encoding="utf-8"
)

# 对外暴露logger
log = logger