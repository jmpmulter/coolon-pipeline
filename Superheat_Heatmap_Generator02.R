#Superheat_Heatmap_Generator
#install.packages("devtools")
#install.packages("Rtools")
#R.Version()
#devtools::install_github("rlbarter/superheat")
#install.packages(c("ggplot2","readr","descr"),dependencies = TRUE)
#install.packages("tidyverse", dependencies = TRUE)
library(tidyverse)
library(xlsx)
library(superheat)
library(plyr); library(dplyr)

dat <- read.xlsx("C:/Users/User/Desktop/Junior Spring/Coolon Lab/Targets_ISO_COL_A_heatmap01.xlsx", sheetName="ISO_COL_A_heatmap01")
dat_bckp<-dat
#dat<-dat_bckp
save(dat_bckp,file = "dat_bckp")

var_keep <- c("Scaf_num_Pos_Fbgn_Gmnum", "F0_CL_vs_FIG", "F1_CL_vs_HA", "F2_CL_vs_LDOPA", "F3_CL_vs_NONI", "F4_CL_vs_OAHA", "F5_CL_vs_OA", "Sig.Hits","Non.Sig.Hits","Total.Hits","Dmel.Ortholog","GM_num")
d_lim<- dat[ ,var_keep]
df<-d_lim[d_lim$Sig.Hits>=1,]
df[] <- lapply(df, as.character)
tmp<- df

#R.Version()

#Replaces the factor versions of variables with Numbers
tmp <- lapply(tmp, function(x) {gsub("^O$", 0, x) })
tmp <- lapply(tmp, function(x) {gsub("^N$", 1, x) })
tmp <- lapply(tmp, function(x) {gsub("^S$", 2, x) })
tmp<-data.frame(lapply(tmp,as.numeric))
df[,2:10]<-tmp[,2:10]


df$intermediate_name<-df$Dmel.Ortholog
df$intermediate_name[df$intermediate_name=="-"]<-df$GM_num
df$intermediate_name[df$intermediate_name=="Act87E <newline> Act57B <newline> Act88F"]<-"Actin"

hold<-data.frame(apply(df[c("Scaf_num_Pos_Fbgn_Gmnum")],1,function(x) {strsplit(as.character(x),"_")}),row.names = c("t1","scaf","pos","FBGN","GMNUM"))
hold2<-data.frame(t(hold))
hold3<-hold2
hold3$ID <- seq.int(nrow(hold3))
df$ID<-seq.int(nrow(df))
comb<-merge.data.frame(df,hold3)



#df$spl<- strsplit(as.character(df$Scaf_num_Pos_Fbgn_Gmnum),"_")

#df$pos<-apply(df[,c("spl")],1,function(x){x[[]]})

#by(df, 1:nrow(df),function(row) str(row$Non.Sig.Hits))

#df$scaf<- strsplit(as.character(df$Scaf_num_Pos_Fbgn_Gmnum),"_")

comb$new_row_names<-paste(comb$intermediate_name,"Scaf",comb$scaf,"Pos",comb$pos,
                         sep = "_")#strsplit(df$Scaf_num_Pos_Fbgn_Gmnumm,as.character("_"),)[3],collapse = "_")

#colnames(df)
names(comb)[3]<-"FIG"
names(comb)[4]<-"HA"
names(comb)[5]<-"LDOPA"
names(comb)[6]<-"NONI"
names(comb)[7]<-"OAHA"
names(comb)[8]<-"OA"
names(comb)[2]<-"Dmel"
row.names(comb)<-comb$new_row_names #TODO Edit this to be DMEL_SCAF_POS


vis_1<-superheat(comb[,3:8],title = "Heatmap of Editing Presence Across Treatments",
                 left.label.size = 0.4,left.label.text.size=3,
                 bottom.label.size = 0.2,
                 grid.hline.col = "white",grid.vline.col = "white",
                 legend.breaks = c(0,1,2),
                 
                 )


#tmp <- data.frame(lapply(tmp, function(x) {gsub("^O$", 0, x) }))
#tmp <- data.frame(lapply(tmp, function(x) {gsub("^N$", 1, x) }))
#tmp <- data.frame(lapply(tmp, function(x) {gsub("^S$", 2, x) }))
#tmp[]<-lapply(tmp,as.numeric)
#df[,2:10]<-tmp[,2:10]

#df[,2:8] <- data.frame(lapply(df[,2:8], function(x) {gsub("^O$", 0, x) }))
#df[] <- lapply(df, as.character)
#df <- data.frame(lapply(df, function(x) {gsub("^O$", 0, x) }))
#df <- data.frame(lapply(df, function(x) {gsub("^N$", 1, x) }))
#df <- data.frame(lapply(df, function(x) {gsub("^S$", 2, x) }))

#df[] <- lapply(df, as.numeric)

#df$F0_CL_vs_FIG[df$F0_CL_vs_FIG=="N"]<-"B"



#Import the dataset
#change the O/N/S values into 0,1,2
#Give the sig reads, total hits numbers a heatmap value
#Limit to only the significant portion of the data
#Choose only the relevant columns
