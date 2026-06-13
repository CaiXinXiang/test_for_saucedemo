# SauceDemo 自动化测试项目

基于 **Python + Selenium + pytest** 的 Web 自动化测试框架，使用 Page Object 设计模式，对 [SauceDemo](https://www.saucedemo.com/) 电商演示站进行端到端功能测试。

## 项目结构

```
saucedemo-test-automation/
├── SauceDemo_测试用例.xlsx          # Excel 测试用例文档（35条）
│   ├── 测试用例                    # 专业格式测试用例
│   ├── 测试数据                    # 测试账号信息
│   └── 覆盖概览                    # 按模块/优先级统计
├── generate_testcases.py           # Excel 测试用例生成器
├── test_saucedemo.py               # 全流程自动化脚本
├── conftest.py                     # pytest 配置（fixture: WebDriver 管理）
├── pages/                          # 页面对象层
│   ├── base_page.py                # 基础页面（通用操作封装）
│   ├── login_page.py               # 登录页
│   ├── inventory_page.py           # 商品列表页
│   ├── cart_page.py                # 购物车页
│   └── checkout_page.py            # 结算页
├── tests/                          # POM 测试用例
│   ├── test_login.py               # 登录模块（4 条）
│   ├── test_inventory.py           # 商品列表模块（4 条）
│   ├── test_cart.py                # 购物车模块（2 条）
│   └── test_checkout.py            # 结算模块（2 条）
├── reports/                        # 测试报告输出
├── requirements.txt
└── README.md
```

## 技术栈

| 技术 | 说明 |
|------|------|
| Python 3 | 编程语言 |
| Selenium WebDriver | 浏览器自动化 |
| pytest | 测试框架 |
| pytest-html | HTML 测试报告 |
| Page Object Model | 设计模式 |

## 测试覆盖

### Excel 测试用例（35 条）

| 测试模块 | 用例数 | 优先级分布 |
|---------|--------|-----------|
| 登录 | 16 条 | P0~P3 |
| 商品浏览 | 5 条 | P0/P2 |
| 购物车 | 4 条 | P1/P2 |
| 结账 | 6 条 | P0~P2 |
| 异常账户 | 3 条 | P2/P3 |
| 退出 | 1 条 | P1 |

### POM 自动化测试（12 条）

### 登录模块
- ✅ 正确账号密码登录成功
- ✅ 错误密码登录失败
- ✅ 空用户名登录失败
- ✅ 锁定账号登录失败

### 商品列表模块
- ✅ 商品列表正常加载（6 个商品）
- ✅ 按名称升序排序
- ✅ 按价格降序排序
- ✅ 添加商品后购物车徽标更新

### 购物车模块
- ✅ 空购物车页面展示
- ✅ 从购物车移除商品

### 结算模块
- ✅ 完整结算流程
- ✅ 结算信息缺失校验

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行全部测试
pytest tests/ -v

# 3. 运行并生成 HTML 报告
pytest tests/ -v --html=reports/report.html --self-contained-html

# 4. 运行单个模块
pytest tests/test_login.py -v
```

## 设计要点

- **Page Object 模式**：页面元素定位与业务操作分离，提高可维护性
- **Fixture 复用**：`logged_in_driver` fixture 自动完成登录，减少重复代码
- **显式等待**：使用 `WebDriverWait` 确保元素就绪后再操作，避免时序问题
- **JS Click**：headless 模式下使用 `execute_script` 绕过元素拦截问题
