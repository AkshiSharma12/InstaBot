import requests,urllib
#imports requests and urllib libraries
from textblob import TextBlob
#imports textblob from TextBlob library
from textblob.sentiments import NaiveBayesAnalyzer
from token1 import AS
#Sandbox Users : _as1228_
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    #function to fetch user's own information
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (AS)
    #url fetches user's information by using the access token of the user
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    #get call to fetch the data
    #json object gives response in form of a dictionary
    print user_info

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
        exit()

def get_user_id(insta_username):
    #function to get other user's id
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, AS)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

def get_user_info(insta_username):
    #function to get other user's information using user id
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, AS)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'
        exit()



def get_own_post():
    #function to fetch own recent post
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (AS)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
     if len(own_media['data']):
         image_name = own_media['data'][0]['id'] + '.jpeg'
         #retrieving the data from the dictionary
         image_url = own_media['data'][0]['images']['standard_resolution']['url']
         urllib.urlretrieve(image_url, image_name)
         print 'Your image has been downloaded!'
     else:
         print 'Post does not exist!'
    else:
         print 'Status code other than 200 received!'
         exit()
def get_user_post(insta_username):
    #function to fetch other user's recent post
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AS)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()
  if user_media['meta']['code'] == 200:
      if len(user_media['data']):
          image_name = user_media['data'][0]['id'] + '.jpeg'
          image_url = user_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          #retrieving image info from the dictionary
          print 'Your image has been downloaded!'
      else:
          print 'Post does not exist!'
  else:
      print 'Status code other than 200 received!'
      exit()

def get_post_id(insta_username):
    #function to get the id of a post
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AS)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def like_a_post(insta_username):
    #function to like a post of the given user
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": AS}
    #the data being sent with the post is stored in payload
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()
    #post request to post the like
  if post_a_like['meta']['code'] == 200:
      print 'Like was successful!'
  else:
      print 'Your like was unsuccessful. Try again!'
      exit()

def recent_like():
    #function to fetch the recently liked post by the user
    request_url=(BASE_URL+ 'users/self/media/liked?access_token=%s') % (AS)
    print 'Get request url : %s' %(request_url)
    own_media=requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'No recent media liked!'
    else:
        print 'Status code other than 200 received!'
        exit()

def get_comment_list(insta_username):
    #function to fetch list of comments on the recent post of the other user
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+ 'media/%s/comments?access_token=%s') %(media_id,AS)
    print 'Get request url : %s' %(request_url)
    comment_list=requests.get(request_url).json()

    if comment_list['meta']['code']==200:

        if len(comment_list['data']):
            for x in range(0,len(comment_list['data'])):
                comment_text=comment_list['data'][x]['text']
                print "Comment List: %s" %(comment_text)

        else:
            print 'There is no comment on this post!'
    else:
        print 'Status code other than 200 received!'
        exit()


def post_a_comment(insta_username):
    #function to post a comment on the other user's recent post
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": AS, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"
        exit()


def delete_negative_comment(insta_username):
    #function to delete negative comments from a post
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, AS)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    #condition to check if comment is negative or positive
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, AS)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    #delete request to delete the negative comment


                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
        exit()

def target_caption_comments(insta_username):
    #function for posting targetted comments on a post based on the caption

        user_id = get_user_id(insta_username)
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, AS)
        print 'GET request url : %s' % (request_url)
        caption_info = requests.get(request_url).json()
    #get call to fetch caption info of the post

        if caption_info['meta']['code'] == 200:

            if len(caption_info['data']):

                for y in range(0, len(caption_info['data'])):

                    caption_text =str(caption_info['data'][y]['caption'])
                    caption = caption_text.split(" ")
                    if 'Shopping' in caption:

                        print 'Read Caption: %s' % (caption)
                        media_id = get_post_id(insta_username)
                        comment_text = "AMAZON Monday Deals Week. Get your free gift card worth 5000. Only a few days left!. Get it "
                        payload = {"access_token": AS, "text": comment_text}
                        request_url = (BASE_URL + 'media/%s/comments') % (media_id)
                        print 'POST request url : %s' % (request_url)

                        make_comment = requests.post(request_url, payload).json()

                        if make_comment['meta']['code'] == 200:
                            print "Successfully Posted Targetted Comment!"
                        else:
                            print "Unable to add comment. Try again!"
                    else:
                        print 'There is no caption on the post!'

        else:

            print 'Status code other than 200 received!'
            exit()


def target_hashtag_comments():
    #function for posting targetted comments on a post based on hashtag
    tag_name = 'choclate'
    #asking user to input the hashtag
    request_url = (BASE_URL + "tags/%s/media/recent?access_token=%s") % (tag_name, AS)
    post_tag = requests.get(request_url).json()
    if post_tag['meta']['code'] == 200:
        comment_text = raw_input("Your comment: ")
        payload = {"access_token": AS, "text": comment_text}
        for ids in range(0, len(post_tag["data"])):
            media_id = post_tag["data"][ids]["id"]
            user_name = post_tag["data"][ids]["user"]["username"]
            print "%s media of %s user" % (media_id, user_name)
            request_url = (BASE_URL + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            make_comment = requests.post(request_url, payload).json()
            if make_comment['meta']['code'] == 200:
                print "Successfully added a new comment!"
            else:
                print "Unable to add comment. Try again!"
                exit()


def target_location_comments():
    #posting targetted comments on a post based on the location
    #here default location has been taken
    lat2 = 30.7333
    long2 = 76.7794
    request_url = (BASE_URL + "media/search?lat=%f&lng=%f&access_token=%s&distance=5000") % (lat2, long2, AS)
    locate = requests.get(request_url).json()
    if locate['meta']['code'] == 200:
        if len(locate['data']):
            keyword = raw_input("What are you searching for ?:")
            comment_text = raw_input("Your comment: ")
            for ids in range(0, len(locate["data"])):
                caption_text = str(locate["data"][ids]["caption"])
                comment = caption_text.split(" ")

                if keyword in comment:
                    print "keyword found in post"
                    media_id = locate["data"][ids]["id"]
                    payload = {"access_token": AS, "text": comment_text}
                    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
                    make_comment = requests.post(request_url, payload).json()
                    if make_comment['meta']['code'] == 200:
                        print "Successfully added a new comment!"
                    else:
                        print "Unable to add comment. Try again!"
                else:
                    print"your searched keyword in not in the recent media from this location"
        else:
            print "no data present"
    else:
        print "status code other than 200 received"
        exit()


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get recent media liked by the user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Target comment on posts based on caption\n"
        print "k.Target comment on posts based on hashtag\n"
        print "l.Target comment on posts based on location\n"
        print "m.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"

            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"

            get_user_post(insta_username)
        elif choice=="e":
           recent_like()
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"

            like_a_post(insta_username)
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                print "Invalid entry. Please enter a Valid Name!"

        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
               print "Invalid entry. Please enter a Valid Name!"

           get_comment_list(insta_username)
           if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
               print "Invalid entry. Please enter a Valid Name!"

        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
               print "Invalid entry. Please enter a Valid Name!"

           post_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
               print "Invalid entry. Please enter a Valid Name!"

           delete_negative_comment(insta_username)
        elif choice == "j":
           insta_username=raw_input("Enter the username of the user: ")
           if set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
               print "Invalid entry. Please enter a Valid Name!"

           target_caption_comments(insta_username)
        elif choice=="k":
            target_hashtag_comments()
        elif choice=="l":
            target_location_comments()
        elif choice=="m":
             exit()
        else:
            print "wrong choice"

start_bot()