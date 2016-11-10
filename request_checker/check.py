#python 2
import urllib2
urllib2.urlopen("http://localhost/").read()

#python 3
import urllib.request
urllib.request.urlopen("http://example.com/foo/bar").read()
