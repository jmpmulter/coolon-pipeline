##import files -- working draft.
library(descr)
library(readr)
library(tidyr) # to get data into "tidy" format
library(dplyr) # to manipulate data
library(broom) # to tidy up the output of the default t test function.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) # For R Studio
#setwd(getSrcDirectory()[1])#For Command Line
#args = commandArgs(trailingOnly=TRUE)#For Command Line

input<-"D:/Clust_Formatted_CSVs/FO_A_to_I_[CL,OA]_CSV.csv"
input_no_ext<-unlist(strsplit(input,split="[.]"))[0:1]
cln_filename<-unlist(strsplit(input_no_ext,split="[/]"))[-2:-1]



#set dir
#import csv
#skip header line
df <- read.table(file = input, sep = ",", header = TRUE)

df$group<- factor(paste0(df$Scaffold,df$Position,df$ID,df$Name))
df$type[grepl("type0",df$RunFileName)]<-0 #Control
df$type[grepl("type1",df$RunFileName)]<-1 #Treatment
df$type <- factor(df$type, levels = c(0,1) ,labels = c("Control","Experimental"))
df$log_alt_div_ref<- log10(df$Ratio_Alt_div_Ref)

#freq(as.ordered(df$log_alt_div_ref))

#results <- gather(df, key = "type", value = "log_alt_dif_ref",factor_key = TRUE)
results<-df
results <- group_by(results,group)
#freq(df$type)
#freq(results$type)
results <- do(results, tidy(t.test(.$log_alt_div_ref~.$type,
                                   alternative = "two.sided",
                                   #mu = 0,
                                   paired = FALSE,
                                   var.equal = FALSE,
                                   conf.level = 0.95
)))
#holm_corr <-do(results,tidy(p.adjust(.$p.value, method = "holm")))

#freq(results$p.value)
#results_holm<-results
#results_holm$adj_p<-p.adjust(results$p.value, method = "holm")
results_fdr<-results
results_fdr$adj_p<-p.adjust(results$p.value, method = "fdr")

getwd()
write.csv(results_fdr, paste("Res",cln_filename,"fdr_corr.csv",sep="_")) #"Res_RUNNAME_holm_corr.csv"



#freq(results$p.value)
#wd<-getwd()
#print(wd)
#setwd(wd)

#write.csv(results_holm, "Res_RUNNAME_holm_corr.csv") #"Res_RUNNAME_holm_corr.csv"
#write.csv(results_fdr, "Res_RUNNAME_fdr_corr.csv")
#write.csv(results_holm, paste("Res",cln_filename,"holm_corr.csv",sep="_")) #"Res_RUNNAME_holm_corr.csv"

#df$Ref.A.[grepl("Ref.A.",df$RunFileName)]<-"Ref_A"
#df$type[grepl("RefGA.",df$RunFileName)]<-"Ref_G"
#Build out more of the above statements if comparing multiple files

#freq(df$type)
#freq(df$group)

#m1<-matrix()

#by(df,df$group,function(x) var.test(x$log_alt_div_ref ~ x$type, alternative = "two.sided"))
#The variances are not equal
#by(df,df$group,function(x) t.test(x$log_alt_div_ref~x$type, paired=FALSE, var.equal = FALSE)) #Current working version of the line

#file.create("rOutp.txt", open="w")
#sink("rOutp.txt")
#sink(type = "message")
#file.show("rOUtp.txt")

#by(df,df$group,function(x) x$p_val<-t.test(x$log_alt_div_ref~x$type, paired=FALSE, var.equal = FALSE)$p.value) #Current working version of the line

#sink()
#file.show("rOutp.txt")
#cat("str")
#by(df,df$group,function(x) by(x,x$type,function(x) freq(x$Ref.A.)))



#all_lines<- iter(orig_data, by = "row")
#line<-" " # intitialize
#gene<-" "
#dset<-" "
#last_line<-" "
#temp_set_1<-" "
#grp<-0

#for(i in 1:nrow(orig_data)){
#  line <- nextElem(orig_data)
#}
#for line in CSV
  #grab pos+ Name, write to a new dataset
  #while(Pos and Name are both the same):\
    #add line to the dataset
  #once they're not the same:
    #run stats on the dataset
    #dump stats ouput to ouput_path
  #set for index to first different line
#figure out a way to catch possible end of file errors

#library(iterators)
#library(itertools)
#suppressPackageStartupMessages(library(dplyr))
#library(Hmisc)
#library(reshape)
#library(fifer)
#library(ggplot2)
#install.packages("tidyr") # only needed if you didn't ever install tidyr
#install.packages("dplyr") # only needed if you didn't ever install dplyr
#install.packages("broom") # only needed if you didn't ever install broom