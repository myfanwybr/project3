function getWeather(city){
	if(city){
	var xhr=new XMLHttpRequest();
	xhr.onreadystatechange=function(){
		if(this.station==200 && this.readyState==4){
			var formattedData=formatWeather(JSON.parse(xhr.responseText));
			document.getElementById("weather-data").innerHTML=formattedData;
			document.getElementById('cityname').value="";

		}
	};
	xhr.open("GET","http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=d610395e85b50074b834a0234b0776db");
	xhr.send();
}

function formatWeather(data){
	return
}

function getForecast(city,days){

}