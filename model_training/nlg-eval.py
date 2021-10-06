from nlgeval import compute_metrics

metrics_dict = compute_metrics(hypothesis='final outquestions.txt', references=['data/answers.txt'], no_skipthoughts = True, no_glove = True)
for key in metrics_dict:
  metrics_dict[key] *=100
  print(key,': ', metrics_dict[key])