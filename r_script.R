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
test_data$class_label <- paste0(test_data$toxic,test_data$severe_toxic,test_data$severe_toxic,test_data$obscene,test_data$threat,test_data$insult,test_data$identity_hate)
test_data <- test_data[,-3:-8]

train_data <- na.omit(train_data)
train_data <- train_data[rowSums(abs(train_data[,3:8])) != 0,]
data_corpus <- select(test_data,id,comment_text)
train_data$class_label <- paste0(train_data$toxic,train_data$severe_toxic,train_data$severe_toxic,train_data$obscene,train_data$threat,train_data$insult,train_data$identity_hate)
train_data <- train_data[,-3:-8]

#Naive Bayes:
set.seed(6)
library(e1071)
naive_bayes_model <- naiveBayes(as.factor(class_label) ~ ., data = train_data)
predicted_labels <- predict(naive_bayes_model,train_data)
require(caret)
confusionMatrix(predicted_labels,train_data$class_label)



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

#using LSA:
library(lsa)
lsa_model <- lsa(data_matrix)


#using LDA:
library(lda)
library(topicmodels)
data_lda <- LDA(data_matrix, k = 6)
document_probabilities <- posterior(data_lda)$topics

for(i in 1:5){
  lst <- sort(posterior(data_lda)$terms[i,], index.return=TRUE, decreasing=TRUE)
  top_terms_id <- c(lapply(lst, `[`, lst$x %in% head(unique(lst$x),10)))
  print(colnames(data_matrix)[top_terms_id$ix])
}




data_svd <- svd(data_matrix)
u <- data_svd$u[,1:6]
v <- data_svd$v[1:6,]
set.seed(10)
data_cluster <- kmeans(u, 6)
data_cluster$size

for(i in 1:5){
  lst <- sort(v[i,], index.return=TRUE, decreasing=TRUE)
  top_terms_id <- c(lapply(lst, `[`, lst$x %in% head(unique(lst$x),10)))
  print(colnames(data_matrix)[top_terms_id$ix])
}



