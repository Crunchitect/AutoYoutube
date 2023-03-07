# AutoYoutube

An automatic [YouTube](https://youtube.com) video maker. (still in dev)

### How to use
1. Install and unzip the installed folder.
2. Get OpenAI credentials by going to [OpenAI's ChatGPT](https://chat.openai.com/chat) and go to dev tools by clicking `F12`.
3. Go to find `__Secure-next-auth.sesstion-token` by `Devtools` > `Application` > `Storage` > `Cookies`
   ![Cookies](\ReadmeImages\cookies.png)
4. Create a `creds.py` file and write this in
```python 
session_token = '[SESSION TOKEN HERE]' 
```
Replace the '[SESSION TOKEN HERE]' with your token from step 3.
5. Run the `main.py` file (`main.exe`, might be in the directory soon),