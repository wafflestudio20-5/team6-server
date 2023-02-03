<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wafflestudio/snutt-ios">
    <img src="https://user-images.githubusercontent.com/102639700/216500052-d46faea8-8b54-4553-9e9d-c3c994aa3774.PNG" alt="Logo" width="150" height="170" style="padding-bottom:20pt">
  </a>
  <h3 align="center" style="font-size:150%">🧇 Waffle mate 🧇</h3>
  <p align="center">
 //&nbsp&nbsp&nbsp&nbsp일정&일기 공유를 통한 효과적인 일정관리를 경험하세요&nbsp&nbsp&nbsp&nbsp// </br></br>

 <strong>Waffle mate REST API Server</strong>

본 프로젝트는 [todo mate](https://www.todomate.net/) 애플리케이션의 클론 코딩입니다. </br>주요 기능으로는 일정 관리와 일기 작성 등이 있으며, </br>다른 사람을 팔로우하고 댓글을 작성하는 등 다른 유저와의 소통 또한 가능합니다.
</br></br></br>
## ⚒️ Software Stack ⚒️
### < Requirements >
</br>
<img src="https://img.shields.io/badge/Python-3776AB??style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.8-3776AB"></br>
<img src="https://img.shields.io/badge/Django-092E20??style=flat&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.2.16-092E20"></br>
<img src="https://img.shields.io/badge/MySQL-4479A1??style=flat&logo=MySQL&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon EC2-FF9900??style=flat&logo=Amazonec2&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon RDS-527FFF??style=flat&logo=Amazonrds&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon S3-569A31??style=flat&logo=AmazonS3&logoColor=white"/></br>

// &#160; &#160; &#160; &#160; 기타 사항은 [requirements.txt](https://github.com/wafflestudio20-5/team6-server/blob/develop/toDoMateProject/requirements.txt) 참고  &#160; &#160; &#160; &#160;//

  </p> 
</div>
</br></br>


## 서버 환경
 * Platfrom : Linux/UNIX (AWS Linux 2 Free-tier)
 * Database : AWS RDS / MySQL / db.t3.micro 


### Note
* 본 프로젝트는 Django REST framework을 기반한 REST API 서버로 별도의 프론트엔드 클라이언트가 필요합니다.
* 구글과 카카오톡 로그인을 지원하며, 이를 위해서는 구글 클라우드 플랫폼과 카카오 Developers에서 자신의 프로젝트를 따로 등록해야 합니다. 
* 데이터베이스로는 MySQL을 사용하고 있습니다.
* 서버는 Amazon EC2을 통해 호스팅하고 있습니다.
* Amazon S3을 사용하여 이미지를 관리하기 위해서는 별도의 설정이 필요합니다.


## Installation
추가 요망

## Detail 
추가 요망
<p>
<h>1. 다이어리</h>

- 날짜별 일기 등록
- 일기 제목 및 내용 수정, 삭제
- 전체 일기 목록, 각 날짜의 일기 조회
- 다른 사람의 일기 조회(팔로우 한정)

</p>

<p>
<h>2. 할 일 목록</h>

- 날짜별 할 일 등록
- 날짜나 내용 변경 및 할 일 삭제
- 할 일 성취 여부 변경
- 할 일 하루 미루기
- 전체 할 일, 각 날짜의 할 일 조회

</p>

<p>
<h>3. 팔로우</h>


</p>

<p>
<h>4. 댓글</h>

- 팔로우 관계인 사람의 일기에 댓글 달기
- 댓글 내용 수정 및 삭제

</p>

<p>
<h>5. 계정</h>

- 회원가입
- 로그인
- 소셜 로그인 (구글, 카카오)
- 소셜 계정 연동
- 비밀번호 초기화 및 재설정
- 인증번호 재전송
- 유저 정보 조회 및 수정
- 회원탈퇴
</p>


## Contributing
서비스 개선을 위한 제안이 있으시다면, [Issue](https://github.com/wafflestudio20-5/team6-server/issues) 또는 [Pull Request](https://github.com/wafflestudio20-5/team6-server/pulls)을 자유롭게 이용해 주세요!

### Contributors
* [@kjae0](https://github.com/kjae0)
* [@mathema123](https://github.com/mathema123)
* [@sungsung718](https://github.com/sungsung718)

## License
MIT