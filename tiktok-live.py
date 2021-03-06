import pandas as pd
import atexit
import signal
import sys

from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent
 
listComment = [];

client: TikTokLiveClient = TikTokLiveClient(
    unique_id="trangdinhgiay", **(
        {
            "enable_extended_gift_info": True
        }
    )
)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connect to Room Id:", client.room_id)

@client.on("comment")
async def on_connect(event: CommentEvent):
    print(f"{event.user.uniqueId} -> {event.comment}")
    listComment.append({'username': event.user.uniqueId, 'Comment': event.comment})
    # df = pd.DataFrame({'Username':[event.user.uniqueId],'Comment':[event.comment]})
    # df.to_excel('tikTokLiveData.xlsx', header=None, index=True, encoding='utf-8')

@client.on("gift")
async def on_gift(event: GiftEvent):
    print(f"{event.user.uniqueId} sent a gift")
    # print(f"{event.user.uniqueId} sent a {event.gift.gift_id}!")
    # for giftInfo in client.available_gifts:
    #     if giftInfo["id"] == event.gift.gift_id:
    #         print(f"Name: {giftInfo['name']} Image: {giftInfo['image']['url_list'][0]} Diamond Amount: {giftInfo['diamond_count']}")

@client.on("like")
async def on_like(event: LikeEvent):
    print(f"{event.user.uniqueId} has liked the stream {event.likeCount} time, there is now {event.totalLikeCount} total likes!")

@client.on("follow")
async def on_follow(event: FollowEvent):
    print(f"{event.user.uniqueId} followed the streamer")

@client.on("share")
async def on_share(event: ShareEvent):
    print(f"{event.user.uniqueId} shared the stream!")

@client.on("viewer_count_update")
async def on_connect(event: ViewerCountUpdateEvent):
    print("Received a new vewer count:", event.viewerCount)

def exit_handler():
    print('App is ending, going to save excel:' + listComment)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Going to save excel: ')
    df = pd.DataFrame(listComment)
    df.to_excel('tikTokLiveData.xlsx', header=None, index=True, encoding='utf-8')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    # Run the client and block the main thread
    # Await client.start() to run non-blocking

    client.run()