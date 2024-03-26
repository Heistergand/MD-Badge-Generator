# MD-Badge-Generator
for ingress mission day orga teams

# Installation

- make sure Pillow and Flask is installed `pip3 install --update Pillow Flask`
- run the server via `python3 app.py`

# How to run this on google colab
1. Visit https://colab.research.google.com/
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
5. Click on the linke where it says "CLICK HERE" (obviously...)
6. The script does not clean up the folder (yet), so watch out when downloading as zipfile it will download all files.
7. When you're ready, stop the cell
8. Be kind and stop the runtime when your work is done. You can also just abandon it, but it saves energy when you close and delete the runtime.

# usage
- select images to upload
- enter the name of your city
- choose a font size
- click upload

- get all your images generated as mission day badges in 512x512 png format

# disclaimer
Ingress fan project. Not affiliated with Ingress or Niantic.
