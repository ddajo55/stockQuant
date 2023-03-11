import slack_sdk
import time

slack_token = 'xoxb-4943432272401-4934898376098-bVcLFCxUtOC4xgNhiNpu9T3A'
client = slack_sdk.WebClient(token=slack_token)

# 메시지 보내기
client.chat_postMessage(channel='#stock_quant', text='hi, dododang')

# https://dododanghq.slack.com/archives/C04TCLFLMEX
# 채널 아이디를 알아내서
channel_id = client.conversations_history(channel='C04TCLFLMEX')
# 해당 채널에 채팅내역을 가져옴
messages = channel_id.data['messages']

# ts[0]는 가장 최근 메시지
message_ts = messages[0]['ts']

# 가장 최근 메시지에 답글 달기
client.chat_postMessage(channel='#stock_quant', text='댓글을 입력합니다', thread_ts=message_ts)

# 현재 시각을 출력
txt = time.strftime('%Y-%m-%d %H:%M:%S')
client.chat_postMessage(channel='#stock_quant', text=txt)