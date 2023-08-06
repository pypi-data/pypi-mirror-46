swh-loader-npm
==============

Software Heritage loader to ingest [`npm`](https://www.npmjs.com/) packages into the archive.

# What does the loader do?

The npm loader visits and loads a npm package [1].

Each visit will result in:
- 1 snapshot (which targets n revisions ; 1 per package release version)
- 1 revision (which targets 1 directory ; the package release version uncompressed)

[1] https://docs.npmjs.com/about-packages-and-modules

## First visit

Given a npm package (origin), the loader, for the first visit:

- retrieves information for the given package (notably released versions)
- then for each associated released version:
  - retrieves the associated tarball (with checks)
  - uncompresses locally the archive
  - computes the hashes of the uncompressed directory
  - then creates a revision (using ``package.json`` metadata file) targeting such directory
- finally, creates a snapshot targeting all seen revisions (uncompressed npm package released versions and metadata).

## Next visit

The loader starts by checking if something changed since the last visit. If nothing changed, the visit's snapshot is left unchanged. The new visit targets the same snapshot.

If something changed, the already seen package release versions are skipped. Only the new ones are loaded. In the end, the loader creates a new snapshot based on the previous one. Thus, the new snapshot targets both the old and new package release versions.

# Development

## Configuration file

### Location

Either:
- `/etc/softwareheritage/loader/npm.yml`
- `~/.config/swh/loader/npm.yml`

### Configuration sample

```lang=yaml
storage:
  cls: remote
  args:
    url: http://localhost:5002/

debug: false
```

## Local run

The built-in command-line will run the loader for a specified npm package.

For instance, to load `jquery`:
```lang=bash
$ python3 -m swh.loader.npm.loader jquery
```

If you need more control, you can use the loader directly. It expects
three arguments:
- `package_name` (required): a npm package name
- `package_url` (optional): URL of the npm package description (human-readable html page) that will be used as the associated origin URL in the archive
- `project_metadata_url` (optional): URL of the npm package metadata information (machine-parsable JSON document)

```lang=python
import logging

from urllib.parse import quote

from swh.loader.npm.loader import NpmLoader

logging.basicConfig(level=logging.DEBUG)

package_name='webpack'

NpmLoader().load(package_name,
                 'https://www.npmjs.com/package/%s/' % package_name,
                 'https://replicate.npmjs.com/%s/' % quote(package_name, safe=''))
```