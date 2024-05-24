#an attempt at crating a character level rnn to predict the determiner for the word list
#realised the word list can be prefixed super simpely and jsut classified as plurul or singular to determine prefix so scrapped the idea

import torch
import torch.nn as nn
import string
import random

# Define the vocabulary
all_letters = string.ascii_letters + " .,;'-"  # Define all possible characters
n_letters = len(all_letters) + 1  # Plus EOS (End of Sentence) marker

# Define the RNN model
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        # Define the linear transformations for the input, hidden, and output layers
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.o2o = nn.Linear(hidden_size + output_size, output_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        # Concatenate the input and hidden state
        combined = torch.cat((input, hidden), 1)
        # Calculate the hidden state based on the combined input and previous hidden state
        hidden = self.i2h(combined)
        # Calculate the output based on the combined input and hidden state
        output = self.i2o(combined)
        # Concatenate the hidden state and output
        output_combined = torch.cat((hidden, output), 1)
        # Calculate the final output
        output = self.o2o(output_combined)
        # Apply dropout for regularization
        output = self.dropout(output)
        # Apply softmax activation to obtain probabilities
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        # Initialize the hidden state with zeros
        return torch.zeros(1, self.hidden_size)
    

# Prepare the training data
# You need to prepare your dataset containing sentences with objects and their determiners
# For demonstration, we'll use a simple dataset
training_data = [
    ("a", "aeroplane"),
    ("a", "bicycle"),
    ("a", "bird"),
    ("a", "boat"),
    ("a", "bottle"),
    ("a", "bus"),
    ("a", "car"),
    ("a", "cat"),
    ("a", "chair"),
    ("a", "cow"),
    ("a", "diningtable"),
    ("a", "dog"),
    ("a", "horse"),
    ("a", "motorbike"),
    ("a", "person"),
    ("a", "pottedplant"),
    ("a", "sheep"),
    ("a", "sofa"),
    ("a", "train"),
    ("a", "tvmonitor"),
    ("an", "aeroplane"),
    ("an", "bicycle"),
    ("an", "bird"),
    ("an", "boat"),
    ("an", "bottle"),
    ("an", "bus"),
    ("an", "car"),
    ("an", "cat"),
    ("an", "chair"),
    ("an", "cow"),
    ("an", "diningtable"),
    ("an", "dog"),
    ("an", "horse"),
    ("an", "motorbike"),
    ("an", "person"),
    ("an", "pottedplant"),
    ("an", "sheep"),
    ("an", "sofa"),
    ("an", "train"),
    ("an", "tvmonitor"),
    ("and", "aeroplane"),
    ("and", "bicycle"),
    ("and", "bird"),
    ("and", "boat"),
    ("and", "bottle"),
    ("and", "bus"),
    ("and", "car"),
    ("and", "cat"),
    ("and", "chair"),
    ("and", "cow"),
    ("and", "diningtable"),
    ("and", "dog"),
    ("and", "horse"),
    ("and", "motorbike"),
    ("and", "person"),
    ("and", "pottedplant"),
    ("and", "sheep"),
    ("and", "sofa"),
    ("and", "train"),
    ("and", "tvmonitor")
    
]

# Helper functions for processing data
def categoryTensor(category):
    # Convert a character to a one-hot tensor
    tensor = torch.zeros(1, n_letters)
    tensor[0][all_letters.find(category)] = 1
    return tensor

def inputTensor(line):
    # Convert a sequence of characters to a tensor
    tensor = torch.zeros(len(line), 1, n_letters)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][all_letters.find(letter)] = 1
    return tensor

def targetTensor(line):
    # Convert a sequence of characters to a tensor of character indexes
    letter_indexes = [all_letters.find(line[li]) for li in range(len(line))]
    letter_indexes.append(n_letters - 1)  # Append EOS marker
    return torch.LongTensor(letter_indexes)

def randomTrainingExample():
    # Randomly select a training example
    line, category = random.choice(training_data)
    category_tensor = categoryTensor(category)
    input_line_tensor = inputTensor(line)
    target_line_tensor = targetTensor(line) 
    return category_tensor, input_line_tensor, target_line_tensor

# Training the model
n_hidden = 128
rnn = RNN(n_letters, n_hidden, n_letters)

criterion = nn.NLLLoss()  # Define the loss function
learning_rate = 0.0005

def train(category_tensor, input_line_tensor, target_line_tensor):
    target_line_tensor.unsqueeze_(-1)
    hidden = rnn.initHidden()

    rnn.zero_grad()  # Zero the gradients

    loss = 0

    for i in range(input_line_tensor.size(0)):
        output, hidden = rnn(input_line_tensor[i], hidden)
        # Calculate the loss between predicted and target categories
        l = criterion(output, target_line_tensor[i])  # Use category tensor as the target
        loss += l

    loss.backward()  # Backpropagation

    # Update the model parameters using gradient descent
    for p in rnn.parameters():
        p.data.add_(p.grad.data, alpha=-learning_rate)

    return output, loss.item() / input_line_tensor.size(0)


n_iters = 5000
print_every = 1000
plot_every = 100
all_losses = []
total_loss = 0

for iter in range(1, n_iters + 1):
    output, loss = train(*randomTrainingExample())
    total_loss += loss

    if iter % print_every == 0:
        print('%d %d%% %.4f' % (iter, iter / n_iters * 100, loss))

    if iter % plot_every == 0:
        all_losses.append(total_loss / plot_every)
        total_loss = 0

max_length = 20

def sample(word):
    start_letter = random.choice(string.ascii_letters)
    with torch.no_grad():  # no need to track history in sampling
        category_tensor = categoryTensor("start")
        input = inputTensor(word)  # Use the input word
        hidden = rnn.initHidden()

        output_name = word

        for i in range(max_length):
            output, hidden = rnn(input[0], hidden)
            topv, topi = output.topk(1)
            topi = topi[0][0]
            if topi == n_letters - 1:
                break
            else:
                letter = all_letters[topi]
                output_name = letter + " " + output_name
            input = inputTensor(output_name[-1])  # Use the last generated letter as input for the next step

        return output_name

# Generating samples
words = ["cat", "boat", "dog", "bird", "car"]  # Example words
for word in words:
    print(sample(word))
for word in words:
    print(sample(word))
for word in words:
    print(sample(word))    
