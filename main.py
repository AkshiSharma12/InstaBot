import requests,urllib
from token import APP_ACCESS_TOKEN,AS
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (AS)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
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

def get_user_id(insta_username):
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


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (AS)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
     if len(own_media['data']):
         image_name = own_media['data'][0]['id'] + '.jpeg'
         image_url = own_media['data'][0]['images']['standard_resolution']['url']
         urllib.urlretrieve(image_url, image_name)
         print 'Your image has been downloaded!'
     else:
         print 'Post does not exist!'
    else:
         print 'Status code other than 200 received!'

def get_user_post(insta_username):
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
          print 'Your image has been downloaded!'
      else:
          print 'Post does not exist!'
  else:
      print 'Status code other than 200 received!'

#def get_likes():
  #request_url = (BASE_URL + 'users/{user-id}/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
  #print 'GET request url : %s' % (request_url)

def get_post_id(insta_username):
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
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": AS}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()
  if post_a_like['meta']['code'] == 200:
      print 'Like was successful!'
  else:
      print 'Your like was unsuccessful. Try again!'



def post_a_comment(insta_username):
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

post_a_comment('_as1228_')