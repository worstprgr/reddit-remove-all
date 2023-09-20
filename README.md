# Reddit Post Remover

This script removes **all posts and comments** you ever made on Reddit.  
Since Reddit does not provide a "nuke all" option, we have to do it.

## Installation
1. You'll need Selenium https://selenium-python.readthedocs.io/installation.html
    ```text
    pip install selenium
    ```

2. Running Chrome or Firefox in debug mode via a command line
   ```text
   <path to chrome>/chrome.exe --remote-debugging-port=9222
   ```
   ```text
   <path to firefox>/firefox.exe -marionette -start-debugger-server 2828
   ```
   The debug port for Firefox is fixed by Firefox itself. So you have to stick with it.  
   The debug port for Chrome is customizable, but you have to change it in the **postremover.py** too.
   In the initializer of the class **PostRemover** you can modify the port at: **self.debug_port_chrome = 9222**

## Usage (Basic)
Because we're using the browser in debug mode, we can use the existing session of Reddit.  
1. The browser must be open in debug mode
2. You need to be logged in on Reddit. It doesn't matter if you have the page already open
   since it creates a new tab anyway
3. Open a command line with the following command
   ```text
   py <path to the script>/pr-cli.py <RedditUserName> <Mode> <Browser>
   ```
   For &lt;Browser> you have the choice between 'C' (Chrome) and 'F' (Firefox)  
   And for &lt;Mode> your have the choice between 'p' (delete posts) and 'c' (delete comments)
   Example:
   ```text
   py C:/Users/Steve/Scripts/reddit-remove-posts/pr-cly.py steve p C
   ```
   
## Usage (Advanced)
If you want to use it inside a script:
```python
import postremover

postrem = postremover.PostRemover('<REDDIT_USERNAME>', '<MODE>, '<BROWSER>')
postrem.deletePost()
```

## Compatibility
|        | Chrome     | Firefox    |
|--------|------------|------------|
| Win 11 | Yes        | Yes        |
| Win 10 | Yes        | Yes        |
| Ubuntu | not tested | not tested |
| Debian | not tested | not tested |


## How It Works
The starting point is the method **deletePost()**
1. **__checkUsernameExist()**: Check if the username even exist
2. **__checkLogin()**: Check if the user has an active session
3. **__checkCurrentUsername()**: Check if the active session matched the provided username
4. Running the deletion routine

## Disclaimer
You're using this script at your own responsibility. There's no way to restore your comments and posts by this script.  
If you want to restore deleted comments and posts, you have to contact the Reddit support, but I'm unsure if they're  
providing such an option.  

## Bugs
If you encounter some bugs, you can open an issue on GitHub. Please follow the template below:
1. Description of the issue
2. Step-by-Step Reproduction
3. If present: exception message/stacktrace

## Contributing
You can open a pull request. Or even fork it and implement more features

