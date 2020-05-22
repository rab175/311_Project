
#  A Machine Learning Analysis of NYC Non-Emergency Service Requests

## Project Abstract

To support New York City city managers' plans for workload and resource distribution it is important to understand where and when issues will arise across the city. NYC receives roughly 2 million non-emergency service requests (or complaints) via 311 (the city’s non-emergency service line) each year. The city is committed to resolving each complaint received in a timely manner, which means that it must be prepared to anticipate what service requests will be received and to activate and support the appropriate responding city agency. As NYC is a large city with very diverse neighborhoods, the types of requests, the volume of those requests, and the time in which they are resolved are likely to vary greatly in different areas. To help city managers prepare for the future we will visualize and analyze historical 311 data to identify trends in call volume, response times, and geographic concentration of issues. 


## Data

There is a lot of data! NYC 311 has over 10 years worth of service request data that is updated daily via NYC Open Data (see link below), which currently includes over 20 million unique records. There are 40 values for each record that roughly contain time, location, responsible city agency, complaint type, community board, and complaint method (online, phone, etc.). Most of the data is categorical, however a number of continuous variables may be derived. 

To augment this data we will combine it with data from the 2018 U.S. Census American Community Survey 5-year summary (see link and library below). The demographic data will hopefully help us see if there are complaint trends that have a relationship with specific demographic factors. We will use zip codes to specify geographic groups, as that is the clearest geographic grouping in the 311 data still providing for a significant number of different values. As it turns out, the census does not regularly use zip codes, and therefore only estimates zip code approximations for the 5-year summary. These are known as Zip Code Tabulation Areas (ZCTA).  After removing zip codes that do not appear in both sets of data, and removing zip codes with a population of zero, we are left with 184 unique NYC zip codes. 

For this analysis we've also reduced the dataset down to the 6 most common agancies and removed incomplete records, records with dummy values, or values that are non-sensical (e.g. closed date earlier than created date). After cleaning and down selecting our initial dataset is comrised of 24 variables. Select variables include:  

<table>
    <thead>
        <tr>
            <th colspan="5">Select Variables in Cosideration (see full list in link below)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>**Variable**</td>
            <td>**Description**</td>
            <td>**Data type**</td>
            <td>**Unique values**</td>
            <td>**Source**</td>
        </tr>
        <tr>
            <td>Created date</td>
            <td>Date service request was created</td>
            <td>Datetime - year-month-day hour:min:sec</td>
            <td>11,822,621</td>
            <td>NYC 311</td>
        </tr>
        <tr>
            <td>Agency</td>
            <td>Date service request was created</td>
            <td>Categorical - string - ex. 'NYPD' or 'HPD'</td>
            <td>6</td>
            <td>NYC 311</td>
        </tr>
        <tr>
            <td>Complaint Type</td>
            <td>This is the first level of a hierarchy identifying the topic of the incident or condition. Complaint Type may have a corresponding Descriptor or may stand alone.</td>
            <td>Categorical - string - ex. 'Noise - Residential', or 'Heat/Hot Water'</td>
            <td>162</td>
            <td>NYC 311</td>
        </tr>
        <tr>
            <td>Borough</td>
            <td>NYC Borough where request submitted</td>
            <td>Categorical - string - ex. 'BRONX', or 'BROOKLYN'</td>
            <td>6</td>
            <td>NYC 311</td>
        </tr>
        <tr>
            <td>Zip code</td>
            <td>5-digit zip code derived from the reported incident zip and compared to available zip codes (with population > 0) provided by the Census</td>
            <td>Categorical - string - ex. '11101'</td>
            <td>184</td>
            <td>NYC 311 and US Census</td>
        </tr>
        <tr>
            <td>Total population</td>
            <td>Total estimated population within the ZCTA</td>
            <td>Continuous - integer'</td>
            <td>184</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>Median Income</td>
            <td>Estimated median income within the ZCTA</td>
            <td>Continuous - integer'</td>
            <td>183</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>HS or above</td>
            <td>Estimated % with high school degree or above</td>
            <td>Continuous - integer'</td>
            <td>184</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>Response time</td>
            <td>Duration of time between service request created data and closed date - in days</td>
            <td>Continuous - integer'</td>
            <td>>10 million</td>
            <td>Calculated from 311 data</td>
        </tr>
    </tbody>
</table>



### Final Project Requirements

Congratulations on making it to the final project! It's been a long journey, but we can finally see the light at the end of the tunnel!

<center><img src='https://raw.githubusercontent.com/learn-co-curriculum/dsc-capstone-project-v2/master/end-of-tunnel.gif'>
<strong><em>Actual Footage of you seeing the light at the end of the tunnel</strong></em>
</center>

Now that you've learned everything we have to teach you, it's time to show off and flex your data science muscles with your own **_Capstone Project_**! This project will allow you to showcase everything you've learned as a data scientist to by completing a professional-level data science project of your choosing. This project will be significantly larger than any project you've completed so far, and will be the crown jewel of your portfolio. A strong capstone project is the single most important thing you can do to get the attention of potential employers, so be prepared to put as much effort into this project as possible--the results are **_worth it!_**

<center><img src='https://raw.githubusercontent.com/learn-co-curriculum/dsc-capstone-project-v2/master/milkshake.gif'>
<strong><em>Your <s>milkshake</s> portfolio brings all the <s>boys</s> employers to <s>the yard</s> your inbox! </strong></em>
</center>

Let's take a look at the project requirements.

### Topic requirements
The projects are in a domain of your choosing.  Your project does not have to answer just one question, but may try to answer multiple questions in a domain, or subsequent questions.  (e.g. Now that we know _X_, what's the next question that comes from this?)  When choosing a topic, try to think through the "So what?" of your question.  

* What are the possible outcomes you think you will find? 
* How could a company or individual make use of your findings to benefit them?  What about your findings are _actionable_?

You're completely free to choose any project topic that interests you. However, the project scope must be end-to-end, from data sourcing and cleaning all the way through tuning and analysis of your trained model(s). 

Make sure to plan in advance for feasibility of the question in the time allowed--consider the following questions when selecting your project topic:

* What version this question would allow me to find an answer in a feasible amount of time?
* What version of this question would allow me/motivate me to work on this problem even after completing Flatiron School?

### Technical Requirements

Your project must meet the following technical requirements:

1. **_No Off-The-Shelf Datasets_**. This project is a chance for you to highlight your critical thinking and data gathering skills by finding the perfect dataset to answer your question. If a pre-existing dataset exists that you'd like to use, it is okay to use it in your project. However, you should consider combining it with other existing sources of data, modifying the dataset through feature engineering. The goal here is to showcase your ability to find and work with data, so just grabbing Boston Housing Dataset or the MNIST dataset is out of the question. 

2. **_Strong Data Exploration, with at least 4 relevant data visualizations._**  Think of this project as a way for your to showcase your best possible work in every area that matters. There are few skills that impress employers more than the ability to dive into a new dataset and produce engaging visualizations that communicate important information. For this project, anything worth knowing is worth visualizing. Consider all that you have learned, and don't be afraid to dig into more advanced visualization libraries like seaborn to see what you make! You should make use of visualizations whenever possible during this project, not just during the Data Exploration phase--for instance, consider visualizing your confusion matrices rather than just printing them out as text!

3. **_Makes use of Supervised Learning_**. This requirement dovetails with having a well-defined question, because you'll make use of supervised learning to find the answer! It is both acceptable and encouraged to make use of **_Unsupervised Learning_** techniques as needed in your project (for instance, segmentation with clustering algorithms), but the supervised learning should play a central role in answering your question. 

4. **_Explicitly makes use of a Data Science Process such as OSEMN or CRISP-DM_**. This part is fairly straightforward--you should select a Data Science Process to use and then use this to give structure to your project. Each section should be clearly delineated in your Jupyter Notebook.  

5. **_A well-defined question, with a well-defined answer._** Your project should clearly state the question you are trying to answer, and provide any background context needed to understand it. For instance, if you are trying to detect fault lines using Earthquake data, you should provide a brief primer on both the topic and your dataset so that the reader can better understand your topic and approach.  Similarly, the findings of your project should be clearly communicated. Do not just tell your audience the final accuracy of your models--be sure to answer "big picture" questions as well. For instance--why are these findings important or useful? Would you recommend shipping this model to production, or is more work needed? Who are these findings useful to, and why should they care?  **_NOTE:_** Inconclusive results are okay--from a purely scientific perspective, they are no more or less important or valuable than any other kinds of results. If your results are inconclusive, you should discuss what your next steps would be from there. For instance, what do you think it would take to get conclusive results--more data? Different data that was unavailable? Both? 


## Deliverables

For online students, the deliverables for this project consist of the following three components:

1. A Jupyter notebook for a presentation.
  * The Jupyter notebook will have two components:
    1. An **_Abstract_** section that briefly explains your problem, your methodology, and your findings, and business recommendations as a result of your findings. This section should be 1-2 paragraphs long.  
    2. The technical analysis for a data science audience. This detailed technical analysis should explicitly follow a Data Science Process as outlined in the previous section. It should be well-formatted and organized, and should contain all code, visualizations, and detailed explanations/analysis.
    
2. An organized **README.md** file in the GitHub repository containing your project code that describes the contents of the repository. This file should be the source of information for navigating through all the code in your repository. 
    
3. A blog post showcasing your project, with a focus on your methodology and findings. A well-written blog post about your project will probably be the first thing most recruiters and hiring managers see, so really take the time to polish up this blog post and explain your project, methodology, and findings/business recommendations in a clear, concise manner. This blog post should cover everything important about your project, but remember that your audience for this blog post will largely be non-technical. Your blog post should definitely contain visualizations, code snippets, and anything else you find important, but don't get bogged down trying to explain highly technical concepts. Your blog post should provide a link to the Github repository containing your actual project, for people that want to really dive into the technical aspects of your project.
* Refer back to the [Blogging Guidelines](https://github.com/learn-co-curriculum/dsc-welcome-blogging) for the technical requirements and blog ideas.

Note: On-campus students may have different deliverables, please speak with your instructor.

### Rubric 

Online students can find a PDF of the rubric for the final capstone project [here](https://github.com/learn-co-curriculum/dsc-capstone-project-v2/blob/master/capstone_project_rubric.pdf). _Note: On-campus students may have different requirements, please speak with your instructor._


## Final Project Proposals (2 project ideas)

Selecting the right topic and selecting a problem with the appropriate scope can make or break a good project before you even begin. When starting, try to think up at least 2 different project ideas to explore that you can discuss with your instructor.  Consider the following questions when coming up with your project. 

### Project Ideation Questions

1. What question/questions are you trying to solve?
  * What are the outcomes you think you will find (could use mutually exclusive collectively exhaustive for this)? Why do they matter?
  * How would a person or business take action upon learning the results of your project? How will your findings be _useful_?
  * What version this question would allow me to find an answer in 2-3 days?
  * What version of this question would allow me/motivate me to work on this problem even after completing Flatiron School?

2. What are some data sources that would allow you to answer this?
  * What is the ideal data you would hope to gather to answer this question?  
  * Potentially missing data, that could cause omitted variable bias?
3. Is this a classification task? A regression task? Both?
4. What are the challenges or obstacles you foresee with this project?
5. What are your next steps moving forward?

### Example Student Project

To give you a frame of reference, take a look at this amazing [technical report](https://github.com/paulinaczheng/twitter_flu_tracking) from a previous student that used tweet data to predict the weekly number of flu cases during flu season. Pay attention to how well structured the project is, and how much she relies on great visualizations to tell her story for her. Your explanations don't have to be wordy--a visualization is worth a thousand words!
 

# Summary

The Capstone Project and project review are the most critical part of the program. They give you a chance to both bring together all the skills you've learned into realistic projects and to practice key "business judgement" and communication skills that you otherwise might not get as much practice with.  Most importantly, they provide employers with very strong signal about your technical abilities, and allow you to show the world what an amazing Data Scientist you've become!

The projects are serious and important. They are not graded, but they can be passed and they can be failed. Take the project seriously, put the time in, ask for help from your peers or instructors early and often if you need it, and treat the review as a job interview and you'll do great. We're rooting for you to succeed and we're only going to ask you to take a review again if we believe that you need to. We'll also provide open and honest feedback so you can improve as quickly and efficiently as possible.

We don't expect you to remember all of the terms or to get all of the answers right. If in doubt, be honest. If you don't know something, say so. If you can't remember it, just say so. It's very unusual for someone to complete a project review without being asked a question they're unsure of, we know you might be nervous which may affect your performance. Just be as honest, precise and focused as you can be, and you'll do great!
