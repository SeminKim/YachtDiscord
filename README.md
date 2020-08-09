# YachtDiscord
최근 인기를 얻고있는 Yacht Dice 게임을 디스코드 봇으로 구현하는 프로젝트입니다.
출석체크를 통해 점수를 쌓는 날갱봇(https://github.com/3-24/nalgang)과 연동하여 점수를 걸고 게임할 수 있습니다.

# 현재 상태
아직 미완성인 프로젝트입니다. 핵심 기능은 대략 구현되어 있으나, 날갱봇과의 연동성은 아직 시험되지 않았습니다.

# 초기 작업
날갱봇이 사용하는 DB 경로를 nalgang_ext의 db_path에 설정하여야 합니다.(기본은 YachtDiscord 폴더와 나란히 nalgang-master 폴더가 있는 경우)
Discord Developer Portal (https://discord.com/developers/applications)에서 봇을 생성하여, token값을 data/token.txt에 넣어야 합니다.

# 게임 규칙
게임 규칙은 Clubhouse Games: 51 Worldwide Classics 의 Yacht Dice와 동일합니다.
