# MBTA-Web-App-Project
This project was completed by: Bertrand Aristide Inshuti & Arjun Masciarelli

## Brief Project Overview:
This project is a simple web application that takes in a user provided location, returning the nearest MBTA stop, it's wheelchair accessabillity and the next train's predicted arrival. 

## Reflection
### Dev Process:
In terms of the development process it first consisted of filling out each sub-function in the mbta_helper.py file. During this stage we used basic tests embedded in our "main" function to verify the outputs of each function as we were building them. This process helped create an almost Jupyter Notebok-like workflow where one could make the edits to a function and run the code to quickly verify the output. That said, as the functions grew in complexity, building upon one another, this testing framework wasn't entirely enough and we had to use intermittent debug lines to see how variables were changing or being declared across various points.

### API Issues:
One particular API issue we ran into was trying to get a prediction of an upcoming train's arrival time. Initially when testing with the MBTA's /predictions API we kept receving an empty dictionary which required me to try moving to the /schedules endpoint. Yet even there we dealt with similar results. Using a debug line on line 94 (which we've left in) helped us identify that our stop_id we were passing into downstream functions was actually a station door and required us to explicitly filter the stops endpoint to explicitly return a station (location_type: 1). 

Another issue we ran into was retrieving an accurate earliest arrival time for the next train. Using the /schedules endpoint we were able to get the earliest train departure of the day yet were failling to get the next departing train. We spent some on the MBTA V3 documentation trying to solve this and asked AI assistants for help, to little avail. We ended up looking at MBTA's site and inspecting the API calls made over the browser network to see which endpoint they were using. We specifically looked at [this page](https://www.mbta.com/stops/place-brkhl) and identified this public API that was being called: "https://www.mbta.com/api/stops/place-brkhl/schedules?last_stop_departures=false&future_departures=true" We decided to use this API ourselves as it ended up working with a higher degree of accuracy than our previous attempts. 

Another struggle that we faced and failled to conquer was that of successfully implementing MapBox's autofill and minimap feature. Despite many attempts, reading multiple Documentation pages and pleading for AI assistance we were not able to implement the feature into our app. It's a feature we'd like to revisit in the future.  

### Collaboration:
Collaborating on code was also a learning experience. This was one of the first times either of us used Git for collaborative coding. Bertrand worked very quickly and completed some of the core functions early, which meant I (Arjun) had to get better at understanding and building on his code rather than writing my own functions from scratch. This process of workign backwards from existing code was challenging, but educational. From conversations with industry professionals it seems like being able to understand a partner's codebase is a key skill in software development.

### AI Usage: 
Finally, in terms of AI usage we deployed ChatGPT periodically throughout the coding process to assist with debugging and answer pointed questions. AI's most significant contribution to our project was help with creating a style sheet and beautifying our Flask App's front-end. For context we've attached a before & after below. 

One limitation we noticed is that GPT can sometimes struggle with providing code for APIs that change frequently or are less maintstream. For example when trying to implement MapBox's autofill GPT kept sending us on wild goose chases with antiquated API endpoints, functions and terminology. To the point that it was faster to read line by line through the docs ourselves. 

### Before GPT Effects:
![Before](/images/before.png)
### After GPT Effects:
![Before](/images/after.png)

