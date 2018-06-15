window.onload=function(){
    //alert("hey js is working");
    var x=13.08387245;
    var y=77.5743201838385;
    var mymap = L.map('mapid').setView([x,y], 14);
    L.tileLayer('https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 20,
		id: 'mapbox.streets-satellite'
	}).addTo(mymap);
	L.marker([x,y]).addTo(mymap);

	console.log("test : "+htmlSoilLand);
	var soil_land_details = htmlSoilLand;
    console.log("Soil details : "+soil_land_details.coordinates[0]);
    var len=soil_land_details.coordinates.length;
    console.log("Soil details length : "+len);

    console.log("Side details "+htmlSideSoil);
    var side_details=htmlSideSoil;
    var sideLen=side_details.length;
    var polygonMarker=[]
    //console.log("Side details JS: "+side_details[0].area+side_details[1].name+" Len of side details : "+side_details.length);

    if(soil_land_details!=""){
        for(var i=0;i<len;i++)
        {
            polygonMarker[i]=L.polygon(soil_land_details.coordinates[i], {color: 'black',wieght:'10',fillOpacity:'0.4'}).addTo(mymap);
            var popupContent='<p><b>Survey No. : '+side_details[i].surveyno +'</b><br>Name : '+side_details[i].name+'<br>Current Crop : '+side_details[i].ccrop+'<br>Area : '+side_details[i].area.toFixed(2)+'acr</p>';
            polygonMarker[i].bindPopup(popupContent).openPopup();
        }
    }
    else{
	    console.log("Its NULL");
    }
}