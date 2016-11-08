function updateTelemetryParameter(type,value,time) {
  console.log(" --> updateTelemetryParameter()");
  
  var unit = getUnits(type);

  $(".telemetry-parameter." + type).not(".time").html(value + " " + unit);
  $(".telemetry-parameter." + type + ".time").html(formatDateTime(time));
  
  console.log(" <-- updateTelemetryParameter()");
}

function updateParameterPosition(position) {
  console.log(" --> updateParameterPosition()");
  
  var timestamp = position.time;

  var coords = getReadableCoords(position.lat,position.lng);
  $(".telemetry-parameter.position").not(".time").html(coords);
  $(".telemetry-parameter.position.time").html(formatDateTime(timestamp));
}

function getUnits(type) {
  var units = {
    "altitude": "m",
    "temperature": "°C"
  }

  return units[type];
}

function updateStartPosition(data) {
  var lat = data.location.lat;
  var lng = data.location.lng;

  console.log("updateStartLocation(" + lat + ", " + lng + ")");

  var newPosition = new google.maps.LatLng(lat, lng);
  startMarker.setPosition(newPosition);
}

function updateLandingPosition(data) {
  var lat = data.location.lat;
  var lng = data.location.lng;

  console.log("updateLandingLocation(" + lat + ", " + lng + ")");

  var newPosition = new google.maps.LatLng(lat, lng);
  landingMarker.setPosition(newPosition);
}

function updateBurstPosition(message) {
  console.log(" --> updateBurstLocation():");

  var point = message.data.point;
  var infoBoxData = message.data.info;

  var lat = point.lat;
  var lng = point.lng;

  if( verifyCoords(lat,lng) ) {
    setMarkerPosition(burstPosition,burstMarker,point,null);
  }
  console.log(" <-- updateBurstLocation()");
}

function updateBalloonPosition(message) {
  console.log(" --> updateBaloonLocation()");

  var point = message.data.point;
  var lat = point.lat;
  var lng = point.lng;

  if( verifyCoords(lat,lng) ) {

    setMarkerPosition(balloonPosition,balloonMarker,point,null);
    var points = [point];
    setPath(path,points,"append");
    
    updateParameterPosition(point);
    pathPredicted.setVisible(false);
  }

  console.log(" <-- updateBaloonLocation()");
} 

function updatePredictedPath(message) {
  console.log(" --> updatePredictedPath():");

  var points;
  if( message.data.mode == "new" ) {

    console.log(balloonPosition);
    var balloonPoint = [{
      "time": null,
      "lat": balloonPosition.lat(),
      "lng": balloonPosition.lng()
    }];

    points = balloonPoint.concat(message.data.points);
  } else {
    points = message.data.points;
  }

  setPath(pathPredicted,points,message.data.mode);

  console.log(" <-- updatePredictedPath()");
}

function updatePath(message) {
  console.log(" --> updatePath():");

  setPath(path,message.data.points,message.data.mode);

  var lastPoint = message.data.points[message.data.points.length-1];
  console.log("Last point: ", lastPoint);

  setMarkerPosition(balloonPosition,balloonMarker,lastPoint,null);
  updateParameterPosition(lastPoint);

  console.log(" <-- updatePath()");
}

function handlePathUpdate(message) {
  console.log(" --> handlePathUpdate()");
  switch(message.data.type) {
    case "path":
      updatePath(message);
      break;
    case "predictedPath":
      updatePredictedPath(message);
      break;
  }
  console.log(" <-- handlePathUpdate()");
}

function handleBalloonEvent(message) {
  console.log(" --> handleBalloonEvent()");
  switch(message.data.type) {
    case "start":
      updateStartPosition(message);
      break;
    case "currentPosition":
      updateBalloonPosition(message);
      break;
    case "burst":
      updateBurstPosition(message);
      break;
    case "landing":
      updateLandingPosition(message);
      break;
  }
  console.log(" <-- handleBalloonEvent()");
}

function handleTelemetryUpdate(message) {
  console.log(" --> handleTelemetryUpdate()");

  var parameters = message.data.parameters;

  for ( i in parameters ) {
    var param = parameters[i];
    updateTelemetryParameter(param.type,param.value,param.time);
  }

  console.log(" --> handleTelemetryUpdate()");
}