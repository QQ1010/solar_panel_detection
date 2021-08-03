
//建立空白地圖
const center = [23.9975423,121.0795833];
var map = L.map('map', {
    center: center,
    zoom: 8
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// const center = [23.450648316816473, 120.40191650390626]

//產生marker
const marker = L.marker(center,{
    title:'跟 <a> 的 title 一樣', // 跟 <a> 的 title 一樣
    opacity:1.0
}).addTo(map);
marker.bindPopup("<b>Hello</b>").closePopup();

// 隨便點擊地可上任一地方，就會出現座標
const popup = L.popup();
function onMapClick(e) {
  let lat = e.latlng.lat; // 緯度
  let lng = e.latlng.lng; // 經度
  popup
    .setLatLng(e.latlng)
    .setContent(`緯度：${lat}<br/>經度：${lng}`)
    .openOn(map);
}
map.on('click', onMapClick);

//群聚的座標集合、邊界
//隨機在最小和最大值中產生數值
function random(min, max) {
    return Math.random()*(max - min) + min;
}

let arr = [];
//產生隨機數量的點放到arr陣列中
function CreatePoint(count) {  //count 為產生的點數量
    for (let i = 0 ; i < count ; i++) {
        let longitude = random(120.5 , 121.4); //經度介於120.5 到 121.4之間
        let latitude = random(23 , 24.6);  //緯度介於23到24.6之間

        arr.push({x:longitude, y:latitude});
    }
}
CreatePoint(1500);

//繪製ClusterGroup
var markers = L.markerClusterGroup();
arr.map(item => L.marker(new L.LatLng(item.y , item.x))    //新增marker
    .bindPopup(`<p>太陽能板面積: </p>`))  //資訊視窗
    .forEach(item => markers.addLayer(item));                   //把marker加入L.mmarkweClusterGroup中

map.addLayer(markers);

// 控制右上角選單按鈕
$("#btn-open").click(function() {
    $("#modal").css("opacity",0.8);
    $("#modal").css("zIndex",1000);
    $("#btn-open").css("zIndex",-1);
});

$("#btn-close").click(function () {
    $("#modal").css("opacity", 0);
    $("#modal").css("zIndex", -1);
    $("#btn-open").css("zIndex", 2);
  });
