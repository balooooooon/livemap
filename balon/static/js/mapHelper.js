function verifyCoords(lat,lng) {
  console.log(" --> verifyCoords(" + lat + ", " + lng + ")");
  console.log("NOT IMPLEMENTED!!!");
  // TODO Coordinates verification
  console.log(" <-- verifyCoords()");
  return true;
}

function getReadableCoords(lat,lng) {
  var x,y;
  const DECIMAL = 5;
  if( lat > 0 ) {
    x = lat.toFixed(DECIMAL) + " N";
  } else if( lat < 0 ) {
    x = lat.toFixed(DECIMAL) + " S";
  } else {
    x = lat.toFixed(DECIMAL);
  }

  if( lng > 0 ) {
    y = lng.toFixed(DECIMAL) + " E";
  } else if( lng < 0 ) {
    y = lng.toFixed(DECIMAL) + " W";
  } else {
    y = lng.toFixed(DECIMAL);
  }

  return x + ", " + y; 
}

function leadingZero(x) {
  return ("0" + x).slice(-2);
}

function formatDateTime(timestamp) {
  var d = new Date(timestamp*1000);

  var stringDateTime;
  stringDateTime = leadingZero(d.getDate()) + "." + leadingZero((d.getMonth()+1)) + "." + d.getFullYear() + " " + 
                  leadingZero(d.getHours()) + ":" + leadingZero(d.getMinutes()) + ":" + leadingZero(d.getSeconds());

  return stringDateTime + " " + formatTimeZone(d);
}

function formatDateTimeUTC(timestamp) {
  var d = new Date(timestamp*1000);

  var stringDateTime;
  stringDateTime = leadingZero(d.getUTCDate()) + "." + leadingZero((d.getUTCMonth()+1)) + "." + d.getUTCFullYear() + " " + 
                  leadingZero(d.getUTCHours()) + ":" + leadingZero(d.getUTCMinutes()) + ":" + leadingZero(d.getUTCSeconds());
  return stringDateTime + " GMT";
}

function formatTimeZone(date) {
  return date.toTimeString().split(" ")[1];
}

function setMarkerPosition(position,marker,positionData,textData) {
  console.log(" --> setMarkerPosition()");
  console.log("PositionData: ", positionData);
  console.log("TextData: ", textData);

  position = new google.maps.LatLng(positionData.lat,positionData.lng);
  
  console.log("Marker: ", marker);
  console.log("New position: " + positionData.lat + ", " + positionData.lng);
  
  marker.setPosition(position);
  
  console.log(" <-- setMarkerPosition()"); 
  return position;
}

function setPath(polyline,points,mode="new") {
  console.log(" --> setPath()");
 
  var path = polyline.getPath();
  
  if( mode == "new" ) {
    console.log("   setPath(): Clear old path.");
    path.clear();      
  } else if ( mode == "append" ) {
    console.log("   setPath(): Appending to path.");
  } else {
    console.log("   setPath(): Undefined mode: " + mode);
  }

  for( i in points ) {
    console.log("   setPath(): New point: " + points[i].lat + ", " + points[i].lng)
    var point = new google.maps.LatLng(points[i].lat,points[i].lng);
    path.push(point);
  }

  polyline.setVisible(true);
 
  console.log(" <-- setPath()");
}
