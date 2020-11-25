import pandas as pd
import torch as torch

df = pd.read_csv("set.csv")
#Che merda
extract = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,19,20,21,23,24] 
df = df.iloc[:, extract]

for x in range(len(df.index)):
    df.iloc[x, len(df.columns)-2] += 1
    df.iloc[x, :-2] /= df.iloc[x, -2]
    

for e in range(len(df.columns) - 2): #iterate for each column
    num = df.iloc[:, e].max()
    df.iloc[:, e] /= num

df = df.loc[:, df.columns != 'matchday']

def mapWinHome(row):
    if row['winner'] == "HOME":
        return 1
    else:
        return 0

    
def convert_output_win(source):
    return source.apply(mapWinHome, axis = 1)


df = df.sample(frac=1)
training = df.iloc[:-50]
test = df.iloc[-50:]

test_input  = test.iloc[:, :-1]
test_output = convert_output_win(test.iloc[:, -1:])

training_input  = training.iloc[:, :-1]
training_output = convert_output_win(training.iloc[:, -1:])

class Net(torch.nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Net, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(self.hidden_size, 1)
        self.sigmoid = torch.nn.Sigmoid() 
    def forward(self, x):
        hidden = self.fc1(x)
        relu = self.relu(hidden)
        output = self.fc2(relu)
        output = self.sigmoid(output)
        return output

#convert to tensors
training_input = torch.FloatTensor(training_input.values)
training_output = torch.FloatTensor(training_output.values)
test_input = torch.FloatTensor(test_input.values)
test_output = torch.FloatTensor(test_output.values)

input_size = training_input.size()[1] # number of features selected
hidden_size = 30 # number of nodes/neurons in the hidden layer
model = Net(input_size, hidden_size) # create the model
criterion = torch.nn.BCELoss() # works for binary classification
# without momentum parameter
optimizer = torch.optim.SGD(model.parameters(), lr = 0.9) 
#with momentum parameter
#optimizer = torch.optim.SGD(model.parameters(), lr = 0.9, momentum=0.2)

model.eval()
y_pred = model(test_input)
before_train = criterion(y_pred.squeeze(), test_output)
print('Test loss before training' , before_train.item())

model.train()
epochs = 5000
errors = []
for epoch in range(epochs):
    optimizer.zero_grad()
    # Forward pass
    y_pred = model(training_input)
    # Compute Loss
    loss = criterion(y_pred.squeeze(), training_output)
    errors.append(loss.item())
    print('Epoch {}: train loss: {}'.format(epoch, loss.item()))
    # Backward pass
    loss.backward()
    optimizer.step()

model.eval()
y_pred = model(test_input)
after_train = criterion(y_pred.squeeze(), test_output)
print('Test loss after Training' , after_train.item())
