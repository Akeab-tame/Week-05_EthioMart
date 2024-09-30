# EthioMart Telegram Data Ingestion and Preprocessing System
This project is designed to ingest and preprocess messages (text, images, and documents) from multiple Ethiopian-based Telegram e-commerce channels. The data is prepared for further processing, including entity extraction, to support tasks like product, price, and location identification.

# Project Structure
```bash
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows
│       ├── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md
```

# Features
**Telegram Scraping:** Fetch real-time messages from specified Ethiopian e-commerce Telegram channels.
**Data Preprocessing:**
- Tokenization and normalization of Amharic text.
- Separation of metadata (sender, timestamp) from content.
- Handling of Amharic-specific linguistic features.
- Structuring of messages for easy access and further analysis.
**CoNLL Labeling:** A subset of the dataset is labeled in CoNLL format to identify entities such as products, prices, and locations.

# Installation
**Step 1: Clone the Repositor**
```bash
git clone https://github.com/Akeab-tame/Week-05_EthioMart.git
cd ethioMart-data-ingestion
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```
**Step 3: Set Up Telegram API Credentials**
Obtain your Telegram API ID and API Hash from my.telegram.org.
Set up a .env file in the project directory with the following content:
```bash
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=your_phone_number  # If using a phone number for authentication
BOT_TOKEN=your_bot_token        # If using a bot token for authentication
```
**Step 4: Running the Data Ingestion Script**
Run the script to fetch messages from the specified Telegram channels:

```bash
python data_ingestion.py
```
This will start collecting messages (text, images, documents) in real-time.

**Step 5: Running Data Preprocessing**
After data ingestion, preprocess the data using the preprocessing script:

```bash
python data_preprocessing.py
```
This script will:

- Tokenize and normalize Amharic text.
- Handle Amharic-specific linguistic features.
- Clean and structure the data for analysis.
**Step 6: Labeling Data in CoNLL Format**
To label a subset of the data for Named Entity Recognition (NER) tasks, run:

```bash
python conll_labeling.py
```
This script will output a plain text file in CoNLL format where entities like products, prices, and locations are labeled.

**Usage**
- Data Collection: The system connects to the Telegram channels and continuously ingests data.
- Data Preprocessing: The collected data is cleaned and prepared for further analysis.
- Entity Labeling: The data is labeled for product, price, and location extraction in Amharic text.
Example Output (CoNLL Format)
```bash
ዋጋ    B-PRICE
1000   I-PRICE
ብር    I-PRICE
ቢቢ    B-Product
አዲስ  B-LOC
አበባ  I-LOC
```
# Contributing
Fork the repository.
Create your feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.

