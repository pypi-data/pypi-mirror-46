// This file contains the javascript that is run when the notebook is loaded.
// It contains some requirejs configuration and the `load_ipython_extension`
// which is required for any notebook extension.
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
window.__webpack_public_path__ = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/jupyter-escher'

// Pull jupyter object out when importing escher
window.define(
  'jupyter-escher-intercept',
  ['escher'],
  escher => escher.initializeJupyterWidget()
)

// Configure requirejs
if (window.require) {
  window.require.config({
    map: {
      '*': {
        'jupyter-escher': 'jupyter-escher-intercept'
      },
      'jupyter-escher-intercept': {
        escher: 'nbextensions/jupyter-escher/escher.min'
      }
    }
  })
}

// Export the required load_ipython_extension
module.exports = {
  load_ipython_extension: () => {}
}
