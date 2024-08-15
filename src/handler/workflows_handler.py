import os
import json
from enum import Enum

class WorkFlow:
    def __init__(self, display_name, file_path):
        self.display_name = display_name
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

def create_workflow_enum(directory):
    workflows = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            name = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)
            workflows[name.upper()] = (name, file_path)

    class WorkFlows(Enum):
        def __new__(cls, display_name, file_path):
            obj = object.__new__(cls)
            obj._value_ = display_name
            obj.display_name = display_name
            obj.file_path = file_path
            obj.data = WorkFlow.load_json(obj)
            return obj

        @classmethod
        def load_json(cls, obj):
            with open(obj.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

    return WorkFlows('WorkFlows', workflows)

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构造 workflow 目录的路径
workflow_dir = os.path.join(current_dir, 'workflow')

# 确保 workflow 目录存在
if not os.path.exists(workflow_dir):
    raise FileNotFoundError(f"Workflow directory not found: {workflow_dir}")

# 创建 WorkFlows 枚举
WorkFlows = create_workflow_enum(workflow_dir)

# 打印所有工作流
def print_all_workflows():
    for wf in WorkFlows:
        print(f"{wf.display_name}: {wf.file_path}")
        # 如果需要，你也可以打印 JSON 数据
        # print(f"Data: {wf.data}")

# 根据名称获取工作流
def get_workflow_by_name(name):
    for wf in WorkFlows:
        if wf.display_name == name:
            return wf
    return None

if __name__ == "__main__":
    print("Available workflows:")
    print_all_workflows()

    # 测试 get_workflow_by_name 函数
    test_name = "高级文生图"  # 假设这是其中一个 JSON 文件的名称（不包括 .json 扩展名）
    result = get_workflow_by_name(test_name)
    if result:
        print(f"\n找到工作流: {result.display_name}")
        print(f"文件路径: {result.file_path}")
        print(f"JSON 数据: {result.data}")
        print(f"JSON 数据类型: {type(result.data)}")
        print(f"JSON 数据类型: {json.dumps(result.data)}")

    else:
        print(f"\n未找到名为 '{test_name}' 的工作流")
