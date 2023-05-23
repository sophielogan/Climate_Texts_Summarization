COLOR ='#BC5F55'


fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
fig.suptitle('Comparing Accuracies across Models')

sns.histplot(summary_comparison_df.max_meteor_model_only, ax=axes[0],color=COLOR)
axes[0].set_title('Number of Max Meteor Scores for All Summaries')
axes[0].set_xlabel('')

sns.histplot(summary_comparison_df.max_bleu_model_only, ax=axes[1],color=COLOR)
axes[1].set_title('Number of Max Bleu Scores for All Summaries')
axes[1].set_xlabel('')




fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
fig.suptitle('Comparing Accuracies across Human and Model Summaries')

sns.histplot(summary_comparison_df.max_meteor, ax=axes[0],color=COLOR)
axes[0].set_title('Number of Max Meteor Scores for All Summaries')
axes[0].set_xlabel('')

sns.histplot(summary_comparison_df.max_bleu, ax=axes[1],color=COLOR)
axes[1].set_title('Number of Max Bleu Scores for All Summaries')
axes[1].set_xlabel('')
