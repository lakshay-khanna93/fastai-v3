var el = x => document.getElementById(x);

window.onload=function(){
  document.getElementById("file-input").addEventListener("change", handleFiles, false);
}

function handleFiles(event) {
  var files = event.target.files;
  el("upload-label").innerHTML = files[0].name;
  $("#src").attr("src", URL.createObjectURL(files[0]));
  document.getElementById("audio-picked").load();
}


function showPicker() {
  el("file-input").click();
}


function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var files = event.target.files;
  $("#src").attr("src", URL.createObjectURL(files[0]));
  document.getElementById("audio-picked").load();
/*  reader.onload = function(e) {
    el("audio-picked").src = input.files[0];
    el("audio-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);*/
}

/*let reader = new FileReader();
reader.addEventListener('load', e=>{
  console.log(reader.result);
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST"," http://localhost:8080/rest/api/v1/audio/submit", true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.send({data:reader.result});
});
reader.readAsDataURL(blob);*/



function analyze() {

  var uploadFiles = document.getElementById("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `Result = ${response["result"]}`;
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

