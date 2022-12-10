# Selenium browser
 

## Instructions

1. Install:

```
pip install git+https://github.com/AtieDag/selenium-browser
```

2. Run the browser:

```python
from browser.webscraper import Browser

# initialize the browser
browser = Browser()
# load a page
browser.load_page('https://www.avanza.se/aktier/lista.html')
# get the soup data
soup = browser.get_soup()
```
