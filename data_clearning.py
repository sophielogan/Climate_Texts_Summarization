def elim_non_str(df, col): 
  df = df.copy()
  og_shape = df.shape[0]

  # Eliminate anything in column that is not a string
  df = df[df[col].apply(lambda x: isinstance(x, str))]
  
  print(f'Eliminated {og_shape - df.shape[0]} non-string entries, from {og_shape} to {df.shape[0]}')
  
  return df

def add_lang_col(df, content_col):
  df = df.copy()
  lang = []
  for idx,i in enumerate(df[content_col]):
    # Use detect function to predict language
    try:
      lang.append(detect(i))
    except:
      language = "error"
      print("This row throws and error:", idx)
      lang.append(None)
  df['Language'] = lang
  
  return df

def isolate_en(df, col='Language'):
  df = df.copy()
  og_shape = df.shape[0]
  df = df[df[col]=='en']
  print(f'Eliminated {og_shape - df.shape[0]} non-English entries, from {og_shape} to {df.shape[0]}')

  return df

def clean_text(df, col): 
  df = df.copy()

  # Strip punctuation
  df[col] = df[col].map(lambda x: re.sub('[,\.!?]', '', x))
  df[col] = df[col].map(lambda x: x.replace("\n", " "))
  
  # Everything to lowercase
  df[col] = df[col].map(lambda x: x.lower())
  
  return df 
