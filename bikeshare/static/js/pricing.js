console.log("for pricing.html");

d3.json('/api/pricing').then((data) => {
    console.log(data);
});
