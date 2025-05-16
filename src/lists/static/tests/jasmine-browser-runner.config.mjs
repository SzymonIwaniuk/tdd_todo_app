export default {
  srcDir: ".",
  srcFiles: [
    "*.js"
  ],
  specDir: "tests",
  specFiles: [
    "**/*[sS]pec.js"
  ],
  cssFiles: [
    "bootstrap/css/bootstrap.min.css"
  ],
  helpers: [
    "helpers/**/*.js"
  ],
  env: {
    stopSpecOnExpectationFailure: false,
    stopOnSpecFailure: false,
    random: true,
    // Fail if a suite contains multiple suites or specs with the same name.
    forbidDuplicateNames: true
  },

  // For security, listen only to localhost. You can also specify a different
  // hostname or IP address, or remove the property or set it to "*" to listen
  // to all network interfaces.
  listenAddress: "localhost",
  
  // The hostname that the browser will use to connect to the server.
  hostname: "localhost",

  browser: {
    name: "headlessFirefox"
  }
};
