# HPC and containers for Machine Learning

This book is a guide to get started with High Performance Computer clusters (HPCC) and more particularly [Uninett Sigma2's HPCC](https://www.sigma2.no/high-performance-computing). It covers the basic commands for navigating in the terminal of an HPCC, running a **job script**, and managing files, and includes a walk-through of training a machine learning model in containers.

The book is the result of Strategic Funding given by the [Norwegian Institute for Nature Research](https://www.nina.no/english/home) (NINA). It is **not static** and constantly subject to improvement based on feedback. You can contribute by opening issues on the [GitHub repository](https://github.com/NINAnor/91126800_ML_and_associated_tech).

## Setup

Install `uv`: https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync --dev
uv run prek install # optional
```

## Building the book

The book is built with [mdBook](https://rust-lang.github.io/mdBook/):

```bash
mdbook build
```

The output lands in `book/`. The built book is deployed to GitHub Pages from the `.github/workflows/deploy.yml` workflow.

## Development with docker

A basic docker image is provided, run:

```bash
docker compose up --build watch
```

## Tools installed

- uv
- mdBook
- prek (optional)

## Update from template

To update this project with the latest changes from the NINAnor `template-python`, run:

```bash
uvx --with copier-template-extensions copier update --trust
```

You can keep your previous answers by using:

```bash
uvx --with copier-template-extensions copier update --trust --defaults
```
