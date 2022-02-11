-- Looking at the data to see what we're working with 

SELECT * FROM dbo.NYR_Twitter
order by 1,3

-- Checking to see what categories are available

SELECT DISTINCT tweet_category FROM dbo.NYR_Twitter

-- Checking to see which categrories had the most tweets (desc) using partition

SELECT tweet_created, tweet_category, tweet_state, user_gender,
COUNT (tweet_category) OVER (PARTITION BY tweet_category)
AS TotalTweetsPerCategory
FROM dbo.NYR_Twitter
ORDER BY 5 desc

-- Personal Growth had most tweets (1678) followed by Humour (887) Health (825) Recreation & Lifetyle (461) Family/Friends (327) Finance (167) Career (123) Education/Training (87) Time Management (85) Philanthropic (83)

-- Further analysis, differentiating tweets by state

SELECT tweet_created, tweet_category, tweet_state, user_gender,
COUNT (tweet_category) OVER (PARTITION BY tweet_state)
AS TotalTweetsPerCategory
FROM dbo.NYR_Twitter
ORDER BY 5 desc

-- Most tweets came from LA, then NY, TX Fl.. as expected relative to population 

-- Doing the same analysis for gender

SELECT tweet_created, tweet_category, tweet_state, user_gender,
COUNT (tweet_category) OVER (PARTITION BY user_gender)
AS TotalTweetsPerCategory
FROM dbo.NYR_Twitter
ORDER BY 5 desc

-- 2367 Females 2356 Males

SELECT tweet_created, tweet_category, tweet_state, user_gender,
COUNT (tweet_category) OVER (PARTITION BY tweet_category,user_gender)
AS TotalTweetsPerCategory
FROM dbo.NYR_Twitter
ORDER BY 5 desc

-- Tweets per category per gender

SELECT tweet_created, tweet_category, tweet_topics, tweet_state, user_gender,
COUNT (tweet_topics) OVER (PARTITION BY tweet_category, tweet_topics)
AS TotalTweetsPerTopic
FROM dbo.NYR_Twitter
ORDER BY 6 desc,tweet_category,tweet_topics, user_gender

-- Tweets per topic 
-- Conclusions Most tweeted topic was "Be more positive" (463) followed by "improve my attitude" (175)
-- Least tweeted topic "Learn to cook" (1) and "Wake up earlier" (2)
