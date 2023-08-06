import re
from .Constants import *
from .Validator import *
from .Regex import *


def CreateProperLinkForImage(hostname,url):
	try:
		result = re.search(base64Reg, url)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str):
				return url
	except:
		return ""
	if url.startswith("./"):
		url = "http://"+hostname+url[1:]
	elif url.startswith("../"):
		url = "http://"+hostname+url[2:]
	elif url.startswith("//"):
		url = "http://"+url[2:]
	elif url.startswith("/"):
		url = "http://"+hostname+image[i]
	elif validUrl(url) == False:
		url = "http://"+hostname+"/"+url
	return url

def getImgOnWeb(hostname,html):
	image = re.findall(imgUrlReg, html, flags = re.I | re.M)
	try:
		if image:
			for i in range(len(image)):
				image[i] = CreateProperLinkForImage(hostname,image[i])
			return image
	except:
		pass
	return []

def getLogoOldWay(hostname,html):
	try:
		logo = re.search(logoReg, html, flags = re.I)
		if logo:
			return CreateProperLinkForImage(hostname,logo.groups()[0])
		logo = re.search(logoReg_a, html, flags = re.I)
		if logo:
			return CreateProperLinkForImage(hostname,logo.groups()[0])
		logo = re.search(logoReg_b, html, flags = re.I)
		if logo:
			return CreateProperLinkForImage(hostname,logo.groups()[0])
	except:
		pass
	return ""

def getTitleOldWay(html):
	try:
		title = re.search(titleReg, html, flags = re.I)
		if title:
			return title.groups()[0]
	except:
		pass
	return ""

def getMeta_basic(html,field):
	try:
		v_regs = metaRegGenrator_basic(field)
		if not v_regs:
			return ""
		result = re.search(v_regs["a"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		result = re.search(v_regs["b"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		return ""
	except:
		return ""

def getMeta_og(html,field):
	try:
		v_regs = metaRegGenrator_og(field)
		if not v_regs:
			return ""
		result = re.search(v_regs["a"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		result = re.search(v_regs["b"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		return ""
	except:
		return ""

def getMeta_prop(html,field):
	try:
		v_regs = metaRegGenrator_og_prop(field)
		if not v_regs:
			return ""
		result = re.search(v_regs["a"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		result = re.search(v_regs["b"], html, flags = re.I)
		if result:
			if result.groups()[0] and isinstance(result.groups()[0], str) and (len(result.groups()[0].strip()) > 0):
				return result.groups()[0]
		return ""
	except:
		return ""


def getLogo(hostname,html):
	try:
		result = getMeta_prop(html,"image")
		if result and (len(result.strip()) > 0):
			return CreateProperLinkForImage(hostname,result)
	except:
		pass
	return getLogoOldWay(hostname,html)

def getTitle(html):
	try:
		result = getMeta_og(html,"title")
		if result:
			if len(result.strip()) > 0:
				return result
		result = getTitleOldWay(html)
		if len(result.strip()) > 0:
			return result
		result = getMeta_og(html,"site_name")
		if result:
			if len(result.strip()) > 0:
				return result
	except Exception as err:
		pass
	return ""	


def getImagesFromUrl(url,html):
	finalMetaResult = {}
	finalMetaResult["success"] = True
	try:
		hostname = getHostName(url)
		imgOnWeb = getImgOnWeb(hostname,html)
		finalMetaResult["images"] = imgOnWeb
	except:
		finalMetaResult["success"] = False
		finalMetaResult["type"] = "webScrapingErr"
		finalMetaResult["type"] = errorMsg("webScrapingErr")
	return finalMetaResult

def getmetadata(url,html):
	finalMetaResult = {}
	finalMetaResult["success"] = True
	try:
		hostname = getHostName(url)
		imgOnWebResult = getImagesFromUrl(url,html)
		if imgOnWebResult["success"] == False:
			return imgOnWebResult
		imgOnWeb = imgOnWebResult["images"]
		html = removeScriptContent(html)
		html = removeBodyContent(html)
		html = removeCssContent(html)
		for meta in validFields_basic:
			if meta == "logo":
				result = getLogo(hostname,html)
				if len(result)==0:
					if len(imgOnWeb) == 0:
						finalMetaResult["logo"] = ""
					else:
						finalMetaResult["logo"] = imgOnWeb[0]
				finalMetaResult["logo"] = result
			elif meta == "title":
				result = getTitle(html)
				finalMetaResult["title"] = result
			else:
				result = getMeta_basic(html,meta)
				if len(result) == 0:
					result = getMeta_og(html,meta)
					if len(result) == 0:
						result = getMeta_prop(html,meta)
				finalMetaResult[meta] = result
	except:
		finalMetaResult["success"] = False
		finalMetaResult["type"] = "webScrapingErr"
		finalMetaResult["type"] = errorMsg("webScrapingErr")
	return finalMetaResult