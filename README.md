# YachtDiscord
최근 인기를 얻고있는 Yacht Dice 게임을 디스코드 봇으로 구현하는 프로젝트입니다.
출석체크를 통해 점수를 쌓는 날갱봇(https://github.com/3-24/nalgang)과 연동하여 점수를 걸고 게임할 수 있습니다.  
Python으로 작성되었습니다.

# 현재 상태
모두 구현되어 정상 작동합니다. 만약 날갱봇이 아닌 다른 점수 관리 봇을 사용한다면, ```ext_nalgang.py```
를 수정하면 됩니다.

# 초기 작업
Discord Developer Portal (https://discord.com/developers/applications)에서 봇을 생성하여, token값을 data/token.txt에 넣어야 합니다.  
또한 많은 메시지를 전송하기 때문에 기본적으로 whitelist된 채널에서만 메시지를 보내도록 되어있습니다.  
이를 위해 channel id를 data/channel.txt에 넣어주세요.

# 게임 규칙
게임 규칙은 Clubhouse Games: 51 Worldwide Classics 의 Yacht Dice와 동일합니다.
 
