import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
    0   - Administrative, an integer
    1   - Administrative_Duration, a floating point number
    2   - Informational, an integer
    3   - Informational_Duration, a floating point number
    4   - ProductRelated, an integer
    5   - ProductRelated_Duration, a floating point number
    6   - BounceRates, a floating point number
    7   - ExitRates, a floating point number
    8   - PageValues, a floating point number
    9   - SpecialDay, a floating point number
    10  - Month, an index from 0 (January) to 11 (December)
    11  - OperatingSystems, an integer
    12  - Browser, an integer
    13  - Region, an integer
    14  - TrafficType, an integer
    15  - VisitorType, an integer 0 (not returning) or 1 (returning)
        New_Visitor = 0
        Returning_Visitor = 1
    16  - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is True, and 0 False.
    """
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader) # Skips headers
        
        months = {
            'JAN': 0,
            'FEB': 1,
            'MAR': 2,
            'APR': 3,
            'MAY': 4,
            'JUNE': 5,
            'JUL': 6,
            'AUG': 7,
            'SEP': 8,
            'OCT': 11,
            'NOV': 12,
            'DEC': 13
        }
        
        evidence = []
        labels = []
        
        for row in reader:
            # Change specific column to number
            row[10] = months[row[10].upper()]
            
            # Assign number value to string
            for i, value in enumerate(row):
                try:
                    row[i] = int(value)
                except ValueError:
                    if value in ("Returning_Visitor", "TRUE"):
                        row[i] = 1
                    else:
                        try: row[i] = float(value)
                        except: row[i] = 0
                        
                        
            # Append to lists
            evidence.append(row[:-1])
            labels.append(row[-1])
        
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    total_positive = sum(labels)
    total_negative = len(labels) - total_positive
    
    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            sensitivity += 1
        elif label == 0 and prediction == 0:
            specificity += 1
    
    return (sensitivity / total_positive, specificity / total_negative)


if __name__ == "__main__":
    main()
