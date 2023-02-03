<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wafflestudio/snutt-ios">
    <img src="https://user-images.githubusercontent.com/102639700/216500052-d46faea8-8b54-4553-9e9d-c3c994aa3774.PNG" alt="Logo" width="150" height="160" style="padding-bottom:20pt">
  </a>
  <h3 align="center" style="font-size:150%">🧇 Waffle mate 🧇</h3>
  <p align="center">
 //&nbsp&nbsp&nbsp&nbsp일정&일기 공유를 통한 효과적인 일정관리를 경험하세요&nbsp&nbsp&nbsp&nbsp// </br></br>

 <strong>Waffle mate REST API Server</strong>

본 프로젝트는 [todo mate](https://www.todomate.net/) 애플리케이션의 클론 코딩입니다. </br>주요 기능으로는 일정 관리와 일기 작성 등이 있으며, </br>다른 사람을 팔로우하고 댓글을 작성하는 등 다른 유저와의 소통 또한 가능합니다.
</br></br></br>
## ⚒️ Software Stack ⚒️
### < Requirements & Environments >

<img src="https://img.shields.io/badge/Python-3776AB??style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.8-3776AB"></br>
<img src="https://img.shields.io/badge/Django-092E20??style=flat&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.2.16-092E20"></br>
<img src="https://img.shields.io/badge/MySQL-4479A1??style=flat&logo=MySQL&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon EC2-FF9900??style=flat&logo=Amazonec2&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon RDS-527FFF??style=flat&logo=Amazonrds&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon S3-569A31??style=flat&logo=AmazonS3&logoColor=white"/></br>
  Platfrom : Linux/UNIX (AWS Linux 2 Free-tier) </br>
  Database : AWS RDS / MySQL / db.t3.micro </br>

// &#160; &#160; &#160; &#160; 기타 사항은 [requirements.txt](https://github.com/wafflestudio20-5/team6-server/blob/develop/toDoMateProject/requirements.txt) 참고  &#160; &#160; &#160; &#160;//

  </p> 
</div>
</br></br>

## 🚀 Installation
  ```
  / git clone /
  $ git clone --branch develop https://github.com/wafflestudio20-5/team6-server.git

  / install requirements /
  $ pip install -r requirements.txt

  / migration /
  $ python manage.py makemigrations
  $ python manage.py migrate

  / runserver /
  $ python manage.py runserver ...
  ```


</br>

## 🔥 Details
</br>
<p>
<h style="font-size:120%"><strong>1. Diary</strong></h>

- 날짜 / 유저 별로 <strong>일기 CRUD</strong>
- 일기 조회에 <strong>follow authorization</strong> 설정
- 각 일기에 댓글 달기 가능
</p>

<p>
<h style="font-size:120%"><strong>2. Task</strong></h>

- 날짜 / 유저 별로 <strong>할 일 CRUD</strong>
- 성취 여부 / 미루기 기능 추가
</p>

<p>
<h style="font-size:120%"><strong>3. Search & Follow</strong></h>

- 이메일을 통해 <strong>유저 검색</strong> 가능
- <strong>팔로우 / 차단 기능</strong> 추가

</p>

<p>
<h style="font-size:120%"><strong>4. Comment</strong></h>

- 일기에 <strong>댓글 CRUD</strong>
- 댓글을 달 때 <strong>follow authorization</strong> 설정
</p>

<p>
<h style="font-size:120%"><strong>5. Account</strong></h>

- <strong>유저 정보 CRUD</strong>
- <strong>회원가입 / 로그인 / 소셜 로그인</strong> (구글 & 카카오)
- 소셜 계정 연동
- 인증번호 재전송 및 부가기능
</p>

</br>

### ✔️ Note
* 본 프로젝트는 Django REST framework을 기반한 REST API 서버로, 별도의 프론트엔드 클라이언트가 필요합니다.
* 구글과 카카오톡 로그인을 지원하며, 이를 위해서는 구글 클라우드 플랫폼과 카카오 Developers에서 자신의 프로젝트를 따로 등록해야 합니다. 
* 데이터베이스로는 MySQL을 사용하고 있습니다.
* 서버는 Amazon EC2을 통해 호스팅하고 있습니다.
* Amazon S3을 사용하여 이미지를 관리하기 위해서는 별도의 설정이 필요합니다.

</br>

## ✨ Contributing
서비스 개선을 위한 제안이 있으시다면, [Issue](https://github.com/wafflestudio20-5/team6-server/issues) 또는 [Pull Request](https://github.com/wafflestudio20-5/team6-server/pulls)을 자유롭게 이용해 주세요!

### 😊 Contributors
* [@kjae0](https://github.com/kjae0)
* [@mathema123](https://github.com/mathema123)
* [@sungsung718](https://github.com/sungsung718)

</br>

## 📄 License
MIT License