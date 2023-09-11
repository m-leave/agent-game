1.填入openai的api-key

2.运行action.py，会从log中分析最近的status和object

3.根据人物基本信息，短期记忆，推理出目前情况下最可能做出的反应和对话

4.使用reflect方法，从旧的summary_memory.json和最近发生过的events中，总结发生过的事情，覆盖写入summary_memory.json
