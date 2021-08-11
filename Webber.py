from random import randint, random
from time import sleep, strftime, time
from ExGen import ExGen
from Login import login
import os
import pandas as pd
from Poster import *
from PIL import Image, ImageFilter
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from shutil import copyfile


from selenium.common.exceptions import NoSuchElementException, WebDriverException
import glob
import json



def randomSleep(low, high):
    sleep(random() + randint(low, high))
def windowsLogin():
    chromedriver_path = 'C:/Users/bardi/chromedriver.exe' # Change this to your own chromedriver path!
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--auto-open-devtools-for-tabs")
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
    generator = ExGen()
    randomSleep(1,2)
    login(driver)
    driver.get('https://www.instagram.com/nature/')
    sleep(5)
    return driver

#Basic Interaction
FIRST_THUMB = "div._2z6nI > article > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1)"
LIKE_BUT = "div.eo2As > section.ltpMr.Slqrh > span.fr66n > button"
COMMENT_BUT = "div.eo2As > section.ltpMr.Slqrh > span._15y0l > button"
COMMENT_BOX = "div.eo2As > section.sH9wk._JgwE > div > form > textarea"
FOLLOWER_BUT= 'div.bY2yH > button'
USER_BUT = "div.e1e1d > a"
LIKE_NUM = "div.Nm9Fw > button > span"
CAPTION = "div.C4VMK > span"
VIEW_NUM = "div.eo2As > section.EDfFK.ygqzn > div > span"

def click(element, driver):
    driver.find_element_by_css_selector(element).click()
def keyInput(string ,element, driver):
    driver.find_element_by_css_selector(element).send_keys(string)
def clickFirstThumbnail(driver):
    click(FIRST_THUMB,driver)
def getNext(driver):
    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.ARROW_RIGHT)
def like(driver):    
    click(LIKE_BUT,driver)
def comment(driver):
    p = randint(1,10);
    if (p>7):
        click(COMMENT_BUT, driver)
        comment_box = driver.find_element_by_css_selector(COMMENT_BOX)
        keyInput(generator.generateComment(),COMMENT_BOX,driver)
        keyInput(Keys.ENTER,COMMENT_BOX,driver)
def follow(driver):
    follow_button = driver.find_element_by_css_selector(FOLLOWER_BUT)
    if (follow_button.text == 'Following'):
        pass
    else:
        follow_button.click()
def imagineFuturePath(*nestedFolders):
    cwd = os.getcwd()
    path = cwd
    for folder in nestedFolders:
        path += '\\' + folder
    return path
def openMobileDriver():
    mobile_emulation = { "deviceName": "Pixel 2" }
    mobile_options = webdriver.ChromeOptions()
    mobile_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver2 = webdriver.Chrome(executable_path=chromedriver_path ,desired_capabilities = mobile_options.to_capabilities())
    return driver2
def closeDriver():
    driver.__exit__()
def indStalking(li, driver = driver):
    following = readFromCSVflat(imagineFuturePath("Following.csv"))
    for l in li:
        try:
            if(following.__contains__(l)):
                continue
            else:
                driver.get("https://www.instagram.com/" + l + "/")
                following.append(l)
                saveToCsv(following,imagineFuturePath("Following.csv"))
                click(FIRST_THUMB, driver)
                randomSleep(1,2)
                click(LIKE_BUT, driver)
                randomSleep(1,3)
                for i in range(2):
                    getNext(driver)
                    randomSleep(20,30)
        except:
            continue;
#Basic Data Mining
def getUser(driver):
    selector = USER_BUT
    user_button = driver.find_element_by_css_selector(selector)
    return user_button.text;
def getVidlikes(driver):
    try:
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/span").click()
        randomSleep(1,2)
        likes = driver.find_element_by_xpath("//section/div/div/div/span").text
    except:
        print("couldn't get likes on a vid by " + Username )
def getLikes(driver = driver):
    try:
        try:
            like_number = driver.find_element_by_css_selector(LIKE_NUM)
            return like_number.text
        except:
            pass
        try:
            click(VIEW_NUM, driver)
            sleep(0.3)
            likes = driver.find_element_by_css_selector("body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div > div > div.vJRqr > span")
            return likes.text
        except:
            pass
    except:
        return 0
def getViews(driver):
    try:
        view_number = driver.find_element_by_xpath("//section/div/span/span")
        return view_number.text
    except:
        return '';
def getCSVsAsListOfSets(foldername, ext, flat = False):
    cwd = os.getcwd()
    ccs = glob.glob(cwd + "\\"+ foldername + "\*" + ext)
    listOfSets = []
    for f in ccs:
        try:
            if(flat == True):
                listOfSets.append(set(readFromCSVflat(f)))
            else:
                listOfSets.append(set(readFromCSV(f)))
        except:
            continue
    return listOfSets
def getlistofcsvs(folderpath):
    csvs = glob.glob(folderpath + "\*.csv")
    l = []
    for csv in csvs:
        l.append(readFromCSV(csv))
    return l
def getBinaryIntersectionsOfAllSets(listOfSets):
    intersections = []
    for set1 in listOfSets:
        for set2 in listOfSets:
            if (set1 != set2):
                intersection = set1.intersection(set2)
                intersections.append(intersection)
                
             #if intersection not in intersections else intersections 
    s =  list(set(frozenset(item) for item in intersections)) 
    return [set(item) for item in set(frozenset(item) for item in intersections)]
def generalUnion(listOfSets):
    union = set()
    for i in listOfSets:
        union = union.union(i)
    return union
def getCaption(driver = driver, r = 2):
    caption = ''
    try:
        selector = CAPTION
        captionEl = driver.find_element_by_css_selector(selector)
        caption = captionEl.text
    except:
        sleep(2)
        if(r>=0):
            getCaption(r = r-1)
        else:
            pass
    return caption
def getImageLink(driver):
    try:
        try:  
            try:
                image = driver.find_element_by_css_selector("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img")
            except:
                image = driver.find_element_by_css_selector("div.KL4Bh > img")
                                                            
        except:
            try:
                image = driver.find_element_by_css_selector("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.tN4sQ.zRsZI > div > div > div > ul > li:nth-child(1) > div > div > div > div.eLAPa._23QFA > div.KL4Bh > img")
            except:
                image = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/ul/li[1]/div/div/div/div[1]/img")
                
        imlink = image.get_attribute('src')

        return imlink
    except:
        print('There\'s no image here')
        return ''
def getImageLink(driver):
    l = []
    l.append("body > div._2dDPU.CkGkG > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img")
    l.append("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img")
    l.append("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.tN4sQ.zRsZI > div > div > div > ul > li:nth-child(1) > div > div > div > div.KL4Bh > img")
    l.append("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.tN4sQ.zRsZI > div > div > div > ul > li:nth-child(1) > div > div > div > div.eLAPa._23QFA > div.KL4Bh > img")
    l.append("body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.eLAPa._23QFA > div.KL4Bh > img")
    for el in l:
        try:
            image = driver.find_element_by_css_selector(el)
            return image.get_attribute('src')
            #imlink = imlink.split(",")
            #if (len(imlink) == 1):
            #    imlink = imlink[0]
            #else:
            #    imlink = imlink[-1]
             
        except:
            continue;
    return ''

def getVidLink(driver):
    try:
        vid = driver.find_element_by_xpath("//div/div/div/video")
        vidlink = vid.get_attribute('src')
        vidlink = vidlink.split(",")
        if (len(vidlink) == 1):
            vidlink = vidlink[0]
        else:
            vidlink = vidlink[-1]
        return vidlink

    except:
        print('There\'s no video here')
        return ''
def getContentLink(driver):
    iml = getImageLink(driver)
    vidlink = getVidLink(driver)
    if (iml != ''):
        return iml
    elif (vidlink != ''):
        return vidlink
    else:
        return ''
def getFollowers(driver):
    sel = "body > div.RnEpo.Yx5HN > div > div:nth-child(2) > ul > div > li > div > div.t2ksc > div.enpQJ > div.d7ByH > a"

    el = driver.find_elements_by_css_selector(sel)
    followers = []
    for follower in el:
        followers.append(follower)
    return followers
def getFollowersMobile(driver):
    sel = '#react-root > section > main > div:nth-child(2) > ul > div > li > div > div.t2ksc > div.enpQJ > div.d7ByH > a'
    f = driver.find_elements_by_css_selector(sel)
    followers = [i.text for i in f]
    return followers
def getFollowing(driver):
    sel = "div.t2ksc > div.enpQJ > div.d7ByH > span > a"
    el = driver.find_elements_by_css_selector(sel)
    followers = []
    for follower in el:
        followers.append(follower)
    return followers
def getLocation(driver):
    try:
        selector = 'body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.M30cS > div.JF9hh > a'
        location = driver.find_element_by_css_selector(selector)
        return location.text
    except:
        print('no location found')
        return None
def getImageDescription(driver):
    try:
        selector = "body > div._2dDPU.vCf6V > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img"
        t = driver.find_element_by_css_selector(selector)
        desc = t.get_attribute('alt')
        if (desc == "No photo description available."):
            return None
        else:
            return desc
    except:
        return None
def DownloadVideo(driver, name):
    with open(name + '.mp4', 'wb') as handle:
        response = requests.get(getContentLink(driver), stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
def DownloadPhoto(driver,name):
    with open(name + '.jpg', 'wb') as handle:
        response = requests.get(getContentLink(driver), stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

#DATA MINING
def getRelatedUsers(driver):
    caption = getCaption(driver)
    try:
        users = re.findall(r"@\w+",caption)
        return users
    except:
        return None
def setOfRelatedUsers(n, driver):
    users = []
    try:
        clickFirstThumbnail()
    except:
        pass
    for i in range(n):
        try:
            getNext(driver)
        except:
            break;
        randomSleep(1,2)
        try:
            relatedUsers = getRelatedUsers()
            if (relatedUsers != None):
                users.extend(relatedUsers)
        except:
            randomSleep(2,3)
            relatedUsers = getRelatedUsers()
            if (relatedUsers != None):
                users.extend(getRelatedUsers())
        else:
            continue
    return list(set(users))
def setOfRelatedUsers(l, n, driver):
    try:
        clickFirstThumbnail(driver)
    except:
        pass
    for i in range(n):
        try:
            getNext(driver)
        except:
            break;
        randomSleep(2,3)
        try:
            relatedUsers = getRelatedUsers(driver)
            if (relatedUsers != None):
                l.extend(getRelatedUsers(driver))
        except:
            randomSleep(3,4)
            relatedUsers = getRelatedUsers(driver)
            if (relatedUsers != None):
                l.extend(getRelatedUsers(driver))
        else:
            continue
    l =  list(set(l))
def getPhotosandData(n, driver):
    photos = []
    captions = []
    cwd = os.getcwd()

    for i in range(n):
        Username = getUser(driver)
        imLink = getContentLink(driver)
        likes = getLikes(driver)
        loci = getLocation(driver)
        tags = getHashtags(driver)
        captions.append(getCaption(driver))
        hash1 = hash(imLink)

        ImgDataDir = os.path.join(cwd,"ImageData")
        if not os.path.exists(ImgDataDir):
            os.makedirs(ImgDataDir)


        if (tags == set()):
            tags = ''

        imgname = str(hash1)
    
        if (getImageLink(driver) != ''):
            photodir = ImgDataDir + "\\" +"Images"+"\\"+ Username
            if (os.path.exists(imagineFuturePath('ImageData','Images',Username,imgname, ".jpg"))):
                continue;
            if not os.path.exists(photodir):
                os.makedirs(photodir)
            photos.append([Username, likes, loci, tags, imgname, photodir])
            DownloadPhoto(driver, ImgDataDir + "\\" +"Images"+"\\"+ Username +"\\"+ imgname)
            
        elif(getVidLink(driver) != ''):
            if (os.path.exists(imagineFuturePath('ImageData','Videos',Username,imgname, ".mp4"))):
                continue;

            imgname = str(hash1)
            viddir = ImgDataDir+ "\\"+"Videos"+"\\"+Username
            if not os.path.exists(viddir):
                os.makedirs(viddir)
            photos.append([Username, likes, loci, tags, imgname, viddir])
            DownloadVideo(driver, viddir +"\\" + imgname)
        else:
            continue;

        try:
            uniqueAddToCSV(ImgDataDir +"\\Logs\\"+ 'log2' + ".csv", photos)
            #saveToCsv(captions, os.path.join(cwd,"ImageData","Captions",Username + ".csv"))
        except:
            saveToCsv(photos,ImgDataDir +"\\Logs\\"+ 'log2' + ".csv")
        getNext(driver)
        randomSleep(3,4)

    saveToCsv(photos,ImgDataDir+"\\Logs\\"+Username + ".csv")
    return photos
def getPhotosandDataFromList(CClist, n, driver):
    for user in CClist:
        driver.get('https://www.instagram.com/' + str(user) + '/')
        try:
            randomSleep(2,3)
            clickFirstThumbnail(driver)
            randomSleep(2,3)
            getPhotosandData(n, driver)
            randomSleep(3,4)
        except:
            continue
#FOLLOWER FUNCTIONS
def getFollwerButtons():
    buttons = driver.find_elements_by_css_selector('body > div.RnEpo.Yx5HN > div > div:nth-child(2) > ul > div > li> div > div.Pkbci > button')
    return buttons
def getFollwingButtons():
    buttons = driver.find_elements_by_css_selector('body > div.RnEpo.Yx5HN > div > div:nth-child(3) > ul > div > li > div > div.Pkbci > button')
    return buttons
def followFollwers(n):
    Followed = readFromCSV('Followed.csv')
    Following = readFromCSV('Following.csv')
    fButtons = getFollwerButtons()
    f = getFollowers()
    newFollowed = []
    for i in range(n):
        try:
            Followed.index(f[i])
            continue
        except ValueError:
            newFollowed.extend(f[i])
            fButtons[i].click()
            randomSleep(1,2)
    _addToCsv('Followed.csv', newFollowed)
    saveToCsv(newFollowed, "Following.csv") ###Check integrity
def unfollow(n):
    buttons = getFollwingButtons()
    following = getFollowing()
    Following = readFromCSV('Following.csv')
    for i in range(n):
        randomSleep(1,2)
        buttons[i].click()
        randomSleep(1,2)
        unfollowButton = driver.find_element_by_css_selector("body > div:nth-child(19) > div > div > div.mt3GC > button.aOOlW.-Cab_")
        unfollowButton.click()
        try:
            Following.remove(following[i])
            saveToCsv('Following.csv')
        except ValueError:
            continue
def getFollowerNum(username, logfolder):
    """Prints and logs the current number of followers to
    a seperate file"""
    user_link = "https://www.instagram.com/{}".format(username)
    driver.get(user_link)

    try:
        followed_by = driver.execute_script(
            "return window._sharedData.""entry_data.ProfilePage[0]."
            "graphql.user.edge_followed_by.count")

    except Exception:  # handle the possible `entry_data` error
        try:
            driver.execute_script("location.reload()")

            randomSleep(1)
            followed_by = driver.execute_script(
                "return window._sharedData.""entry_data.ProfilePage[0]."
                "graphql.user.edge_followed_by.count")

        except Exception:
            followed_by = None

    return followed_by
def getFollowinNum(username, logfolder):
    try:
        followed_by = driver.execute_script(
            "return window._sharedData.""entry_data.ProfilePage[0]."
            "graphql.user.edge_followed_by.count")
    except Exception:  # handle the possible `entry_data` error
        try:
            driver.execute_script("location.reload()")
            randomSleep(1,1)
            followed_by = driver.execute_script(
                "return window._sharedData.""entry_data.ProfilePage[0]."
                "graphql.user.edge_followed_by.count")

        except Exception:
            following = None

    return following
def mineFollowersOfList(l):
    for i in l:
        try:
            driver.get("https://www.instagram.com/" + i + "/")
            randomSleep(2,3)
            sel = "#react-root > section > main > div > ul > li:nth-child(2) > a > span"
            followers_Button = driver.find_element_by_css_selector(sel)
            followers_Button.click()
            randomSleep(60,65)
            followers = driver.find_elements_by_css_selector("#react-root > section > main > div:nth-child(2) > ul > div > li > div > div.t2ksc > div.enpQJ > div.d7ByH > a")
            rfol = [follower.text for follower in followers]
            saveToCsv (rfol , os.getcwd() + "\\\\Data\\\\FLs\\\\ "+ "FL" + i + ".csv") 
        except:
            continue

#HASHTAGS
def getHashtags(driver):
    selector = "body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > ul > div > li > div > div.C7I1f > div.C4VMK > span > a"
    As = driver.find_elements_by_css_selector(selector)
    tags = set()
    for a in As:
        if (a.text.startswith('#')):
            tags.add(a.text)
    return tags
def getManyTags( n,l = [] ):
    for i in range(n):
        l.append(getHashtags(driver))
        getNext(driver)
        randomSleep(2,2)
    return l
def generalIntersection(listWithSets):
    generics = listWithSets[0]
    for i in range(len(listWithSets)):
        s = generics.intersection(listWithSets[i])
        if(s != set()):
            generics = generics.intersection(listWithSets[i])
    return generics
def getHashtagsList():
    caption = getCaption()
    caption = caption.split(" ")
    tags = list(filter(lambda x: x.startswith("#"), caption))
    firstComment = "body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > ul > div > li > div > div.C7I1f > div.C4VMK > span > a"
    As = driver.find_elements_by_css_selector(firstComment)
    for a in As:
        if (a.text.startswith('#')):
            tags.append(a.text)
    return tags
def getHashtagData(n,tags = []):
    for i in range(n):
        tags.append([getHashtagsList(), getLikes(), getUser()])
        getNext(driver)
        sleep(0.5)
    return tags

HASHTAG = "explore/tags/"    
FIRST_THUMB_TAG = "#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div"
def mineTags(target_list, n , tags = [],  driver = driver, Hashtag = None):
    for target in target_list:
        driver.get("https://www.instagram.com/" + Hashtag + target + "/")
        randomSleep(0,1)
        try:
            click(FIRST_THUMB_TAG, driver)
        except:
            continue
        tags = getHashtagData(n, tags = tags)
    return tags

#CSV FUNCTIONS
def saveToCsv(list, name):
    l = pd.DataFrame(list)
    l.to_csv(name, index=False)
def readFromCSVflat(csv):
    df = pd.read_csv(csv)
    return df.values.flatten().tolist()
def readFromCSV(csv):
    try:
        df = pd.read_csv(csv)
        return df.values.tolist()
    except:
        return [];
def _addToCsv(csv, list):
    if not os.path.exists(csv):
        os.makedirs(csv)
    csvlist = readFromCSV(csv)
    csvlist.extend(list)
    saveToCsv(csvlist,csv)
def uniqueAddToCSV(csv,list):
    if not os.path.exists(csv):
        saveToCsv(list,csv)
    else:
        csvlist = readFromCSV(csv)
        csvlist.extend(list)
        csvlist = list(set(csvlist))
        saveToCsv(csvlist,csv)
        
def appendtoCSV(csv, str):
    c = readFromCSVflat(csv)
    if(c.__contains__(str) ==False):
        c.append(str)
    saveToCsv(c, csv)


#Chooser >>>> Set 3 lists
def chooseUsersInList(li, driver = driver):
    for l in li:
        driver.get('https://www.instagram.com/' + l + '/')
        i = 0
        while(i < 1):
            i = 1
            decision = input("Stay or Go (Y/N)")
            decision = decision.lower()
            if decision== "n":
                li.remove(l)
            elif decision== "d":
                appendtoCSV("dCCs.csv", l)

            elif decision== "h":
                appendtoCSV("hCCs.csv", l)

            elif decision== "c":
                appendtoCSV("cCCs.csv", l)
            else:
                 i = i-1


#Administration
def getLogfile(filename):
    return readFromCSV(imagineFuturePath("ImageData","Logs",filename))
def randomChoose(li):
    return li[randint(0,len(li))]
def trash(todaysphoto, todayslog):
    modifiedlog = getLogfile(todayslog)
    modifiedlog.remove(todaysphoto)
    saveToCsv(modifiedlog,imagineFuturePath("ImageData","Logs",todayslog))   
def show(todaysphoto):
    os.startfile(getF_n_L(todaysphoto)[0])

def showimg():
    show(todaysphoto)
def pimg():
    postImage(F_n_L[0])
def isphoto(fp):
    if(fp.split("\\")[7] =="Images"):
        return True
def getF_n_L(logdata):
    if(isphoto(logdata[-1])):
        filepath = logdata[-1] + "\\" + str(logdata[-2]) + ".jpg"
    else:
        filepath = logdata[-1] + "\\" + str(logdata[-2]) + ".mp4"

    location = logdata [2] 
    return filepath, location

#Today's Photo & Data
todayslog = "log1.csv"
todaysphoto= randomChoose(getLogfile(todayslog))
F_n_L = getF_n_L(todaysphoto)

if(isphoto(F_n_L[0])):
    im = Image.open(F_n_L[0])
    im_resized = im.resize((im.width*2, im.height*2), resample = Image.BILINEAR)
    im_resized.show()
    im_final = im_resized.filter(filter=ImageFilter.SHARPEN)
    im_final.save(imagineFuturePath('Data','AI','temp.jpg'))
    fp = imagineFuturePath('Data', 'AI','temp.jpg')
    copyfile(fp, "C:\\Users\\bardi\\IG\\Dreamscape\\temp.jpg")
else:
    fp = F_n_L[0]
    copyfile(fp, "C:\\Users\\bardi\\IG\\Dreamscape\\temp.mp4")
    os.startfile(fp)
print(todaysphoto)

def next():
    todayslog = "log1.csv"
    todaysphoto= randomChoose(getLogfile(todayslog))
    F_n_L = getF_n_L(todaysphoto)
    if(isphoto(F_n_L[0])):
        im = Image.open(F_n_L[0])
        im_resized = im.resize((im.width*2, im.height*2), resample = Image.BILINEAR)
        im_resized.show()
        im_final = im_resized.filter(filter=ImageFilter.SHARPEN)
        im_final.save(imagineFuturePath('Data','AI','temp.jpg'))
        fp = imagineFuturePath('Data', 'AI','temp.jpg')
        copyfile(fp, "C:\\Users\\bardi\\IG\\Dreamscape\\temp.jpg")
        print(todaysphoto)
    else:
        fp = F_n_L[0]
        copyfile(fp, "C:\\Users\\bardi\\IG\\Dreamscape\\temp.mp4")
        os.startfile(fp)
        print(todaysphoto)

def sync():
    os.startfile("C:\\Users\\bardi\\Desktop\\Software\\syncthing-windows-amd64-v0.14.51\\syncthing.exe")



#Concurrent Futures
"""import concurrent.futures
import random 
import datetime
import time
import uuid

def do_something(seconds, name):
	print(f"Sleeping {seconds}\t{name}\t{str(datetime.datetime.now())[:19][11:]}")
	time.sleep(seconds)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
	for i in range(50):
		executor.submit(do_something
			, seconds = random.randint(1,6)
			, name = str(uuid.uuid4())[:6].upper())"""