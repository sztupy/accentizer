# Accentizer

This is the static webpage repository of [accentizer](http://sztupy.hu/accentizer). It is built using foundation, and the
source can be found in the `gh-pages-source` branch, while the generated code is put into `gh-pages`.

# Building

## Requirements

The project is based on Foundation, so please install it first

Then when you're working on your project, just run the following command:

```bash
bundle exec compass watch
```

If you are ready and want to clean up the directory for the `gh-pages` branch please run `github-pages-generate.sh`

## Upgrading Foundation

If you'd like to upgrade to a newer version of Foundation down the road just run:

```bash
bower update
```
