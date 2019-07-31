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

dat <- read.xlsx("C:/Users/User/Desktop/C-to-U End of 2019 Summer Pass/JM_C-to-U_Competition_XL.xlsx", sheetName="Sheet1")
dat_bckp<-dat
#dat<-dat_bckp
#save(dat_bckp,file = "dat_bckp")

var_keep <- c("Scaf_num_Pos_Fbgn_Gmnum", "F0_CL_vs_FIG", "F1_CL_vs_HA", "F2_CL_vs_LDOPA", "F3_CL_vs_NONI", "F4_CL_vs_OAHA", "F5_CL_vs_OA", "Sig.Hits","Non.Sig.Hits","Total.Hits","Dmel.Ortholog","GM_num")
d_lim<- dat[ ,var_keep]
#df<-d_lim[d_lim$Total.Hits>=1,]
df<-d_lim
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


#set.seed(1234)
#par(bg = 'black')
#rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col =        "black")

#tiff("Plot4b.tiff", width = 4, height = 4, pointsize = 1/300, units = 'in', res = 300)
#plot(x, y) # Make plot
#dev.off()
bitmap("Plot7.tiff", height = 4, width = 4, units = 'in', type="tifflzw", res=300)
plot(x, y)
dev.off()
par(mfrow = c(1,1))
#png("superheat.png", height = 704, width = 1245)
pdf("superheat2.pdf",width=9,height=6)
vis_1<-superheat(comb[,3:8],
                 title = "C-to-U Point Editing Presence Across Treatments", title.alignment = "center",
                 title.size = 4,
                 
                 #title.alignment = "center",
                 left.label.size = 0.05,left.label.text.size=2,
                 #left.label.text.col = "white",
                 bottom.label.size = 0.05, bottom.label.text.size = 2,
                 left.label.col = c("#99cc33","#6B8E23"),
                 bottom.label.col = c("#99cc33","#6B8E23"),
                 
                 #grid.hline.col = "white",
                 grid.hline.col = "#add65c",
                 grid.hline.size = .5,
                 ##006400
                 ##00FF00
                 ##228B22
                 #008000
                 #98FB98
                 #808000
                 #6B8E23
                 #8ab82e
                 #99cc33
                 #add65c
                 
                 #grid.vline.col = "white",
                 grid.vline = FALSE, #grid.hline = FALSE,
                 #n.clusters.rows = 4,n.clusters.cols = 4,
                 
                 legend.breaks = c(0,1,2),
                 #heat.pal.values = c(0, 0.5, 1),
                 #heat.pal = c("#fee8c8","cornflower blue","#e34a33"), #Bad
                 #heat.pal = c("#fee8c8","#fdbb84","#e34a33"), #Oranges/Reds
                 #heat.pal = c("#DCDCDC","#fdbb84","#e34a33"), #Best, includes Grey
                 #heat.pal = c("#e41a1c","#377eb8","#4daf4a"), #Red Green Blue Qualitative Difference. Too Bright
                 #heat.pal = c("#fbb4ae","#b3cde3","#ccebc5"), #Other Best Pale RGB Qualitative Differences
                 #heat.col.scheme = "Purples",
                 #heat.pal = c("#fc8d62","#8da0cb","#66c2a5"),
                 #heat.pal = c("#fee8c8","#fdbb84","#e34a33"),
                 #heat.pal = c("#ffeda0","#feb24c","#f03b20"),
                 #heat.pal = c("#fff7bc","#feb24c","#f03b20"),
                 heat.pal = c("#efedf5","#bcbddc","#756bb1"),
                 #row.dendrogram = TRUE,
                 col.dendrogram = TRUE,
                
                 #pretty.order.rows = TRUE,
                 #pretty.order.cols = TRUE,
                 column.title = "Treatment (Versus Control)", column.title.size = 3.5, #column.title.col = "white",
                 row.title = "Dmel Ortholog and Specific Editing Locus", row.title.size = 3.5, #row.title.col = "white",
                 
                 #X.text = as.matrix(v1_txt),
                 
                 legend.vspace = 0.03,
                 legend.width = 4,
                 legend.text.size = 3,
                 
                 
                 
                 # order the columns in a standard order
                 #order.cols = c(1,2,3,4,5,6),
                              ##3,4,5,6,7,8
                 #order.cols = c("LDOPA","FIG","OAHA","OA","HA","NONI"), #this does not work
                 
                 yr = comb[,11], #barchart
                 yr.axis.name = "Number Treatments\nWith Editing",
                 yr.axis.name.size = 10,
                 yr.axis.size = 4,
                 yr.plot.type ="bar",
                 yr.bar.col = "#756bb1",
                 yr.obs.col = rep("#efedf5", nrow(comb)),
                 yr.lim = c(0,6),
                 yr.breaks = c(0,1,2,3,4,5,6), 

                #row.dendrogram = TRUE,                 
                 # set bar colors
                
                 
                 #yt = cor(comb[,3:8],comb$OA),
                 #yt.plot.type = "bar",
                 #yt.bar.col = "black",
                 #yr.obs.col = rep("beige", nrow(comb)),
                 
                 n.clusters.rows = 9, #left.label = 'variable',
                 clustering.method = "hierarchical",
                 #smooth.heat = TRUE,
)
dev.off()

