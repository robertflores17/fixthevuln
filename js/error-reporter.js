// FixTheVuln — Client Error Reporter
// Catches uncaught errors and sends them to the worker for logging.
(function() {
  'use strict';
  var ENDPOINT = 'https://fixthevuln-checkout.robertflores17.workers.dev/errors';
  var reported = {};
  var count = 0;
  var MAX = 10;

  function send(message, source, lineno, colno, stack) {
    var key = (message || '') + ':' + (source || '') + ':' + (lineno || 0);
    if (reported[key] || count >= MAX) return;
    reported[key] = 1;
    count++;
    try {
      var payload = JSON.stringify({
        message: String(message || '').slice(0, 1000),
        source: String(source || '').slice(0, 500),
        lineno: lineno || 0,
        colno: colno || 0,
        stack: String(stack || '').slice(0, 2000),
        page: location.pathname
      });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([payload], { type: 'text/plain' }));
      }
    } catch(e) { /* silent */ }
  }

  window.onerror = function(msg, src, line, col, err) {
    send(msg, src, line, col, err && err.stack ? err.stack : '');
  };

  window.addEventListener('unhandledrejection', function(e) {
    var reason = e.reason;
    var msg = reason ? (reason.message || String(reason)) : 'Unhandled Promise Rejection';
    var stack = reason && reason.stack ? reason.stack : '';
    send(msg, '', 0, 0, stack);
  });
})();
