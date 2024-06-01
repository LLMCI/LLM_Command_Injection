Yes, this code has potential command/code injection vulnerability. 

The reason is that it uses the exec() function, which is a potentially dangerous function that executes the Python code it is passed as a string. This can be a serious security risk if you're executing strings of code that you haven't generated yourself or strings that can be modified by an attacker. 

In this case, the string being executed is 'computed' + 5 + 'stuff', which will actually cause a TypeError because you can't concatenate a string and an integer. However, if the integer was instead a string that was being input by a user or from another untrusted source, then they could potentially input malicious code that would then be executed by the exec() function. 

Therefore, it's generally recommended to avoid using exec() if possible, especially with strings that can be influenced by an outside source.