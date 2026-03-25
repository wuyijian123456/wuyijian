# 📖 框架功能快速参考手册

## 🔧 导入语句速查

```python
# 重试机制
from core.retry import retry, flaky

# 测试标记
from common.marker import tag, priority, smoke_test, regression_test

# 变量管理
from common.var_util import var_util

# 数据提取
from common.response_extractor import ResponseExtractor

# 数据库断言
from common.db_util import db_assert, db

# 数据清理
from common.cleanup import CleanUpManager

# 测试数据
from common.data_factory import data_factory

# 错误处理
from core.error_handler import on_failure, ErrorHandler

# 速率控制
from core.rate_limiter import rate_limit, concurrent_limit

# 报告增强
from core.report_enhancer import ReportEnhancer, performance_monitor
```

---

## 🎯 常用装饰器

### 重试装饰器
```python
@retry(max_attempts=3, delay=1, backoff=2)
def test_api():
    pass

@flaky(max_runs=3, min_passes=2)
def test_unstable():
    pass
```

### 标记装饰器
```python
@tag("smoke", "critical")
@priority("P0")
@smoke_test
@regression_test
def test_feature():
    pass
```

### 性能监控
```python
@performance_monitor
def test_with_metrics():
    pass
```

### 错误处理
```python
@on_failure
def test_with_error_handling():
    pass
```

### 速率限制
```python
@rate_limit(calls_per_second=5)
def test_rate_limited():
    pass

@concurrent_limit(max_concurrent=3)
def test_concurrent():
    pass
```

---

## 📦 数据生成速查

```python
# 随机数据
data_factory.random_string(8)           # "aB3dE5fG"
data_factory.random_email()             # "abc12345@test.com"
data_factory.random_phone()             # "13812345678"
data_factory.random_id_card()           # 身份证号
data_factory.random_name()              # "张伟"
data_factory.random_password(10)        # 随机密码
data_factory.random_number(1, 100)      # 随机整数
data_factory.random_float(0.0, 100.0)   # 随机小数
data_factory.random_date()              # "2024-03-25"
data_factory.random_uuid()              # UUID

# 完整数据集
data_factory.create_user_data()
data_factory.create_order_data()
data_factory.create_patient_data()
```

---

## 🔗 接口关联

```python
# 从响应提取变量
ResponseExtractor.extract(response, {
    "user_id": "$.data.user.id",
    "token": "$.data.token"
})

# 使用变量
next_api(var_util.get_var("user_id"))

# 保存整个响应
var_util.set_var("last_response", response.json())
```

---

## 💾 数据库操作

```python
# 查询
result = db.query("SELECT * FROM users WHERE id = %s", (123,))
single = db.query_one("SELECT * FROM users WHERE id = %s", (123,))
count = db.count("users", "status = %s", (1,))

# 执行 SQL
db.execute("UPDATE users SET status = %s WHERE id = %s", (1, 123))

# 断言
db_assert.assert_exists("users", "id = %s", (123,))
db_assert.assert_field_value("users", "name", "John", "id = %s", (123,))
db_assert.assert_record_count("orders", 5, "user_id = %s", (456,))
```

---

## 🧹 数据清理

```python
# 注册单个清理任务
CleanUpManager.register(test_name, delete_func, resource_id)

# 批量注册
CleanUpManager.register_batch(test_name, [
    {"func": delete_order, "args": (order_id,)},
    {"func": delete_user, "args": (user_id,)}
])

# 使用上下文管理器
with CleanUpManager.context("test_order"):
    order = create_order()
    CleanUpManager.register("test_order", delete_order, order["id"])
```

---

## 📊 报告增强

```python
# 添加请求详情
ReportEnhancer.add_request_details(url, method, headers, params)

# 添加响应详情
ReportEnhancer.add_response_details(status_code, response.json())

# 添加 SQL 详情
ReportEnhancer.add_sql_details(sql, params, result)

# 添加附件
ReportEnhancer.add_attachment("/path/to/file.txt", "描述")

# 添加截图
ReportEnhancer.add_screenshot("/path/to/screenshot.png")
```

---

## 🏷️ Pytest 命令行

```bash
# 基本运行
pytest testcases/test_file.py -v

# 带标签运行
pytest -m smoke -v
pytest -m "priority and P0" -v

# 重试
pytest --retry 3 -v

# 指定环境
pytest --env prod -v

# 生成报告
pytest --alluredir=./report

# 查看报告
allure serve ./report

# 并发运行（pytest-xdist）
pytest -n 4  # 4 个进程并行
```

---

## 🎯 完整测试模板

```python
import allure
from api.xxx_api import XxxApi
from common.marker import tag, priority, smoke_test
from common.var_util import var_util
from common.response_extractor import ResponseExtractor
from common.db_util import db_assert
from common.cleanup import CleanUpManager
from common.data_factory import data_factory
from core.retry import retry
from core.error_handler import on_failure
from core.report_enhancer import ReportEnhancer, performance_monitor

@allure.feature("功能模块")
@tag("module", "type")
class TestXxx:
    
    @allure.story("用户故事")
    @allure.title("测试标题")
    @smoke_test
    @priority("P0")
    @retry(max_attempts=3)
    @on_failure
    @performance_monitor
    def test_xxx(self, login_token, test_context):
        """测试描述"""
        test_name = test_context["test_name"]
        
        # 生成测试数据
        test_data = data_factory.create_xxx_data()
        
        # 添加请求到报告
        ReportEnhancer.add_request_details(url, method, headers, params)
        
        # 执行请求
        response = XxxApi.xxx(login_token, url, **params)
        
        # 提取变量
        ResponseExtractor.extract(response, {"id": "$.data.id"})
        
        # 添加响应到报告
        ReportEnhancer.add_response_details(status_code, response.json())
        
        # 断言
        assert response.status_code == 200
        
        # 数据库验证
        db_assert.assert_exists("table", "id = %s", (var_util.get_var("id"),))
        
        # 注册清理
        CleanUpManager.register(test_name, cleanup_func, var_util.get_var("id"))
```

---

## ⚙️ 配置文件

### pytest.ini
```ini
[pytest]
testpaths = testcases
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -vs --alluredir=./report
markers =
    smoke
    regression
    priority
```

### conftest.py fixtures
```python
@pytest.fixture(scope="session")
def login_token():
    # 全局 token
    
@pytest.fixture(scope="function")
def test_context(request):
    # 测试上下文
```

---

## 🐛 常见问题

### Q: 如何在多个接口间共享数据？
```python
# 接口 A 提取数据
ResponseExtractor.extract(resp_a, {"user_id": "$.data.id"})

# 接口 B 使用数据
user_id = var_util.get_var("user_id")
resp_b = ApiB(user_id=user_id)
```

### Q: 如何确保测试数据被清理？
```python
# 在 setup 中创建，teardown 中自动清理
with CleanUpManager.context("test_name"):
    resource = create_resource()
    CleanUpManager.register("test_name", delete_resource, resource["id"])
```

### Q: 如何调试失败的测试？
```python
# 1. 查看日志
# 2. 查看错误截图
# 3. 查看保存的错误上下文
# 4. 查看 Allure 报告的详细步骤
```

---

## 📞 获取帮助

1. 查看 `OPTIMIZATION_SUMMARY.md` - 完整优化总结
2. 查看 `framework_guide.md` - 详细使用指南
3. 查看各模块源码中的文档字符串

---

**祝测试顺利！** 🎉
