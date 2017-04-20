var textarea, select, input_number, search_button, caps_button,
  add_button, get_button, put_button, del_button,
  speak_button, search_button, audio, result;
var speak = true;

function playAudio() {
  console.log('playAudio', audio);
  audio.addEventListener("canplay", function(){
    this.play();
  });
  audio.load();
}

function request(method, url, text, should_speak, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      if (xhr.status == 200) {
        console.log(xhr.responseText);
        var data = JSON.parse(xhr.responseText)['data'];
        result.innerHTML = data;
        if(callback)
          callback(data)
        if(should_speak)
          playAudio();
      }
    }
  }
  if(typeof(text) == "string")
    text = text.trim();
  if(method == 'GET' || method == 'PUT' || method == 'DELETE') {
    if(typeof(text) == "string")
      query = "q=" + text + "&";
    url = url + "?" + query + "speak=" + should_speak;
  }

  xhr.open(method, url);
  if (method == "POST" || method == "PUT") {
    xhr.setRequestHeader("Content-Type", "application/json");
  }

  var data = (method == "POST" || method == "PUT") ? JSON.stringify({"data": text, "speak": should_speak}) : null;
  xhr.send(data);
}

function load_voice_list() {
  function req(method, url, callback){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        if (xhr.status == 200) {
          var data = JSON.parse(xhr.responseText)['data'];
          callback(data);
        }
      }
    }
    xhr.open(method, url);
    xhr.send(null);
  }

  req('GET', './voicelist', function(data) {
    select = document.getElementById("select_voices");
    data.sort(function(a,b) {return (a.voice_language > b.voice_language) ? 1 : ((b.voice_language > a.voice_language) ? -1 : 0);} );
    data.forEach(function(voice) {
      var option = document.createElement("option");
      option.text = voice["voice_name"] + " ( " + voice["voice_language"] + " )";
      option.value = voice["language"]+"#"+voice["gender"];
      select.appendChild(option);
    });
  });

  req('GET', './voice', function(data) {
    select = document.getElementById("select_voices");
    select.value = data["language"]+"#"+data["gender"];
  });
}

function fillURL() {
  if (typeof location.origin === 'undefined')
    location.origin = location.protocol + '//' + location.host;

    var elms = document.querySelectorAll("[id='url']");
    for(var i = 0; i < elms.length; i++)
      elms[i].innerHTML = location.origin + "/get-audio";
}

function init() {
  voices_button = document.getElementById("voices");
  add_button = document.getElementById("add");
  get_button = document.getElementById("get");
  put_button = document.getElementById("edit");
  del_button = document.getElementById("del");
  caps_button = document.getElementById("caps");
  speak_button = document.getElementById("speak");
  search_button = document.getElementById("search");
  audio = document.getElementById("response_audio");
  result = document.getElementById("result");
  var inputGET = document.getElementById("url-input");
  var inputPOST = document.getElementById("url-input-post");

  speak_button.onchange = function() {
    speak = speak_button.checked;
    console.log("Should the response be spoken?", speak);
  };

  add_button.onclick = function() {
    textarea = document.getElementById("user_input_add");
    request('POST', './data', textarea.value, speak);
  };

  get_button.onclick = function() {
    input_number = document.getElementById("user_input_get");
    request('GET', './data/' + input_number.value, input_number.value, speak, function(data) {
      textarea = document.getElementById("user_input_edit");
      textarea.value = data;
    });
  };

  put_button.onclick = function() {
    input_number = document.getElementById("user_input_get");
    textarea = document.getElementById("user_input_edit");
    var data = {"data": textarea.value, "id": parseInt(input_number.value)};
    request('PUT', './data/' + input_number.value, data, speak);
  };

  del_button.onclick = function() {
    input_number = document.getElementById("user_input_del");
    request('DELETE', './data/' + input_number.value, input_number.value, speak);
  };

  caps_button.onclick = function() {
    textarea = document.getElementById("user_input_caps");
    request('POST', './capitalize', textarea.value, speak);
  };

  search_button.onclick = function() {
    textarea = document.getElementById("user_input_search");
    request('GET', './search', textarea.value, speak);
  };

  voices_button.onclick = function() {
    select = document.getElementById("select_voices");
    var value = select.options[select.selectedIndex].value;
    console.log(value);
    request('POST', './voice', value, speak);
  };

  inputGET.onchange = function() {
    var url = location.origin + "/get-audio?q="
    var encodedInput = encodeURIComponent(this.value)
    document.getElementById("url-text").innerHTML = url + encodedInput;
  }

  inputPOST.onchange = function() {
    document.getElementById("url-data").innerHTML = '{ "data": "' + this.value + '" }';
  }

  load_voice_list();
  fillURL();
}

window.addEventListener('load', function() {
  init();
}, false);
