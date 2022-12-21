# PETMOON Back-end

## How to run

1. Install dependencies

```bash
pip install -r requirements/dev.txt # for development
pip install -r requirements/production.txt # for production
pip install -r requirements/test.txt # for test
```

1. Make .env file

    use either prod.env.template or dev.env.template to create .env file

1. Make sure you have Postgredb running

1. enjoy!

## How to update deps

```bash
cd requirements
make update_deps
```
