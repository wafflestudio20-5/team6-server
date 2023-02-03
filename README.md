<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wafflestudio/snutt-ios">
    <img src="https://user-images.githubusercontent.com/102639700/216500052-d46faea8-8b54-4553-9e9d-c3c994aa3774.PNG" alt="Logo" width="100" height="110">
  </a>
  <h3 align="center">waffle mate server</h3>
  <p align="center">
  #diary #todo list #SNS
  </p> 
</div>

## Overview
waffle mate REST API Server

본 프로젝트는 [todo mate](https://www.todomate.net/) 애플리케이션의 클론 코딩입니다. 주요 기능으로는 할 일 목록 관리와 일기 작성 등이 있으며, 다른 사람을 팔로우하고 댓글을 작성하는 등 다른 유저와의 소통 또한 가능합니다.

## 개발 환경 (서버 환경)

## Software Stack
### Requirements
* Python==3.8.15
* Django==3.2.16
* MySQL
* Amazon EC2
* Amazon S3
* 기타 사항은 [requirements.txt](https://github.com/wafflestudio20-5/team6-server/blob/develop/toDoMateProject/requirements.txt) 참고
### Note
* 본 프로젝트는 Django REST framework을 기반한 REST API 서버로 별도의 프론트엔드 클라이언트가 필요합니다.
* 구글과 카카오톡 로그인을 지원하며, 이를 위해서는 구글 클라우드 플랫폼과 카카오 Developers에서 자신의 프로젝트를 따로 등록해야 합니다. 
* 데이터베이스로는 MySQL을 사용하고 있습니다.
* 서버는 Amazon EC2을 통해 호스팅하고 있습니다.
* Amazon S3을 사용하여 이미지를 관리하기 위해서는 별도의 설정이 필요합니다.


## Installation

## Detail 
<p>
<h>1. 다이어리</h>


</p>

<p>
<h>2. 할 일 목록</h>


</p>

<p>
<h>3. 팔로우</h>


</p>

<p>
<h>4. 댓글</h>


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