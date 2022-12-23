# team6-server
# 협업 방식
Android팀의 README 파일을 가져왔습니다.

1. team6-android 레포지토리를 fork 한다.
2. fork한 소스코드를 Clone한다.
3. origin/develop branch를 checkout 한다 > 자동으로 local에 develop branch 생성
4. local의 develop branch에서 새로운 기능에 대한 feature branch를 분기한다. (branch 우클릭> New branch from 'develop' 클릭> featrue branch 이름 입력 (예:feature/login)
5. feature branch에서 새로운 기능에 대한 작업을 수행한다. (중간중간 add, commit 수행)
6. 작업이 끝나면 develop branch로 merge 한다.
7. 더이상 필요하지 않은 feature branch는 삭제한다.
8. develop branch에서 origin/develop branch로 작업내용을 push 한다.
9. push한 내용을 pull request로 team6-android 레포에 날린다.