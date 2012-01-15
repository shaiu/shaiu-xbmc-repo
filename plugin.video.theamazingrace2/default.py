import sys
import xbmc, xbmcgui, xbmcplugin
import urllib,urllib2,re

#hello world

#The Amazing Race 2 plugin by Shai Ungar

def CATEGORIES():
        addDir('The Amazing Race 2','http://reshet.ynet.co.il/Shows/The_Amazing_Race/The_Amazing_Race_Video/.aspx?bo=10795&pa=1',1,'')
        #addLink('Chapter 20','http://s3fdl.castup.net/server12/434/433/43367245-80.flv?ct=IL&rg=NV&aid=434&cu=D2943B47-3D69-4C5B-B720-E5A81080DF3A&att=1')
        #addLink('Chapter 21','http://slsdl.castup.net/server12/434/808/80898721-80.flv?ct=IL&rg=NV&aid=434&cu=D2943B47-3D69-4C5B-B720-E5A81080DF3A&att=1')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile(r'<a href=".+?(vmlId=(\d+)).+?" rel=".+?" subTitle=".+?" ><img alt="(.+?)"  src=".+?" /> </a>').findall(link)
        url = 'http://reshet.ynet.co.il//Handlers/mrssHandler.ashx?'
        for vmlIdstr,vmlIdnum,name in match:
                addDir(name,url+vmlIdstr,2,vmlIdnum)

def VIDEOLINKS(url,name,vmlId):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<item>(?:[.\w\W]+?)<vmlId>'+str(vmlId)+'(?:[.\w\W]+?)<media:content url="(.+?)"(?:[.\w\W]+?)</item>').findall(link)
        match[0] = match[0].replace('amp;','')
        curettype = '&curettype=1'
        req = urllib2.Request(match[0]+curettype)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile('(http.+?)\?').findall(link)
        addLink(name,match[1])
        #resolve_url(match[1])
##        flag = False
##        for url in match:
##                if flag: break
##                try:
##                        resolve_url(url)
##                        flag = True
##                except:
##                        continue
        #for url in match:
        #        addLink(name,url,'')
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url):
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,vmlId):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&vmlId="+vmlId
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def resolve_url(stream_url):
    print 'stream_url: ',stream_url
    #xbmcplugin.setResolvedUrl(plugin_handle, True,xbmcgui.ListItem(path=stream_url))
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url)


plugin_handle = int(sys.argv[1])
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        vmlId=int(params["vmlId"])
except:
        pass

print "###############################################"
print "Mode: ",str(mode)
print "URL: ",str(url)
print "Name: ",str(name)
print "params: ",str(sys.argv[2])
print "###############################################"

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name,vmlId)



xbmcplugin.endOfDirectory(int(sys.argv[1]))