# Employing LLM-Prompted Test Cases Command Injection Vulnerability Detection in Dynamic Programming: An Empirical Study

# About
We explored the ability of large language models for vulnerability detection in this project. Specifically, we evaluated the ability of GPT4 to detect potential command injection vulnerabilities in python functions. We conducted experiments using six well-known python third-party libraries (Django, Flask, TensorFlow, Scikit-learn, PyTorch and Langchain). In the experiments, GPT4 is first used to analyze python code and let it determine whether there is a vulnerability in the code, and it is asked to generate security tests for the code that it considers vulnerable, and we run the test code manually to verify GPT's judgment. Through our experiments, we found that GPT4 has an accuracy of 78.5% in detecting whether a vulnerability exists in the code. This is much better than existing tool for detecting python security problems.
