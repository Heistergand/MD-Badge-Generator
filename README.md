# Ingress Mission Day Badge Generator
A tool for Ingress Mission Day POC teams.

## Status
This tool is in early development. It's design is not yet looking great, it has bugs and it is still missing a bunch of features. But to generate 24 Badges on-the-fly, it's already doing the job.

## Contribute
- If you're a programmer and you like to contribute, you're hereby invited to fork this repo, make your changes and send pull requests.
- Everybody is welcomed to open an issue when they have found a bug or have an idea for an enhancement.

# Installation
## Install and run on google colab
_Totally recommended for just using it temporarily and forget about it later. Which would be a typical scenario for this kind of tool._
1. Visit https://colab.research.google.com/ using `CTRL + click` (on Windows and Linux)  or `CMD + click` (on MacOS) to open colab in a new tab.
2. Crate a new Notebook
3. In the code cell, paste e the following code:
```python
!pip install pygit2==1.12.2
%cd /content
!git clone https://github.com/heistergand/md-badge-generator.git
%cd /content/md-badge-generator/
!git pull
!pip install -q -U -r requirements.txt
from google.colab.output import eval_js
print(f'CLICK HERE >>>>> {eval_js("google.colab.kernel.proxyPort(5000)")} <<<<<<')
!python app.py
```
4. Run the cell
5. It should now look somewhat like this: ![image](https://github.com/Heistergand/MD-Badge-Generator/assets/16416532/0b2aa1ca-d1e6-4ea4-a3d6-7ff33b2b6492)
6. Click on the linke where it says "CLICK HERE" (obviously...)
7. You can now use the tool.
8. Optionally save the notebook in your personal google drive.
9. When you're finishes using the tool, consider stopping the cell and the runtime
10. Be kind and stop and delete the runtime in colab when your work is done. You can also just abandon it, but it saves energy when you close and delete the runtime.

## Install and run using docker compose
You need a functioning docker environment with docker compose.
1. on your machine, make a new project folder
2. Clone (or download) this repository into your project folder
3. open the repository main dirctory `md-badge-generator`
4. run `docker compose up -d`
5. access the server on port 5000 on your machine
6. I recommend lazydocker to monitor your running docker container

## Install manually
_Not recommended, because this would change your system environment. You could be ending up shearing a bison when your python version is not up to date_
- Clone or download the repo to your machine into a new folder
- make sure Pillow and Flask is installed `pip3 install --update Pillow flask`
- run the server via `python3 app.py`

# Usage
- select images to upload
- enter the name of your city
- choose a font size
- click upload

- get all your images generated as mission day badges in 512x512 png format

# Disclaimer
This is an Ingress fan project. Not affiliated with Ingress or Niantic.
