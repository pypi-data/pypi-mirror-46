lis = $("ul.sao-list>li")
for(i=0; i< lis.length; i++){
	l = jQuery(lis[i]);
	console.log(l)

	if (l.has("span").length == 0){
		l.prepend('<span class="glyphicon glyphicon-book"></span>')
	}
}

bts = $("ul.sao-btns").find("button[icon]")
for(i=0; i< bts.length; i++){
	l = bts[i]
	console.log(l)
	icon_name = l.getAttribute("icon");
	$(l).html('<span class="glyphicon glyphicon-'+ icon_name + '"></span>')
}


function wait(id){
  $("a").each(function(e){
    $(e).css("pointer-events", "none")
  })
  $("input").each(function(e){
    $(e).css("pointer-events", "none")
  })

  $("body").css({
    "filter":"blur(15px)"
  })
  if (id != null){
    $(id).css("filter","blur(0px)")
  }
}

function wait_ok(){
  $("body").css({
    "filter":"blur(0px)"
  })
  $("a").each(function(e){
    $(e).css("pointer-events", "")
  })
  $("input").each(function(e){
    $(e).css("pointer-events", "")
  })
  

}


function drag_start(event) {
    var style = window.getComputedStyle(event.target, null);
    event.dataTransfer.setData("text/plain",
    (parseInt(style.getPropertyValue("left"),10) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top"),10) - event.clientY));
    console.log(event.target)
} 
function drag_over(event) { 
    event.preventDefault();
    console.log(event.target) 
    return false; 
} 



var show_in = function(id, x, y){
    $(id).css({
        "display" : "block",
        "position": "absolute",
        "z-index": 2000,
        "left": x-20,
        "top":y
    })
    $(id).collapse("show");
    open_id = id.slice(1, id.length) + "-opened"
    $(id).attr("id", open_id);
    console.log("show " + open_id)
    var dm = document.getElementById(open_id); 
    dm.addEventListener('dragstart',drag_start,false);

    container = document.getElementById("map-id-leaf")
    container.addEventListener('dragover', drag_over, false)

    container.addEventListener('drop',function(event){
      var offset = event.dataTransfer.getData("text/plain").split(',');
      var dm = document.getElementById(open_id);
      dm.style.left = (event.clientX + parseInt(offset[0],10)) + 'px';
      dm.style.top = (event.clientY + parseInt(offset[1],10)) + 'px';
      console.log(dm.style)
      event.preventDefault();
      return false;
    },false); 

    
}


var change_in = function(id, x, y){
  console.log("changed " + id)
  $(id).css({
    "left": "+=" + x+"px",
    "top":  "+=" + y+"px",
  })
}

function QrGen(data){
  var qrcode = new QRCode("qrcode", {
  text: data,
  width: 260,
  height: 260,
  colorDark: '#efb73e',
  colorLight: "#ffffff"
  });
}

function JsonPost(url, data, callback, no_wait){
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        success: function( data ) {
            console.log(data);
            if (no_wait == null){
              wait_ok()  
            }
            
            if (callback != null){
                callback(data);
            }
        },
        dataType: 'json'
    });
    if (no_wait == null){
      wait()  
    }
    
}

function JsonGet(url, callback){
    $.getJSON(url, callback);
}


var get_width = function(id){
  w = $(id).css("width")
  return w.slice(0, w.length -2)
}

var get_height = function(id){
  w = $(id).css("height")
  return w.slice(0, w.length -2)
}

var close_in = function(id){
  if ($(id).length == 0){
    open_id = id + "-opened"
    $(open_id).collapse("hide");
    $(open_id).hide();
    setTimeout(function () {
        $(open_id).attr("id", id.slice(1, id.length));
    }, 1000);  
  }else{
    open_id = id
    $(open_id).collapse("hide");
    $(open_id).hide();
  }
   
}

var sao_table = function(id, data){
              // console.log(data);
              console.log("=== some ==")
              table = "<table class=\"table\" ><thead><tr>"
              head = Object.keys(data.data[0])
              for(i=0; i < head.length; i++){
                table += "<th>"+head[i] + "</th>"
              }
              table += "</tr></thead><tbody>"
              for(i = 0; i< data.data.length; i ++){
                item = data.data[i]
                ii = '<tr>'
                for(i2 = 0; i2 < head.length ; i2 ++){
                  ii += '<td>' + item[head[i2]] + '</td>'
                }
                ii += '</tr>'
                table += ii
                // console.log(item)
              }
              table += '</tbody></table>'
              // remove old popover
              $(".sao-list").find("div.popover").remove()
              //init and show
              $(id).popover({
                'content':table,
                'title':'Get Status |pid/port',
                'placement':'right'
              }).popover('show')
              // change some attr  
              $(".sao-list>li>div.popover").css({
                "left": "105%",
                "opacity": "0.9"
              });
              tid = "#" + $(".sao-list > li > div.popover")[0].id
              $(".sao-list>li>div.popover>.popover-title").html("<span class='glyphicon glyphicon-envelope' ></span>Get Status <button class='close' onclick='close_in(\'"+ tid + "\")'  ><span aria-hidden='true'>&times;</span></button>");
              $(".sao-list>li>div.popover>.popover-content").html(table);
              // $("#get-status").popover('show')
          }