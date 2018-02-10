setwd("~/Documents/uncommonhacks/toxic-comments-kaggle")
require("tm")
require("stringr")
require("dplyr")

data <- read.csv("data/train.csv")

library(caTools)

smp_siz = floor(0.75*nrow(data))
set.seed(123)
index <- sample(seq_len(nrow(data)),size = smp_siz)
train_data <- data[index,]
test_data <- data[-index,]

data_corpus <- select(test_data,id,comment_text)
colnames(data_corpus) <- c("doc_id","text")
data_corpus <- VCorpus(DataframeSource(data_corpus))

RemoveEmail <- function(x) {
  str_replace_all(x,"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+", "")
}

data_corpus <- tm_map(data_corpus,content_transformer(RemoveEmail))
data_corpus <- tm_map(data_corpus,removePunctuation)
data_corpus <- tm_map(data_corpus,removeNumbers)
data_corpus <- tm_map(data_corpus,stripWhitespace)
data_corpus <- tm_map(data_corpus,removePunctuation)
data_corpus <- tm_map(data_corpus,stripWhitespace)
data_corpus <- tm_map(data_corpus,stemDocument)
data_corpus <- tm_map(data_corpus,removeWords,stopwords("english"))
data_corpus <- tm_map(data_corpus,stripWhitespace)

data_matrix <- DocumentTermMatrix(data_corpus)
removeSparseTerms(data_matrix,0.999)
rowTotals <- apply(data_matrix , 1, sum) 
data_matrix   <- data_matrix[rowTotals> 0, ]

data_svd <- svd(data_matrix)


library(lda)
library(topicmodels)
data_lda <- LDA(data_matrix, k = 6)
