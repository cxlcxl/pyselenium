Scorenga = function () {
  var self = this;

  self.VERSION = '20210505';
  self.ACTIONS = {
    READY: 'READY',
    INFO: 'INFO',
    COMMAND: 'COMMAND',
    EVENT: 'EVENT',
    WARNING: 'WARNING',
    ERROR: 'ERROR'
  };
  self.EVENTS = {
    GAME_START: 'GAME_START',
    GAME_FINISH: 'GAME_FINISH',
    LEVEL_START: 'LEVEL_START',
    LEVEL_FINISH: 'LEVEL_FINISH',
    HIGH_SCORE: 'HIGH_SCORE'
  };
  self.SENDERS = {
    SYSTEM: 'Scorenga system',
    BRIDGE: 'Scorenga bridge'
  };

  self.callbacks = {
    mute: null,
    unmute: null,
    pause: null,
    resume: null,
    loadScript: function (scriptUrl) {
      var scriptElement = document.createElement('script');
      scriptElement.src = scriptUrl;
      document.body.appendChild(scriptElement);
    },
    execScript: function (scriptCode) {
      var scriptElement = document.createElement('script');
      scriptElement.innerText = scriptCode;
      document.body.appendChild(scriptElement);
    },
    pushScript: function (scriptHtml) {
      var parser = new DOMParser();
      var source = parser.parseFromString(scriptHtml, "text/html");
      var scripts = source.getElementsByTagName('script');
      for (var script of scripts) {
        var scriptElement = document.createElement('script');
        for (var attribute of Array.prototype.slice.call(script.attributes)) {
          scriptElement.setAttribute(attribute.nodeName, attribute.nodeValue);
        }
        scriptElement.innerText = script.innerText;
        document.body.appendChild(scriptElement);
      }
    }
  };

  self.setMuteCallback = function (muteCallback) {
    self.callbacks.mute = muteCallback;
  };
  self.setUnMuteCallback = function (unMuteCallback) {
    self.callbacks.unmute = unMuteCallback;
  };
  self.setPauseCallback = function (pauseCallback) {
    self.callbacks.pause = pauseCallback;
  };
  self.setResumeCallback = function (resumeCallback) {
    self.callbacks.resume = resumeCallback;
  };
  self.setReady = function () {
    self.postMessage(self.ACTIONS.READY, {version: self.VERSION});
  };

  self.postMessage = function (action, payload) {
    if (!window.parent) {
      console.log('SCORENGA ERROR: Can not find parent window to send message to scorenga system');
      return;
    }
    window.parent.postMessage(JSON.stringify({
      sender: self.SENDERS.BRIDGE,
      action: action,
      payload: payload
    }, function (key, val) {
      return (typeof val === 'function') ? '<function>' : val;
    }), '*');
  };

  self.reportEvent = function (event, level, score) {
    if (!self.EVENTS.hasOwnProperty(event)) {
      console.log('[SCORENGA] Error: unknown event ' + event + ', please use window.scorenga.EVENTS enum');
      return;
    }
    self.postMessage(self.ACTIONS.EVENT, {
      event: event,
      level: parseInt(level),
      score: parseInt(score)
    });
  };

  window.addEventListener('message', function (event) {
    try {
      var message = JSON.parse(event.data);
      if (!message || !message.sender || message.sender !== self.SENDERS.SYSTEM) return;
      if (!message.action) return;
      if (message.action === self.ACTIONS.INFO) {
        self.postMessage(self.ACTIONS.INFO, {version: self.VERSION, callbacks: self.callbacks});
        return;
      }
      if (message.action === self.ACTIONS.COMMAND) {
        if (!self.callbacks[message.payload.callback]) {
          self.postMessage(self.ACTIONS.WARNING, {
            error: 'You asked to perform ' + message.payload.callback + ' callback, but it is not filled by game'
          });
          return;
        }
        self.callbacks[message.payload.callback](message.payload.params);
      }
    } catch (e) {
    }
  });
};

window.scorenga = new Scorenga();