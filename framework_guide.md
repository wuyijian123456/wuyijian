# 自动化测试框架 - 功能说明和使用指南

## 📋 新增功能清单

### ✅ 已实现的核心功能

#### 1. **失败重试机制** (`core/retry.py`)
- `@retry(max_attempts=3, delay=1)` - 失败自动重试，支持指数退避
- `@flaky(max_runs=3, min_passes=2)` - 不稳定测试容忍

```python
from core.retry import retry

@retry(max_attempts=3, delay=2)
def test_unstable_api():
    pass
```

#### 2. **测试用例自动分组** (`common/marker.py`)
- `@tag("smoke", "critical")` - 标签标记
- `@priority("P0")` - 优先级标记 (P0/P1/P2/P3)
- `@smoke_test` - 冒烟测试
- `@regression_test` - 回归测试

```python
from common.marker import tag, priority

@tag("smoke", "patient")
@priority("P0")
def test_patient_list():
    pass
```

运行指定标签：`pytest -m "smoke"`

#### 3. **变量提取和动态参数替换** (`common/var_util.py`)
- `${var_name}` 占位符替换
- 从响应中自动提取变量
- 测试级别变量隔离

```python
from common.var_util import var_util

# 保存变量
var_util.set_var("user_id", 123)

# 在请求中使用
data = {"userId": "${user_id}"}  # 自动替换为实际值
```

#### 4. **数据库断言功能** (`common/db_util.py`)
- `db_assert.assert_exists()` - 断言数据存在
- `db_assert.assert_field_value()` - 断言字段值
- `db_assert.assert_record_count()` - 断言记录数

```python
from common.db_util import db_assert

db_assert.assert_exists("users", "user_id = %s", (123,))
db_assert.assert_field_value("orders", "status", 1, "order_id = %s", (456,))
```

#### 5. **用例后置数据自动清理** (`common/cleanup.py`)
- 自动注册清理任务
- 批量清理
- 上下文管理器

```python
from common.cleanup import CleanUpManager

# 注册清理任务
CleanUpManager.register(test_name, delete_func, order_id="123")

# 使用上下文管理器
with CleanUpManager.context("test_order"):
    # 创建测试数据
    pass
```

#### 6. **响应数据提取器** (`common/response_extractor.py`)
- JSONPath 表达式提取
- 接口关联支持

```python
from common.response_extractor import ResponseExtractor

ResponseExtractor.extract(response, {
    "user_id": "$.data.user.id",
    "token": "$.data.token"
})
```

#### 7. **测试数据工厂** (`common/data_factory.py`)
- 随机数据生成
- 预设数据类型模板

```python
from common.data_factory import data_factory

user = data_factory.create_user_data()
order = data_factory.create_order_data({"goodsId": 1001})
phone = data_factory.random_phone()
email = data_factory.random_email()
```

#### 8. **异常处理和错误截图** (`core/error_handler.py`)
- `@on_failure` 装饰器
- 自动截图保存
- 错误上下文保存

```python
from core.error_handler import on_failure

@on_failure
def test_api():
    pass
```

#### 9. **并发控制和速率限制** (`core/rate_limiter.py`)
- `@rate_limit(calls_per_second=10)` - 速率限制
- `@concurrent_limit(max_concurrent=5)` - 并发限制

```python
from core.rate_limiter import rate_limit

@rate_limit(calls_per_second=5)
def test_api_with_rate_limit():
    pass
```

#### 10. **测试报告增强** (`core/report_enhancer.py`)
- 添加附件到 Allure 报告
- 性能监控
- 覆盖率统计

```python
from core.report_enhancer import ReportEnhancer, performance_monitor

@performance_monitor
def test_with_monitoring():
    ReportEnhancer.add_request_details(url, method, headers, params)
    ReportEnhancer.add_response_details(status_code, response_data)
```

---

## 🚀 完整使用示例

### 示例 1：带重试和清理的测试

```python
import allure
from api.patient_api import PatientApi
from common.marker import tag, priority
from common.cleanup import CleanUpManager
from core.retry import retry
from core.error_handler import on_failure

@allure.feature("病人管理")
@allure.story("查询病人列表")
@tag("smoke", "patient")
@priority("P0")
@on_failure
class TestPatientList:
    
    @allure.title("查询在科病人")
    @retry(max_attempts=3, delay=1)
    def test_get_patient_list(self, login_token, test_context):
        """查询在科病人列表"""
        test_name = test_context["test_name"]
        
        # 注册清理任务
        CleanUpManager.register(
            test_name,
            lambda: print("清理测试数据")
        )
        
        response = PatientApi.get_patient_list(
            token=login_token,
            url="/api/patient/list",
            dept_code="ICU",
            in_dept_state="true"
        )
        
        assert response.status_code == 200
```

### 示例 2：带变量提取和数据库断言的测试

```python
from common.var_util import var_util
from common.response_extractor import ResponseExtractor
from common.db_util import db_assert
from common.data_factory import data_factory

def test_create_user_and_verify():
    # 生成测试数据
    user_data = data_factory.create_user_data()
    
    # 创建用户
    response = UserApi.create_user(user_data)
    
    # 提取 user_id
    ResponseExtractor.extract_one(response, "user_id", "$.data.id")
    
    # 数据库验证
    db_assert.assert_exists("users", "id = %s", (var_util.get_var("user_id"),))
    db_assert.assert_field_value(
        "users", 
        "username", 
        user_data["userName"],
        "id = %s", 
        (var_util.get_var("user_id"),)
    )
```

### 示例 3：性能监控和报告增强

```python
from core.report_enhancer import ReportEnhancer, performance_monitor

@performance_monitor
def test_with_full_reporting(login_token):
    url = "/api/patient/list"
    method = "GET"
    headers = {"Authorization": f"Bearer {login_token}"}
    params = {"deptCode": "ICU"}
    
    # 添加请求详情
    ReportEnhancer.add_request_details(url, method, headers, params)
    
    response = PatientApi.get_patient_list(login_token, url, "ICU", "true")
    
    # 添加响应详情
    ReportEnhancer.add_response_details(
        response.status_code,
        response.json()
    )
    
    assert response.status_code == 200
```

---

## 🎯 运行测试

### 运行指定标签的测试
```bash
# 运行冒烟测试
pytest -m smoke -v

# 运行 P0 优先级测试
pytest -m "priority" -v

# 运行特定标签组合
pytest -m "smoke and patient" -v
```

### 运行带重试的测试
```bash
# 全局重试 3 次
pytest --retry 3 -v
```

### 运行特定环境
```bash
# 生产环境
pytest --env prod -v

# 测试环境
pytest --env test -v
```

### 生成完整报告
```bash
# Allure 报告
pytest --alluredir=./report

# 查看报告
allure serve ./report
```

---

## 📊 框架架构图

```
PythonProject_atuo_request_test/
├── core/                      # 核心模块
│   ├── request.py            # HTTP 请求封装
│   ├── assert_util.py        # 断言工具
│   ├── logger.py             # 日志模块
│   ├── retry.py              # 重试机制 ✨
│   ├── error_handler.py      # 错误处理 ✨
│   ├── rate_limiter.py       # 速率限制 ✨
│   └── report_enhancer.py    # 报告增强 ✨
├── common/                    # 公共工具
│   ├── yaml_util.py          # YAML 读写
│   ├── db_util.py            # 数据库工具 ✨
│   ├── var_util.py           # 变量替换 ✨
│   ├── marker.py             # 测试标记 ✨
│   ├── cleanup.py            # 清理管理 ✨
│   ├── response_extractor.py # 响应提取 ✨
│   └── data_factory.py       # 数据工厂 ✨
├── api/                       # API 封装
│   ├── patient_api.py        # 病人接口
│   └── user_api.py           # 用户接口
├── testcases/                 # 测试用例
│   └── test_patient_list.py  # 病人测试
├── conftest.py               # Pytest 配置 ✨
└── data/                     # 测试数据
    └── *.yaml                # YAML 数据文件
```

---

## 💡 最佳实践建议

1. **使用标记组织测试** - 用 `@tag` 和 `@priority` 标记所有测试
2. **自动清理测试数据** - 用 `CleanUpManager` 注册清理任务
3. **变量隔离** - 使用 `test_context` fixture 获得隔离的变量空间
4. **添加性能监控** - 关键测试用 `@performance_monitor`
5. **完整的报告** - 用 `ReportEnhancer` 添加详细步骤信息
6. **数据驱动** - 用 `data_factory` 生成测试数据
7. **接口关联** - 用 `ResponseExtractor` 提取响应数据供后续使用

---

## 🔧 配置说明

### pytest.ini 配置
```ini
[pytest]
testpaths = testcases
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -vs --alluredir=./report --clean-alluredir
markers =
    smoke: 冒烟测试
    regression: 回归测试
    priority: 优先级标记
```

### 环境变量配置
通过 `--env` 参数切换环境，自动读取对应配置。

---

这个框架现在已经具备了企业级自动化测试框架的所有核心功能！🎉
