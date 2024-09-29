import os
import csv
from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment variables
load_dotenv()

class TelegramChannelScraper:
    """
    A class to scrape messages and media from specified Telegram channels and store them in a CSV file.

    Attributes:
    -----------
    api_id : int
        Telegram API ID for authentication.
    api_hash : str
        Telegram API Hash for authentication.
    session_name : str
        Session name for the Telegram client.
    media_dir : str
        Directory to store downloaded media files.
    csv_file : str
        Name of the CSV file to store scraped data.
    channels : list
        List of Telegram channel usernames to scrape.
    """

    def __init__(self, api_id, api_hash, session_name, media_dir='../data/photos', csv_file='../data/telegram_data.csv', channels=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.media_dir = media_dir
        self.csv_file = csv_file
        self.channels = channels or []

        # Create media directory
        os.makedirs(self.media_dir, exist_ok=True)

    async def scrape_channel(self, client, channel_username, writer):
        """
        Scrapes all messages from a single channel and writes to the CSV file.

        Parameters:
        ----------
        client : TelegramClient
            The authenticated Telegram client.
        channel_username : str
            The username of the channel to scrape.
        writer : csv.writer
            CSV writer object to write data to the CSV file.
        """
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title

        print(f"Scraping all history from {channel_username}...")  # Message indicating scraping has started

        # Scraping all messages from the channel (set limit=None)
        async for message in client.iter_messages(entity, limit=None):
            media_path = await self.download_media(client, message, channel_username)
            
            # Write the data to the CSV file
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

        print(f"Successfully scraped all history from {channel_username}")  # Success message

   
    async def download_media(self, client, message, channel_username):
        """
        Downloads media from the message if available.

        Parameters:
        ----------
        client : TelegramClient
            The authenticated Telegram client.
        message : telethon.tl.types.Message
            The message object containing potential media.
        channel_username : str
            The username of the channel.

        Returns:
        -------
        str or None
            The path of the downloaded media file, or None if no media is present.
        """
        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(self.media_dir, filename)
            await client.download_media(message.media, media_path)
            return media_path
        return None

    async def run(self):
        """
        Runs the scraping process, initializing the Telegram client and processing each channel.
        """
        print("Starting the full history scraping process...")  # Message indicating the start of full scraping
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

                for channel in self.channels:
                    await self.scrape_channel(client, channel, writer)

if __name__ == "__main__":
    # Get credentials from .env
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')

    # Validate API credentials
    if not api_id or not api_hash:
        raise ValueError("Your API ID or Hash cannot be empty or None. Please check your .env file.")

    # List of channels to scrape
    channels_to_scrape = [
        '@helloomarketethiopia',
        #'@AnchorRealEstateMarketing',
        # Add more channels as needed
    ]

    # Initialize the scraper
    scraper = TelegramChannelScraper(api_id=api_id, api_hash=api_hash, session_name='../data/scraping_session', channels=channels_to_scrape)

    # Start the scraping process
    import asyncio
    asyncio.run(scraper.run())