# STATBOT-API

Statbot-API is an API to query SWISS OGD via NL questions.

## Installation

Install RUST
```bash
curl https://sh.rustup.rs -sSf | sh
```

Install pyenv dependencies
```bash
sudo apt update
sudo apt install \
    build-essential \
    curl \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev
```

Install pyenv
```bash
curl https://pyenv.run | bash
```

Install correct python version
```bash
pyenv install 3.12.3
pyenv local 3.12.3
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

```bash
pip install -r docker/requirements.txt
```
create `.env` file and set:
    `OPENAI_API_KEY=[OPENAI_API_KEY]`
## Usage

```bash
python app/main.py
```

## Docs:

Open address `http://127.0.0.1:8000/docs` to read the API doc.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)