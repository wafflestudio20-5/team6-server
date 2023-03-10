<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wafflestudio/snutt-ios">
    <img src="https://user-images.githubusercontent.com/102639700/216500052-d46faea8-8b54-4553-9e9d-c3c994aa3774.PNG" alt="Logo" width="150" height="160" style="padding-bottom:20pt">
  </a>
  <h3 align="center" style="font-size:150%">ð§ Waffle mate ð§</h3>
  <p align="center">
 //&nbsp&nbsp&nbsp&nbspì¼ì &ì¼ê¸° ê³µì ë¥¼ íµí í¨ê³¼ì ì¸ ì¼ì ê´ë¦¬ë¥¼ ê²½ííì¸ì&nbsp&nbsp&nbsp&nbsp// </br></br>

 <strong>Waffle mate REST API Server</strong>

ë³¸ íë¡ì í¸ë [todo mate](https://www.todomate.net/) ì íë¦¬ì¼ì´ìì í´ë¡  ì½ë©ìëë¤. </br>ì£¼ì ê¸°ë¥ì¼ë¡ë ì¼ì  ê´ë¦¬ì ì¼ê¸° ìì± ë±ì´ ìì¼ë©°, </br>ë¤ë¥¸ ì¬ëì íë¡ì°íê³  ëê¸ì ìì±íë ë± ë¤ë¥¸ ì ì ìì ìíµ ëí ê°ë¥í©ëë¤.
</br></br>
## âï¸ Software Stack âï¸
### < Requirements & Environments >

<img src="https://img.shields.io/badge/Python-3776AB??style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.8-3776AB"></br>
<img src="https://img.shields.io/badge/Django-092E20??style=flat&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/version-3.2.16-092E20"></br>
<img src="https://img.shields.io/badge/MySQL-4479A1??style=flat&logo=MySQL&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon EC2-FF9900??style=flat&logo=Amazonec2&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon RDS-527FFF??style=flat&logo=Amazonrds&logoColor=white"/>
<img src="https://img.shields.io/badge/Amazon S3-569A31??style=flat&logo=AmazonS3&logoColor=white"/></br>
<img src="https://img.shields.io/badge/NGINX-009639??style=flat&logo=NGINX&logoColor=white"/>
<img src="https://img.shields.io/badge/Gunicorn-499848??style=flat&logo=Gunicorn&logoColor=white"/></br>
Platfrom : Linux/UNIX (AWS Linux 2 Free-tier) </br>
 Database : AWS RDS / MySQL / db.t3.micro </br>
  </p> 
</div>
</br>

## ð Installation
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

## ð¥ Details
<p>
<h style="font-size:120%"><strong>1. Diary</strong></h>

- ë ì§ / ì ì  ë³ë¡ <strong>ì¼ê¸° CRUD</strong>
- ì¼ê¸° ì¡°íì <strong>follow authorization</strong> ì¤ì 
- ê° ì¼ê¸°ì ëê¸ ë¬ê¸° ê°ë¥
</p>

<p>
<h style="font-size:120%"><strong>2. Task</strong></h>

- ë ì§ / ì ì  ë³ë¡ <strong>í  ì¼ CRUD</strong>
- ì±ì·¨ ì¬ë¶ / ë¯¸ë£¨ê¸° ê¸°ë¥ ì¶ê°
</p>

<p>
<h style="font-size:120%"><strong>3. Search & Follow</strong></h>

- ì´ë©ì¼ì íµí´ <strong>ì ì  ê²ì</strong> ê°ë¥
- <strong>íë¡ì° / ì°¨ë¨ ê¸°ë¥</strong> ì¶ê°

</p>

<p>
<h style="font-size:120%"><strong>4. Comment</strong></h>

- ì¼ê¸°ì <strong>ëê¸ CRUD</strong>
- ëê¸ì ë¬ ë <strong>follow authorization</strong> ì¤ì 
</p>

<p>
<h style="font-size:120%"><strong>5. Account</strong></h>

- <strong>ì ì  ì ë³´ CRUD</strong>
- <strong>íìê°ì / ë¡ê·¸ì¸ / ìì ë¡ê·¸ì¸</strong> (êµ¬ê¸ & ì¹´ì¹´ì¤)
- ìì ê³ì  ì°ë
- ì¸ì¦ë²í¸ ì¬ì ì¡ ë° ë¶ê°ê¸°ë¥
</p>

</br>

### âï¸ Note
* ë³¸ íë¡ì í¸ë Django REST frameworkì ê¸°ë°í REST API ìë²ë¡, ë³ëì íë¡ í¸ìë í´ë¼ì´ì¸í¸ê° íìí©ëë¤.
* êµ¬ê¸ê³¼ ì¹´ì¹´ì¤í¡ ë¡ê·¸ì¸ì ì§ìíë©°, ì´ë¥¼ ìí´ìë êµ¬ê¸ í´ë¼ì°ë íë«í¼ê³¼ ì¹´ì¹´ì¤ Developersìì ìì ì íë¡ì í¸ë¥¼ ë°ë¡ ë±ë¡í´ì¼ í©ëë¤. 
* ë°ì´í°ë² ì´ì¤ë¡ë MySQLì ì¬ì©íê³  ììµëë¤.
* ìë²ë Amazon EC2/Gunicorn/NGINXë¥¼ íµí´ í¸ì¤ííê³  ììµëë¤.
* Amazon S3ì ì¬ì©íì¬ ì´ë¯¸ì§ë¥¼ ê´ë¦¬íê¸° ìí´ìë ë³ëì ì¤ì ì´ íìí©ëë¤.

</br>

## â¨ Contributing
[Pull Request](https://github.com/wafflestudio20-5/team6-server/pulls)ë ì¸ì ë íììëë¤!  
ìë¹ì¤ ê°ì ì ì´ë ë²ê·¸ë [Issue](https://github.com/wafflestudio20-5/team6-server/issues)ë¥¼ ìì ë¡­ê² ì´ì©í´ ì£¼ì¸ì!

### ð Contributors
* [@kjae0](https://github.com/kjae0)
* [@mathema123](https://github.com/mathema123)
* [@sungsung718](https://github.com/sungsung718)

</br>

## ð License
MIT License