# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2023-05-14

### Added

- User can see sources that are used to generate the response
- User can follow the relevant links based on which the response was generated

## [0.0.1] - 2023-05-11

First version to deploy on Streamlit Share.

### Added

- Initial description of the project in `README.md`
- Initial list of user stories in `STORIES.md`
- `Makefile`
- `requirements.txt` generated with `pip-tools` from `requirements.in`
- `CHANGELOG.md`
- `texts/` folder with texts to use for the app
- `data/` folder where the embeddings and cached questions are stored
- `src/` folder with code, especially:
  - `src/create_embeddings.py` to create embeddings for the texts
  - `src/app.py` with a basic Streamlit app

[0.0.2]: https://github.com/dudarev/ask-my-texts/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/dudarev/ask-my-texts/releases/tag/v0.0.1
