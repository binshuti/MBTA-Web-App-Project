# MBTA-Web-App-Project
This project was completed by: Bertrand Aristide Inshuti & Arjun Masciarelli

## Brief Project Overview:
This project is a simple web application that takes in a user-provided location, returning the nearest MBTA stop, its wheelchair accessibility, and the next train's predicted arrival. 

## Reflection
### Dev Process:
In terms of the development process, it first consisted of filling out each sub-function in the mbta_helper.py file. At this stage, we used basic tests embedded in our "main" function to verify the outputs of each function as we were building them. This process helped create a Jupyter Notebook-like workflow where we could make the edits to a function and quickly run code to verify outputs. That said, as the functions grew in complexity, building upon one another, this testing framework wasn't enough. We had to use tools like print statements to see how variables were changing across the program.

### API Issues:
One specific API issue we ran into was trying to get a prediction of an upcoming train's arrival time. Initially, when testing with the MBTA's /predictions API we kept receiving an empty dictionary, which required us to try moving to the /schedules endpoint. Yet we dealt with similar results at that endpoint as well. Using a debug line on line 94 (which we've kept) helped us identify that the stop_id we were passing to downstream functions was actually a "station door" rather than a station id. To fix this we had to add an explicit filter to our /stops API call endpoint, limiting location_type to 1. 

Another issue we ran into was retrieving an accurate train arrival time. Using the /schedules endpoint, we were able to get the earliest train departure of the day, yet were failing to get the next departing train. We spent some on the MBTA V3 documentation trying to solve this and asked AI assistants for help, to little avail. We ended up looking at the MBTA's site and inspecting the API calls made over the browser network to see which endpoint they were using. We specifically looked at [this page](https://www.mbta.com/stops/place-brkhl) and identified this public API that was being called: "https://www.mbta.com/api/stops/place-brkhl/schedules?last_stop_departures=false&future_departures=true" We decided to use this API ourselves as it ended up working with a higher degree of accuracy than our previous attempts. 

Another struggle that we faced and failed to conquer was that of successfully implementing MapBox's autofill and minimap features. Despite many attempts, reading multiple documentation pages and pleading for AI assistance, we were not able to implement the feature into our app. It's a feature we'd like to revisit in the future.  

### Collaboration:
Collaborating on code was also a learning experience. This was one of the first times either of us used Git for collaborative coding. Bertrand worked very quickly and completed some of the core functions early, which meant I (Arjun) had to get better at understanding and building on his code rather than writing my own functions from scratch. This process of working backwards from existing code was challenging, but educational. From conversations with industry professionals, it seems like being able to understand a partner's codebase is a key skill in software development.

### AI Usage: 
Finally, in terms of AI usage, we deployed ChatGPT periodically throughout the coding process to assist with debugging and answer pointed questions. AI's most significant contribution to our project was helping with creating a style sheet and beautifying our Flask App's front-end. For context, we've attached a before & after below. 

One limitation we noticed is that GPT can sometimes struggle with providing code for APIs that change frequently or are less mainstream. For example , when trying to implement MapBox's autofill, GPT kept sending us on wild goose chases with antiquated API endpoints, functions, and terminology. It ended up being more trouble than it was worth to use GPT in those cases. 

### Before GPT Effects:
![Before](/images/before.png)
### After GPT Effects:
![Before](/images/after.png)

