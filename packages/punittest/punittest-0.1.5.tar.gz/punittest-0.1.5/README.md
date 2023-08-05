
# 简介
punittest 是基于 unittest 的第三方扩展 utx 的修改版本。使用起来非常方便，和 unittest 类似。

除了满足 unittest 的常用功能之外，还提供日志、html 报告、excel 组织用例、用例失败重新执行、利用 tag 加载用例等功能。
# 安装
**依赖库**
- openpyxl - 解析 xlsx 文件

如果是离线安装，请访问 PyPi 下载 tar.gz 压缩包后使用 pip 安装
```shell
pip install punittest-0.1.1.tar.gz
```
如果是联网环境，直接使用 pip 工具下载安装即可
```shell
pip3 install punittest
```

# 使用 Demo
demo 的测试用例都在 demo 目录的 testsuite 目录下：

运行 demo 目录下的 main.py：
```python
from punittest import SETTINGS, RELOAD_SETTINGS

SETTINGS.EXCEL_TEST_SET = True
SETTINGS.RUN_TAGS = ["All"]
SETTINGS.LOG_DIR = "D:\Temp\Logs"
SETTINGS.REPORT_DIR = "D:\Temp\Reports"
RELOAD_SETTINGS()


from punittest import TestRunner

runner = TestRunner("demo接口测试用例")
runner.run()

```
输出结果包含三部分：

- 控制台日志
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190505153314130.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzgzNzYy,size_16,color_FFFFFF,t_70)
- 日志文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190505153425972.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzgzNzYy,size_16,color_FFFFFF,t_70)
- html 报告
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190505153525204.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzgzNzYy,size_16,color_FFFFFF,t_70)

# 使用说明
- 使用 punittest 的日志器 logger
```python
from punittest import logger

logger.debug("xxx")
logger.info("xxx")
logger.warning("xxx")
logger.error("xxx")
```
- 使用 punittest 编写测试用例
```python
from punittest import PUnittest, logger


class TestLogin(PUnittest):
    """测试登录功能"""

    @PUnittest.tag("Smoke", "Regression")
    @PUnittest.data([{'user': 'username', 'pass': 'password'}], [True])
    def test_login_successfully(self, params, asserts):
        """测试登录成功"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)

    @PUnittest.tag("Regression")
    @PUnittest.data(
        [{'user': 'username', 'pass': '123'},
         {'user': '123', 'pass': 'password'},
         {'user': '', 'pass': ''}],
        [False, False, False])
    def test_login_failed(self, params, asserts):
        """测试登录失败"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = False
        self.assertTrue(_result, result)

    @PUnittest.skip("这里跳过不测")
    @PUnittest.tag("Regression")
    @PUnittest.data([{'user': 'username', 'pass': 'password'}], [True])
    def test_relogin_successfully(self, params, asserts):
        """测试重新登录成功"""
        _user, _passwd = params['user'], params['pass']
        _result = asserts
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)
        logger.info("调用登录接口，用户名/密码: {}/{}， 获取登录结果".format(_user, _passwd))
        result = True
        self.assertTrue(_result, result)
       
```
- 在入口文件 Main.py 中修改 punittest 的 SETTING 后重载
```python
from punittest import SETTINGS, RELOAD_SETTINGS
from Utils.Paths import *

# 在这里设置punittest的参数，然后调用RELOAD()重载
SETTINGS.TEST_EXCEL_PATH = TEST_CASE_EXCEL_PATH
SETTINGS.TEST_SUITE_DIR = TESTSUITE_PATH
SETTINGS.LOG_DIR = RESULTS_LOGS_PATH
SETTINGS.REPORT_DIR = RESULTS_REPORTS_PATH
SETTINGS.RUN_TAGS = ["Regression", "Smoke"]
SETTINGS.EXCEL_TEST_SET = True
RELOAD_SETTINGS()
```
- 再在入口文件 Main.py 中导入 TestRunner 并调用其 run() 方法运行测试
```python
from punittest.testrunner import TestRunner
# 调用TestRunner的run()方法运行测试框架
runner = TestRunner("XXX接口功能测试用例")
runner.run()
```

# 功能说明
- 组织测试用例
    - 使用装饰器组织
    - 使用 excel 表格组织
-  加载测试用例
    - 使用 unittest.TestLoader() 加载
    - 使用 excel 表格加载
- 执行测试
    - 断言
    - 异常处理 
    - 失败重新执行
- 获取测试结果
    - 日志
    - 测试报告
- 配置文件
## 1. 使用装饰器组织测试用例
punittest 为测试类中的测试方法提供了4种装饰器：skip, skip_if, data, tag。

测试类继承了 PUnittest 类后，测试方法即可使用这4种装饰器：
- skip - 跳过某一条测试用例（和 unittest 的 skip 用法一致）
```python
@PUnittest.skip("这里书写跳过的原因")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```
- skip_if - 在某种情况下跳过某一条测试用例（和 unittest 的 skip 用法一致）
```python
@PUnittest.skip_if(counter<10, "这里书写跳过的原因")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```
- data - 为测试方法传递参数
    data 接收2个参数 params 和 asserts，类型为 list，对应测试参数和断言的参数，两个列表的元素位置需要对应。
    被 data 装饰过的测试方法会根据参数列表中的元素数目将该条测试用例拆分成数个用例，分别使用对应的参数进行测试。
```python
@PUnittest.data([[1, 2], [-1, 1]], [3, 0])
def test_04(self, params, asserts):
    """测试04"""
    logger.info("hehe")
    result = params[0] + params[1]
    self.assertEqual(result, asserts)
```
```python
@PUnittest.data([{'user': 'user1', 'pass': 1}, {'user': 'user2', 'pass': 2}], [1, 2])
def test_07(self, params, asserts):
    """测试07"""
    result = params['pass']
    self.assertEqual(result, asserts)
```
- tag - 为测试用例添加 tag，在加载用例的时候可以加载指定 tag 的用例，不填写 tag 参数的则默认 tag 为 All 
```python
@PUnittest.tag("Smoke", "Regression")
def test_02(self):
    """测试02"""
    logger.debug("jaja")
    self.assertEqual(1, 2)
    self.assertEqual(1, 3)
```
## 2. 使用装饰器组织测试用例
excel_testset 目录中的 TestCases.xlsx 文件记录了需要测试的用例，格式如下：
![](https://img-blog.csdnimg.cn/20190429160942101.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzgzNzYy,size_16,color_FFFFFF,t_70)
- Priority - 测试用例优先级，和编码无关的属性，可以删除
- Tags - 测试用例标签，对应 tag 装饰器中的标签
- Skip - 是否跳过，如果需要跳过，则填写跳过内容，无内容则认为不跳过
- TestDir - 测试目录名称，测试文件所在的目录，多级菜单之间用 . 连接，如 TestSuite.TestSubSuite
- TestFile - 测试文件名称
- TestClass - 测试类名称
- TestCase - 测试用例名称
- CaseDescription - 测试用例描述
- ParamsData - 测试用例的测试参数，多个测试数据之间用换行符隔开，对应于 data 装饰器第一个参数列表中的元素
- AssertResult - 测试用例的断言参数，多个断言数据之间用换行符隔开，对应于 data 装饰器第二个参数列表中的元素

**可以对 excel 的标题进行过滤，punittest 只会运行过滤后依然显示的测试用例。**

## 3. 使用 unittest.TestLoader() 加载
在 settings.py 中进行设置，如果 EXCEL_TEST_SET = False，则需要填写 TEST_SUITE_DIR = ""，将需要将执行测试用例的目录地址填入 TEST_SUITE_DIR 。
```
# 是否从Excel表格中读取测试用例
EXCEL_TEST_SET = True

# 需要执行测试用例（python文件）的目录地址
TEST_SUITE_DIR = ""
```

punittest 会调用 unittest.TestLoader() 来加载已经组织过的用例，注意加载时不会识别 excel 文件中的内容，而是根据测试方法上的装饰器内容进行加载。

## 4. 使用 excel 表格加载
在 settings.py 中进行设置，如果 EXCEL_TEST_SET = True，则会根据 excel 中的设置进行加载。
```
# 是否从Excel表格中读取测试用例
EXCEL_TEST_SET = True
```

## 5. 断言
punittest.py 中的 PUnittest 类继承了 unittest.TestCase 类，但也进行了扩展：
- 针对断言行为添加了日志
- 为断言失败添加了异常队列，在同一条用例中出现断言失败，不再会终止用例，而是继续执行，直到结束后再抛出所有的断言异常

如果需要让断言方法添加以上 2 种扩展功能，则需要在 PUnittest 类中显式地重定义一次相应的断言方法即可：
```python
class PUnittest(unittest.TestCase, metaclass=Meta):
    
    def assertEqual(self, first, second, msg=None):
        super(PUnittest, self).assertEqual(first, second, msg=msg)

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        super(PUnittest, self).assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    def assertDictEqual(self, d1, d2, msg=None):
        super(PUnittest, self).assertDictEqual(d1=d1, d2=d2, msg=msg)
```

## 6. 异常处理 
测试用例执行过程中一旦发现异常，则会终止该用例的测试，抛出异常，和 unittest 保持一致。不像改写过的断言过程会有异常列表。

## 7. 失败重新执行
settings.py   进行设置，数字设置为1，则失败后不会重新执行，>1 则会重新执行。
```
CASE_FAIL_RERUN = 1
```

**请注意重新执行的用例不会再重新执行 setUp 和 tearDown 过程。**

## 8. 日志
PUnittest 提供 3 种类型的日志，分别是控制台，日志文件和测试报告日志，都有开关控制是否开启，3 种日志能分别设置日志级别。这些可以在 settings.py 中进行设置。
```
# 日志文件存放的目录
LOG_DIR = os.path.join(_base, "logs")

# 过滤日志的级别
LOG_CONSOLE_LEVEL = "DEBUG"
LOG_FILE_LEVEL = "DEBUG"
LOG_REPORT_LEVEL = "DEBUG"

# 是否开启日志的开关
LOG_CONSOLE_SWITCH = True
LOG_FILE_SWITCH = False
LOG_REPORT_SWITCH = True
```

## 9. 测试报告
PUnittest 会自动生成一份 html 形式的测试报告，供测试者查阅。相关设置如下：
```
# 报告文件存放的目录
REPORT_DIR = os.path.join(_base, "reports")
```
## 10. 配置文件
配置文件是 settings.py，可以编写 python 代码
```python
class Settings:

    _root = os.path.abspath(os.path.dirname(__file__))
    _base = os.path.abspath(os.path.dirname(_root))

    # 日志文件存放的目录
    LOG_DIR = os.path.join(_base, "logs")
    # 报告文件存放的目录
    REPORT_DIR = os.path.join(_base, "reports")
    # 需要执行测试用例（python文件）的目录地址
    TEST_SUITE_DIR = ""
    # 需要执行测试用例（excel文件）的地址
    TEST_EXCEL_PATH = os.path.join(_root, "excel_testset", "TestCases.xlsx")

    # 过滤日志的级别
    LOG_CONSOLE_LEVEL = "DEBUG"
    LOG_FILE_LEVEL = "DEBUG"
    LOG_REPORT_LEVEL = "DEBUG"

    # 是否开启日志的开关
    LOG_CONSOLE_SWITCH = True
    LOG_FILE_SWITCH = False
    LOG_REPORT_SWITCH = True

    # 测试用例执行次数（>=1 则失败后会重新执行）
    CASE_FAIL_RERUN = 1
    # 是否从Excel表格中读取测试用例
    EXCEL_TEST_SET = True
    # 执行包含如下Tags的测试用例
    RUN_TAGS = "Regression, Smoke"
```
使用配置文件时不需要修改源码，而是在入口文件中先导入 punittest.SETTINGS，修改 SETTINGS 项后调用 RELOAD_SETTINGS 即可，比如：
```python
from punittest import SETTINGS, RELOAD_SETTINGS

SETTINGS.EXCEL_TEST_SET = True
SETTINGS.RUN_TAGS = ["All"]
SETTINGS.LOG_DIR = "D:\Temp\Logs"
SETTINGS.REPORT_DIR = "D:\Temp\Reports"
RELOAD_SETTINGS()


from punittest import TestRunner

runner = TestRunner("demo接口测试用例")
runner.run()
```

# 文件说明
- excel_testset - 存放 excel 用例文件的目录
- report - 存放 html 报告模板的目录
- static - 存放 html 报告模板所需 css 和 js 的目录
- utils - 工具目录，提供日志格式和 excel 解析方法
- punittest - PUnittest 供测试类继承，以便调用相应的装饰器
- testcase - 提供测试方法的装饰器，并且会在加载过程中动态修改名称和添加测试参数
- testresult - 处理测试用例的测试结果
- testrunner - 执行 run() 方法执行测试，产生 html 测试报告
- testset - make_test_suite() 方法加载测试集
- settings - 配置文件
