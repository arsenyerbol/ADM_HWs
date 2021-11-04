# ADM-HW3

<p align="center">
  <img src="https://raw.githubusercontent.com/MirkoLozzi/ADM-HW3/main/goodreads_logo.jpg" />
</p>

  
#### **Description of the tasks**

In this homework we build a dataset from scratch by collecting information about books from [goodreads](https://www.goodreads.com/), site for readers and book recommendations.
We downloaded the url’s connetted to the first 300 pages of the most loved books and their HTML file where we stored Information about the book.
This Information was then parsed to mantain only what was relevant to us, such as book title, author name, and plot. Then , it was saved in a unique tsv file ```Books.tsv```.
You can retrieve the code to perform this task in the python notebook ```Download_and_parsing.ipynb```.

We build two different search engines wich retrives the books title, plot and links of the documents that contain the input query of the user. The first one gives us the documents that contain all the words in the input query, while the second search engine will retrive the top-k documents sorted by the cosine similarity evaluated over TF-IDF.

One of the task that we had was to build a new score. We define a new quantity called Importance_score as shown below.

<img src="https://render.githubusercontent.com/render/math?math=importance\_score_{doc_i} = \frac{ratevalue_{doc_i}\log(1+ratenumber_{doc_i})}{maxratevalue{docs}\log(1+maxratenumber{docs})}">

where:
* ratevalue = integer value between [0,5] 
* ratenumber = number of rates for each document 
* maxratevalue = max rate value among the documents found 
* maxratenumber = max rate number among the documents found

The final score is given by 30% Importance_score and 70% Similarity_score

Also we studied the cumulative numer of page during time, of the top-10 book series in the catalogue.

Finally we answered the algorithmic question about the longest common sub-sequence. Showing the exponential running time of the recursive algorithm can be improoved using dynamic progamming.

#### **Content**

* ```main.ipynb```: In this file there are the code about the search engines, and the questions 3, 4 and 5.
* ```Download_and_parsing.ipynb```: We saved in this file all the code we used to download and parse information about the books.
* ```Function.py```: Where it's possible to find all the functions concernig the parsing, and question 4 and 5.
* ```search_engine.py```: In this file there are all the functions to run the search engines








