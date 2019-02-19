Loading the data.
We'll start off the project by importing our trusty pandas library to read in our csv file:

In [1]:
import pandas as pd
dataset = pd.read_csv("assets/topcharts/billboard.csv")
print dataset.shape
print dataset.dtypes.value_counts()
pd.set_option('display.max_columns', dataset.shape[1])
dataset.head()
(317, 83)
float64    75
object      6
int64       2
dtype: int64

Top 100 chart ranking data;
317 songs;
From the period of June 1999 to December 2000;
Spanning 76 weeks
In addition to basic information about each song such as its artist, track name, song length and genre, the dataset also tracks chart position over time measured in units of weeks, including when it entered the chart and the time of peaking.

There are a large number of NaNs in the weekly chart ranking columns. It can be reasonably assumed that it indicates a song falling out of Top 100. These NaNs will have to be handled as we do our data cleaning.

Data cleaning.
We're going to:

Rename some feature columns that are poorly named
Shorten any strings that may be too long
Check for missing values and impute them as appropriate
In [2]:
# building dictionary for renaming columns
rename = {'artist.inverted':'artist'}
for i in dataset.columns:
    if 'week' in i:
        if len(i) == 9:
            new = int(i[1:2])
        else:
            new = int(i[1:3])
        rename.setdefault(i,new)
		
		The following code block simplifies column names:

In [3]:
# renaming columns in place
dataset.rename(columns=rename,inplace=True) 
dataset.head()

In [3]:
# renaming columns in place
dataset.rename(columns=rename,inplace=True) 
dataset.head()

Furthermore, this table is very wide due to the way it organises the weekly rank information by column. The use of pivot tables and melting will be useful for consolidating that information.

Here the rank values are converted from floats to integers:

In [4]:
# converting NaN rank numbers to 101
dataset.fillna(value = 101, inplace=True)
# converting float rank numbers to integers
dataset.iloc[:,7:]= dataset.iloc[:,7:].applymap(lambda x: int(x))
dataset.head()

Below, the columns 'year', 'time', 'date.entered' and 'date.peaked' are converted to datetime:

In [5]:
from datetime import datetime
for col in ['year','time','date.entered','date.peaked']:
    pd.to_datetime(dataset[col])
	
	Now, we will use Pandas' built in melt function and pivot the weekly ranking data to be long, instead of wide. Doing so removes the 72 'week' columns and replaces them with just two: Week and Ranking.

In [6]:
weeklist = list(dataset.columns[7:])
In [7]:
melted = pd.melt(dataset, id_vars=['artist', 'track'],
       var_name="Week", value_name="Ranking",
       value_vars = weeklist)
# displaying .head(10)
pivoted = pd.pivot_table(melted, index = ['artist','track', 'Week'], )

Data Visualisation.
Using Tableau, we will create some visualisations that will provide context to this dataset. The cleaned DataFrame and melted pivot table from the last code block will be looked at using data visualisation.

Problem Statement.
1. Were the songs in the Top 100 chart dominated by a few artists in '99-'00?
The rationale behind posing this question can be summed up as follows:

The music industry has to devote resources and manpower to promote artists and songs.
If Top 100 chart songs are dominated by a few artists, the industry can pour resources into just a handful of them to maximize their audience, and by extension their economic return.
Conversely, if the statement were proven to not be true, then industry leaders should focus instead on casting a wide net in order to capture a greater variety of artists that appeal to more people.
The above logic applies equally to genres as to artists: if certain genres have an outsize popularity as reflected by the charts, then more effort should be put into promoting artists who create that genre of music.
2. Follow-up: Does that hold true today?
The follow-up question is outside the scope of this exercise, but for future follow-up work, answering this second and more relevant question will allow us to see if the distributions of song/artist popularity and chart persistence have changed. The results of this investigation can potentially be very revealing, because a number of trends in the years between the dataset timeframe of 1999 - 2000 and the present day of 2016 have changed the music landscape beyond recognition:

The advent of Ipods, then smartphones
The explosive popularity of Youtube and music streaming services
Fall-off in popularity of traditional media, e.g. CDs, radio, TV
Shift from traditional to digital marketing
As the underlying factors that influence music production, promotion and consumption change, it would be interesting to see if these have led to a change in the distribution of songs, artists and genres in the Top 100, not only for prosaic academical reasons, but more importantly for market research purposes that players in the music industry today will no doubt be keeping an eye on.

Approaches to problem solving.
We can approach problem statement 1 by looking at artist popularity in a number of different ways, mainly by investigating the distribution of:

number of songs by artist that appeared in the Top 100
ranking achieved by these songs
persistence in the charts
Data visualisation is essential to see if any of the three elements are affected by outsize influences of a small number of artists, or not. For item 1, a treemap can be very useful because it displays interval measurements well by linking the area of blocks with the magnitude of measurements.

Regarding item 2, a full investigation can involve following individual song ranks or artist's songs ranks, with the latter being additionally characterisable by highest rank, lowest rank, median rank, standard deviation and other statistical measures for a grouping of songs. A simple table with coloured-in cells for heat values can be an effective visualisation tool for simple measures of rank, and perhaps candlestick charts for better visualisation of data distribution.

To tackle item 3, we can track chart persistence by visualising changes in rank over time. Plotting a time series line chart of median rank can be an effective means to screen out extreme outliers in ranking; though it is arguably more important to look at top ranks, because those are likely to be the greatest drivers of revenue. An additional tool can again be candlestick charts to visualise the distribution of ranks.

Looking at genre popularity is just as important, for which the above methods apply, but generalised to an entire genre of music as opposed to just one artist.

That's it for now - to recap: We've looked at two essential aspects of any Data Science workflow: Exploratory Data Analysis and problem formulation, and also brainstormed approaches to problem solving using data. For a showcase of other equally important elements and tools for the practicing Data Scientist, check out the other notebooks hosted on my Github page!