##import files
#library(descr)
library(readr)
library(iterators)
library(itertools)
suppressPackageStartupMessages(library(dplyr))
#library(Hmisc)
#library(reshape)
#library(fifer)
library(ggplot2)

#set dir
#import csv
#skip header line
orig_data <- read.table(file = "/FILENAME_HERE.csv", sep = ",", header = TRUE)

all_lines<- iter(orig_data, by = "row")
line<-" " # intitialize
gene<-" "
dset<-" "

for(row in 1:nrow(orig_data)){

  line <- nextElem(orig_data)

}
#for line in CSV
  #grab pos+ Name, write to a new dataset
  #while(Pos and Name are both the same):\
    #add line to the dataset
  #once they're not the same:
    #run stats on the dataset
    #dump stats ouput to ouput_path
  #set for index to first different line
#figure out a way to catch possible end of file errors




#Stats code:
  #divide size by 2
  #Group one is 