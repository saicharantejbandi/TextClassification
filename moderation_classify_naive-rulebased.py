import pandas as pd

'''
dictionary=['remove', "unfortunately", "repost","naming rule", "ban","banned", "removed",
            'removing', "block", "not appropriate", "not allowed","spam","does not belong", 
            "doesn't belong","viloation", "sidebar rules","give us cancer","no swearsies",
            "siderbar","not tagged correctly","asking for upvotes","no cakeday","little content",
            "resubmit your post","reminder","please do not","not allowe","re-submit","is not suitable for this subreddit",
            "no politic","may not be suitable","please use","re-upload","too little content","reminder","entirely of capitals",
            "should be resubmitted","no longer allow","we only allow","markdown","submission","seem to be yelling",
            "resubmit","valid url","download site","resubmitting","please use","rules",
            "add the flair","consider posting","please do not","no longer suitable","re-post",
            "guidelines","should not be submitted","require approval","removal","rule","your post",
            "please add","your account is too young","please refrain from posting polls",
            "more approriate","top level comment"]
'''
dictionary={"removal":['remove', "will be banned", "banned in future", "bad link", "not appropriate", "not allowed here", "spam","offensive","seem to be yelling"]
            , "ban_off":["ban"], 
            "warning":["do not","warn", " next time do"],
            "recommendation":["you on the wrong sub","do the opposite", "edit this", "i will unblock", "i'll unblock","i recommend","try /r","please use","try resubmitting", 
            "please use","may i suggest", "this belongs in", "report him","please check","try adding", "please add","consider posting"],
            "explain":["we admins", "sorry for the inconvenience", "pointed it out","rely on user","posting personal","mod here", "refer to rule","no swearsies","require approval"],
            "answering":["isn't the correct sub","don't post", "i am going to remove this","i have to remove this", "i'm going to remove this", "i've to remove this",
             "please refrain from posting polls","we only allow","no longer allow","too little content", "no cakeday","we only allow","not tagged correctly"],
             "flair":["gold", "gliding"]}

    



df = pd.read_csv('C:\Master Docs\ASU\Sem 2\Emily\Moderation\moderation\human_mod_cmts.csv',encoding='utf-8')
print(df.shape)

for i, row in df.iterrows():
    print('i')
    print(i)
 
    content = str(row['body_no_quote']).lower()

    flag = 1
    do=1
    for m in dictionary:
        if do:

            for j in dictionary[m]:

                if j in content:
                    df.at[i,m] = 1
                    flag = 0
                    do=0
                    for n in dictionary:

                        if n!=m:

                            df.at[i,n] = 0
                    df.at[i,"engage"] = 0
                    break
    if flag:

        df.at[i,"engage"] = 1
        for n in dictionary:

            if n!="engage":

                df.at[i,n] = 0
    
df.to_csv('human_mod_cmts_rules.csv',encoding='utf-8')

    




        


