from selenium import webdriver
import os
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; rfphound/1.0; +http://rfphound.com/bot; AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36)"

class Driver:
    def __init__ (self, driver_path, headless = False, user_agent = DEFAULT_USER_AGENT, window_size = (1600, 900), **kargs):
        self.driver_path = driver_path
        self.capabilities = self.setopt (headless, user_agent, window_size, **kargs)
        self.driver = None
        self.main_window = None
    
    # -----------------------------------------------------------------
    def _parse_host (self, host):
        try:
            server, port = host.split (":", 1)    
        except ValueError:
            raise ValueError ("proxy port is required")                
        port = int (port)
        return server, host

    def __getattr__ (self, attr):
        if self.driver:
            return getattr (self.driver, attr)
        raise AttributeError ("driver does not be stared or driver has not '{}' attribute".format (attr))    

    def __enter__ (self): 
        self.create ()
        return self
    
    def __exit__ (self, type, value, tb):        
        self.driver.quit ()
        self.driver = None

    # callables ---------------------------------------------------------
    def set_timeout (self, timeout):
        self.driver.set_page_load_timeout(timeout)

    def get (self, url):
        self.main_window = self.driver.current_window_handle
        self.driver.get (url)

    def html (self, timeout = 10):
        self.wait (timeout)
        return "<html>%s</html>" % self.driver.execute_script ("return document.getElementsByTagName('html')[0].innerHTML;").replace ("&nbsp;", " ")

    def wait (self, timeout = 5):
        def document_loaded (driver):
            return driver.execute_script ("return document.readyState;") == "complete"
        WebDriverWait(self.driver, timeout).until(document_loaded)
            
    def query (self, by, what, timeout = 5):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located ((by, what)))    
        return self.driver.find_elements (by, what)
    
    def fetch (self, css, by = By.CSS_SELECTOR):
        return self.query (by, css)

    def one (self, css, by = By.CSS_SELECTOR):
        try:
            return self.fetch (css, by) [0]
        except IndexError:
            return None    

    # shortcuts ---------------------------------------------------
    def get_frames (self, for_human = True, timeout = 10):
        self.wait (timeout)
        names = []
        index = 0
        for ftype in ("frame", "iframe"):
            frames = self.driver.find_elements_by_tag_name(ftype)            
            for frame in frames:
                if for_human:                    
                    names.append (
                        "FRAME #%d. type: %s, name: %s, width: %s, height: %s, src: %s" % (
                        index, ftype, 
                        frame.get_attribute ("name"), 
                        frame.get_attribute ("width"), frame.get_attribute ("height"),
                        frame.get_attribute ("src")
                        )
                    )
                else:
                    names.append (frame)
                index += 1    
        return names
    
    def get_windows (self, for_human = True):        
        windows = []
        index = 0
        for w in self.driver.window_handles:
            if w == self.main_window:
                continue
                
            if for_human:
                self.driver.switch_to.window (w)
                windows.append ("WINDOW #%d. name: %s, url: %s, title: %s" % (
                        index,
                        self.driver.name,
                        self.driver.current_url,
                        self.driver.title
                    )
                )
            else:
                windows.append (w)
            index += 1
        #self.driver.switch_to.window (self.main_window)
        return windows        
    
    def switch_to_window (self, index = None):
        if index is None:
            return self.driver.switch_to.window (self.main_window)
        self.driver.switch_to.window (self.get_windows (False)[index])
        
    def switch_to_frame (self, index = None):
        if index is None:
            return self.driver.switch_to.default_content()
        self.driver.switch_to.frame (self.get_frames (False)[index])        
            
    def switch_to_alert (self):
        self.driver.switch_to.alert()
    
    def close_window (self):
        self.driver.close ()
        self.switch_to_window ()
    
    #--------------------------------------------
    # inputs handling
    #--------------------------------------------
    # SELECT
    def select (self, s, index):
        s = Select (s)
        if type (index) is int:
            s.select_by_index(index)
        else:
            s.select_by_value(index)
    
    def unselect (self, s, index):
        s = Select (s)
        if type (index) is int:
            s.deselect_by_index(int (index))
        else:
            s.deselect_by_value(index)        
        
    def deselect_all (self, s):
        s = Select (s)
        select.deselect_all ()    
    
    def select_all (self, s, text):
        s = Select (s)
        select.select_all ()    
    
    def select_by_text (self, s, text):
        s = Select (s)
        s.select_by_visible_text(text)
    
    def unselect_by_text (self, s, text):
        s = Select (s)
        s.deselect_by_visible_text(text)
                
    # CHECKBOX, RADIO
    def check (self, group, thing):
        if type (thing) is int:
            if not group [thing].is_selected():
                group [thing].click ()
            return        
        
        for cb in group:            
            if cb.get_attribute ("value") == thing and not cb.is_selected():
                cb.click()
    
    # CHECKBOX, RADIO
    def uncheck (self, group, thing):    
        if type (thing) is int:
            if group [thing].is_selected():
                group [thing].click ()
            return        
        
        for cb in group:            
            if cb.get_attribute ("value") == thing and cb.is_selected():
                cb.click()
                
    def uncheck_all (self, group):
        for cb in group:
            if cb.is_selected():
                cb.click ()
    
    def check_all (self, group):
        for cb in group:
            if not cb.is_selected():
                cb.click ()
                
    # TEXT, PASSWORD, TEXTAREA
    def set_text (self, e, *text):
        e.send_keys (*text)
    
    def save_html (self, path):
        with codecs.open (path, "w", "utf8") as f:
            f.write (self.get_html ())

    # @abstractmethod ----------------------------------------------
    def setopt (self, headless, user_agent, window_size, **opts):
        pass

    def create (self):
        pass