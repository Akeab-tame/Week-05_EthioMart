import pandas as pd

class AmharicNERLabeler:
    """
    A class to label tokens in Amharic text for Named Entity Recognition (NER).
    
    The class identifies and labels tokens as prices, locations, products, or others
    based on predefined rules and keywords.

    Attributes:
    -----------
    price_keywords : list
        Keywords associated with price entities.
    location_list : list
        Predefined list of known location keywords.
    product_keywords : list
        Predefined list of known product keywords.
    """

    def __init__(self):
        # Define keywords for different entities
        self.price_keywords = ['ዋጋ', 'ብር', 'ከ']
        self.location_list = [
            'አዲስ', 'የታይላንድ', 'ቦሌ', 'ቡልጋሪ', 
            'በረራ', 'ልደታ', 'ባልቻ', 'አአ'
        ]
        self.product_keywords = [
            'ምርት', 'ስቶቭ', 'ማንኪያ', 'የችበስመጥበሻ',
            'መጥበሻ', 'መጥበሻዎች', 'ምርቶች', 'ባትራ', 'ካርድ'
        ]

    def label_tokens(self, tokens):
        """
        Label the tokens with their corresponding NER labels.

        Parameters:
        -----------
        tokens : list
            A list of tokenized strings in Amharic.

        Returns:
        --------
        list
            A list of tuples where each tuple contains a token and its corresponding label.
        """
        labels = []

        for i, token in enumerate(tokens):
            token_stripped = token.strip()  # Strip any surrounding whitespace

            # Step 1: Check if the current token ends with "ብር"
            if token_stripped.endswith('ብር'):
                labels.append('I-PRICE')  # Label as I-PRICE
                continue
            
            # Step 2: Check if the current token is "ዋጋ"
            if token_stripped == 'ዋጋ':
                labels.append('B-PRICE')  # Label as B-PRICE
                continue
            
            # Step 3: Check if the current token is numeric
            if token_stripped.isdigit():
                # Check if the next token is "ብር"
                next_token = tokens[i + 1].strip() if i < len(tokens) - 1 else None
                if next_token == 'ብር':
                    labels.append('I-PRICE')  # Label as I-PRICE
                    continue

                # Check if the previous token is "ዋጋ"
                prev_token = tokens[i - 1].strip() if i > 0 else None
                if prev_token == 'ዋጋ':
                    labels.append('I-PRICE')  # Label as I-PRICE
                    continue
                else:
                    labels.append('O')  # Not a price entity
                    continue
            
            # Step 4: Check if the current token is "ብር"
            if token_stripped == 'ብር':
                # Check if the previous token is numeric
                prev_token = tokens[i - 1].strip() if i > 0 else None
                if prev_token and prev_token.isdigit():
                    labels.append('I-PRICE')  # Label as I-PRICE
                    continue
            
            # Step 5: Check if the current token contains both "ዋጋ" and "ብር"
            if 'ዋጋ' in token_stripped and 'ብር' in token_stripped:
                labels.append('I-PRICE')  # Label as I-PRICE
                continue
            
            # Step 6: Check if the current token contains "ከ" and "ብር"
            if 'ከ' in token_stripped and 'ብር' in token_stripped:
                labels.append('I-PRICE')  # Label as I-PRICE
                continue
            
            # Step 7: Check if the current token contains both "ዋጋ" and numeric values
            if 'ዋጋ' in token_stripped and any(char.isdigit() for char in token_stripped):
                labels.append('I-PRICE')  # Label as I-PRICE
                continue

            # Step 8: Check for location entities
            if token_stripped in self.location_list:
                labels.append('B-LOC')  # Label as B-LOC
                continue
            
            # Step 9: Check for product entities
            if token_stripped in self.product_keywords:
                labels.append('B-PROD')  # Label as B-PROD
                continue

            # Step 10: Default case for tokens that are not part of any entities
            labels.append("O")  # Non-entity words

        return list(zip(tokens, labels))  # Return token-label pairs

    def label_dataframe(self, df, token_column):
        """
        Label tokens for each message in a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the tokenized text.
        token_column : str
            The column name in the DataFrame where tokenized Amharic text is stored.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame with tokens and their corresponding NER labels.
        """
        df['Labeled'] = df[token_column].apply(self.label_tokens)
        return df
    
    def save_conll_format(self, labeled_data, file_path):
        """
        Save the labeled data in CoNLL format.

        Parameters:
        -----------
        labeled_data : pandas.DataFrame
            The DataFrame containing token-label pairs.
        file_path : str
            The path to the file where the CoNLL format will be saved.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            for _, row in labeled_data.iterrows():
                for token, label in row['Labeled']:
                    f.write(f"{token} {label}\n")
                f.write("\n")  # Blank line between sentences/messages