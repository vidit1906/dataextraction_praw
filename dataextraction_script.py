import praw
import json
import sys
import warnings
warnings.filterwarnings("ignore")
#This part has the details of Reddit App created for the data extraction. Name of the user: u/irproject
reddit = praw.Reddit(user_agent="Comment Extraction (by /u/irproject)",
                     client_id="kDrP4C1vGpKvET4kprMexw", client_secret="VWU0iNZSNFv3Hho_kDuQxzHNCiHsmQ")
#This part has a list of subreddits which are related to cryptocurrencies
#Data like the subreddit name, post title, post body, comments and subcomments will be retrieved
crypto_subreddits = [
    "Bitcoin",
    "Ethereum",
    "CryptoCurrency",
    "Ripple",
    "Litecoin",
    "BitcoinMarkets",
    "CryptoMarkets",
    "CryptoCurrencies",
    "Altcoin",
    "NEO",
    "Bitcoincash",
    "Cardano",
    "Stellar",
    "Tronix",
    "Dashpay",
    "Iota",
    "EthereumClassic",
    "NEM",
    "Vechain",
    "Monero",
    "QTUM",
    "OMGnetwork",
    "ICON",
    "EOS",
    "Zcash",
    "BitcoinPrivate",
    "BinanceCoin",
    "Dogecoin",
    "BytecoinBCN",
    "BitcoinCashSV",
    "Decred",
    "WavesPlatform",
    "0xProject",
    "Electroneum",
    "BitcoinGoldHQ",
    "PIVX",
    "BasicAttentionToken",
    "Steemit",
    "Augur",
    "ArkEcosystem",
    "Siacoin",
    "TrueUSD",
    "NanoCurrency",
    "HoloChain",
    "CryptoCom",
    "Hyperledger",
    "GolemProject",
    "Chainlink",
    "StratisPlatform",
    "KyberNetwork",
    "PowerLedger",
    "Loopring",
    "StatusIM",
    "CivicPlatform",
    "Particl",
    "EnjinCoin",
    "Aeternity",
    "Ardor",
    "MakerDAO",
    "DigiByte",
    "Cortex_Official",
    "Waltonchain",
    "Omise_go",
    "QASH",
    "PolymathNetwork",
    "BATProject",
    "GnosisPM",
    "Aeternity",
    "StratisPlatform",
    "0xProject",
    "AionNetwork",
    "Kucoin",
    "GolemTrader",
    "GolemTrader",
    "CryptoCurrencyTrading",
    "BitcoinMining",
    "EthereumMining",
    "LitecoinMining",
    "MiningPoolHub",
    "Mining",
    "MoneroMining",
    "MiningRig",
    "MiningPool",
    "NiceHash",
    "ZcashMining",
    "BitcoinBeginners",
    "BitcoinHelp",
    "EthereumBeginners",
    "AltcoinBeginners",
    "CryptoCurrencies",
    "NEOnewstoday",
    "DashNews",
    "IOTAmarkets",
    "EthereumClassic",
    "LitecoinMarkets",
    "TronixTrading",
    "EOSDev",
    "QtumTrader",
    "BitcoinPrivate",
    "BitcoinMarketsBeta"
]
#File to be created where all the scraped data will be stored
json_filename = "reddit_comments_duplicates.json"
#A function is defined where the data to be scraped is retrieved and stored in a dictionary called data

def data_scrape(comments, post_title, post_body):
    with open(json_filename, 'a', encoding='utf-8') as jsonfile:
        for comment in comments:
            ir_proj_data = {
                'subreddit': comment.subreddit.display_name,
                'post_title': post_title,
                'post_body': post_body,
                'parent_comment_id': comment.parent_id,
                'comment_id': comment.id,
                'author': comment.author.name if comment.author else "[deleted]",
                'body': comment.body
            }
            json.dump(ir_proj_data, jsonfile, ensure_ascii=False)
            jsonfile.write('\n')
    

#This part of the code extracts comments from the post
#the comments are stored in a python list called comments and this also checks if the comment has already been visited by the crawler
def extract_comments(comment, post_title, post_body, visited_comments):
    comments = []
    for reply in comment.replies:
        if reply.id not in visited_comments:  # for loop to check if the comment has been visited
            visited_comments.add(reply.id)  # Once comment is visited, mark it so that crawler doesn't visit it again
            comments.extend(extract_comments(reply, post_title, post_body, visited_comments))
    comments.append(comment)
    return comments

for subreddit_name in crypto_subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Data extraction of r/{subreddit_name}...")
    try:
        #Data extraction limit is set to None so that all the data of a subreddit can be scraped
        #if we want top posts, an approrpiate limit can be set
        for submission in subreddit.top(limit=None):
            post_title = submission.title
            post_body = submission.selftext
            submission.comments.replace_more(limit=None)
            for top_level_comment in submission.comments:
                visited_comments = set()  #Visited comments are stored in a set so that duplicates are avoided.
                comments = extract_comments(top_level_comment, post_title, post_body, visited_comments)
                data_scrape(comments, post_title, post_body)
               
    except Exception as e:
        print("ERROR WHILE FETCHING DATA", e)
