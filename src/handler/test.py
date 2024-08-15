import json

from prompt_handler import update_prompt
from workflows_handler import get_workflow_by_name

def test():
    pre_prompt = "Expand the following content in English, including detailed descriptions, artistic style, masterful works, high quality, and intricate details, and condense it into a single paragraph of no more than 100 words:" + "一个女孩"
    workflowResult = get_workflow_by_name("高级文生图")
    # print(json.dumps(workflowResult.data))
    workflowJson = json.dumps(workflowResult.data)

    result = update_prompt(json.loads(workflowJson), pre_prompt)
    print(result)

if __name__ == '__main__':
    test()
