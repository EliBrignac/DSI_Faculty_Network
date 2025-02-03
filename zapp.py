import streamlit as st
import os
import pandas as pd

# Folder containing images
IMAGE_FOLDER = "images"

# Mapping of button selections to image filenames (now using SVGs)
IMAGE_MAPPING = {
    ("Name",): "Name.svg",
    ("Amount",): "Amount.svg",
    ("Weight",): "Weight.svg",
    ("Amount", "Name"): "Name_Amount.svg",
    ("Name", "Weight"): "Name_Weight.svg",
    ("Amount", "Weight"): "Amount_Weight.svg",
    ("Amount", "Name", "Weight"): "Name_Amount_Weight.svg",
    # Topics
    ("Interests"): "Name_Interests.svg",
    ("Amount", "Interests"): "Amount_Interests.svg",
    ("Interests", "Weight"): "Weight_Interests.svg",
    ("Amount", "Interests", "Name"): "Name_Amount_Interests.svg",
    ("Interests", "Name", "Weight"): "Name_Weight_Interests.svg",
    ("Amount", "Interests", "Weight"): "Amount_Weight_Interests.svg",
    ("Amount", "Interests", "Name", "Weight"): "Name_Amount_Weight_Interests.svg",
}

st.set_page_config(layout="wide")


# Create checkboxes in the sidebar for multi-selection
selected_options = set()
if st.sidebar.checkbox("Graph of Research Interests"):
    selected_options.add("Interests")
if st.sidebar.checkbox("Name"):
    selected_options.add("Name")
if st.sidebar.checkbox("Amount"):
    selected_options.add("Amount")
if st.sidebar.checkbox("Weight"):
    selected_options.add("Weight")

if "Interests" not in selected_options:


    st.title("UD DSI Faculty Collaboration Network")

    # Find the corresponding image
    selected_tuple = tuple(sorted(selected_options))
    image_filename = IMAGE_MAPPING.get(selected_tuple)

    # Display the image if a valid selection was made
    if image_filename:
        image_path = os.path.join(IMAGE_FOLDER, image_filename)
        
        # Read the SVG content
        with open(image_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        
        # Apply inline CSS for scaling the SVG
        scaled_svg = svg_content.replace('<svg', '<svg width="250%" height="auto"')

        # Display the scaled SVG
        
        # Add responsive scaling CSS
        st.markdown("""
            <style>
                .svg-container {
                    width: 100%;
                    max-width: 100%;
                    overflow: hidden;
                }
                .svg-container svg {
                    width: 100%;
                    height: auto;
                    max-width: none;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)

        # Display the SVG with responsive container
        st.markdown(
            f'<div class="svg-container">{svg_content}</div>',
            unsafe_allow_html=True
        )


    else:

        image_path = os.path.join(IMAGE_FOLDER, "Name.svg")
        
        # Read the SVG content
        with open(image_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        
        # Apply inline CSS for scaling the SVG
        scaled_svg = svg_content.replace('<svg', '<svg width="250%" height="auto"')

        # Display the scaled SVG
        
        # Add responsive scaling CSS
        st.markdown("""
            <style>
                .svg-container {
                    width: 100%;
                    max-width: 100%;
                    overflow: hidden;
                }
                .svg-container svg {
                    width: 100%;
                    height: auto;
                    max-width: none;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)

        # Display the SVG with responsive container
        st.markdown(
            f'<div class="svg-container">{svg_content}</div>',
            unsafe_allow_html=True
        )


        #st.write("Select at least one option to display an image.")

    """
    This is a graphical representation of the faculty within the University of Delaware
    Data Science Institute (DSI) and their co-authorship network. The nodes represent 
    faculty members, and the edges represent wether or not the two faculty have worked
    on a paper together. The size of the nodes is based on the number of papers the
    faculty member has published, and the width of the edges is based on the number of
    papers the two faculty members have worked on together. The colors of the nodes 
    represent different groups within the network that are more closely connected to each other 
    (determined by modularity). Use the checkboxes on the sidebar to customize the 
    visualization to your liking! For more information on the methods view the README.md file.
    """


    col1, col2 = st.columns(2)

    # Most Published Faculty Members table
    with col1:
            # Example data for the table
        published_faculty = [
            [ "Md. Jobayer Hossain", 1123 ],
            [ "Dionisios G. Vlachos", 1117],
            [ "Xiang-Gen Xia", 924],
            [ "Frank G. Schröder", 840],
            [ "Gonzalo R. Arce", 615]
        ]

        # Create a pandas DataFrame with custom column names
        df_published_faculty = pd.DataFrame(published_faculty, columns=["Faculty Member", "Publication Count"])
        
        df_published_faculty.index += 1

        # Display the table with custom column names
        st.markdown("### Most Published Faculty Members")
        #st.table(df_published_faculty)
        st.dataframe(df_published_faculty[["Faculty Member", "Publication Count"]].style.set_table_attributes("style='width:50%'"))


    # Most Collaborative Faculty Members table
    with col2:
        highest_degree = [
            [ "Cathy Wu", 15 ],
            [ "Benjamin E. Bagozzi", 10],
            [ "Sunita Chandrasekaran", 7],
            [ "Adam Fleischhacker", 6],
            [ "Delphis F. Levia", 6]
        ]

        # Create a pandas DataFrame with custom column names
        df_highest_degree = pd.DataFrame(highest_degree, columns=["Faculty Member", "Collaborators"])
        df_highest_degree.index = ["1", "2", "3", "4", "4"]
        # Display the table with custom column names
        st.markdown("### Most Collaborators")
        st.dataframe(df_highest_degree[["Faculty Member", "Collaborators"]].style.set_table_attributes("style='width:50%'"))

    # Create another row of columns for the remaining tables
    col3, col4 = st.columns(2)

    # Most Collaborative Pairs table
    with col3:
        st.markdown("### Most Collaborative Pairings")
        collaborative_pairs = [
            ["Cathy Wu & Cecilia Arighi", 84],
            ["Cathy Wu & Dr. Chuming Chen", 61],
            ["Kenneth E. Barner & Gonzalo R. Arce", 38],
            ["K Eric Wommack & Shawn W. Polson", 37],
            ["Tian-Jian Hsu & Jack Puleo", 26],
        ]
        df_collaborative_pairs = pd.DataFrame(collaborative_pairs, columns=["Collaborative Pair", "Number of Collaborations"])
        df_collaborative_pairs.index += 1
        st.dataframe(df_collaborative_pairs[["Collaborative Pair", "Number of Collaborations"]].style.set_table_attributes("style='width:100%'"))

    # Graph Metrics table
    with col4:
        st.markdown("### Most Collaborations")
        most_collaborations = [
            ["Cathy Wu", 173],
            ["Cecilia Arighi", 109],
            ["Dr. Chuming Chen", 94],
            ["Shawn W. Polson", 56],
            ["Gonzalo R. Arce", 47],
        ]

        df_most_collaborations = pd.DataFrame(most_collaborations, columns=["Faculty Member", "Number of Collaborations"])
        df_most_collaborations.index += 1
        st.dataframe(df_most_collaborations.style.set_table_attributes("style='width:100%'"))


    st.markdown("### Graph Metrics")
    graph_metrics = [
        ["Nodes", 132],
        ["Edges", 104],
        ["Groupings", 14],
        ["Connected Components", 62],
        ["Average Degree", 1.564],
        ["Avg. Weighted Degree", 7.85],
        ["Avg. Path Length", 4.315],
        ["Network Diameter", 11],
        ["Density", 0.012],
        ["Total Triangles", 35],
        ["Avg. Clustering Coefficient", 0.361],
    ]
    df = pd.DataFrame(graph_metrics, columns=["Metric", "Value"])


    df['Value'] = df['Value'].apply(lambda x: str(x))
    df.index = [" "]*11
    # Display the table without index
    st.dataframe(df[["Metric", "Value"]].style.set_table_attributes("style='width:100%' align='center' height='100%'"))



    col5, col6 = st.columns(2)


    # Most Collaborative Pairs table
    with col5:
        st.markdown("### Highest Page Rank")
        page_rank = [
            ["Cathy Wu", 0.0643],
            ["Ceco;oa Arighi", 0.0366],
            ["Gonzalo R. Arce", 0.0363],
            ["Kenneth E. Barner", 0.0328],
            ["Dr. Chuming Chen", 0.0325],
        ]
        df_page_rank = pd.DataFrame(page_rank, columns=["Collaborative Pair", "Page Rank (Probability=0.85)"])
        df_page_rank.index += 1

        st.dataframe(df_page_rank)

    with col6:
        st.markdown("### Highest Betweenness Centrality")
        betweenness = [
            ["Cathy Wu", 0.0651],
            ["Rodrigo Vargas", 0.0624],
            ["Delphis F. Levia", 0.0584],
            ["Pinki Mondal", 0.0566],
            ["Kenneth E. Barner", 0.0541],
        ]
        df_betweenness = pd.DataFrame(betweenness, columns=["Faculty Member", "Betweenness Centrality"])
        df_betweenness.index += 1
        st.dataframe(df_betweenness)



# FLAG FLAG RESEARCH INTERESTS FLAG FLAG
else:
    st.title("UD DSI Faculty Research Interests Network")

    # Find the corresponding image
    selected_tuple = tuple(sorted(selected_options))
    image_filename = IMAGE_MAPPING.get(selected_tuple)

    # Display the image if a valid selection was made
    if image_filename:
        image_path = os.path.join(IMAGE_FOLDER, image_filename)
        
        # Read the SVG content
        with open(image_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        
        # Apply inline CSS for scaling the SVG
        scaled_svg = svg_content.replace('<svg', '<svg width="250%" height="auto"')

        # Display the scaled SVG
        
        # Add responsive scaling CSS
        st.markdown("""
            <style>
                .svg-container {
                    width: 100%;
                    max-width: 100%;
                    overflow: hidden;
                }
                .svg-container svg {
                    width: 100%;
                    height: auto;
                    max-width: none;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)

        # Display the SVG with responsive container
        st.markdown(
            f'<div class="svg-container">{svg_content}</div>',
            unsafe_allow_html=True
        )



    else:
        image_path = os.path.join(IMAGE_FOLDER, "Name_Interests.svg")
        
        # Read the SVG content
        with open(image_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        
        # Apply inline CSS for scaling the SVG
        scaled_svg = svg_content.replace('<svg', '<svg width="250%" height="auto"')

        # Display the scaled SVG
        
        # Add responsive scaling CSS
        st.markdown("""
            <style>
                .svg-container {
                    width: 100%;
                    max-width: 100%;
                    overflow: hidden;
                }
                .svg-container svg {
                    width: 100%;
                    height: auto;
                    max-width: none;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)

        # Display the SVG with responsive container
        st.markdown(
            f'<div class="svg-container">{svg_content}</div>',
            unsafe_allow_html=True
        )

    
    """
    This is a graphical representation of the faculty within the University of Delaware
    Data Science Institute (DSI) and their network of research interests. The nodes represent 
    faculty members, and the edges represent wether or not the two faculty have similar research interests and have worked on a paper together. 
    The size of the nodes is based on the number of papers the
    faculty member has published, and the width of the edges is based on the amount of interests that the two authors have
    in common. The colors of the nodes represent different groups within the network that are more closely connected to each other 
    (determined by modularity). Use the checkboxes on the sidebar to customize the 
    visualization to your liking.
    
    NOTE: Professors with nothing listed for research interests on google scholar are not included in this network.
    For more information on the methods view the README.md file.
    """


    col1, col2 = st.columns(2)

    # Most Published Faculty Members table
    with col1:
        published_faculty = [
            [ "Machine Learning",  "Bioinformatics"],
            [ "Data Science", "Astronomy"],
            [ "Environment", "Education"],
            [ "Physics", "Biology"],
            [ "Analytics", "Finance"]
        ]

        # Create a pandas DataFrame with custom column names
        df_published_faculty = pd.DataFrame(published_faculty, columns=["Common Interests", ""])
        
        df_published_faculty.index = [" "] * 5

        # Display the table with custom column names
        st.markdown("### Common Interests (no order)")
        #st.table(df_published_faculty)
        st.dataframe(df_published_faculty.style.set_table_attributes("style='width:100%'"))


    # Most Collaborative Faculty Members table
    with col2:
        highest_degree = [
            [ "Cathy Wu", 10 ],
            [ "Wei Qian", 5],
            [ "Shawn W. Polson", 5],
            [ "Shanshan Ding", 5],
            [ "Kenneth E. Barner", 5]
        ]

        # Create a pandas DataFrame with custom column names
        df_highest_degree = pd.DataFrame(highest_degree, columns=["Faculty Member", "Collaborators"])
        df_highest_degree.index = ["1", "2", "2", "2", "2"]
        # Display the table with custom column names
        st.markdown('### Most Relateable Collaborators')
        st.dataframe(df_highest_degree[["Faculty Member", "Collaborators"]].style.set_table_attributes("style='width:50%'"))

    # Create another row of columns for the remaining tables
    col3, col4 = st.columns(2)

    # Most Collaborative Pairs table
    with col3:
        st.markdown("### Most Similar Research Interests")
        collaborative_pairs = [
            ["K. Eric Wommack & Shawn W. Poison", 20],
            ["Wei Qian & Shanshan Ding", 17],
            ["Wei Qian & Austin J. Brockmeier", 15],
            ["Kenneth E. Barner & Gonzalo R. Arce", 14],
            ["Shawn W. Poison & Cecilia Arighi", 14],
        ]
        df_collaborative_pairs = pd.DataFrame(collaborative_pairs, columns=["Faculty", "Similar Interests"])
        df_collaborative_pairs.index = ["1", "2", "3", "4", "4"]
        st.dataframe(df_collaborative_pairs.style.set_table_attributes("style='width:100%'"))

    # # Graph Metrics table
    # with col4:
    #     st.markdown("**Most Collaborations**")
    #     most_collaborations = [
    #         ["Cathy Wu", 173],
    #         ["Cecilia Arighi", 109],
    #         ["Dr. Chuming Chen", 94],
    #         ["Shawn W. Polson", 56],
    #         ["Gonzalo R. Arce", 47],
    #     ]

    #     df_most_collaborations = pd.DataFrame(most_collaborations, columns=["Faculty Member", "Number of Collaborations"])
    #     df_most_collaborations.index += 1
    #     st.dataframe(df_most_collaborations.style.set_table_attributes("style='width:100%'"))


    st.markdown("### Graph Metrics")
    graph_metrics = [
        ["Nodes", 123],
        ["Edges", 74],
        ["Groupings", 12],
        ["Connected Components", 63],
        ["Average Degree", 1.22],
        ["Avg. Weighted Degree", 5.967],
        ["Avg. Path Length", 5.166],
        ["Network Diameter", 14],
        ["Density", 0.01],
        ["Total Triangles", 13],
        ["Avg. Clustering Coefficient", 0.258],
    ]
    df = pd.DataFrame(graph_metrics, columns=["Metric", "Value"])


    df['Value'] = df['Value'].apply(lambda x: str(x))
    df.index = [" "]*11
    # Display the table without index
    st.dataframe(df[["Metric", "Value"]].style.set_table_attributes("style='width:100%' height='100%'"))



    col5, col6 = st.columns(2)


    # Most Collaborative Pairs table
    with col5:
        st.markdown("### Highest Page Rank")
        page_rank = [
            ["Cathy Wu", 0.040],
            ["Delphis F. Levia", 0.029],
            ["Kenneth E. Barner", 0.024],
            ["Wei Qian", 0.024],
            ["Roghayeh Leila Barmaki", 0.022],
        ]
        df_page_rank = pd.DataFrame(page_rank, columns=["Collaborative Pair", "Page Rank (Probability=0.85)"])
        df_page_rank.index += 1

        st.dataframe(df_page_rank)

    with col6:
        st.markdown("### Highest Betweenness Centrality")
        betweenness = [
            ["Cathy Wu", 608.1],
            ["Kenneth E. Barner", 400.8],
            ["Cecilia Arighi", 371.3],
            ["Keith Decker", 368.3],
            ["Benjamin E. Bagozzi", 352.63],
        ]
        df_betweenness = pd.DataFrame(betweenness, columns=["Faculty Member", "Betweenness Centrality"])
        df_betweenness.index += 1
        st.dataframe(df_betweenness)