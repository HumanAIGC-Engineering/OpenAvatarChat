;(function () {
  'use strict'
  let e = null
  self.onmessage = function (t) {
    const { type: a, interval: s } = t.data
    switch (a) {
      case 'start':
        ;(e && clearInterval(e),
          (e = setInterval(() => {
            self.postMessage({ type: 'heartbeat' })
          }, s || 1e4)))
        break
      case 'stop':
        e && (clearInterval(e), (e = null))
        break
    }
  }
})()
