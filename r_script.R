setwd("~/Documents/uncommonhacks/toxic-comments-kaggle")
require("tm")
require("stringr")
require("dplyr")

data <- read.csv("data/train.csv")
testset <- read.csv("data/test.csv")
library(caTools)

smp_siz = floor(0.75*nrow(data))
set.seed(123)
index <- sample(seq_len(nrow(data)),size = smp_siz)
train_data <- data[index,]
test_data <- data[-index,]


train_data <- na.omit(train_data)
testset <- na.omit(testset)

data_df <- select(test_data,id,comment_text)
testdata_df <-  select(testset,id,comment_text)

colnames(data_df) <- c("doc_id","text")
colnames(testdata_df) <- c("doc_id","text")

data_corpus <- VCorpus(DataframeSource(data_df))
testdata_corpus <- VCorpus(DataframeSource(testdata_df))

#Naive Bayes:
set.seed(6)
library(e1071)
naive_bayes_model <- naiveBayes(as.factor(class_label) ~ ., data = train_data)
predicted_labels <- predict(naive_bayes_model,train_data)
require(caret)
confusionMatrix(predicted_labels,train_data$class_label)



RemoveEmail <- function(x) {
  str_replace_all(x,"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+", "")
}

data_corpus <- tm_map(data_corpus,content_transformer(RemoveEmail))
testdata_corpus <- tm_map(testdata_corpus,content_transformer(RemoveEmail))
data_corpus <- tm_map(data_corpus,removePunctuation)
testdata_corpus <- tm_map(testdata_corpus,removePunctuation)
data_corpus <- tm_map(data_corpus,removeNumbers)
testdata_corpus <- tm_map(testdata_corpus,removeNumbers)
data_corpus <- tm_map(data_corpus,stripWhitespace)
testdata_corpus <- tm_map(testdata_corpus,stripWhitespace)
data_corpus <- tm_map(data_corpus,removePunctuation)
testdata_corpus <- tm_map(testdata_corpus,removePunctuation)
data_corpus <- tm_map(data_corpus,stripWhitespace)
testdata_corpus <- tm_map(testdata_corpus,stripWhitespace)
data_corpus <- tm_map(data_corpus,stemDocument)
testdata_corpus <- tm_map(testdata_corpus,stemDocument)
data_corpus <- tm_map(data_corpus,removeWords,stopwords("english"))
testdata_corpus <- tm_map(testdata_corpus,removeWords,stopwords("english"))
data_corpus <- tm_map(data_corpus,stripWhitespace)
testdata_corpus <- tm_map(testdata_corpus,stripWhitespace)

data_matrix <- DocumentTermMatrix(data_corpus)
testdata_matrix <- DocumentTermMatrix(testdata_corpus)
data_matrix <- removeSparseTerms(data_matrix,0.999)
testdata_matrix <- removeSparseTerms(testdata_matrix,0.999)

matrix_data_frame <- as.data.frame(as.matrix(data_matrix))
matrix_testdata_frame <- as.data.frame(as.matrix(testdata_matrix))

matrix_data_frame$threat <- test_data$threat
matrix_data_frame$toxic <- test_data$toxic
matrix_data_frame$severe_toxic <- test_data$severe_toxic
matrix_data_frame$obscene  <- test_data$obscene
matrix_data_frame$insult  <- test_data$insult
matrix_data_frame$identity_hate <- test_data$identity_hate

# rowTotals <- apply(data_matrix , 1, sum) 
# data_matrix   <- data_matrix[rowTotals> 0, ]

#Exploratory analysis:
N <- 10
findFreqTerms(testdata_matrix, N)

install.packages("wordcloud") # word-cloud generator 
install.packages("RColorBrewer") # color palettes
library("wordcloud")
library("RColorBrewer")
#Word Cloud:
m <- as.matrix(t(data_matrix))
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
  
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


#Naive Bayes:
set.seed(6)
library(e1071)
naive_bayes_model <- naiveBayes(as.factor(matrix_data_frame$threat) ~ ., data = matrix_data_frame)
predicted_labels <- predict(naive_bayes_model,test_data)
require(caret)
confusionMatrix(predicted_labels,matrix_data_frame$threat)

#using LSA:
library(lsa)
lsa_model <- lsa(data_matrix,dim=40)

lsa_matrix <- as.matrix(lsa_model)
lsa_data_frame <- as.data.frame(lsa_model[1])

for(i in 1:5){
  lst <- sort(lsa_model$dk[,i], index.return=TRUE, decreasing=TRUE)
  top_terms_id <- c(lapply(lst, `[`, lst$x %in% head(unique(lst$x),5)))
  print(colnames(data_matrix)[top_terms_id$ix])
}

#Word Cloud:
m <- as.matrix(t(data_matrix))
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)

set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

##Threat
lsa_data_frame$threat <- test_data$threat



#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(threat) ~ .-class_label, data = lsa_data_frame)
predicted_labels_threat <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_threat <- predicted_labels_threat[,2]
# confusionMatrix(predicted_labels,lsa_data_frame$threat)

##Toxic
#Naive Bayes:
set.seed(6)
naive_bayes_model <- naiveBayes(as.factor(toxic) ~ ., data = matrix_data_frame)
predicted_labels <- predict(naive_bayes_model,test_data,type = c("raw"))
# confusionMatrix(predicted_labels,matrix_data_frame$toxic)

#using LSA:
lsa_data_frame$toxic <- test_data$toxic

#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(toxic) ~ .-class_label, data = lsa_data_frame)
predicted_labels_toxic <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_toxic <- predicted_labels_toxic[,2]
# confusionMatrix(predicted_labels,test_data$toxic)


##severe_toxic

#Naive Bayes:
set.seed(6)
naive_bayes_model <- naiveBayes(as.factor(severe_toxic) ~ ., data = matrix_data_frame)
predicted_labels_severe_toxic <- predict(naive_bayes_model,test_data)
# confusionMatrix(predicted_labels,matrix_data_frame$severe_toxic)

#using LSA:
lsa_data_frame$severe_toxic <- test_data$severe_toxic

#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(severe_toxic) ~ .-class_label, data = lsa_data_frame)
predicted_labels_severe_toxic <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_severe_toxic <- predicted_labels_severe_toxic[,2]
# confusionMatrix(predicted_labels,lsa_data_frame$severe_toxic)

##obscene
#Naive Bayes:
set.seed(6)
naive_bayes_model <- naiveBayes(as.factor(obscene) ~ ., data = matrix_data_frame)
predicted_labels <- predict(naive_bayes_model,test_data)
# confusionMatrix(predicted_labels,matrix_data_frame$obscene)

#using LSA:
lsa_data_frame$obscene <- test_data$obscene

#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(obscene) ~ .-class_label, data = lsa_data_frame)
predicted_labels_obscene <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_obscene <- predicted_labels_obscene[,2]
# confusionMatrix(predicted_labels,lsa_data_frame$obscene)

##insult
#Naive Bayes:
set.seed(6)
naive_bayes_model <- naiveBayes(as.factor(insult) ~ ., data = matrix_data_frame)
predicted_labels <- predict(naive_bayes_model,test_data)
# confusionMatrix(predicted_labels,matrix_data_frame$insult)

#using LSA:
lsa_data_frame$insult <- test_data$insult

#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(insult) ~ .-class_label, data = lsa_data_frame)
predicted_labels_insult <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_insult <- predicted_labels_insult[,2]
# confusionMatrix(predicted_labels,lsa_data_frame$insult)

##identity_hate

#Naive Bayes:
set.seed(6)
naive_bayes_model <- naiveBayes(as.factor(matrix_data_frame$identity_hate) ~ ., data = matrix_data_frame)
predicted_labels <- predict(naive_bayes_model,test_data)
confusionMatrix(predicted_labels,matrix_data_frame$identity_hate)

#using LSA:
lsa_data_frame$identity_hate <- test_data$identity_hate

#naive bayes on lsa
naive_bayes_model <- naiveBayes(as.factor(identity_hate) ~ .-class_label, data = lsa_data_frame)
predicted_labels_identity_hate <- predict(naive_bayes_model,matrix_testdata_frame,type = c("raw"))
predicted_labels_identity_hate <- predicted_labels_identity_hate[,2]
# confusionMatrix(predicted_labels,lsa_data_frame$identity_hate)


predicted_data <- cbind(predicted_labels_threat,predicted_labels_toxic,predicted_labels_severe_toxic,predicted_labels_obscene,predicted_labels_insult,predicted_labels_identity_hate)
colnames(predicted_data) <- colnames(data[-1:-2])
predicted_dataframe <- as.data.frame(predicted_data)
predicted_dataframe <- cbind(test$id,predicted_dataframe)
colnames(predicted_dataframe)[1] <- "id"
write.table(predicted_dataframe,file="predicted_probabilities.csv", quote=FALSE, sep=',', row.names=FALSE)

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



