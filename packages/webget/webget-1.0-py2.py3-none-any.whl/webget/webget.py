import re
from .MetaExtractor import *
from .WebScraper import *


def getHtml(url):
	html = WebThief(url)
	return html

def getMeta(url):
	result = getHtml(url)
	if result and result["success"] == False:
		return result
	return getmetadata(url,result["html"])

def getImages(url):
	result = getHtml(url)
	if result and result["success"] == False:
		return result
	return getImagesFromUrl(url,result["html"])