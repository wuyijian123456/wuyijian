# 🏷️ 测试标签（Markers）使用指南

## 📋 已配置的标签列表

在 `pytest.ini` 中已配置以下标签，可以直接使用：

### 1️⃣ 测试类型标记

| 标签 | 说明 | 使用场景 |
|------|------|----------|
| `@pytest.mark.smoke` | 冒烟测试 | 核心功能快速验证，日常检查 |
| `@pytest.mark.regression` | 回归测试 | 确保现有功能正常，发布前验证 |
| `@pytest.mark.integration` | 集成测试 | 多接口联调，端到端测试 |
| `@pytest.mark.performance` | 性能测试 | 响应时间、并发测试 |

### 2️⃣ 优先级标记

| 标签 | 说明 | 执行频率 |
|------|------|----------|
| `@pytest.mark.P0` | 最高优先级 | 每次提交都执行 |
| `@pytest.mark.P1` | 高优先级 | 每天执行 |
| `@pytest.mark.P2` | 中优先级 | 每周执行 |
| `@pytest.mark.P3` | 低优先级 | 每月或按需执行 |

### 3️⃣ 功能模块标记

| 标签 | 说明 | 对应模块 |
|------|------|----------|
| `@pytest.mark.patient` | 病人管理 | 病人列表、病人信息 |
| `@pytest.mark.user` | 用户管理 | 用户登录、用户信息 |
| `@pytest.mark.order` | 订单管理 | 订单创建、查询、取消 |
| `@pytest.mark.auth` | 认证授权 | Token、权限验证 |
| `@pytest.mark.report` | 报表统计 | 数据统计、报表生成 |

### 4️⃣ 其他标记

| 标签 | 说明 | 使用场景 |
|------|------|----------|
| `@pytest.mark.critical` | 关键测试 | 影响上线的核心测试 |
| `@pytest.mark.wip` | 进行中 | 正在开发中的测试 |
| `@pytest.mark.skip` | 跳过测试 | 暂时不执行的测试 |

---

## 💡 使用方式

### 方式 1：使用 pytest.mark 装饰器（推荐）

```python
import pytest

@pytest.mark.smoke
@pytest.mark.P0
def test_login():
    """登录测试"""
    pass

@pytest.mark.regression
@pytest.mark.patient
def test_get_patient_list():
    """获取病人列表"""
    pass
```

### 方式 2：使用 common.marker 模块的便捷函数

```python
from common.marker import tag, priority, smoke_test

@tag("smoke", "patient")
@priority("P0")
@smoke_test
def test_patient_list():
    pass
```

### 方式 3：组合使用

```python
import pytest
from common.marker import tag, priority

@pytest.mark.smoke
@tag("critical")
@priority("P0")
def test_critical_feature():
    pass
```

---

## 🚀 运行带标签的测试

### 单个标签

```bash
# 运行冒烟测试
python -m pytest -m smoke -v

# 运行 P0 优先级测试
python -m pytest -m P0 -v

# 运行病人模块测试
python -m pytest -m patient -v
```

### 多个标签组合

```bash
# 运行 P0 优先级的冒烟测试
python -m pytest -m "smoke and P0" -v

# 运行病人或用户模块的测试
python -m pytest -m "patient or user" -v

# 运行病人模块的 P0 和 P1 测试
python -m pytest -m "(patient) and (P0 or P1)" -v
```

### 排除某些标签

```bash
# 运行非性能测试
python -m pytest -m "not performance" -v

# 运行非 WIP 的测试
python -m pytest -m "not wip" -v

# 运行除了病人模块外的所有测试
python -m pytest -m "not patient" -v
```

### 组合复杂条件

```bash
# 运行核心功能的 P0/P1 测试（排除性能测试）
python -m pytest -m "(smoke or critical) and (P0 or P1) and not performance" -v

# 运行病人和用户模块的回归测试
python -m pytest -m "(patient or user) and regression" -v
```

---

## 📊 标签最佳实践

### 1. 冒烟测试（Smoke Tests）
- ✅ 覆盖核心业务流程
- ✅ 执行时间短（< 5 分钟）
- ✅ 稳定性高
- ✅ 每天多次运行

```python
@pytest.mark.smoke
@pytest.mark.P0
def test_user_login():
    """用户登录 - 核心功能"""
    pass

@pytest.mark.smoke
@pytest.mark.P0
def test_create_order():
    """创建订单 - 核心业务"""
    pass
```

### 2. 回归测试（Regression Tests）
- ✅ 覆盖所有功能点
- ✅ 确保新代码不破坏旧功能
- ✅ 发布前必须执行

```python
@pytest.mark.regression
@pytest.mark.patient
def test_patient_crud():
    """病人增删改查 - 完整流程"""
    pass
```

### 3. 优先级划分

**P0 - 阻塞级**
```python
@pytest.mark.P0
@pytest.mark.critical
def test_payment():
    """支付功能 - 直接影响收入"""
    pass
```

**P1 - 重要级**
```python
@pytest.mark.P1
def test_send_email():
    """发送邮件 - 重要但非阻塞"""
    pass
```

**P2 - 一般级**
```python
@pytest.mark.P2
def test_export_excel():
    """导出 Excel - 辅助功能"""
    pass
```

**P3 - 低级**
```python
@pytest.mark.P3
def test_ui_theme():
    """UI 主题切换 - 锦上添花"""
    pass
```

### 4. 模块化标记

```python
# 病人模块
@pytest.mark.patient
class TestPatient:
    
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_get_patient_list(self):
        pass
    
    @pytest.mark.regression
    @pytest.mark.P1
    def test_update_patient(self):
        pass

# 用户模块
@pytest.mark.user
class TestUser:
    
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_login(self):
        pass
```

---

## 🎯 实际项目示例

### 示例 1：完整的测试类

```python
import pytest
import allure
from api.patient_api import PatientApi
from common.marker import tag, priority

@allure.feature("病人管理")
@pytest.mark.patient
class TestPatientManagement:
    """病人管理模块测试"""
    
    @allure.story("查询病人列表")
    @pytest.mark.smoke
    @pytest.mark.P0
    @pytest.mark.critical
    def test_get_patient_list_smoke(self, login_token):
        """冒烟测试：查询病人列表"""
        response = PatientApi.get_patient_list(login_token, ...)
        assert response.status_code == 200
    
    @allure.story("创建病人")
    @pytest.mark.regression
    @pytest.mark.P1
    def test_create_patient_regression(self, login_token):
        """回归测试：创建病人"""
        response = PatientApi.create_patient(login_token, ...)
        assert response.status_code == 200
    
    @allure.story("更新病人信息")
    @pytest.mark.integration
    @pytest.mark.P2
    def test_update_patient_integration(self, login_token):
        """集成测试：更新病人信息（涉及多个系统）"""
        # 先查询，再更新，最后验证
        pass
    
    @allure.story("批量导入病人")
    @pytest.mark.performance
    @pytest.mark.P3
    def test_batch_import_performance(self, login_token):
        """性能测试：批量导入病人（1000 条数据）"""
        # 测试响应时间和并发处理
        pass
```

### 示例 2：CI/CD 集成

**.gitlab-ci.yml 示例**
```yaml
stages:
  - test

# 提交时运行冒烟测试和 P0 测试
commit_tests:
  stage: test
  script:
    - python -m pytest -m "smoke or P0" -v

# 每日构建运行所有 P0 和 P1 测试
daily_build:
  stage: test
  script:
    - python -m pytest -m "P0 or P1" -v --alluredir=./report

# 发布前运行回归测试
pre_release:
  stage: test
  script:
    - python -m pytest -m regression -v --alluredir=./report
```

### 示例 3：不同环境的测试策略

**测试环境**
```bash
# 每天运行所有 P0、P1、P2 测试
python -m pytest -m "P0 or P1 or P2" --env test -v
```

**生产环境**
```bash
# 只运行冒烟测试和 P0 测试
python -m pytest -m "smoke or P0" --env prod -v
```

---

## ⚠️ 注意事项

### 1. 标签命名规范
- ✅ 使用小写字母
- ✅ 使用下划线分隔单词
- ❌ 不要使用大写字母
- ❌ 不要使用连字符

```python
# ✅ 正确
@pytest.mark.smoke_test
@pytest.mark.p0_priority

# ❌ 错误
@pytest.mark.SmokeTest
@pytest.mark.P0-Priority
```

### 2. 避免过度标记
```python
# ❌ 不要这样用
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
@pytest.mark.performance
def test_something():
    # 一个测试不应该属于太多类型
    pass

# ✅ 建议
@pytest.mark.smoke
def test_smoke():
    pass

@pytest.mark.regression
def test_regression():
    pass
```

### 3. 标签冲突处理
```python
# ❌ 避免冲突
@pytest.mark.skip
@pytest.mark.smoke  # 跳过的测试不应该标记为冒烟
def test_skip():
    pass

# ✅ 正确做法
@pytest.mark.wip  # 进行中的测试
def test_in_progress():
    pass
```

---

## 📈 标签统计报告

### 查看标签分布

```bash
# 收集测试信息
python -m pytest --collect-only -q

# 查看各标签的测试数量
python -m pytest --markers -v
```

### 生成标签报告

```python
# conftest.py
import pytest

def pytest_collection_modifyitems(items):
    """统计各标签的测试数量"""
    markers_count = {}
    
    for item in items:
        for marker in item.iter_markers():
            name = marker.name
            markers_count[name] = markers_count.get(name, 0) + 1
    
    print("\n=== 测试标签分布 ===")
    for marker, count in sorted(markers_count.items()):
        print(f"{marker}: {count} 个测试")
```

---

## 🎓 总结

通过合理使用标签，可以：

✅ **快速筛选测试** - 按需执行特定类型的测试  
✅ **优化 CI/CD** - 在不同阶段运行不同测试集  
✅ **明确优先级** - 合理分配测试资源  
✅ **模块化管理** - 按功能模块组织测试  
✅ **灵活策略** - 针对不同环境制定测试策略  

**记住：好的标签体系 = 高效的测试管理！** 🎉
