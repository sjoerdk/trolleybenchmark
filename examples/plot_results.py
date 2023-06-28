from matplotlib import pyplot as plt
from trolleybenchmark.experiments import TrolleyDownloadResults
from trolleybenchmark.plotting import boxplot_per_label

results = TrolleyDownloadResults.load("/tmp/test_results.pcl")
boxplot_per_label(results=results, title='test plot')
plt.show()

