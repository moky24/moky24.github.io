# Neural Network Titanic

# clean workspace
rm(list = ls())
cat("\014")

library(reticulate) 
use_condaenv('tf_env', required=T) 
py_config()

library(tensorflow)
tf$config$list_physical_devices("GPU") # we need "device:GPU:0"


# Load necessary libraries
library(keras)
library(caret) # for scaling
library(dplyr)


# Data
titanic = read.csv(file='data/Titanic.csv')
head(titanic)

set.seed(200)
tensorflow::set_random_seed(200)
idx = sample(1:dim(titanic)[1],size=floor(dim(titanic)[1]*0.8),replace=F)
train = titanic[+idx,]
test  = titanic[-idx,]


train <- train[complete.cases(train), ]

# --- ---
# Separate features (X) and target (y)
y_train <- train$survived
X_train <- train %>% select(Top, Mid, female, age, parent, child)  # Define train features

y_test <- test$survived
X_test <- test %>% select(Top, Mid, female, age, parent, child)  # Define test features

# Handle missing values by imputing with the median for both training and test sets
X_train <- X_train %>% mutate_all(~ifelse(is.na(.), median(., na.rm = TRUE), .))
X_test <- X_test %>% mutate_all(~ifelse(is.na(.), median(., na.rm = TRUE), .))

# Scale the features using caret's preProcess function on the training data
preprocess_params <- preProcess(X_train, method = c("center", "scale"))
X_train_scaled <- predict(preprocess_params, X_train)
X_test_scaled <- predict(preprocess_params, X_test)

# Convert data to matrices for Keras
X_train_scaled <- as.matrix(X_train_scaled)
X_test_scaled <- as.matrix(X_test_scaled)
y_train <- as.numeric(y_train)
y_test <- as.numeric(y_test)

# --- ---
# Define the neural network model
model <- keras_model_sequential() %>%
  layer_dense(units = 8, activation = "relu", input_shape = ncol(X_train_scaled)) %>% #96 to overfit, 32 ok
  #layer_dropout(0.5) %>% 
  layer_dense(units = 8, activation = "relu") %>% #96 to overfit, 32 ok
  #layer_dropout(0.5) %>% 
  layer_dense(units = 1, activation = "sigmoid")  # Output layer for logit

# --- ---
# Compile the model
model %>% compile(
  optimizer = keras$optimizers$legacy$RMSprop(learning_rate = 0.0001), #0.0075
  loss = "binary_crossentropy", 
  metrics = c("accuracy")
)

# --- ---
# Train the model
history <- model %>% fit(
  X_train_scaled,
  y_train,
  epochs = 75, #75
  batch_size = 16,
  validation_split = 0.2, #0.2
  verbose = 1
)

# --- ---
# Evaluate the model
results <- model %>% evaluate(X_test_scaled, y_test)
print(results)
