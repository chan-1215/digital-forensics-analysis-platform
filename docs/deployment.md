# Deployment Notes

이 프로젝트는 당시 Ubuntu Server 환경에서 Flask 애플리케이션을 Gunicorn으로 실행하고 Nginx를 Reverse Proxy로 앞단에 두는 방식으로 구성했습니다.

## Development

```bash
cd ~/forensics-site
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Gunicorn

```bash
gunicorn --workers 2 --bind unix:/tmp/forensics-site.sock app:app
```

## systemd example

```ini
[Unit]
Description=Digital Forensics Flask App
After=network.target

[Service]
User=master
WorkingDirectory=/home/master/forensics-site
Environment="PATH=/home/master/forensics-site/venv/bin"
ExecStart=/home/master/forensics-site/venv/bin/gunicorn --workers 2 --bind unix:/tmp/forensics-site.sock app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Nginx example

```nginx
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/forensics-site.sock;
    }
}
```

## Useful commands

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now forensics-site
sudo systemctl status forensics-site
sudo nginx -t
sudo systemctl restart nginx
journalctl -u forensics-site -n 100 --no-pager
```

> 서비스명과 경로는 당시 환경 기록을 바탕으로 정리한 재현용 예시입니다. 실제 서버에 남아 있던 최종 설정 파일 원문이 모두 보존된 것은 아니므로, 현재 저장소에서는 실행 가능한 형태로 정리했습니다.
