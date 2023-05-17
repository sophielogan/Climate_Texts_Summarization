nltk.download('punkt')
nltk.download('wordnet')

#from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from nltk.translate.gleu_score import corpus_gleu
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import mutual_info_classif


class Accuracies: 
    '''
    Class to measure accuracy of summarizies. Different accuracies measure different 
    features of the summary. 

    Bleu: Bilingual Evaluation Understudy Measures precision and originally for machine 
        translation. It measures how much the word (and/or n-grams) in the machine 
        generated summaries appeared in the human reference summaries
    Meteor: Metric for Evaluation of Translation with Explicit ORdering considers 
        unigram matching, stemming and word order similarity between the generated summary 
        and the reference summary. It incorporates several linguistic and semantic 
        features to compute a similarity score
    Gleu: Grammar-based Evaluation Understudy method is an evaluation metric 
        specifically designed for text summarization tasks. It aims to measure the 
        grammaticality and fluency of the generated summaries by comparing them with 
        the reference summaries
    Information gain/perplexity: measures the reduction in entropy or uncertainty 
        between the original texts and their corresponding summaries. It quantifies 
        how much information the summaries provide compared to the original texts.The 
        calculation of information gain in text summarization accuracy involves 
        comparing the distribution of words or features in the original texts to their 
        distribution in the generated summaries. 

    Inputs: (list of strings) full texts 
            (list of strings) summaries of the texts
    Outputs: 
        calculate_bleu (list) of bleu score for each text/summary pair
        calculate_meteor (list) of meteor score for each text/summary pair
        calculate_gleu (int) gleu score for all text/summary pairs
        calculate_information_gain (list) of information gain scores for each text/summary pair

    '''
    def __init__(self, references, summaries):
        self.references = references
        self.summaries = summaries
        self.smoothing_function = SmoothingFunction().method4  # Smoothing method for BLEU
    
    # def calculate_rouge(self):
    #     rouge_scores = []
    #     rouge = Rouge()
    #     for reference, summary in zip(self.references, self.summaries):
    #         rouge_score = rouge.get_scores(
    #             summary, reference, avg=True
    #         )
    #         rouge_scores.append(rouge_score)
    #     return rouge_scores

    def calculate_bleu(self):
        bleu_scores = []
        for reference, summary in zip(self.references, self.summaries):
            reference_tokens = reference.split()
            summary_tokens = summary.split()
            bleu_score = sentence_bleu(
                [reference_tokens], summary_tokens, smoothing_function=self.smoothing_function
            )
            bleu_scores.append(bleu_score)
        return bleu_scores
    
    def calculate_meteor(self):
        meteor_scores = []
        for reference, summary in zip(self.references, self.summaries):
            meteor_score_value = meteor_score([reference], summary)
            meteor_scores.append(meteor_score_value)
        return meteor_scores

    def calculate_gleu(self):
        gleu_score = corpus_gleu([[reference] for reference in self.references], self.summaries)
        return gleu_score

    def calculate_information_gain(self):
      vectorizer = CountVectorizer()
      text_vectors = vectorizer.fit_transform(self.references)

      information_gain = mutual_info_classif(text_vectors, self.summaries)
      return information_gain
    