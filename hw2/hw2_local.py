import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = load_csv('./hw2/CreditCard.csv')

    df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'M' else 0)
    df['CarOwner'] = df['CarOwner'].apply(lambda x: 1 if x == 'Y' else 0)
    df['PropertyOwner'] = df['PropertyOwner'].apply(lambda x: 1 if x == 'Y' else 0)

    x = df[['Gender', 'CarOwner', 'PropertyOwner', '#Children', 'WorkPhone', 'Email_ID']].values
    y = df['CreditApprove'].values
    
    '''
    print('Main df:')
    print(df)
    print('x df:')
    print(x)
    print('y df: ')
    print(y)
    
    weights = initialize_weights()
    print("weights:")
    print(weights)
    print("x at row 0:")
    print(x[0])
    print("estimation:")
    print(estimation(x[0], weights))
    '''

    best_errors, best_weights, errors, rounds = hill_climb_search(x, y)
    print('Best error:')
    print(best_errors)
    print('Best weights:')
    print(best_weights)

    plt.plot(range(len(errors)), errors, marker='o')
    plt.title('Errors vs rounds of search')
    plt.xlabel('Round #')
    plt.ylabel('er(w)')
    plt.grid(True)
    plt.show()
    

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def initialize_weights():
    return np.random.choice([-1, 1], size=6)

def estimation(x, weights):
    estimation = np.dot(x, weights)
    return estimation

def error_func(x, y, weights):
    estimations = estimation(x, weights) # 2D array dotted with 1D array = 1D array

    return np.mean((estimations - y) ** 2)

def hill_climb_search(x, y):
    num_attributes = 6
    current_weights = initialize_weights()
    current_error = error_func(x, y, current_weights)
    rounds = 0
    errors = []

    while True:
        best_weights = current_weights
        best_error = current_error
        

        for i in range(num_attributes):
            neighbor_weights = current_weights.copy()
            neighbor_weights[i] *= -1

            neighbor_error = error_func(x, y, neighbor_weights)
            #print(f'Neighbor error: {neighbor_error}, Best error: {best_error}')

            if neighbor_error < best_error:
                best_error = neighbor_error
                best_weights = neighbor_weights
            
            rounds += 1
            errors.append(best_error)
        
        if best_error >= current_error:
            #print(f'Exiting...best error: {best_error}, Current error: {current_error}')
            break

        current_weights = best_weights
        current_error = best_error

        #print(f'Current error: {current_error}, Best error: {best_error}, Weights: {current_weights}')
    
    return best_error, best_weights, errors, rounds


if __name__ == "__main__":
    main()