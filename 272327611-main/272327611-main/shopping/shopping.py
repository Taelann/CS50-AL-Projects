import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def main():
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=0.4
    )

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    print(f"Correct: {(predictions == y_test).sum()}")
    print(f"Incorrect: {(predictions != y_test).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    evidence, labels = [], []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    with open(filename) as file:
        for row in csv.DictReader(file):
            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                months.index(row["Month"]),
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                int(row["VisitorType"] == "Returning_Visitor"),
                int(row["Weekend"] == "TRUE")
            ])
            labels.append(int(row["Revenue"] == "TRUE"))

    return evidence, labels


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    positive = [i for i in range(len(labels)) if labels[i] == 1]
    negative = [i for i in range(len(labels)) if labels[i] == 0]

    sensitivity = sum(predictions[i] == 1 for i in positive) / len(positive)
    specificity = sum(predictions[i] == 0 for i in negative) / len(negative)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
