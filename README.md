# YachtDiscord
Yacht Dice 게임을 디스코드 봇으로 구현하는 프로젝트입니다.
출석체크를 통해 점수를 쌓는 [날갱봇](https://github.com/3-24/nalgang)과 연동하여 점수를 걸고 게임할 수 있습니다.  
discord.py를 기반으로 작동합니다.

# 게임 규칙
게임 규칙은 Clubhouse Games: 51 Worldwide Classics의 Yacht Dice와 동일합니다. [이곳](https://namu.wiki/w/%EC%9A%94%ED%8A%B8(%EA%B2%8C%EC%9E%84))을 참고해주세요.

# 현재 상태
모든 기능이 구현되었으나, 봇을 구동시키고 있지는 않습니다.
사용을 위해서는 아래를 참고하여 직접 세팅하여야 합니다.

# 세팅 방법
- 먼저 [Discord Developer Portal](https://discord.com/developers/applications)에서 새 봇을 생성합니다.
- 생성된 봇의 토큰 값을 ```data/token.txt```에 넣습니다.
- 사용할 채널의 channel id를 확인하여 ```config.py```의 ```CHANNEL_WHITELIST```에 넣습니다.
(많은 메시지를 전송하기 때문에 기본적으로 whitelist된 채널에서만 메시지를 보내도록 되어있습니다.)
- ```ext_nalgang.py```를 필요에 따라 수정합니다. 날갱봇을 사용한다면 날갱봇 api url을 ```config.py```에 넣어야하며, 포인트 기능 없이 사용하려면 ```ext_nalgang.py```의 함수들을 적절히 비활성화시키면 됩니다. 
