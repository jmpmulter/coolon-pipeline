#Superheat_Heatmap_Generator
#install.packages("devtools")
#R.Version()
#devtools::install_github("rlbarter/superheat")
install.packages("superheat",dependencies = TRUE)


library(xlsx)
library(superheat)
dat <- read.xlsx("C:/Users/User/Desktop/Junior Spring/Coolon Lab/Targets_ISO_COL_A_heatmap01.xlsx", sheetName="ISO_COL_A_heatmap01")
dat_bckp<-dat

var_keep <- c("Scaf_num_Pos_Fbgn_Gmnum", "F0_CL_vs_FIG", "F1_CL_vs_HA", "F2_CL_vs_LDOPA", "F3_CL_vs_NONI", "F4_CL_vs_OAHA", "F5_CL_vs_OA", "Sig.Hits","Non.Sig.Hits","Total.Hits","Dmel.Ortholog","GM_num")
d_lim<- dat[ ,var_keep]
df<-d_lim[d_lim$Sig.Hits>=1,]
df[] <- lapply(df, as.character)
tmp<- df

#Replaces the factor versions of variables with Numbers
tmp <- lapply(tmp, function(x) {gsub("^O$", 0, x) })
tmp <- lapply(tmp, function(x) {gsub("^N$", 1, x) })
tmp <- lapply(tmp, function(x) {gsub("^S$", 2, x) })
tmp<-data.frame(lapply(tmp,as.numeric))
df[,2:10]<-tmp[,2:10]

vis_1<-superheat(X = df[,2:10])


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
