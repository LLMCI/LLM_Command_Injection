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
    
    sudo apt-get update
    
    sudo apt-get upgrade 
    
    python --version

And then you can use the following command to easily install these python libraries on Ubuntu: 

    pip install openai
     
    pip install python-dotenv

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

    source_folder = "folder_path"

    destination_folder = "folder_path"

Where `source_folder ` is the path to the python project folder you downloaded, and `destination_folder ` is the path to the new folder you extracted the python files from the project to.

After that, running `extractfile.py ` by the following command to execute this step.

    python3 extractfile.py

In our experiment, we extracted the python files from all 6 python libraries into the corresponding subfolders in the `dataset ` folder, e.g., all python files from the Django library were extracted into the `django ` folder in `dataset `.

### Step2 Extract candidate function 
Step2 is finding the candidate function from the python files in each python projects we extracted in the first step.

Change the `foler_path ` in `finding.py ` to the actual path in your computer

    directory = 'folder_path' 

The running `finding.py ` by the following command to find candidate functions in all 6 python projects.

    python3 finding.py

We need to find all the python functions which inclued the following methods(These methods can easily lead to command injection vulnerabilities): 

        'eval', 'exec', 'subprocess.call', 'subprocess.run', 'subprocess.Popen', 'subprocess.check_output', 'os.popen', 'os.system', 
        'os.spawnl', 'os.spawnle', 'os.spawnlp', 'os.spawnlpe', 'os.spawnv', 'os.spawnve', 'os.spawnvp', 'os.spawnvpe', 'os.posix_spawn()', 
        'os.posix_spawnp()', 'os.execl', 'os.execle', 'os.execlp', 'os.execlpe', 'os.execv', 'os.execve', 'os.execvp', 'os.execvpe'

We named these function as "candidate functions".

In our experiments, we store these candidate functions into the `test_dataset ` folder. Each file include on candidate function. 

### Step3 and step4 Let GPT4 determine if there is a command injection vulnerability in the candidate functions and generate security tests for functions that it determines are vulnerable
Step3 is the main part in our experiments, we asked GPT-4 to analysis code. 
Specifically, we let GPT-4 determine whether there is a command injection vulnerability in the candidate function, and if it thinks there is, it proceeds to generate a security test for this function.

For executing this task, you need to modify some parameters in the `gpt4script.py `.

First, changing `your LLM key ` to your own openai API key.

     openai.api_key  = 'your LLM key' 

Secondly, changing three `file_path ` to the actual path in the dvice.

     with open("file_path", "r") as file:

     with open("file_path", "w") as output_file:
         output_file.write(analysis_result)
        
     with open("file_path", "w") as output_file:
         output_file.write(testcase_result)

The first one need to change it to the file pathes in the `test_dataset `, such as `test_dataset/django/django1.py `, this is for letting GPT-4 read the contents of these candidate functions.

The second one is for storing the analysis results of GPT-4 to facilitate subsequent analysis. We stored it in the `test_analysis_result `.

The third one is for storing the security cases which GPT-4 generated. We stored it in the `test_output `.

Running `extractfile.py ` by the following command to execute the code: 

    python3 gpt4script.py

### Step5 Manually modify and run the security tests
Some of the security cases which generated by GPT-4 can't run directly. We need to modify them manually.
Through executing these security cases, we can verify the judgements of GPT-4. And then evaluating its performance on command injection vulnerability detection.



