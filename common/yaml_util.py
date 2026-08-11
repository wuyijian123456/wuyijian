import yaml
from config.env_config import DATA_DIR
from core.logger import log

class YamlUtil:
    """YAML文件读写工具"""
    @staticmethod
    def read_yaml(file_name):
        """读取YAML文件（默认从data目录读取）"""
        file_path = DATA_DIR / file_name
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                log.info(f"读取YAML文件成功：{file_path}")
                return data
        except yaml.YAMLError as e:
            # 提取错误位置，给出友好提示
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                error_msg = (
                    f"❌ YAML 格式错误\n"
                    f"   文件: {file_path}\n"
                    f"   位置: 第 {mark.line + 1} 行，第 {mark.column + 1} 列\n"
                    f"   错误: {e.problem}"
                )
                raise ValueError(error_msg)
            raise ValueError(f"YAML 解析失败: {e}")

        except Exception as e:
            log.error(f"读取YAML文件失败：{str(e)}")
            raise

    @staticmethod
    def write_yaml(file_name, data):
        """写入YAML文件"""
        file_path = DATA_DIR / file_name
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, ensure_ascii=False, indent=4)
                log.info(f"写入YAML文件成功：{file_path}")
        except Exception as e:
            log.error(f"写入YAML文件失败：{str(e)}")
            raise

# 全局实例
yaml_util = YamlUtil()