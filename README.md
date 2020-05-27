
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
            <td><b>Variable</b></td>
            <td><b>Description</b></td>
            <td><b>Data type</b></td>
            <td><b>Unique values</b></td>
            <td><b>Source</b></td>
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
            <td>Continuous - integer</td>
            <td>184</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>Median Income</td>
            <td>Estimated median income within the ZCTA</td>
            <td>Continuous - integer</td>
            <td>183</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>HS or above</td>
            <td>Estimated % with high school degree or above</td>
            <td>Continuous - integer</td>
            <td>184</td>
            <td>US Census</td>
        </tr>
        <tr>
            <td>Response time</td>
            <td>Duration of time between service request created data and closed date - in days</td>
            <td>Continuous - integer</td>
            <td>>10 million</td>
            <td>Calculated from 311 data</td>
        </tr>
    </tbody>
</table>




## Approach

We used the OSEMN (**O**btain, **S**crub, **E**xplore, **M**odel, I**N**terpret) framework for planning and executing our project. The primary questions we sought to answer were: 

Can we reliably predict daily service request volume?
Can we reliably predict service request response times?
Are there noticeable differences in service request types, volumes, or responses across different areas (boroughs or zipcodes)? 

To predict daily service request volume and response times we compared the results from a number of modeling approaches including Seasonal Autoregressive Integrated Moving Average (SARIMA), Random Forest Regression, Linear Regression, and Long Short-Term Memory (LSTM) neural networks. 

To identify and analyze geographic trends we visualized the date and conducted hypothesis tests.  


## Outcomes

Before moving into our ML analysis predicting response times and call volumes, we explored and visualized the data to observe a few high level trends. We observed that different complaint types and areas of the city express very different trends. This ultimately led to the useful insight that our models need to be pointed at fairly specific slices of the data. Since our models in this instance are univariate, that's not too surprising. Model performance was not as strong when it attempted to predict something like citiy-wide respose time. Considering that we were looking at ~30 different types of complaints from across a very diverse metropolitan area, again, that's not too surprising. The response for a noise complaint is likely more timely that something like a pothole or a dead tree, as the issues occur over different time frames and have very different responses. 

For the sake of simplicity for this project we modeled only city-wide trends and trend concerning the most populat complaint types. But first we were intrested to see how demographics and geography may relate to how residents experience response time or types of issues. 

<center>
    <strong><em> Zip codes in the top income range expereience statistically significantly differnt response times than zip codes in lower income ranges</strong></em>
    <img src='images/Noise Response Distribution.png'>
</center>

Our first observation was that median income of a zipcode does appear to have some relationship with response times for residential noise complaints, as there is a statistically significant differrence in mean response times across income ranges. Futher analysis is required to look into this, as a number of other factors likely contribute more directly to the mean response time for these differnt areas, such as volume of complaints or geographic concentration/dispersion, but it is an interesting first insight. 

<center>
    <strong><em> Most common complaint type by zipcode</strong></em>
    <img src='images/Top Complaint Category by Zip.png'>
</center>

Another interesting thing to observe was which compliants occured most frequently in each zipcode. The most interesting insight was that although heat and hot water complaints are the second most common complaint type by volume (by a large margin), it is only the most common complaint in ~8 of the ~160 zip codes we analyzed. It would be interesteing to research this further to determine why these are so tightly clustered and how this may be addressed. 

<center>
    <strong><em>LSTM slighly outperforms SARIMA with an RMSE of 449 vs 459</strong></em>
    <img src='images/Model Performance.png'>
</center>

When it came to modeling we used an LSTM and SARIMA to constuct univariate models of call volumes and response times based on historical data. The LSTM only slightly outperfomed  SARIMA with ~10% margin of error when predicting call volumes and responses. As mentioned previously, the models become more accurate the more you refine the data selection down to specific complaint types and geographies. 

## Recommendations

In order to make more affirmative recommendations we recommend that further refined modeling be done, and a persistent modeling pipeline be developed that updates on a daily bases. It is clear from our outcomes that the most useful and reliably predicted city-wide metric is total call volume. This model (or combination of models) can be used to project and plan for flexible staffing needs and contingent workforces. Additionally, the city may conduct further research into the driving factors beyond observed differences across boroughs and zip codes and suggest and prioritize future public works projects and public funding requests. 

## Future Work

* Multi-step LSTM Modeling
* Multivariate LSTM Modeling
* K-Means Cluster Analysis and Demographic Trends
* Interactive Mapping and Dashboarding


## Citations

* <p><a href="https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9">NYC Open Data - 311 Service Requests from 2010 to Present</a></p> 
* <p><a href="https://www.census.gov/data/developers/data-sets/acs-5year.html">U.S. Census - American Community Survey 5-Year Data</a></p> 
* <p><a href="https://github.com/jtleider/censusdata">Census Data Python API Library</a></p> 
* <p><a href="https://machinelearningmastery.com/time-series-forecasting-long-short-term-memory-network-python/">Time Series Forecasting with the Long Short-Term Memory Network in Python, Machine Learning Mastery</a></p> 

### Research Papers Reviewed:

* <p><a href="http://www.cs.binghamton.edu/~anand/paper/Mobiquitous2018.pdf">NYCER: A Non-Emergency Response Predictor for NYC using Sparse Gaussian Conditional Random Fields, DeFazio et. al.</a></p> 
* <p><a href="https://arxiv.org/pdf/1611.06660.pdf">Structure of 311 Service Requests as a Signature of Urban Location, Wang et. al.</a></p> 
* <p><a href="https://www.aaai.org/ocs/index.php/WS/AAAIW14/paper/view/8834/8266"> Profiling and Prediction of Non-Emergency Calls in New York City, Zha et. al.</a></p> 

### Additional Materials

* <p><a href="https://docs.google.com/presentation/d/1qnCLQuyH6mBJzfZ3jXjMQ_BEnuKsuFkLOE1JllTLyYg/edit?usp=sharing">Non-technical Presentation</a></p>