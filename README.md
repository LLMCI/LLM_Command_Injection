# Employing LLM-Prompted Test Cases Command Injection Vulnerability Detection in Dynamic Programming: An Empirical Study

## About
We explored the ability of large language models for vulnerability detection in this project. Specifically, we evaluated the ability of GPT4 to detect potential command injection vulnerabilities in python functions. We conducted experiments using six well-known python third-party libraries (Django, Flask, TensorFlow, Scikit-learn, PyTorch and Langchain). In the experiments, GPT4 is first used to analyze python code and let it determine whether there is a vulnerability in the code, and it is asked to generate security tests for the code that it considers vulnerable, and we run the test code manually to verify GPT's judgment. Through our experiments, we found that GPT4 has an accuracy of 78.5% in detecting whether a vulnerability exists in the code. This is much better than existing tool for detecting python security problems.

## Prerequisites
Our code can work on Ubuntu 22.04 OS and requires:
- Python (>= 3.6)
- dotenv
- openai

The experiments are performed on Ubuntu OS. The operation system can be downloaded on https://ubuntu.com/download/desktop, or you can download *.iso file and install it on vmware tools if you want to use windows system. There is Python installed in ubuntu os, you just need to check its version. You can use the following command to check the python version:

`sudo apt-get update `

`sudo apt-get upgrade `

`python --version `

And then you can use the following command to easily install these python libraries on Ubuntu: 

`pip install openai `

`pip install python-dotenv `

## Experiment
### Step1 Extract python(.py) files
You can find any python project online and download it to the the project folder.

Change the `foler_path ` in `extractfile.py ` to the actual path in your computer:

`source_folder = "folder_path" `

`destination_folder = "folder_path" `




