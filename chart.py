import json
import matplotlib.pyplot as plt

# Load JSON data
with open('outputs/charts_data_test.json') as f:
    charts_data = json.load(f)

# Generate charts
for chart in charts_data['charts']:
    plt.figure()
    if chart['type'] == 'line':
        plt.plot(chart['data']['x'], chart['data']['y'])
        plt.title(chart['title'])
        plt.xlabel(chart['x_label'])
        plt.ylabel(chart['y_label'])
    elif chart['type'] == 'bar':
        plt.bar(chart['data']['x'], chart['data']['y'])
        plt.title(chart['title'])
        plt.xlabel(chart['x_label'])
        plt.ylabel(chart['y_label'])
    elif chart['type'] == 'pie':
        plt.pie(chart['data']['values'], labels=chart['data']['labels'], autopct='%1.1f%%')
        plt.title(chart['title'])
    plt.show()
