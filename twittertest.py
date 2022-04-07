import pandas as pd
import advertools as adv
from datetime import date

auth_params = {
    'app_key': 'dpCeHm2DJEwkvCpvtY6ihHQ5k',
    'app_secret': '9vQly1Ep2g0YFZC1vkgiWG1g6rw3QR6PTyLlAzoDD1ClevYMkq',
    'oauth_token': 'TkJ1azUyOGs1bUs1TllnRVh4Y3o6MTpjaQ',
    'oauth_token_secret': 'HdpoGg3IPSaaOY2lyUGZ-gnLTr6mY76nARr4EPCSb0qc_dWv-R',
}

today = str(date.today())
adv.twitter.set_auth_params(**auth_params)


alerts_list = {"searchliaison":"core|update|algorithm","googlesearchc":"search/sconsole"} 
df1 = pd.DataFrame(columns = ['TwitterHandle', 'Message'])

for keys,values in alerts_list.items():
    df = adv.twitter.get_user_timeline(screen_name=keys,tweet_mode="extended")

df['tweet_created_at'] = df['tweet_created_at'].astype('string') 
df = df[df['tweet_full_text'].str.contains(values,regex=True) & df['tweet_created_at'].str.contains(today)]

if len(df.index) > 0:
    df1 = df1.append({'TwitterHandle' : keys, 'Message' : df['tweet_full_text']}, ignore_index = True)

getlist = dict(zip(df1['TwitterHandle'].tolist(),df1['Message'].tolist()))
emailmessage = ""

if len(df1.index) > 0:
    for key, value in getlist.items():
        emailmessage += key + ": " + value + "\n\n"
    print(emailmessage)
    