
from .driver import Driver
from selenium import webdriver
import os
import time

class Chrome (Driver):
    def setopt (self, headless, user_agent, window_size, **opts):
        options = webdriver.ChromeOptions ()
        options.add_argument("--disable-gpu")
        headless and options.add_argument('--headless')
        options.add_argument('--window-size={}x{}'.format (*window_size))
        
        capabilities = options.to_capabilities ()
        if opts.get ("proxy"):
            server, port = self._parse_host (opts ["proxy"])
            capabilities ['proxy'] = {
                    'httpProxy' : "%s:%d" %(server, port),
                    'sslProxy' : "%s:%d" %(server, port),
                    'noProxy' : None,
                    'proxyType' : "MANUAL",
                    'class' : "org.openqa.selenium.Proxy",
                    'autodetect' : False
            }
            capabilities['user-agent'] = user_agent
        return capabilities

    def create_driver (self):
        return webdriver.Chrome(self.driver_path, desired_capabilities = self.capabilities)       


class Firefox (Chrome):    
    def setopt (self, headless, user_agent, window_size, **opts):
        profile = webdriver.FirefoxProfile()            
        if opts.get ("proxy"):
            server, port = self.parse_host (opts ["proxy"])

            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", server)
            profile.set_preference("network.proxy.http_port", port)
            profile.set_preference("network.proxy.https", server)
            profile.set_preference("network.proxy.https_port", port)
            profile.set_preference("http.response.timeout", self.TIMEOUT)
            profile.set_preference("dom.max_script_run_time", self.TIMEOUT)
            profile.set_preference("general.useragent.override", user_agent)
            profile.update_preferences()
        return profile                     

    def create_driver (self):        
        return webdriver.Firefox (self.capabilities, executable_path = self.driver_path)


class IE (Chrome):    
    def setopt (self, headless, user_agent, window_size, **opts):
        capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()            
        if opts.get ("proxy"):
            server, port = self.parse_host (opts ["proxy"])
            capabilities['proxy'] = {
                "httpProxy":"%s:%d" %(server, port),
                "ftpProxy":"%s:%d" %(server, port),
                "sslProxy":"%s:%d" %(server, port),
                "noProxy":None,
                "proxyType":"MANUAL",
                "class":"org.openqa.selenium.Proxy",
                "autodetect":False
            }
        return capabilities                     

    def create_driver (self):        
        return webdriver.Ie (self.capabilities)

