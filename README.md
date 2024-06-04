# Employing LLM-Prompted Test Cases Command Injection Vulnerability Detection in Dynamic Programming: An Empirical Study

## About
We explored the ability of large language models for vulnerability detection in this project. Specifically, we evaluated the ability of GPT4 to detect potential command injection vulnerabilities in python functions. We conducted experiments using six well-known python third-party libraries (Django, Flask, TensorFlow, Scikit-learn, PyTorch and Langchain). In the experiments, GPT4 is first used to analyze python code and let it determine whether there is a vulnerability in the code, and it is asked to generate security tests for the code that it considers vulnerable, and we run the test code manually to verify GPT's judgment. Through our experiments, we found that GPT4 has an accuracy of 78.5% in detecting whether a vulnerability exists in the code. This is much better than existing tool for detecting python security problems.

## Prerequisites
Our code can work on Ubuntu 22.04 OS and requires:
- Python (>= 3.6)
- dotenv
- openai

In addition, you need to sign up an openai account and add payment methods to get the permission to using the openai API. You can do these on https://openai.com/.

The experiments are performed on Ubuntu OS. The operation system can be downloaded on https://ubuntu.com/download/desktop, or you can download *.iso file and install it on vmware tools if you want to use windows system. There is Python installed in ubuntu os, you just need to check its version. You can use the following command to check the python version:

`sudo apt-get update `

`sudo apt-get upgrade `

`python --version `

And then you can use the following command to easily install these python libraries on Ubuntu: 

`pip install openai `

`pip install python-dotenv `

### Worflow
Here is the workflow for our experiment:
![IMAGE](https://github.com/LLMCI/LLM_Command_Injection/blob/main/workflow.png)
Our experiment consists of five steps:
- Filtering python files 
- Filtering candidate functions(Python functions containing methods that could lead to command injection vulnerabilities)
- Let GPT4 determine if there is a command injection vulnerability in the candidate functions
- Asking GPT4 generate security tests for functions that it determines are vulnerable
- Manually modify and run the security tests

## Experiment
### Step1 Extract python(.py) files
In our experiments, we selected six well-known python third-party libraries (Django, Flask, TensorFlow, Scikit-learn, PyTorch and Langchain) to do the test. 
The following version numbers are the ones of the projects used in the experiments：

     Django 4.2.7 
     Flask 3.0.0 
     Langchain v0.0.330 
     Tensorflow 2.14.0 
     Scikit-learn 1.3.2 
     PyTorch 2.1

We download them to the `python_projects` folder. But you can find any python project online and download it to the `python_projects` folder.

Change the `foler_path ` in `extractfile.py ` to the actual path in your computer:

`source_folder = "folder_path" `

`destination_folder = "folder_path" `

Where `source_folder ` is the path to the python project folder you downloaded, and `destination_folder ` is the path to the new folder you extracted the python files from the project to.

In our experiment, we extracted the python files from all 6 python libraries into the corresponding subfolders in the `dataset ` folder, e.g., all python files from the Django library were extracted into the `django ` folder in `dataset `.

### Step2 Extract python(.py) files




