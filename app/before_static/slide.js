var images = ["../static/image1.jpg", "../static/image2.jpg", "../static/image3.jpg", "../static/image4.jpg", "../static/image5.jpg"]
var texts = ["うんちぶりぶりの君はこう言った。ちんこはでかい。",
             "ちんちんびろーん。うんちもらしちゃおうかな。",
             "たおぺいぺい。やっぱり僕はたおぺいぺい。",
             "サクラ散るぱるま。イミフたころん。",
             "てらすどんどん。あーてらすどんどん。"]

var current = 0;

var changeImage = function(num){
  if(current+num >= 0 && current+num < images.length){
      current += num;
      document.getElementById("main_image").src = images[current];
      document.getElementById("insert-text").innerHTML = texts[current];
  };
};

//前に戻る処理
document.getElementById("prev").onclick = function(){
  changeImage(-1);
};

//前に進む処理
document.getElementById("next").onclick = function(){
  changeImage(1);
};
