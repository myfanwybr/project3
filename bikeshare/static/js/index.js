console.log("for index.html");

d3.json('/api/pricing').then((data) => {
    console.log(data);
});
