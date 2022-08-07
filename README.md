# Backend Server
### Pré Requisitos
- Python 3.6
```
 sudo apt-get install python3.6 python3-pip
 ```
- virtualenv
```
pip3 install virtualenv
```

- postgresql
```
sudo apt install postgresql postgresql-contrib postgis
```

### Instalação
(Dentro da pastar server/)
Criar ambiente virtual
```
virtualenv -p python3.6 env
```

Ativar ambiente virtual
```
source env/bin/activate
```

Instalar Dependências
```
pip install -r requeriments.txt
```

Executar Migrações
```
python manage.py migrate
```

Executar servidor
```
python manage.py runserver
```


# Frontend
### Pré Requisitos
- Node.js/npm
```
sudo apt-get install nodejs npm
```

### Instalação
(Dentro da Pasta client)
Instalar Dependências
```
npm install
```

Executar cliente:
```
npm run serve
```
