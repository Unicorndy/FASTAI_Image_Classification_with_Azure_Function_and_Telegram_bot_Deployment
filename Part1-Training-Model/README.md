## Part 1: Scrap the images from google image search and train the image classification model using fastai in jupyter notebook.

Before jumping into the notebook.

1. Create your virtual environment in powershell or cmd
```
python -m venv yourprojectname
cd yourprojectname
```
2. To activate virtual environment
* for windows cmd
```
yourprojectname\scripts\activate
```
* for PowerShell
```
.\yourprojectname\scripts\Activate.ps1
```
3. Install all the python packages. If successful, skip to step 8.
```
python -m pip install -r requirements.txt
```
4. Install jupyter notebook if you haven't done so
```
pip install jupyter notebook
```
5. Setup jupyter notebook to run kernel in venv
```
ipython kernel install --name=yourprojectname
```
6. Install pytorch with cuda support
```
pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html
```
7. Install fastai
```
pip install fastai
```

* If you encounter this error:

['ERROR: Could not build wheels for bottleneck which use PEP 517 and cannot be installed directly'](https://github.com/pydata/bottleneck/issues/281)

Resolve this by downloading Windows SDK 10 (latest version). If this alone doesn't work then download Visual Studio 2019 (again whichever is the latest version). This updates the wheel process. From <[https://github.com/pydata/bottleneck/issues/281](https://github.com/pydata/bottleneck/issues/281)>

8. To check if fastai gpu and the rest are installed properly
```
python -m fastai.utils.show_install
```
![fastai.utils.show_install](https://github.com/Unicorndy/FASTAI_Image_Classification_with_Azure_Function_and_Telegram_bot_Deployment/blob/master/image/show_install.png)  
9. Download Fastai_Img_Class.ipynb into this directory and Run jupyter notebook
```
jupyter notebook
```
10. Jupyter notebook will open in your browser. Open Fastai_Img_Class.ipynb and continue from there.

Note: As you can see from the notebook that I stop my training with error rate of less than 0.65 percent. There are definitely more ways to lower the error rate, such as more thorough image clean up or choosing resnet50 or increasing epochs, but I decided to stop here due to time constraints and this error rate is good enough for this mini project.
