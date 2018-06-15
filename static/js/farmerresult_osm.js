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

	console.log("test : "+htmlFarmerLand);
	var farmer_land_details = htmlFarmerLand;
    console.log("Farmer details : "+farmer_land_details.coordinates[0]);
    var len=farmer_land_details.coordinates.length;
    console.log("farmer details length : "+len);

    console.log("Side details "+htmlSideFarmer);
    var side_details=htmlSideFarmer;
    var sideLen=side_details.length;
    var polygonMarker=[]
    //console.log("Side details JS: "+side_details[0].area+side_details[1].name+" Len of side details : "+side_details.length);
    if(farmer_land_details!=""){
        for(var i=0;i<len;i++)
        {
            polygonMarker[i]=L.polygon(farmer_land_details.coordinates[i], {color: 'magenta', wieght:'10',fillOpacity:'0.4'}).addTo(mymap);
            var popupContent='<p><b>Survey No. : '+side_details[i].surveyno +'</b><br>Name : '+side_details[i].name+'<br>Current Crop : '+side_details[i].ccrop+'<br>Area : '+side_details[i].area.toFixed(2)+'acr</p>';
            polygonMarker[i].bindPopup(popupContent).openPopup();
        }
    }
    else{
	    console.log("Its NULL");
    }
}