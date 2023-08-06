validUrlReg = r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::[0-9]{2,5})?(?:[/?#]\S*)?$'
urlPartsReg = r'^(([^:\/?#]+):)?(\/\/([^\/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?'
scriptContentReg = r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>'
cssContentReg = r'<style\b[^<]*(?:(?!<\/>)<[^<]*)*<\/style>'
bodyContentReg = r'<body\b[^<]*(?:(?!<\/>)<[^<]*)*<\/body>'

htmlContentHeaderReg = r'text\/html'

base64Reg = r'^data:image.*$'
imgUrlReg = r'<img[^>]*?src=["\']([^">]+)["\'][^>]*?>'

#title logo detect reg
titleReg = r'<title[^>]*?>([^<]+)<\/title>'
logoReg = r'<link[^>]*?rel=[^>]*? icon[^>]*?href=["\']([^">]+)["\'][^>]*?>'
logoReg_a = r'<link[^>]*?rel=[^>]*?touch-icon[^>]*?href=["\']([^">]+)["\'][^>]*?>'
logoReg_b = r'<link[^>]*?rel=[^>]*?icon[^>]*?href=["\']([^">]+)["\'][^>]*?>'


def metaRegGenrator_basic(meta):
	if isinstance(meta, str) == False:
		meta = ""
	a = r'<meta[^>]*?name=[^>]*?'+meta+'[^>]*?content=["\']([^<]*?)["\'][^>]*?>'
	b = r'<meta[^>]*?content=["\']([^">]+)["\'][^>]*?name=[^>]*?'+meta+'[^>]*?>'
	return {"a":a,"b":b}

def metaRegGenrator_og(meta):
	if isinstance(meta, str) == False:
		meta = ""
	a = r'<meta[^>]*?name=[^>]*?og:'+meta+'[^>]*?content=["\']([^<]*?)["\'][^>]*?>'
	b = r'<meta[^>]*?content=["\']([^">]+)["\'][^>]*?name=[^>]*?og:'+meta+'[^>]*?>'
	return {"a":a,"b":b}

def metaRegGenrator_og_prop(meta):
	if isinstance(meta, str) == False:
		meta = ""
	a = r'<meta[^>]*?property=[^>]*?og:'+meta+'[^>]*?content=["\']([^<]*?)["\'][^>]*?>'
	b = r'<meta[^>]*?content=["\']([^">]+)["\'][^>]*?property=[^>]*?og:'+meta+'[^>]*?>'
	return {"a":a,"b":b}