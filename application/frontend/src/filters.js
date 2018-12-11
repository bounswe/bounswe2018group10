import Vue from 'vue';

Vue.filter('shortDescription', function (value) {
  if (!value) return "";
  const limit = 200;
  if(value.length > limit){
    return value.slice(0,limit) + "...";
  }else{
    return value;
  }
});

Vue.filter('striphtml', function (value) {
  var div = document.createElement("div");
  div.innerHTML = value;
  var text = div.textContent || div.innerText || "";
  return text;
});