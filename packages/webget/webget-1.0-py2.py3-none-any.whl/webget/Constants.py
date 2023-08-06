userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
acceptInRequest = 'text/html'


headers = {
    'User-Agent': userAgent,
    'Content-Type': 'text/html; charset=utf-8',
    'connection' : 'keep-alive',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'accept': acceptInRequest
}


errorMsg = {
	"InvalidUrl" : "Url is invalid try with valid url",
    "InvalidHtml" : "The url did not return any html content",
	"httpErr" : "There is http error durring http request",
	"sslErr"  : "There is SSL Certificate error please try with http if you are using https",
	"unknownErr" : "There is unknown error durring http request",
    "unreachableSite" : "Failed to establish a new connection may be site not exist",
    "webScrapingErr" : "Unable to parse html something went wrong"
}

validFields_basic = [
    "logo",
    "description",
    "title",
    "keywords",
    "subject",
    "copyright",
    "language",
    "robots",
    "revised",
    "abstract",
    "topic",
    "summary",
    "author",
    "designer",
    "reply-to",
    "url",
    "category",
    "site_name",
    "email",
    "country-name",
    "phone_numbe"
]