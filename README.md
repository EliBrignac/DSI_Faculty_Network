# Phase 1 Deliverable:
1. click this link 
2. Read the README.md file
3. Check out the code

# Phase 2 Deliverable:
1. It isn't a "Database record" but the csv titled `ud_faculty_joined.csv` is the closest thing to a database record that I have. It contains the names of the faculty members, their departments, their positions, their research interests, and their publications.


I hope you enjoy 👍

# How this was done


## Gathering the Data

DSI Faculty
- The names of DSI faculty members were scraped from the [DSI website]('https://dsi.udel.edu/faculty/') using the `Faculty_scraper.py` script. The script uses the `requests` and `BeautifulSoup` libraries to scrape the names of the faculty members and save them to a CSV file. The results are in the `ud_dsi_faculty.csv` file.


DSI Faculty Publications
- The publications of the DSI faculty members were scraped from `google_scholar_scraper.py` script. The script uses the `scholarly` library to scrape the publications of the faculty members and save them to a CSV file. I parrallelized the scraping process so that the script can scrape multiple faculty members at the same time and it doesn't take too long to scrape all the thousands of publications. the results are in the `ud_faculty_scholar_publications.csv` file.


DSF Faculty Research Interests
- I used the same `google_scholar_scraper.py` script to scrape the research interests of the faculty members, and saved the interests to the `ud_faculty_scholar_basic_info.csv` file. I then joined the `ud_faculty_scholar_publications.csv` and  `ud_faculty_scholar_basic_info.csv` files on the `name` column to get the research interests of the faculty members. The results are in the `ud_faculty_joined.csv` file.




## Data Cleaning
- I removed duplicate rows
- For the research interests, I removed rows where the research interests was NaN

## Buliding Graph

**Collaboration Graph**
- Built with the `create_graph.py` file. I used the `networkx` library to build a graph of the faculty members and their publications. If two faculty members had a publication with the same Title, then I connected them with an edge. The weight of the edge is the number of publications they have in common. I saved the graph as a `gml` file so that it can be visualized using Gephi.

**Research Interests Graph**
-  Built with the `create_graph_w_research_interests.py` file. I used the `networkx` library to build a graph of the faculty members and their Research Interests, along with their co-authorship. If two faculty members had a publication with the same Title, then I connected them with an edge if and only if they shared a research interest. This research interest is found via the `scholarly` api (google scholar) under research interests. The weight of the edge is the number of research interests they have in common. I saved the graph as a `gml` file so that it can be visualized using Gephi. 
- How I determined if two faculty members shared a research interest was by using the OpenAI API to ask `gpt-3.5-turbo` if any key term in the research interests of one faculty member was similar to the research interests of another faculty member. If the answer was yes, then I connected the two faculty members with an edge. The more research interests faculty had in common, the greater the weight of the edge. This was done to ensure that the research interests were not too broad and that the two faculty members actually had similar research interests (for example: Data Science and Machine Learning are similar research interests)
- Using an LLM proved to be more accurate than using a simple keyword search or simple spacy embedding similarity model. 




## Visualizing the Graphs
- I used Gephi to visualize the graphs. I used the `Force Atlas 2` layout to visualize the graph but then proceeded to drag nodes around myself to improve the readability.The size of the nodes is based on the number of papers the faculty member has published, and the width of the edges is based on the number of
papers the two faculty members have worked on together. The colors of the nodes represent different groups within the network that are more closely connected to each other(determined by modularity). This means the nodes of the same color have more co-authorships/research interests. 

- You can view the graph with the faculty names, the number of publications, and the number of co-authorships by clicking on the buttons in the sidebar.





## Future Work

- You might ask "eli, why not make a graph of purely all the research interests" and my answer to that is I tried to and there were a few problems I faced that prevented me from going further into it.
1.  Accurate results would take too long to run.
    1.  Comparing every research interest to every other research interest for every professor was a lot of comparisons to make using the OpenAI API (Expected 217,470 comparisons for the most accurate results) and I didn't want to wait that long
2.  I also didn't want to spend more money on OpenAI API credits to do all of these comparisons because I am a broke college student and I could spend money on better things than comparing research interests.

HOWEVER, if you would like to see this graph and feel it would be useful, I can try to make a simplified version of it. Just let me know if it is meaninfull enough to make and I can try to make it happen.

