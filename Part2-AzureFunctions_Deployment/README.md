## Part 2: Build docker image for fastai and deploy to Azure function. (Comes with one month free trial)

Refer to [https://course.fast.ai/deployment_azure_functions.html#test-function](https://course.fast.ai/deployment_azure_functions.html#test-function) for the FASTAI official guide to deploy your trained model.

The steps here are almost similar to FASTAI official guide, but I have added a few tweak here and there which work 

Take note: Fastai only works when you provide your own custom Docker image on the App Service plan. 

In the FASTAI official guide, they mentioned that **Python 3.6** is the only Python runtime currently supported by Azure Functions. Which I believe have change now after Azure updated to version 3.x, I have tried **[Python 3.7.4 ](https://www.python.org/downloads/release/python-374/)** and [Azure functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-versions) work perfectly.  Meaning you can change your python version to 3.7 if you wish to do so.

## a. Setup Azure function for local testing
Before jumping in.
I suggest deactivating your previous virtual environment and create a new project directory with a new virtual environment.
Install and register account with Docker Hub and Azure account if you haven't done so.
* Register a one month free trial account with [Microsoft Azure Account](https://azure.microsoft.com/en-us/).
* [Install the Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows#v2) (I'm using version 3.x)
* [Install Azure CLI for windows](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest)
* Register [Docker Hub](https://hub.docker.com/)
* [Install Docker](https://www.docker.com/products/docker-desktop)

1. Create a new project directory <YOUR_AZURE_PROJECT_DIR> and then create your new virtual environment in powershell or cmd
```
python -m venv virtualenvname
```
2. To activate virtual environment
* for windows cmd
```
virtualenvname\scripts\activate
```
* for PowerShell
```
.\virtualenvname\scripts\Activate.ps1
```
3. Download requirements.txt from this repo and install all the python packages by executing the following. If successful, skip to step 6.
```
pip install -r requirements.txt
```
4. Install pytorch with cuda support
```
pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html
```
5. Install fastai
```
pip install fastai
```

* If you encounter this error:

['ERROR: Could not build wheels for bottleneck which use PEP 517 and cannot be installed directly'](https://github.com/pydata/bottleneck/issues/281)

Resolve this by downloading Windows SDK 10 (latest version). If this alone doesn't work then download Visual Studio 2019 (again whichever is the latest version). This updates the wheel process. From <[https://github.com/pydata/bottleneck/issues/281](https://github.com/pydata/bottleneck/issues/281)>

6. To check if fastai cuda support and other packages are installed properly
```
python -m fastai.utils.show_install
```
7. Create an Azure Function Project that uses the Python runtime.
```
func init --docker
```
When prompted select by moving arrow key up and down::
> Select a worker runtime: python
8. Create Function, replace <YOUR_OWN_FUNCTION_NAME> with your own function name
```
func new --name <YOUR_OWN_FUNCTION_NAME> --template "HttpTrigger"
```
9. Output all the dependencies to requirements.txt which will be used when you build the Docker image. This will overwrite the downloaded requirements.txt you have downloaded from this repo.
```
pip freeze > requirements.txt
``` 
10. Update Function

Replace the following files in the directory with the file provided in this repo:

> <YOUR_OWN_FUNCTION_NAME>/init.py

This is where your inference function lives. The following is an example of using a trained image classification model, of which you use to replace the default file. Please open it with **visual studio code** and go through the code.
(Note: You must replace with the code here and not from fastai official guide)

11.  Replace the following files in the directory with the file provided in this repo:

> <FUNCTION_NAME>/function.json

The function authorization will be called without any additional security key. Essentially only this line of code are modified in the original function.json file. 
```python
"authLevel": "anonymous",  
```
Please open this file with **visual studio code** and read through the code.

12. Copy your trained model file **export.pkl** to 
> <YOUR_AZURE_PROJECT_DIR>

Ensure **export.pkl** is copy to the root of <YOUR_AZURE_PROJECT_DIR> and not in the sub-directory. 
Note: If you do not have a trained model, you can use the one provided in this repo.

13. Start your Inference Function
```
func host start
```
you should see in your PowerShell or cmd,
>Http Functions:

><YOUR_OWN_FUNCTION_NAME>: [GET,POST] http://localhost:7071/api/<YOUR_OWN_FUNCTION_NAME>

To check that your function is running properly, visit [http://localhost:7071](http://localhost:7071) and you should see the following:

![azure function 3.0 running image](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/1-azure-running.png)

14. Test your Inference Function with test image
You can send a HTTP POST method to  [http://localhost:7071/api/<YOUR_OWN_FUNCTION_NAME>(http://localhost:7071/api/%3cFUNCTION_NAME%3e)  to check that your inference function is working. 

Open another cmd window. Go to the the directory <YOUR_AZURE_PROJECT_DIR>. Copy your test images into this follow and execute the below command in cmd window

To test a local image file which is in the same directory as your <YOUR_AZURE_PROJECT_DIR>
```
curl -i -X POST -k http://localhost:7071/api/<YOUR_OWN_FUNCTION_NAME> -F "file=@yourfilename.jpg"
```
![cmd  - curl prediction output from image](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/2-curl-predict.png)

Note: If you do not have curl, install [git](https://git-scm.com/downloads) which comes with curl.

To test image file from **url**, modified the code in **\_\_init__.py** the instruction to modified reside in this file.

Then run the code below in PowerShell replacing  <URL_TO_IMAGE>  with a URL that points to the image:
```
curl -i -X POST -H "Content-Type:application/json" -d "{\"url\": \"{the image file url}\"}" http://localhost:7071/api/<YOUR_OWN_FUNCTION_NAME>
```
## b. Docker image setup and build.

1. Build Docker image that contain your app and all require python libraries.
```
docker build --tag <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG> .
```
So for example if you have register:
* docker hub ID as **johnsmith** and 
* image name of **fastai_azure**    
Your code will look like this.
```
docker build --tag johnsmith/fastai_azure .
```
Remember the period at the end of this code.

If the build throws error like

> unable to execute 'gcc': No such file or directory

Add following codes into Dockerfile before the last RUN command.

> RUN apt-get update && apt-get install -y build-essential

2. Testing Docker Image
The following will run the Docker image on your local machine for testing:
```
docker run -p 8080:80 -it <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>
```
Sample code base on above user id and image name. You can omit the \<TAG> for now
```
docker run -p 8080:80 -it johnsmith/fastai_azure
```
Docker image with your newly created app is now running at the URL: localhost:8080. 

Test with the curl local test file to check for output

![image of curl test file](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/3-curl-docker-test.png)

3. Push Docker Image to Docker Hub
Use the following command to log in to Docker from the cmd. Enter your Docker Hub password when prompted.
```
docker login --username <DOCKER_HUB_ID>
```
Sample code
```
docker login --username johnsmith
```

4. Push the Docker image created earlier to Docker Hub.
```
docker push <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>
```
Sample code - [Details on version number tag](https://stackify.com/docker-build-a-beginners-guide-to-building-docker-images/) 
Retag the image with a version number:
```
docker tag johnsmith/fastai_azure johnsmith/fastai_azure:v1
```
Then push with the following:
```
docker push johnsmith/fastai_azure:v1
```

## c. Azure Setup
1. Login to Microsoft Azure using Azure CLI in cmd
```
az login
```
2. **The below text are taken straight from FASTAI official guide
Setup Azure Resources. You can also jump to the sample code below to quickly setup without going through the official guide**

You can now run the following commands to create the Azure resources necessary to run the inference app on Azure Functions.

The following example uses the lowest pricing tier, B1.

Replace the following placeholders with your own names:

-   name of the Resource Group that all other Azure Resources created for this app will fall under
-   e.g. ResourceGroup
-   run the following command to see the list of available locations:

-   az appservice list-locations --sku B1 --linux-workers-enabled

-   e.g. centralus
-   name of the Azure Storage Account which is a general-purpose account to maintain information about your function
-   must be between 3 and 24 characters in length and may contain numbers and lowercase letters only
-   e.g. inferencestorage
-   name of the Azure Function App that you will be creating
-   will be the default DNS domain and must be unique across all apps in Azure
-   e.g. inferenceapp123

Create Resource Group

az group create \  
--name <RESOURCE_GROUP> \  
--location <LOCATION_ID>

Create Storage Account

az storage account create \  
--name <STORAGE_ACCOUNT> \  
--location <LOCATION_ID> \  
--resource-group <RESOURCE_GROUP> \  
--sku Standard_LRS

Create a Linux App Service Plan

az appservice plan create \  
--name <APP_PLAN_NAME> \  
--resource-group <RESOURCE_GROUP> \  
--sku B1 \  
--is-linux

Create the App & Deploy the Docker image from Docker Hub

az functionapp create \  
--resource-group <RESOURCE_GROUP> \  
--name <FUNCTION_APP> \  
--storage-account <STORAGE_ACCOUNT> \  
--plan <APP_PLAN_NAME> \  
--deployment-container-image-name <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>

Configure the function app

The following assumes the Docker image uploaded earlier in your Docker Hub profile is public. If you have set it to private, you can see [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image#configure-the-function-app) to add your Docker credentials so that Azure can access the image.

storageConnectionString=$(az storage account show-connection-string \  
--resource-group <RESOURCE_GROUP> \  
--name <STORAGE_ACCOUNT> \  
--query connectionString --output tsv)

az functionapp config appsettings set --name <FUNCTION_APP> \  
--resource-group <RESOURCE_GROUP> \  
--settings AzureWebJobsDashboard=$storageConnectionString \  
AzureWebJobsStorage=$storageConnectionString

Run your Azure Function

After the previous command, it will generally take 15-20 minutes for the app to deploy on Azure. You can also see your app in the [Microsoft Azure Portal](https://portal.azure.com/) under Function Apps.

The URL for your app will be:

[https://<FUNCTION_APP>.azurewebsites.net/api/<FUNCTION_NAME>](https://%3cFUNCTION_APP%3e.azurewebsites.net/api/%3cFUNCTION_NAME%3e)

You can run the same tests in [Check Test Outputs](https://course.fast.ai/deployment_azure_functions.html###Check-Test-Outputs) with the new URL and you should see the output as before.

**Sample Code for your reference, which is not stated in FASTAI official guide**
* *storage account name :* **storagedogclass** 
* *location :* **"Southeast Asia"**
* *resource-group:* **dogclass**
* *appserivce plan name:* **dogclass_app**
* *functionapp name:* **dogclassfunctionapp**
* *docker hub ID :* **johnsmith**

```
#Create Resource Group
az group create --name dogclass --location "Southeast Asia"

#Create Storage Account
az storage account create --name storagedogclass --location "Southeast Asia" --resource-group dogclass --sku Standard_LRS

#Create a Linux App Service Plan
az appservice plan create --name dogclass_app --resource-group dogclass --sku B1 --is-linux

#Create the App & Deploy the Docker image from Docker Hub (Deployment can take 20-30 minutes to deploy)
az functionapp create --resource-group dogclass --name dogclassfunctionapp --storage-account  storagedogclass --plan dogclass_app --deployment-container-image-name johnsmith/fastai_azure:v1
```
3. Check if the deployment is successful (go to this website https://<FUNCTION_APP>.azurewebsites.net/api/<FUNCTION_NAME>)   
 You can also see your app in the [Microsoft Azure Portal](https://portal.azure.com/) under Function Apps.   
![azure website deploy](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/4-azure-function-deploy.png)

Go to your Azure account Dashboard
Deployment is successful if you can see the availability with a green tick

![azure website deploy](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/5-azure-ticks.png)

4. Test Azure function with curl
```
curl -i -X POST -k [https://dogclassfunctionapp.azurewebsites.net/api/azureDogClass](https://dogclassfunctionapp.azurewebsites.net/api/azureDogClass) -F "file=@yourimagefilename.jpg"
```
![testing curl azure function](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/Part2/6-curl-azure-website.png)

### If you see the predicted class return, congratulation, you have successfully deployed your azure functions and ready to move on to part 3 - Deployed to Telegram Bot   


**IMPORTANT**
Delete Resource Group

When you are done, delete the resource group if you are not going to deploy Telegram BOT. You can also delete after deploying and testing Telegram bot.

az group delete \  
--name <RESOURCE_GROUP> \  
--yes

Remember that with the App Service plan, you are being charged for as long as you have resources running, even if you are not calling the function. So it is best to delete the resource group when you are not calling the function to avoid unexpected charges.
