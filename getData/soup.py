import sys
import urllib2
import time
from bs4 import BeautifulSoup

'''  analyze album page using lxml
cate2Content = urllib2.urlopen("http://www.xiami.com/album/460269").read()
cate2Soup = BeautifulSoup(cate2Content, 'lxml')
print cate2Content
#cate2Soup = BeautifulSoup(cate2Content)
#print cate2Soup

#soup = BeautifulSoup('<em property="v:value"></em>')
#t = cate2Soup.findAll(id="album_rank")[0]
t = cate2Soup.findAll('div')
#t = t.findAll('em')[0]
print len(t) 
#print t.prettify()
exit()
'''

''' // test escape " in string
t = "\"fsd\""
t = t.replace('"', '\\"')
print '"' + t + "a" + '"'
exit()
'''

codeType = 'utf-8'
o = open('out', 'w')
o_err = open('out2', 'w')

def writeFile(data, filepath):
    outfile = open(filepath,'ab')
    data = data.encode('gb2312','ignore')
    outfile.write(data)
    outfile.close()

def processCate2s(cate1Ul):
    cate2s = cate1Ul.findAll('li')
    cate2s = map(lambda x:x.findAll('a')[0], cate2s)
    
    #print cate2s
    for i in range(len(cate2s)):
        cate2Lines = cate2s[i].prettify().split('\n')
        '''
        if i==0:
          print len(cate2Lines)
          print cate2Lines
        print len(cate2Lines)
        print cate2Lines
        '''
        cate2Str = '    {"name": "' + (cate2Lines[1] + " " + cate2Lines[3] + "").encode('gb2312','ignore') + "\",\n"
        cate2Str += '    "href": "' + cate2s[i]['href'].encode('gb2312','ignore') + "\",\n"
        cate2Str += '    "children": [\n'
        print cate2Str
        o.write(cate2Str)
        processSingleCate2(cate2s[i]['href'])
        o.write("    ]}" + ("," if i != len(cate2s) - 1 else "") + "\n")
        '''
        '''
    
def processSingleCate2(cate2Link):
    cate2Content = urllib2.urlopen("http://www.xiami.com" + cate2Link).read()
    cate2Soup = BeautifulSoup(cate2Content.decode(codeType,'ignore'))
    albumUl = cate2Soup.findAll('ul', {"class": "genre_album clearfix"})[0]
    imgs = albumUl.findAll('img')
    ps = albumUl.findAll('p', {"class": "name"})
    ps = map(lambda x:x.find('a'), ps)
    albums = ps[::2]
    artists = ps[1::2]
    albumStrs = []
    #print len(imgs), len(albums), len(artists)
    for img, album, artist, i in zip(imgs, albums, artists, range(len(imgs))):
        imgLink = img['src']
        albumName = album.contents[0].string.strip().replace('"', '\\"')
        artistName = artist.contents[0].string.strip().replace('"', '\\"')
        #print album
        albumLink = album['href']
        count = 0

        try:
            rate, popu = processAlbum(albumLink)
        except:
            o_err.write("http://www.xiami.com" + cate2Link + " http://www.xiami.com" + albumLink + '\n')
            rate = 'noValue'
            popu = 'noValue'

        if (rate == 'noValue'): continue
        albumStr = '       {"name": "' + albumName + '", "img": "' + imgLink + '", "artist": "' + artistName + '", "rate": ' + rate + ', "popu": ' + popu + ', "href": "' + albumLink + '", "size": 1}'
        albumStr = albumStr.encode('gb2312', 'ignore')
        print albumStr
        albumStrs.append(albumStr)
        #o.write(albumStr)
    time.sleep(2)
    o.write(',\n'.join(albumStrs) + '\n')

def processAlbum(albumLink):
    albumContent = urllib2.urlopen("http://www.xiami.com" + albumLink, timeout=10).read()
    albumSoup = BeautifulSoup(albumContent, 'lxml')

    emContents = albumSoup.find('div', id='album_rank').find('em').contents
    aRate = emContents[0].string if len(emContents) > 0 else 'noValue'

    aPopu = albumSoup.find('div', id='sidebar').find('i').contents[0].string
        
    time.sleep(2)
    return (aRate, aPopu)


    '''
def processSingleCate2_Left(cate2Link, idx):
    cate2Content = urllib2.urlopen(cate2Link).read()
    cate2Soup = BeautifulSoup(cate2Content.decode(codeType,'ignore'))
    albumUl = cate2Soup.findAll('ul', {"class": "genre_album clearfix"})[0]
    imgs = albumUl.findAll('img')
    ps = albumUl.findAll('p', {"class": "name"})
    ps = map(lambda x:x.find('a'), ps)
    albums = ps[::2]
    artists = ps[1::2]
    albumStrs = []
    #print len(imgs), len(albums), len(artists)
    for img, album, artist, i in zip(imgs, albums, artists, range(len(imgs))):
        if (i != idx): continue
        imgLink = img['src']
        albumName = album.contents[0].string.strip().replace('"', '\\"')
        artistName = artist.contents[0].string.strip().replace('"', '\\"')
        #print album
        albumLink = album['href']
        count = 0

        try:
            rate, popu = processAlbum(albumLink)
        except:
            #o_err.write("http://www.xiami.com" + cate2Link + " http://www.xiami.com" + albumLink + '\n')
            rate = 'noValue'
            popu = 'noValue'

        if (rate == 'noValue'): continue
        albumStr = '       {"name": "' + albumName + '", "img": "' + imgLink + '", "artist": "' + artistName + '", "rate": ' + rate + ', "popu": ' + popu + ', "href": "' + albumLink + '", "size": 1}'
        albumStr = albumStr.encode('gb2312', 'ignore')
        print albumStr
        albumStrs.append(albumStr)
        #o.write(albumStr)
    #time.sleep(2)
    #o.write(',\n'.join(albumStrs) + '\n')

processSingleCate2_Left("http://www.xiami.com/music/style-detail/sid/65", 7)
exit()
'''


contentAll = urllib2.urlopen("http://www.xiami.com/music/style").read()
soup = BeautifulSoup(contentAll.decode(codeType,'ignore'))

str = '{"name": "xia mi", "children": [' + "\n" 
o.write(str)

t = soup.findAll('div', id="genre_cate")[0]
cate1Heads = t.findAll('a', {"class": "genre_top"})
cate1s = t.findAll('ul', {"class": "genre_sub"})
for i in range(len(cate1Heads)):
    #cateHeadLines = cate1Heads[i].prettify().split('\n')

    cateStr = '  {"name": "' + cate1Heads[i].contents[0].string.replace('"', '\\"').encode('gb2312','ignore') + "\",\n"
    cateStr += '  "href": "' + cate1Heads[i]['href'].encode('gb2312','ignore') + "\",\n"
    cateStr += '  "children": [\n'
    o.write(cateStr)
    processCate2s(cate1s[i])
    o.write("  ]}" + ("," if i != len(cate1Heads) - 1 else "") + "\n")

str = "]}"
o.write(str)
o.close()
print 'end'

exit()

