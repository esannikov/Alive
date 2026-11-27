# Viewer dependencies

- `model-viewer/model-viewer-4.1.0.min.js`: unmodified browser distribution from `@google/model-viewer@4.1.0`, Google, Apache-2.0. https://github.com/google/model-viewer
- Bundled Three.js: MIT, see `model-viewer/LICENSE-Three.txt`. Other bundled dependencies retain license comments in the distribution.
- `draco/`: unmodified decoder files from the `three` npm package's `examples/jsm/libs/draco/gltf/`, Google Draco, Apache-2.0. https://github.com/google/draco

The module and Draco decoder are served locally. No CDN, analytics or third-party upload is used for the model viewer. Existing site comments retain their independent Giscus integration.
