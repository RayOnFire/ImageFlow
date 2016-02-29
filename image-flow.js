function ImageFlow(options) {
  this.ele = options.element;
  this.rows = options.rows;
  this.urls = options.urls;
  this.urlNo = 1;
  this.prepareRow(this.rows);
  this.init();
  this.listenScroll();
}

function setProgressBar(ele) {
  /*
  var wrapper = $('<div class="progress-wrapper"></div>');
  var loaded = $('<div class="progress-loaded"></div>');
  wrapper.css({
    'height': '2px',
    'background': 'black',
    'width': '80%'
  });
  loaded.css({
    'background': 'red',
    'position': 'absolute',
    'bottom': 0
  });
*/
  var wrapper = document.createElement('div');
  wrapper.className += 'progress-wrapper';
  var loaded = document.createElement('div');
  loaded.className += 'progress-loaded';
  wrapper.style.height = 2;
  wrapper.style.background = 'black';
  wrapper.style.width = '60%';
  //wrapper.style.marginTop = '49';
  //wrapper.style.marginLeft = '20';
  //wrapper.style.marginRight = '20';
  wrapper.style.justifyContent = 'center';
  ele.appendChild(wrapper);
  return wrapper;
}

Image.prototype.completedPercentage = 0;

Image.prototype.load = function(url, card){
  var self = this;
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open('GET', url, true);
  xmlHttp.responseType = 'arraybuffer';
  xmlHttp.onload = function(e) {
      var blob = new Blob([this.response]);
      card.style.height = "";
      self.src = window.URL.createObjectURL(blob);
  };
  xmlHttp.onprogress = function(e) {
      self.completedPercentage = parseInt((e.loaded / e.total) * 100);
      console.log(self.completedPercentage);
      //self.progress.innerHTML = self.completedPercentage;
  };
  xmlHttp.onloadstart = function() {
      self.completedPercentage = 0;
      card.style.height = 100;
      //var self.text = document.createTextNode(self.completedPercentage);
      //card.appendChild(self.text);
      //self.progress = document.createElement('p');
      //card.appendChild(self.progress);
      //self.progress.innerHTML = self.completedPercentage;
      //self.progressBar = setProgressBar(card);
      self.src = 'loading.gif';
  };
  xmlHttp.send();
};


ImageFlow.prototype.init = function () {
  this.fromJson(this.urls[0]);
};

ImageFlow.prototype.prepareImage = function (arr) {
  var rows = document.getElementsByClassName("row");
  var rowNo = 0;
  for (i = 0; i < arr.length; i++) {
    var img = new Image();
    var card = document.createElement('div');
    card.className += 'img-card';
    var imgChild = card.appendChild(img);
    var cardChild = rows[rowNo].appendChild(card);
    imgChild.style.maxWidth = '100%';
    rowNo++;
    if (rowNo === 3) {
      rowNo = 0;
    }
    img.load(arr[i], cardChild);
  }
};

ImageFlow.prototype.fromJson = function (url) {
  var self = this;
  var imgObjList = [];
  $.ajax({
    url: url,
  }).done(function (data) {
    data = JSON.parse(data);
    self.rowNo = 0;
    self.prepareImage(data);
  });
};

ImageFlow.prototype.prepareRow = function (rows) {
  this.ele.css({'display': 'flex'});
  for (i = 0; i < rows; i++) {
    var row = $('<div class="row"></div>');
    row.css({'flex': 1});
    row.appendTo(this.ele);
  }
};

ImageFlow.prototype.listenScroll = function () {
  var self = this;
  window.addEventListener('scroll', function () {
    if (window.innerHeight + window.scrollY > document.body.scrollHeight - 1) {
      console.log('scroll to bottom');
      self.fromJson(self.urls[self.urlNo]);
      self.urlNo++;
    }
  })
}