# FASTAI Image Classification with Azure Function and Telegram bot Deployment ( Under Construction: Last update 20 Feb 2020)
A mini project that uses FASTAI Image Classification to classify 3 types of dogs namely, **Pug, French Bulldog,** and **Boston Terrier**.  The trained model will be deployed to Azure Function and the user can send in their dog images to Telegram bot which will reply with the type of breed.

Telegram Bot Demo( Welcome to try at [Dog Whisperer Bot](https://t.me/DogWhispererAi_bot) - t.me/DogWhispererAi_bot)  

![Telegram Bot Gif](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/telegrambot_sample.gif)

## Who is this for
As a beginner who has gone through many online machine learning tutorials and MOOC, I noticed there is a lack of hands-on the gathering of data and deployment of models. It is only until recently that I have completed [Fastai Course Part 1](https://course.fast.ai/). It has alot of emphasis on the practicality and a full walkthrough of the whole process from how to get your dataset, to optimizing your model and finally deployment. With this in mind, I have completed this mini-project with steps by steps explanation and provided the link to where I have gotten the code, resources, and information to complete the project so you may tweak it for your personal projects.

Most of the instructions are found in the README.md of each section and detail url links are provided for your reference. However, you should be able to purely follow the instructions on the README.md and not required to refer to external link unless specified and to download software.


## Getting Started

**The project consists of 3 parts:**
1. [Scrap image from google and train the image classification model using fastai in jupyter notebook](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/tree/master/Part1-Training-Model) (You can skip this step if you are already familiar with FASTAI and go straight to part 2 using the pre-trained model export.pkl which is included in this repo.)
2. [Build docker image for fastai and deploy to Azure function.(One-month free trial)](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/tree/master/Part2-AzureFunctions_Deployment)
3. Setup the Telegram Bot channel and deploy bot python script to Heroku.(Free server)


**The tools involved in this project:**
* Except for the hardware, everything else I use in this project are free.
* Laptop with RTX2060 (You can use google colab which provided GPU processing and should be faster than my hardware.) FASTAI provides the tutorial on how to setup [google colab for FASTAI](https://course.fast.ai/start_colab.html) 
You can choose other online platforms as shown on FASTAI, but I personally like the convenience of google colab that comes with GPU processing and most important of all, its FREE!
* Windows 10 cmd or PowerShell - I have chosen Windows instead of Linux as many beginners like myself use Windows. Linux subsystems such as Ubuntu is also available on windows platform.
* Install python 3.7 and above. I am using [python 3.7.4 64bit version](https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe)
* [Visual Studio Code](https://code.visualstudio.com/Download) Source Code Editor to edit python files
* Register a one month free trial account with [Microsoft Azure Account](https://azure.microsoft.com/en-us/). Unfortunately you need to register with a credit card, although they do not charge you anything during the first month trial.
* [Install Azure CLI for windows](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest)
* [Install the Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows#v2) (I'm using version 3.x)
* [Install Git](https://git-scm.com/downloads)
* Register [Docker Hub](https://hub.docker.com/) and [Install Docker](https://www.docker.com/products/docker-desktop)
* Register [Heroku account](https://www.heroku.com/) and [Install heroku CLI for windows](https://devcenter.heroku.com/articles/heroku-cli)
* Register [Telegram](https://telegram.org/)


### Prerequisites

* Completed FASTAI [Lesson 1](https://course.fast.ai/videos/?lesson=1) and [Lesson 2](https://course.fast.ai/videos/?lesson=2)
* Some basic python and Command-line interface knowledge.

### Contact Author: <poh.dylan@gmail.com>
