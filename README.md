👋🏾 KONNICHIWA! :)
# Table of Contents
- [Abstract](#-abstract)
- [Contents](#contents)
- [Manual](#manual)
- [Docker](#docker)

p.s: just go to our servers IP for official updates on the website. <br>
[Techtutors.com](http://54.221.93.28:5000/)
<br> disclaimer: this is not the latest version. switch to the dev branch for a more recent overview.

# 📓 Abstract:
TechTutors is a web-based platform designed to address digital illiteracy and provide inclusive access to relevant information in Africa. By leveraging the power of technology, the platform aims to bridge the information gap and empower individuals through easy-to-access, bite-sized content. The project targets those with limited digital skills or resources, offering them an opportunity to stay informed, connected, and enriched.
Through a mobile-first approach, TechTutors ensures that users can access the platform via their smartphones, making valuable information available at their fingertips. Moreover, the inclusion of a USSD application widens the platform's reach to those without smartphones, promoting inclusivity across diverse user demographics.

## contents:
TechTutors will house a wide range of content categories, including technology, gaming, social media, education, and more, tailored to cater to users' interests and needs. The platform's simplicity and user-friendly interface will accommodate varying levels of digital literacy, ensuring a seamless experience for all users.
we're using flask for the backend:
[![Flask](https://www.fullstackpython.com/img/logos/flask.jpg)](https://flask.palletsprojects.com/)
<br>

Html, css and Javascript
![29488525-f55a69d0-84da-11e7-8a39-5476f663b5eb](https://github.com/AvitBrian/TechTutors/assets/113444617/da281e52-9f63-43aa-b3c9-f2377fb1f097)




# Manual:
the backend is composed of a flask app that interracts with our database to provide api endpoints. 
to set up the environment, first make sure you're running python3.3 and above. <b>
```
python3 --version
sudo apt update
sudo apt install python3
sudo apt install python3-venv
```
then create and activate the virtual environment
```
python -m venv myenv
```
on macOS and linux:
```
source myenv/bin/activate
```
on windows:
```
myenv\Scripts\activate
```
all you need to do now is install the dependencies and run the app.py
```
pip install -r requirements.txt
python3 app.py
```

# Docker:
What's that, you're a docker lunatic? <br>
Gorgeous! just build image from the Dockerfile in the root directory:<br>
```
sudo docker build -t python-techtutors .
sudo docker run --name techtutors -p 5000:5000 python-techtutors . 
```
you can add the `-d` flag to run it in detached mode
and everything should be running in the blink of an eye! navigate to the address and have fun.


