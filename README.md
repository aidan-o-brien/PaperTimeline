# Research Timeline Streamlit Application

Researchers often have to scour the scientific literature to understand complex topics. Tools like [Connected Papers](https://www.connectedpapers.com/) help with this process by visualising parts of the citation network to higlight influential papers. However, network diagrams can become complex and easily misinterpreted. Therefore, this project aimed to produce a visualisation that was easily interpretable and fast to produce.

__Search, Filter and Visualise__

The application allows users to search for terms in the title and abstract of papers, as well as filter by authors.

![Animation](https://user-images.githubusercontent.com/71706696/139323732-2ff600e5-7cf0-4791-be70-3a2046b8b76b.gif)

__Additional Data__

The application gives user the ability to download the underlying data, as well as view some basic summary statistics.

![Animation2](https://user-images.githubusercontent.com/71706696/139323801-ee6901fc-c7c3-4adb-861c-e6d5524e269a.gif)

# Project Objectives

The main objectives of the project are as follows:

1. Produce an interpretable visualisation of papers related to a query paper
2. Allow the user to search and filter the visualisation
3. Be easy-to-use so that non-coders can use the application

Although the idea behind this project is similar to that of [ConnectedPapers](https://www.connectedpapers.com/), it differs in five very important ways:

1. The visualisation is not a network diagram. This was done to increase interpretability.
2. The visualisation displays the query paper, all papers written by the authors of the query paper, and all papers citing the query paper. This was done to help develop an understanding of how useful a specific paper has been in a given field. Namely, it allows users to understand how the query paper has influenced the research of the authors.
3. The application has easy-to-use search and filtering functionality. This was done to help users explore and understand the data through visualisation.
4. The underlying data can be exported as a csv file. Again, this was done to help users understand the data more if they want to dig deeper.
5. The application provides additional summary statistics. This was done to provide a quick overview of the data.

Additionally, since the framework for the application is already built, additional visualisations and summary statistics can be added upon user request.

# Installation and Requirements

To use the code, clone the repository with:

```
git clone https://github.com/aidan-o-brien/PaperTimeline.git
```

For people who aren't yet comfortable with GitHub and the command line, please do the following:

1. Download the repository

<p align="center">
  <img width="600" alt="download_code" 
   src="https://user-images.githubusercontent.com/71706696/141283376-c5e3dd6c-8e3d-4617-9fdb-8a5368d0a0b0.png">
</p>

2. Unzip the downloaded file to a directory of your choice - remember where you put it!
3. Open the Command Prompt
4. Navigate to the location where you extracted the file (from step 2). For example, if you extracted the files to `C:\Users\bob\research_timeline`, you would use the following command:

```
cd C:\Users\bob\research_timeline
```

5. Install the requirements from the `requirements.txt` file with the following command:

```
pip install -r requirements.txt
```

6. Make sure you are able to connect to Scopus. This can be done if you are connected to your institution's Wi-Fi or connected to their VPN.

7. Run the app!

```
streamlit run streamlit_app.py
```

The following requirements are listed in the `requirements.txt` file:

+ `matplotlib==2.2.2`
+ `plotly==5.3.1`
+ `wordcloud==1.8.1`
+ `pybliometrics==2.9.1`
+ `pandas==1.1.5`
+ `streamlit==1.1.0`
+ `numpy==1.19.5`
