![Poster](https://github.com/sophielogan/Climate_Texts_Summarization/blob/main/Poster.png)

# General Context
Climate finance is an important and complex topic that involves the mobilization and deployment of financial resources to address climate change. Given the complexity and the speed with which the climate crisis must be addressed, having ways to summarize the climate finance landscape is beneficial.  A broad understanding of the different climate financing mechanisms would help policymakers and investors optimize decision making. In 2009, the world committed to $100 billion in climate financing per year at the UN Summit in Copenhagen. Allowing stakeholders to quickly summarize key climate and financial data will help them make informed decisions about how to deploy that capital going forward. 

# High Level Overview of Models, Data and Methods Used
## Models
- Human summaries (ground truth) 
- Distilbart CNN 6-6 
- CNN Sam Sum

## Evaluation Methods 
- Rouge
- Bleu 
- Topic Prevalence (novel metric - developed by authors for this application) 

### Data
- Sources 
  - Climate Policy Initiative (CPI), a top climate finance analysis organization
    - Full report texts 
    - Human generated summaries (ground truth)
- Technique 
  - Web scraping

# Detailed Methodology
We leverage data from the [Climate Policy Initiative](https://www.climatepolicyinitiative.org/), an organization that provides analysis on climate finance to governments and financial institutions. We ingest approximately 500 texts on various climate finance topics. Additionally, we collect the human summaries for those texts. 

We use two pre-trained summarization models to create our own summaries of the texts. They are both BART models from Hugging Face. The first is a Distilbart CNN 6-6 model and the second is a CNN SAMSum model. The CNN 6-6 model is trained with over 500k news articles with summarizations. The SAMSum dataset contains 16k messenger-like conversations with summaries and is one of the most popular summarization models with almost 1 million downloads last month. 

We leverage another model, topic modeling, to evaluate our summarization. We use LDA to find the topics generated for the full text, the human summary, and the model generated summaries and compare the intersections of those topics for one measure of summary accuracy.

To evaluate our results, we treat the human summaries as "ground truth" data. We assume that these summaries are what a good summary should be like. We use several methods to evaluate our models' performance including: 
Bleu: Bilingual Evaluation Understudy measures precision and how much the word (and/or n-grams) appeared in the text vs. the summary
Meteor: Metric for Evaluation of Translation with Explicit ORdering considers unigram matching, stemming and word order similarity
These are different ways of assessing how well the summary captures the most important topics and themes in a text.

# Code Structure
## Data collection 
- Data_collection_pipeline.ipynb

## Summary models
- Summary_model_training_pipeline.ipynb
  
## Evaluate models
- Summary_accuracy_calculation_pipeline.ipynb

### Custom packages to support each step of the pipeline
- data_collection.py
- data_cleaning.py
- entity_recognition.py
- lda_topic_modeling.py
- summarization_accuracies.py
- plot.py
