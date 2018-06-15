window.onload=function(){
    //alert("hey js is working");
    var x=13.08387245;
    var y=77.5743201838385;
    var mymap = L.map('mapid').setView([x,y], 14);
    L.tileLayer('https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
        id:'mapbox.streets-satellite'
	}).addTo(mymap);
	L.marker([x,y]).addTo(mymap);

	console.log("test : "+htmlLand);
	var land_details = htmlLand;
    console.log(land_details);

    console.log("Side details "+htmlSideLand);
    var side_details=htmlSideLand;
    console.log("Side details JS: "+side_details.area+side_details.name);

    var popupContent='<p><b>Survey No. :'+side_details.surveyno+'</b><br>Name : '+side_details.name+'<br>Soil Type : '+side_details.soil_type+'<br>Current Crop : '+side_details.ccrop+'<br>Area : '+side_details.area.toFixed(2)+'acr</p>';

	if(land_details!=""){
	    var polygonMarker=L.polygon(land_details.coordinates,{color:'orange', wieght:'10',fillOpacity:'0.4'}).addTo(mymap);
	    polygonMarker.bindPopup(popupContent).openPopup();
    }
	else{
	    console.log("Its NULL");
    }
}