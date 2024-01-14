import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
## python-telegram-bot version 12.8

class Music:
    def __init__(self, kind, artistName, collectionName, trackName, 
                 artistViewUrl, collectionViewUrl, trackViewUrl, artworkUrl100, releaseDate, primaryGenreName):
        self.kind = kind
        self.artistName = artistName
        self.collectionName = collectionName
        self.trackName = trackName
        self.artistViewUrl = artistViewUrl
        self.collectionViewUrl = collectionViewUrl
        self.trackViewUrl = trackViewUrl
        self.artworkUrl100 = artworkUrl100
        self.releaseDate = releaseDate
        self.primaryGenreName = primaryGenreName

    # def __str__(self) -> str:
    #     str1 = f"kind: {self.kind}, artistName: {self.artistName}, \ncollectionName: {self.collectionName}, "
    #     str2 = f"trackName: {self.trackName}, \nreleaseDate: {self.releaseDate}, primaryGenreName: {self.primaryGenreName}"
    #     return  str1 + str2 
                

class MusicFetcher():
    API_URL = "https://itunes.apple.com/search"

    @staticmethod
    def fetch_music(term):
        params = {'entity': 'song',
                  'term' : term,
                  'limit': 7}
        response = requests.get(MusicFetcher.API_URL , params=params)
        if response.status_code == 200:
            music_items = response.json().get('results')
        else:
            print("Cannot connect to the API")
            music_items = []
        
        musics = []
        for item in music_items:
            music_obj = Music(item.get('kind', ''), item.get('artistName', ''), item.get('collectionName', ''), item.get('trackName', ''), 
                              item.get('artistViewUrl', ''), item.get('collectionViewUrl', ''), item.get('trackViewUrl', ''), 
                              item.get('artworkUrl100', ''), item.get('releaseDate', ''), item.get('primaryGenreName', ''))
            musics.append(music_obj)
        
        return musics


class TelegramBotHandler:
    def __init__(self):
        self.music_fetcher = MusicFetcher()

    def start(self, update, context):
        update.message.reply_text("Just send me a song name and I will find music for you!")

    def handle_message(self, update, context):
        user_input = update.message.text
        recommendations = self.music_fetcher.fetch_music(user_input)
        for music in recommendations:
            response = (f"\n\n*Artist:* [{music.artistName}]({music.artistViewUrl})\n"
                        f"*Collection:* [{music.collectionName}]({music.collectionViewUrl})\n"
                        f"*Track:* [{music.trackName}]({music.trackViewUrl})\n"
                        f"*Release Date:* {music.releaseDate})\n"
                        f"*Genre:* {music.primaryGenreName}\n")
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=music.artworkUrl100, caption=response, parse_mode='Markdown')

        if not recommendations:
            update.message.reply_text("No musics found.") 


def main():
    print("Starting bot...")
    TOKEN = ''
    updater = Updater(TOKEN, use_context=True) 
    dp = updater.dispatcher
    bot_handler = TelegramBotHandler()
    ## Command Handlers:
    dp.add_handler(CommandHandler("start", bot_handler.start))
    ## Message Handlers:
    dp.add_handler(MessageHandler(Filters.text, bot_handler.handle_message))
    print("Polling...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
