ACTION_PUBLISH_RELEASE_ON_TAG = """
name: Publish release

on:
  push:
    tags:
      - "*"

jobs:
  create-release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
    
      - name: Get the version
        id: get_version
        run: echo ::set-output name=VERSION::${GITHUB_REF#refs/tags/}
    
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # This token is provided by Actions, you do not need to create your own token
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: docs/releases/${{ steps.get_version.outputs.VERSION }}.md
          draft: false
          prerelease: false
"""

BUMPVERSION_CONFIG = """
[bumpversion]
current_version = 0.0.1

# [bumpversion:file:setup.py]
"""