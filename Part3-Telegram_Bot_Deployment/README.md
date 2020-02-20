## Part 3: Setup the Telegram Bot channel and deploy bot python script to Heroku for Free!

1. Before we deploy our bot to heroku server, we should do a local test first like before. Continue to setup telegram bot first.
2. Register an account with Telegram if you haven't done so.  Search for [@BotFather](https://telegram.me/BotFather) on telegram
Type in the following:
> /start  

> /newbot. 

Follow the prompt and complete the creation of the new bot.  
A token will be created like below and a link to the new bot channel. (The token here is just a sample and has been revoked)  
![telegram bot registration](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part3/1-telegram-bot-registration.jpg)

3. Create a new directory and a new virtual environment. You should be very familiar with creating virtual environment at this point. Install telegram bot package
```
pip install python-telegram-bot
```

4. Download bot.py in this repo to your virtual environment. Open the file with Visual Studio Code and replace the AZURE ENDPOINT and BOT TOKEN with your own token.

5. Run bot.py in your cmd and keep it running.
```
python bot.py
```
6. Go to your new bot channel and try sending a image of a dog. You should be getting a response! Press ctrl-c twice to stop the script and the bot will stop working.  
![Bot predicted class](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part3/2-image_bot_predicted_class.png)

## Setup Heroku free server to run it online.
1. You wouldn't want to have to leave your pc on 24 hours just to let the bot function. Therefore the best option is to transfer it onto a server. There are couple of options, here we will be using heroku to deploy for FREE!

2. Now to get ready for the deployment, register [heroku account](https://www.heroku.com/) if you haven't done so. Make sure you have also installed [heroku CLI for windows](https://devcenter.heroku.com/articles/heroku-cli) and [git](https://git-scm.com/downloads)

3. Pip freeze your requirements (Remember this is to be done in a new directory and new virtual environment)
```
pip freeze > requirements.txt
```
4. Create a new file **Procfile** without extension in the same dir and type in 
```
web: python heroku_bot.py
```
This is used to execute commands in heroku. 
You can either create the file with notepad or do it in Visual Studio Code as shown below.

![No extension](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part3/3-No-extension.png)

5. Create the heroku app url. Enter this command and copy the url generated (The url can also be retrieve from heroku dashboard.)
```
heroku create 
```
![Heroku url](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part3/4-heroku_url.jpg)

6. Download **heroku_bot.py** in this repo. The code are similar to **bot.py** with some modification. Open the file with Visual Studio Code and replace your own
* **AZURE ENDPOINT** 
* **BOT TOKEN**

Replace the **url** (from step 5) for the webhook which should be near line 64 in Visual Studio Code
```
#Replace your heroku url here

updater.bot.set_webhook("https://<your_heroku_url_name>.herokuapp.com/{}".format(BOT_TOKEN))
```


7. Time to git. 
Ensure the following files you just created are in the same directory
* heroku_bot.py
* Procfile
* requirements.txt

Enter the following command in the same directory
```
git init
```

Buffer to add all local files in this directory
```
git add . 
```
```
git commit -m "first commit"
```
Finally
```
git push heroku master
```

You will see in the log if push successful

>2020-02-18T05:50:25.370657+00:00 heroku[web.1]: Starting process with command `python heroku_bot.py`
2020-02-18T05:50:27.715757+00:00 app[web.1]: 2020-02-18 05:50:27,715 - __main__ - INFO - Starting bot
2020-02-18T05:50:28.218517+00:00 heroku[web.1]: State changed from starting to up
2020-02-18T05:50:30.000000+00:00 app[api]: Build succeeded

8. Run the following command to monitor the process in cmd
```
heroku logs -t
```
Now go to your telegram channel and try sending images to test the bot.
And now you got yourself a 24 hour running bot!


## IMPORTANT  - *Delete Resource Group in Azure Functions*

When you are done, delete the resource group if you are not going to deploy Telegram BOT. You can also delete after deploying and testing Telegram bot. If you are on one month trial for Azure Functions , set timer or calendar to remind yourself.

az group delete \  
--name <RESOURCE_GROUP> \  
--yes

Remember that with the App Service plan, you are being charged for as long as you have resources running, even if you are not calling the function. So it is best to delete the resource group when you are not calling the function to avoid unexpected charges.
