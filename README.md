# About the project
Tweetastrophy is a project which classifies tweets whether they imply a disaster or not. If it implies a disaster, the web-app shows the location that disaster occurs.

- Dataset is gained from Kaggle competition "Natural Language Processing with Disaster Tweets".

- Link to the working app:

### Validity of the project
We had an idea to train both DL and ML models, at the end we reached almost the same validation around %80. We decided to go on with the ML model since it is lighter than DL model to implement and also there is no risk for overfitting.

## Startup the project
The initial setup
Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```
​
Unittest test:
```bash
make clean install test
```
​
Check for tweetastrophy in github.com/{group}. If your project is not set please add it:
​
Create a new project on github.com/{group}/tweetastrophy
Then populate it:
​
```bash
##   e.g. if group is "{group}" and project_name is "tweetastrophy"
git remote add origin git@github.com:{group}/tweetastrophy.git
git push -u origin master
git push -u origin --tags
```
​
Functionnal test with a script:
​
```bash
cd
mkdir tmp
cd tmp
tweetastrophy-run
```
​
# Install
​
Go to `https://github.com/{group}/tweetastrophy` to see the project, manage issues,
setup you ssh public key, ...
​
Create a python3 virtualenv and activate it:
​
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```
​
Clone the project and install it:
​
```bash
git clone git@github.com:{group}/tweetastrophy.git
cd tweetastrophy
pip install -r requirements.txt
make clean install test                # install and test
```
Functional test with a script:
​
```bash
cd
mkdir tmp
cd tmp
tweetastrophy-run
```
