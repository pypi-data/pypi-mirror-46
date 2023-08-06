import requests
from urllib.parse import urljoin
from aquests.protocols.http import treebuilder, localstorage as ls
from . nops import nops
from . import cssutil

class ClickError (Exception):
	pass

class HTTPError (Exception):
	pass

class PythonBrowser:
	name = "PythonBrowser"
	current_window_handle = None
	
	def __init__ (self, useragent, proxy, auth, logger):
		self.useragent = useragent
		self.session = requests.Session ()
		
		self.proxy = {}
		if proxy:
			self.proxy = {
			  'http': "http://" + proxy,
			  'https': "http://" + proxy
			}
			self.session.proxies.update (self.proxy)
			
		self.auth = auth
		if auth:			
			self.session.auth = auth
		self.logger = logger
		
		self.active = False
		self.timeout = 60
		self.current_url = None
		self.history = []
		self.current_history_index = -1				
		if ls.g is None:
			ls.create (logger)
	
	def __getattr__ (self, name):
		raise NotImplementedError ('%s is not available on PythonBrowser' % name)
		
	def quit (self):
		self.close ()
	
	def close (self):
		self.history = []
		
	def implicitly_wait (self, *args, **karg):
		pass
	
	def set_title (self):
		title = nops.by_tag (self.get_doc (), 'title')
		if title:
			self.title = nops.get_text (title [0])
		else:	
			self.title = None
				
	def get_html (self):
		return self.history [self.current_history_index][1]
	
	def get_doc (self):
		return self.history [self.current_history_index][2]
	
	def get_current_url (self):
		return self.history [self.current_history_index][0]
		
	def set_current_url (self, url):
		self.history.append ([url, '', ''])
		self.current_history_index += 1
		self.current_url = url
				
	def back (self):
		self.current_history_index -= 1
		self.current_url = self.history [self.current_history_index][0]
		self.active = False
	
	def click (self, item):
		a = item.item
		if a.tag != "a":
			raise ClickError ('PythonBrowser can handle only A tag')
		url = nops.get_attr (a, "href")		
		self.active = True 
		self.get (urljoin (self.current_url, url))
		
	def _handle_response (self, rsp):			
		self.headers = rsp.headers
		cookies = rsp.headers.get ("set-cookie")
		if cookies:
			if type (cookies) is str:
				cookies = [cookies]			
			for cookie in cookies:		
				ls.g.set_cookie_from_string (self.current_url, cookie)
		
		html = rsp.text.replace ("&nbsp;", " ")
		self.history.append ([self.current_url, html, treebuilder.html (html, self.current_url)])
		self.current_history_index += 1
		self.set_title ()
		
	def _get_request_headers (self, url):
		self.history = self.history [:self.current_history_index + 1]

		headers = {}
		if self.current_url:
			headers ['Referer'] =  self.current_url
		self.current_url = url
		
		if self.useragent:
			headers ['User-Agent'] = self.useragent
		return headers
			
	def get (self, url, data = None):		
		headers = self._get_request_headers (url)
		try:
			if data:
				headers ["Content-Type"] = "application/x-www-form-urlencode"
				rsp = self.session.post (url, data, headers = self._get_request_headers (url), auth = self.auth, verify=False)			
			else:
				rsp = self.session.get (url, headers = self._get_request_headers (url), auth = self.auth, verify=False)
		except:
			self.logger.trace ()
			raise ClickError
		
		if not rsp.ok:
			raise HTTPError ("HTTP Status: %d" % rsp.status_code)
			
		self._handle_response (rsp)	
	
	def get_cookies (self):
		return ls.g.get_cookie_as_dict (self.current_url)
	
	def inject_cookies (self, cookies):
		for k, v in cookies.items ():
			self.session.cookies.set (k, v)
			
	def add_cookie (self, k, v):
		ls.g.set_cookie (self.current_url, k, v)
		self.session.cookies.set (k, v)
			
	def find_elements (self, by, what):
		method, param =  cssutil.make_detector (by, what)
		return method (self.get_doc (), param)
		
	def execute_script (self, *args, **kargs):
		raise NotImplementedError ('cannot execute script on PythonBrowser')
		
	def set_page_load_timeout (self, timeout):	
		self.timeout = timeout
	
	def rebuild_dom (self, batch):
		# remove unneed/anoying sig making node
		doc = self.history [self.current_history_index][2]
		if batch:			
			nops.batch (doc, batch)
		self.history [self.current_history_index][1] = nops.to_string (doc)
		