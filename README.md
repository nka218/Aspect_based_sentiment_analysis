# Aspect_based_sentiment_analysis
Aspect-Based Sentiment Analysis (ABSA) is a type of text analysis that categorizes opinions by aspect and identifies the sentiment related to each aspect.
By aspects, we consider attributes or components of an text review (food or a service, staff etc).

Let’s take an example like the one below. The goal here for the ABSA system is to identify the aspects – food,service,staff – with their related sentiment. 
In other words, <br /> 
food: positive, <br />
service: negative <br />
and staff neutral. 

 

I was offerd a food here in this hotel, I was offered good food with sushi and the serving of food was impressive. But I experienced bad service here. however the staff here was ok.


Notice that in the same text, different aspects can have different sentiments. In this sense, the output of ABSA is not meant to be a general indication of the sentiment expressed in the text but aims at providing a more granular and detailed level of information.  <br />
positive aspect :- good food (talking about food as aspect and giving positive sens.) <br />
negative aspect :- bad service( talling about service in negative sens.) <br />
neurtal aspect :- staff ( talking about staff with ok means neutral while talking about staff.) <br />


# Objective:
  1. Create a high-level visualization of the sentiment in the hotel review based on the aspects in the review.
  2. Make sense of negative, positive, and words present in the review for a particular aspect. Visualization of positive negative word counts using lexicons.
  3. Find the aspects in the hotel review and divide them into positive, negative, or neutral aspects based on sentiment analysis.
  4. Also, integrate it with any text for its aspect and its sentiment analysis. Create a dashboard for the visualization of the sentiments for the aspects in the review, distribution of the emotions in the reviews using lexicon, visualization of the sentences corresponding to the aspects.


# Directory Structure:

	|- root directory
		|- media
		|- Nrc-paper
		|- root_img
		|-sentiment_analysis
		|- src
		|- templates
		|- manage.py
		|- requirements.txt
		|- db.sqlite3 
		

# Input:- 
1. File Format should be either .csv or .json.
2. In any of the file there should be a column named "reviewText",where all the reviews should be kept and gender.
3. Example files are kept under src/test folder upload any text file from there.

# Output:- 
1. High level visualization of sentiments.
2. graph 1 shows   
