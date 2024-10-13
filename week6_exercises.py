import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm # py -m pip install statsmodels
from sklearn.metrics import mean_squared_error

#exercise 1
np.random.seed(2)

x = np.random.uniform(0, 10, 200)
y = 2 * x**2 - 5 * x + 3 + np.random.normal(0, 10, 200)

# Plot the dataset
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Dataset')
plt.show()

# Split into Train/Test
trainValues = {
    'x': x[:80],
    'y': y[:80]
}
training_data = pd.DataFrame(trainValues)

testValues = {
    'x': x[80:],
    'y': y[80:]
}
test_data = pd.DataFrame(testValues)

# Fit the regression model
train_x = training_data['x']
train_x_sq = pd.DataFrame(training_data['x']**2)

# Create polynomial features
train_x_poly = pd.concat([train_x, train_x_sq], axis = 1)

# Fit the OLS model
X = sm.add_constant(train_x_poly)
model = sm.OLS(training_data['y'], X)
results = model.fit()

# Obtain the predicted values
predicted_training_y = results.predict(X)
 
# Plot the training set and regression line
plt.scatter(training_data['x'], training_data['y'])
plt.scatter(training_data['x'], predicted_training_y, color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Regression Model (Degree 2)')
plt.show()

# Evaluate R_squared and MSE
R_squared = results.rsquared
MSE = mean_squared_error(training_data['y'], predicted_training_y) 
print(R_squared, MSE)
# R_squared = 0.9378508186540011

#exercise 2

#exercise 3.1
data_training = pd.read_excel('training.xlsx')
data_predictions = pd.read_excel('predictions_training.xlsx')
def malaria_prediction_accuracy_checker(data_training,data_predictions):
    '''
    A function calculating the accuracy of predictions made by a program based on placing borders around images
    
    Args:
        data_training(dataframe): dataframe containing the exact borders around the images.
        data_predictions(dataframe): dataframe containing predicted borders where images could be.
        
    Returns:
        mean_IOU: the average of the prediction succes rates for each border. 
    '''
    limit_r = int(max(max(data_training['max_r']),max(data_predictions['max_r']))) # vind de hoogste waarde van de rij coordinaten
    limit_c = int(max(max(data_training['max_c']),max(data_predictions['max_c']))) # vind de hoogste waarde van de kolom coordinaten
    A = np.zeros([limit_r,limit_c]) # maakt een lijst van nullen met een lengte en breedte van de maximale waarde. Wordt gebruikt om de borders te visualiseren
    IOU = [] # maakt een lijst aan waarin de IOU opgeslagen worden
    for t in data_training.index:
        t_min_r,p_min_r = data_training['min_r'].iloc[t],round(data_predictions['min_r'].iloc[t]) # vind de minimale coordinaten op de rij van een border
        t_max_r,p_max_r = data_training['max_r'].iloc[t]+1,round(data_predictions['max_r'].iloc[t]+1) # vind de maximale coordinaten op de rij van een border
        t_min_c,p_min_c = data_training['min_c'].iloc[t],round(data_predictions['min_c'].iloc[t]) # vind de minimale coordinaten op de kolom van een border
        t_max_c,p_max_c = data_training['max_c'].iloc[t]+1,round(data_predictions['max_c'].iloc[t]+1) # vind de maximale coordinaten op de kolom van een border
        A[t_min_r:t_max_r,t_min_c:t_max_c] = 1 # voegt een waarde 1 toe om de binnenkant van een border te visualiseren
        A[p_min_r:p_max_r,p_min_c:p_max_c]+=2 # voegt de waarde 2 aan de binnenkant van een predicted border.
        intersection = np.count_nonzero(A > 2) # berekent hoeveel van de predicted border met de daadwerkelijke border matchet
        union = np.count_nonzero(A > 0) # berekent hoeveel er in de daadwerkelijke en predicted border zit.
        IOU.append(intersection/union) # berekent hoeveel van de predicted border in de daadwerkelijke border zit.
        A[data_training['min_r'].iloc[t]-150:data_training['max_r'].iloc[t]+150,data_training['min_c'].iloc[t]-150:data_training['max_c'].iloc[t]+150] = 0 # reset de lijst van nullen zodat een nieuwe border gevisualiseerd kan worden.
        print(f'Currently at row {t}', end = '\r')
    mean_IOU = np.mean(IOU) # berekent het gemiddelde percentage van hoeveel de predicted borders matchen met de echte borders.
    print(f'The average IOU of the prediction is {mean_IOU:.4f}')
    return mean_IOU


#malaria_prediction_accuracy_checker(data_training,data_predictions) #Om de functie te testen. waarschuwing duurt best wel lang om uit te voeren.

#exercise 3.2