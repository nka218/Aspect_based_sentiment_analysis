from textblob import TextBlob
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from textblob import Word
from collections import Counter
import collections
import requests
from nltk.stem.snowball import SnowballStemmer


def get_aspect_df(file_url):
    try:
        data=pd.read_json(file_url,lines=True)
    except:
        data=pd.read_csv(file_url)

    male_count=data[data.gender=='Male'].shape[0]
    female_count=data[data.gender=='Female'].shape[0]
    male_review=list(data[data.gender=='Male'].reviewText.values)
    female_review=list(data[data.gender=='Female'].reviewText.values)
        
    text_data=list(data['reviewText'].values)
    review_data=pd.DataFrame(zip(text_data),columns=['text'])
    filepath = ('src/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    emolex_df = pd.read_csv(filepath,
                            names=["word", "emotion", "association"],
                            sep='\t')
    emolex_words = emolex_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
    emotions = emolex_words.columns.drop('word')
    emo_df = pd.DataFrame(0, index=review_data.index, columns=emotions)
    stemmer = SnowballStemmer("english")
    for i, row in review_data.iterrows():
        document = word_tokenize(review_data.loc[i]['text'])
        for wor in document:
                    wor = stemmer.stem(wor.lower())
                    emo_score = emolex_words[emolex_words.word == wor]
                    if not emo_score.empty:
                        for emotion in list(emotions):
                            emo_df.at[i, emotion] += emo_score[emotion]
    review_data = pd.concat([review_data, emo_df], axis=1)
    emotions_values=list(review_data.sum(axis = 0, skipna = True) .values[1:])

    emotions_name=[x.title() for x in list(review_data.sum(axis = 0, skipna = True).index[1:])]    
    stop_words = set(stopwords.words("english"))
    stop_words=stop_words
    punc=string.punctuation
    punc_list=[]
    for i in punc:
        punc_list.append(i)
    lemmatizer = WordNetLemmatizer()        #Convert into actual words

     
    wordz=[]
    data_text_male=[]
    for sent in male_review:
        TAG_RE = re.compile(r'<[^>]+>') # remove html_tags
        result = re.sub(TAG_RE, ' ', sent)
        result = re.sub(r"http\S+", " ", result) # remove links 
        result = re.sub(r'\d+', " ", result) # remove no.
        result = [not_punc for not_punc in result.split(" ") if not not_punc in punc_list if len(not_punc)<=10]
        words=[i.lower() for i in result]
        # words =[lemmatizer.lemmatize(word) for word in words]
        inter_data=" ".join(words) 
        data_text_male.append(inter_data)

    wordz=[]
    data_text_female=[]
    for sent in female_review:
        TAG_RE = re.compile(r'<[^>]+>') # remove html_tags
        result = re.sub(TAG_RE, ' ', sent)
        result = re.sub(r"http\S+", " ", result) # remove links 
        result = re.sub(r'\d+', " ", result) # remove no.
        result = [not_punc for not_punc in result.split(" ") if not not_punc in punc_list if len(not_punc)<=10]
        words=[i.lower() for i in result]
        # words =[lemmatizer.lemmatize(word) for word in words]
        inter_data=" ".join(words) 
        data_text_female.append(inter_data)    


    wordz=[]
    data_text=[]
    for sent in text_data:
        TAG_RE = re.compile(r'<[^>]+>') # remove html_tags
        result = re.sub(TAG_RE, ' ', sent)
        result = re.sub(r"http\S+", " ", result) # remove links 
        result = re.sub(r'\d+', " ", result) # remove no.
        result = [not_punc for not_punc in result.split(" ") if not not_punc in punc_list if len(not_punc)<=10]
        words=[i.lower() for i in result]
        # words =[lemmatizer.lemmatize(word) for word in words]
        inter_data=" ".join(words) 
        data_text.append(inter_data)

    comments_male = TextBlob(' '.join(data_text_male))
    comments_female = TextBlob(' '.join(data_text_female))
    male_sentences=comments_male.sentences
    female_sentences=comments_female.sentences

    cleaned = list()
    comments = TextBlob(' '.join(data_text)) 


    for phrase in comments.noun_phrases:
        count = 0
        if len(comments.sentences)<10:
            for w in phrase.split():
                    if len(w) >= 2:
                        cleaned.append(phrase) 
        else:
            for w in phrase.split():
                if len(w) <= 2 or (not Word(w).definitions):
                    count += 1 

            if count < len(phrase.split())*0.4: 
                cleaned.append(phrase)

    twowordnp = []

    for Phrase in cleaned:
        if Phrase.count(' ') <= 1:
            twowordnp.append(Phrase)

    feature_count = dict()


    for phrase in twowordnp:
        count = 0
        for word in phrase.split():
            if word not in stopwords.words('english'):
                count += comments.words.count(word)
        feature_count[phrase] = count
    counts = collections.Counter(feature_count)
    new_list = sorted(feature_count, key=counts.get, reverse=True)

    absa_list = dict()
    for f in new_list:
        absa_list[f] = list()
        for comment in data_text:
            blob = TextBlob(comment)
            for sentence in blob.sentences:
                if str(sentence).find(f)!=-1:
                    absa_list[f].append(sentence)

    scores = list()
    absa_scores = dict()
    Positive=list()
    ASP0=list()
    Neutral=list()
    Negative=list()
    Aspect = list()
    aspect = list()
    total1 = list()
    p_male=0
    p_female=0
    nu_male=0
    nu_female=0 
    ne_male=0
    ne_female=0
    main = pd.DataFrame()
    for k, v in absa_list.items():
        if  absa_list[k]:
            p = 0
            nu = 0
            ne = 0
            aspect.append(k)
            # k define the name of aspect and v define the sentences of each aspect
            counter = Counter()
            absa_scores[k] = list()
            for sent in v:
                score = sent.sentiment.polarity
                if score> 0:
                    if str(sent) in female_sentences:
                        p_female +=1
                    else:
                        p_male +=1
                        
                   # print('positive')
                    p = p+1
                    
                elif score == 0:
                    if str(sent) in female_sentences:
                        nu_female +=1
                    else:
                        nu_male +=1
                    #print('neutral')
                    nu = nu+1  
                else:
                    if str(sent) in female_sentences:
                        ne_female +=1
                    else:
                        ne_male +=1
                   # print('negative')
                    ne = ne+1
                scores.append(score)
                absa_scores[k].append(score)

            #Calculate total number of positive, negative and neutral tweets for each aspect
            s = len(v)
            total = str((p)+(nu)+(ne))
            total1.append(total)

            asd = k + ":" + " Positive = " + str(p) + "," +"Neutral = " + str(nu) + "," +"Negative = " + str(ne)
            ASP0.append(asd)

            p = float(p)

            asd_per = float((p/ float(s)) * 100)
            Positive.append(asd_per)

            nu = float(nu)
            asd_per1 = float((nu/ float(s)) * 100)
            Neutral.append(asd_per1)

            ne = float(ne)
            asd_per2 = float((ne/ float(s)) * 100)
            Negative.append(asd_per2)

            asd0 = k
            Aspect.append(asd0)


        #print(ASP0)

        d = {'Aspect': Aspect, 'Positive': Positive, 'Neutral': Neutral, 'Negative': Negative}
        
        #b = df.to_dict('split')
        #main = pd.concat((main,df))
    df = pd.DataFrame(d)
    df.to_csv("src/data_frame.csv",index=False)

    name=[]
    score=[]
    for i in absa_list.keys():
        for j in absa_list[i]:
            name.append(i)
            score.append(str(j))
    absa_df=pd.DataFrame(zip(name,score),columns=['name','score'])

    # print("done abs")

    name=[]
    score=[]
    for i in feature_count.keys():
            name.append(i)
            score.append(feature_count[i])
    feature_count_df=pd.DataFrame(zip(name,score),columns=['name','score'])

    # print("done feature_count")
        
    male_lis=[round((p_male/(p_male+nu_male+ne_male))*100,1),round((ne_male/(p_male+nu_male+ne_male))*100,1),round((nu_male/(p_male+nu_male+ne_male))*100,1)]
    female_lis=[round((p_female/(p_female+nu_female+ne_female))*100,1),round((ne_female/(p_female+nu_female+ne_female))*100,1),round((nu_female/(p_female+nu_female+ne_female))*100,1)]

    absa_df.to_csv("src/absa_df.csv",index=False)
    feature_count_df.to_csv("src/feature_count_df.csv",index=False)

    return feature_count,absa_list,df,male_lis,female_lis,male_count,female_count,emotions_values,emotions_name