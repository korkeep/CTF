## web-misconf-1

> 문제 URL: https://dreamhack.io/wargame/challenges/45  
> 기본 설정을 사용한 서비스입니다. 로그인한 후 Organization에 플래그를 설정해 놓았습니다.

### Solve

1. `defaults.ini`파일 내용을 확인하여 admin 계정으로 로그인

```bash
#################################### Security ############################
[security]
# disable creation of admin user on first start of grafana
disable_initial_admin_creation = false

# default admin user, created on startup
admin_user = admin

# default admin password, can be changed before first start of grafana, or in profile settings
admin_password = admin
```

2. `http://host1.dreamhack.games:22142/admin/settings`에서 `org_name` 값 확인

```bash
DH{default_account_is very dangerous}
```
