# Selenium browser
 

## Instructions

1. Install:

```
pip install aesthetic-ascii
```

2. Generate an aesthetic ASCII visual:

```python
from webscraper import Browser

# initialize the browser
browser = Browser()
# load a page
browser.load_page('https://www.avanza.se/aktier/lista.html')
# get the soup data
soup = browser.get_soup()
```
