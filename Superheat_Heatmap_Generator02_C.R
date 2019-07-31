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

dat <- read.xlsx("C:/Users/User/Desktop/C-to-U End of 2019 Summer Pass/Targets_ISO_COL_C_heatmap01.xlsx", sheetName="Sheet1")
dat_bckp<-dat
#dat<-dat_bckp
#save(dat_bckp,file = "dat_bckp")

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
#df$intermediate_name[df$intermediate_name=="Act87E <newline> Act57B <newline> Act88F"]<-"Actin"

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
                          sep = " ")#strsplit(df$Scaf_num_Pos_Fbgn_Gmnumm,as.character("_"),)[3],collapse = "_")

#colnames(df)
#For Vis1
names(comb)[2]<-"Dmel"
names(comb)[3]<-"FIG"
names(comb)[4]<-"HA"
names(comb)[5]<-"LDOPA"
names(comb)[6]<-"NONI"
names(comb)[7]<-"OAHA"
names(comb)[8]<-"OA"
#For Vis2
names(comb)[9]<-"Number of Significant\n Events (vs. Control)"
names(comb)[10]<-"Number of Non-significant\n Events (vs. Control)"
names(comb)[11]<-"Sum of Editing \nEvents Logged"
row.names(comb)<-comb$new_row_names #TODO Edit this to be DMEL_SCAF_POS


#v1_txt<-comb[,3:8]
#v1_txt <- lapply(v1_txt, function(x) {gsub("^0$", "O", x) })
#v1_txt <- lapply(v1_txt, function(x) {gsub("^1$", "N", x) })
#v1_txt <- lapply(v1_txt, function(x) {gsub("^2$", "S", x) })
#v1_txt<-matrix(v1_txt)

v1_txt<-comb[3:8]
v1_txt<-gsub("0", "O", v1_txt)
v1_txt<-gsub("1", "N", v1_txt)
v1_txt<-gsub("2", "S", v1_txt)
v1_txt
v1_txt<-matrix(v1_txt,ncol = ncol(comb[3:8]))
v1_txt

#v1_txt_transposed<-t(v1_txt)
#v1_txt_transposed


vis_1<-superheat(comb[,3:8],
                 title = "C-to-U Point Editing Presence Across Treatments", title.alignment = "center",
                 left.label.size = 0.205,left.label.text.size=3,#0.205
                 bottom.label.size = 0.2,
                 grid.hline.col = "white",grid.vline.col = "white",
                 #grid.hline = FALSE,grid.vline = FALSE,
                 #n.clusters.rows = 4,n.clusters.cols = 4,
                 legend.breaks = c(0,1,2),
                 heat.pal.values = c(0, 0.5, 1),
                 #heat.pal = c("#fee8c8","cornflower blue","#e34a33"), #Bad
                 #heat.pal = c("#fee8c8","#fdbb84","#e34a33"), #Oranges/Reds
                 #heat.pal = c("#DCDCDC","#fdbb84","#e34a33"), #Best, includes Grey
                 #heat.pal = c("#e41a1c","#377eb8","#4daf4a"), #Red Green Blue Qualitative Difference. Too Bright
                 heat.pal = c("#fbb4ae","#b3cde3","#ccebc5"), #Other Best Pale RGB Qualitative Differences
                 #row.dendrogram = TRUE,
                 col.dendrogram = TRUE,
                 pretty.order.rows = TRUE,
                 #pretty.order.cols = TRUE,
                 column.title = "Treatment (Versus Control)", column.title.size = 5,
                 row.title = "Dmel Ortholog and Specific Editing Locus", row.title.size = 5,
                 
                 #X.text = as.matrix(v1_txt),
                 
                 legend.vspace = 0.03,
                 legend.width = 4,
                 
                 # order the columns in a standard order
                 #order.cols = c(1,2,3,4,5,6),
                              ##3,4,5,6,7,8
                 #order.cols = c("LDOPA","FIG","OAHA","OA","HA","NONI"), #this does not work
                 
                 yr = comb[,11],
                 yr.axis.name = "Number Treatments\nWith Editing",
                 yr.plot.type = "bar",
                 # set bar colors
                 yr.bar.col = "black",
                 yr.obs.col = rep("beige", nrow(comb)),
                 yr.lim = c(0,6),
                 yr.breaks = c(0,1,2,3,4,5,6), 
                 
                 #yt = cor(comb[,3:8],comb$OA),
                 #yt.plot.type = "bar",
                 #yt.bar.col = "black",
                 #yr.obs.col = rep("beige", nrow(comb)),
                 #n.clusters.rows = 5, left.label = 'variable',
)


#vis1.row <- vis_1$membership.rows

#Colors the Text to be legible on dark background
w_or_B.col<- (comb[9:11])>=4
w_or_B.col<- gsub("TRUE", "white", w_or_B.col)
w_or_B.col<- gsub("FALSE", "black", w_or_B.col)
w_or_B.col <- matrix(w_or_B.col, ncol = ncol(comb[9:11]))


vis_2<-superheat(comb[,9:11],
                 title = "Number of Treatments with C-to-U Point Editing Events, by Locus",title.alignment = "center",
                 left.label.size = 0.14,left.label.text.size=3,
                 bottom.label.size = 0.2, bottom.label.text.size = 4,
                 grid.hline.col = "white",grid.vline.col = "white",
                 #heat.pal = c("#feedde","#fdd0a2","#fdae6b","#fd8d3c","#e6550d","#a63603"), #Orange Palette
                 #heat.pal = c("#fdd0a2","#fdae6b","#fd8d3c","#e6550d","#a63603"), #Same as above but no lightest
                 #heat.pal = c("#feedde","#fdd0a2","#fdae6b","#fd8d3c","#e6550d"), #Same as above but no Darkest
                 heat.pal = c("#edf8fb","#b2e2e2","#66c2a4","#2ca25f","#006d2c"),#Green Palette
                 X.text = round(as.matrix(comb[,9:11]), 1),X.text.size = 4,
                 X.text.col = w_or_B.col,
                 #membership.rows = vis1.row, left.label = 'variable'
)

#png("superheat.png", height = 900, width = 800)
#dev.off()
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
