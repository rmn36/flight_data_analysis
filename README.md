# 2015 Flight Delay and Cancellations

## Overview
This is some basic analysis of flight delay and cancellation data as provided by the US Department of Transportation. The data set can be downloaded at this [link](https://www.kaggle.com/usdot/flight-delays) and added to the `./data` dir of this project. This project utilizes Python3, Docker and Jupyter notebooks for various aspects of the analysis. Python3 and the added libs such as pandas, matplotlib and numpy are some of the best tools for data analysis out today. Docker was chosen for ease of use and portability. I don't currently have a Python3 dev environment fully setup so using Docker allowd me to get up and running quickly. Finally, Jupyter notebook was chosen as a way to represent the data and analysis in a straightforward and easy to read way. 

## Viewing the Project

This project can be viewed in a number of different ways. First, if you have your own Jupyter instance running somewhere feel free to grab the data files and the `./data/2015 Flight Delay and Cancellations.ipynb` file and import them into Jupyter. From there run the notebook as usual. For Docker this project is setup to use docker-compose. Simply use the `docker-compose up -d` command to run the Docker container. Lastly, in the `./output` dir there are two standard formats. First is an HTML file that can be viewed in any browser. Second is a python script that includes all of the python code from the Jupyter notebook and any Markdown cells in the Jupyter notebook are represented as comments.

**Docker Notes**:
    
    1. The main downside to this approach is that the first time you run the container the Jupyter notebook image will need to be pulled and it is fairly large
    2. Due to the large size of this dataset there is a possibility of the container running out of memory if cells are run too many times. In this case the `Restart Kernel` at the top and rerun the cells