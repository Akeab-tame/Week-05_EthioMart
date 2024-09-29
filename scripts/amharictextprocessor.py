import re
import numpy as np
import pandas as pd

class AmharicTextPreprocessor:
    def __init__(self):
        # Allow Amharic letters, numbers, spaces, and the '/' character
        self.allowed_characters = re.compile(r'[^ሀ-ፐ0-9\s/]')  # Exclude English letters
        # self.price_pattern = re.compile(
        #     r'(መሸጫ\s*(?:[።፡.-]?\s*)?ዋጋ\s*\d+ብር|መሸጫ\s*\d+\s*ብር|መሸጫ\s*ብር\s*\d+|መሸጫ\s*\d+|(ዋጋ|በ)\s*\d+\s*ብር|\d+\s*ብር|(?:\d+ብር))'
        # )

    def normalize_text(self, text):
        if not isinstance(text, str) or not text.strip():
            return np.nan

        # Remove unwanted characters but keep specific patterns intact
        text = re.sub(self.allowed_characters, '', text)  # Remove unwanted characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces and newlines

        return text

    def preprocess(self, text):
        normalized_text = self.normalize_text(text)
        return normalized_text if normalized_text and normalized_text != '' else np.nan

    def preprocess_dataframe(self, df, text_column):
        # Apply preprocessing to the specified text column only
        df['preprocessed_message'] = df[text_column].apply(self.preprocess)
        return df