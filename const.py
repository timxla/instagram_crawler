#PATH
DRIVER_PATH = "./chromedriver/chromedriver"
BASE_URL = "https://www.instagram.com/explore/tags/"
LOGIN_URL = "https://www.instagram.com/accounts/login/"

#To_search
KEYWORDS = ["봄코디", "패션", "ootd"]

#How many images to save per keyword
IMG_COUNT = 30

#CSS
FIRST_POST = "div.v1Nh3.kIKUG._bz0w"
IMG_CSS = '.v1Nh3.kIKUG._bz0w'
ID_CSS = "div.e1e1d > div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv.T0kll > span.Jv7Aj.mArmR.MqpiF > a.sqdOP.yWX7d._8A5w5.ZIAjV"
LIKES = "_7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll > span" #.get_attribute("innerHTML")
IMGURL_XPATH = "//img[@class='FFVAD']"
SEARCH_XPATH = "//input[@placeholder='Search']"
DATE_XPATH = "//time[@class='_1o9PC']"
RIGHT_ARROW = "div.l8mY4.feth3"
SCROLL_SCRIPT = "window.scrollTo(0,document.body.scrollHeight);"