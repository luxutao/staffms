# 员工管理后台
-------------------

## demo
[http://demo.staffms.animekid.cn](http://demo.staffms.animekid.cn)

## 开发环境
+ Python3.6.8

## 部署环境
+ Centos 7
+ nginx 1.12.2
+ MariaDB 10.2.25
+ uwsgi 2.0.17.1

## 模块环境
+ 查看requirements.txt

## 安装方法(此方法默认环境都已安装完成)
1. 导入staffms.sql
   ```bash
   >>> mysql
   >>> source staffms.sql
   ```
2. 配置nginx
   ```bash
    server {
        listen       80;
        server_name  demo.staffms.animekid.cn;

        location /api {
            include        uwsgi_params;
            uwsgi_pass     127.0.0.1:8799;
            uwsgi_param UWSGI_CHDIR  /var/www/staffms;
            uwsgi_param UWSGI_SCRIPT manage:app;
        }   

        # vue编译完成的文件在dist目录下
        location / {                                                                                                                                                         
            root /var/www/staffms/dist;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }   

        location /static {
            root /var/www/staffms/dist/;
        }   
    }
    ```
3. 打开域名进行访问，默认存在的用户名为admin,密码为123456


## API文档  
可以根据路由来查看注释，以后有时间再补全API文档