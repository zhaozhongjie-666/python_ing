                               flask + gunicon+nginx+supervisor 配置


pip install virtualenv

搭建虚拟环境

 virtualenv /home/wealink/projects/project

激活虚拟环境

source /home/wealink/projects/project/bin/activate


安装 Flask

pip install Flask

在/projects/project 目录下新建一个 project.py，内容是:

from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():

    return "Hello world!"

if __name__ == '__main__':

    app.run()



sudo apt-get install apache2-utils 

实验环境下测试

 ab -c 10 -n 10000 http://127.0.0.1:1234/

开发模式下测试

ab -c 10 -n 1000 http://127.0.0.1:5000/

（使用gunicorn测试）

pip install gunicorn

一次运行4个进程，w 表示开启多少个 worker，-b 表示 gunicorn 开发的访问地址

/home/wealink/projects/project/bin/python    /home/wealink/projects/project/bin/gunicorn -b 127.0.0.1:1234 project:app -w 4

project:app  中project 当前运行module名（文件名），app创建的Flask 对象


安装 supervisor

apt-get install supervisor

apt-get install python-reconfigure  -y

sudo supervisorctl -c /etc/supervisor/supervisord.conf restart all



vim /etc/supervisor/conf.d/test.conf 

在里面写入：（1234 可以更改为你喜欢的端口，只要和其他的端口不重合就行。root 也可改为其他用户）

[program:project]

command = /home/wealink/projects/project/bin/gunicorn -b 127.0.0.1:1234 project:app -w4

directory = /home/wealink/projects/project/

user = root

autostart = true

autorestart = true

stderr_logfile = /home/wealink/projects/project/logs/stderr.log

stdout_logfile = /home/wealink/projects/project/logs/stdout.log


新建 logs 文件夹：

mkdir /home/wealink/projects/project/logs



apt-get install nginx

配置nginx

vim /etc/nginx/conf.d/project.conf

server {
    listen 80;
    server_name  www.123.com;

    access_log /home/wealink/projects/project/logs/access.log;
    error_log /home/wealink/projects/project/logs/error.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:1234;
        }
    }

    location ~.*(js|css|png|gif|jpg|mp3|ogg)$ {
        root/home/wealink/projects/project/;
    }
}

检查nginx是否正确

sudo nginx -t


vim /etc/hosts

127.0.0.l  www.123.com
 

sudo apt-get  install openssl

使用OpenSSL生成证书

生成RSA密钥的方法

 openssl genrsa -des3 -out server.key 2048 
 
这个命令会生成一个2048位的密钥，同时有一个des3方法加密的密码

生成证书请求文件

openssl req -new -key server.key -out server.csr

用之前生成的秘钥 server.ky文件生成 server.csr (证书请求文件)

在加载SSL支持的Nginx并使用上述私钥时除去必须的口令：

cp server.key server.key.org
 
openssl rsa -in server.key.org -out server.key 

标记证书使用上述私钥和CSR：

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt



配置https
vim /etc/nginx/conf.d/project.conf
server {
    listen 443;
    root /home/wealink/projects/project;
    server_name mail.123.com;
    ssl on;
    ssl_certificate /home/wealink/projects/project/ssl/server.crt;
    ssl_certificate_key /home/wealink/projects/project/ssl/server.key;


    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:1234;
            break;
        }
    }

}


















