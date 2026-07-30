import sys
from loguru import logger
from config.settings import LOG_DIR

# 清空默认日志配置
logger.remove()

# 配置日志输出：文件 + 控制台
# 文件日志用独立文件句柄，不受 pytest/os.system 影响
logger.add(
    sink=LOG_DIR / "api_auto_{time:YYYY-MM-DD}.log",  # 文件输出
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="00:00",  # 每天0点分割日志
    retention="7 days",  # 保留7天
    encoding="utf-8"
)

# 控制台日志使用 sys.__stderr__ + error_handler 双重防护
# sys.__stderr__ 是解释器启动时的原始 stderr，不受 pytest 重定向和 os.system 子进程影响
# error_handler 作为兜底，当写入仍失败时静默丢弃而非报错
try:
    logger.add(
        sink=sys.__stderr__,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        enqueue=True,
        error_handler=lambda self, record: None  # 静默丢弃写入失败，不打印 traceback
    )
except Exception:
    pass  # 如果控制台日志初始化失败，降级为纯文件日志

# 对外暴露logger
log = logger