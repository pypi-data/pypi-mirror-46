
var IP_GEO_DATA = {}
var HOST_INFO = []
var tor_exit_layer = null;
var shodan_db = new PouchDB("shodan")
var cursor_fearture = null;
var second_cursor_feature = null;
function save_shodan(id,data){

  // try {
  //   var response = await shodan_db.put({
  //     _id: id,
  //     data: data
  //   });
  // } catch (err) {
  //   console.log(err);
  // }
}

function load_shodan(id, callback){
  // try {
  //   var doc = await db.get(id);
  //   callback(doc.data);
  // } catch (err) {
  //   console.log(err);
  // }
}


function search_shodan(req){
  $("input[name=Shodan]").parent().toggle("hide")
                    // loading.toggle()
  $.ajax({
  type: "POST",
  url: "/search_shodan",
  data: {
      name:req
  },
  success: function(data) {
      var shodan = data

      shodan_layer.remove()
      shodan_layer.addLayer(L.geoJSON(data['graph'], {
        pointToLayer: function(geoJsonPoint, latlng){
          return L.marker(latlng, {icon: redIcon});
        },
        onEachFeature: function(feature, layer){
          layer.bindPopup(feature.properties.name)
        }
      }))

      console.log(data);
      // loading.toggle()
      $("input[name=Shodan]").parent().toggle("show")


  },
      dataType: 'json'
  });
}

function update_ip() {

  $.getJSON( "/get_ip", function( data ) {
      IP_GEO_DATA = data;
      var items = [];

      var from_loc = null;
      console.log(data)
      var now_loc = null;
      var from_point_loc = null;
      var end_loc = null;
      var dylamic_line_id = null;
      line = null;
    // cities_layer.removeLayer(tor_exit_layer);
      feature_layer = L.geoJSON(data, {
        pointToLayer: function(feature, latlng) {
          if (feature.properties.wrn == null){
            return L.marker(latlng, {icon: greenIcon});
          }else{
            return L.marker(latlng, {icon: redIcon});
          }
        },
        onEachFeature: function (feature, layer){
          layer.bindPopup(feature.properties.name);
          HOST_INFO.push(feature.properties.msg)
        }
      })

      
      var onmousemoveF = function(e){
          now_loc = e.latlng;
          lay = line_layer._layers[dylamic_line_id]
          polylist = [from_loc, now_loc]
          console.log(polylist)
          lay.setLatLngs(polylist);
          
      }

      var add_link = function(from_point_loc, target_point_loc, arc){
        if (arc == null){
          lay = new L.Polyline([from_loc],{ 
                  color: "yellow",
                  weight:2,
                  smoothFactor:2,
                  opacity:0.9
              });
          line_layer.addLayer(lay);
          lid = line_layer.getLayerId(lay)
          console.log(from_point_loc)
          console.log(target_point_loc)
          line_layer._layers[lid].setLatLngs([from_point_loc, target_point_loc])
          
        }else{
          s = from_point_loc
          b = target_point_loc
          if (from_point_loc.lng > target_point_loc.lng){
            s = target_point_loc
            b = from_point_loc 
          }
          // if (s.lng < 0){
          //   s.lng = Math.abs(s.lng) + 180 
          // }
          start = {x:s.lng, y:s.lat}
          end = {x:b.lng, y:s.lat}
          console.log(start,end)
          gen = new GreatCircle(start,end, {'name': 'arc line', 'color':'blue'});
          line = gen.Arc(100, {offset:10})
          arcLayer.addData(line.json())
        }
        
      }

      var get_links = function(ip, from_point){
        JsonPost('/asyncremoteapi',{
          'req':{
            'op':'all_links',
            'ip': ip
          }
        }, function(data){
          routes = data.routes
          for(i=0; i< routes.length; i ++){
            link_target = routes[i]
            console.log(link_target)
            target_point_loc = L.latLng([link_target.geo[1], link_target.geo[0]])
            if (from_point_loc == null){
              add_link(from_point, target_point_loc, true)
            }else{
              add_link(from_point_loc, target_point_loc, true)
            }
          }
        },
      true)
      }

      var drawline = function(from_loc){
        lay = new L.Polyline([from_loc],{ 
                  color: "green",
                  weight:2,
                  smoothFactor:2,
                  opacity:0.9
              });
        line_layer.addLayer(lay);
        dylamic_line_id = line_layer.getLayerId(lay); 
      }
      $("#link-setting").click(function(){
          from_point_loc = from_loc
          drawline(from_point_loc)
          lmap.on("mousemove", onmousemoveF)
          close_menu(false)
      })

      $("#base-setting").click(function(){
          console.log("Post base install")
          JsonPost("/asyncremoteapi", {
            'req':{
              'op':'base',
              'ip': cursor_fearture.properties.name
            }
          },function(data){
            close_menu()
          })

      })

      $("#gen-qr").click(function(){
          JsonPost("/asyncremoteapi",{
            'req':{
              'op':'qr',
              'ip' : cursor_fearture.properties.name   
            }
          }, function(data){
            console.log(data)
            qrcode.makeCode(data.data)
            show_in("#qr-panel", relX, relY)
            $("#qr-panel-opened").css("display","block")
            // $("#qr-panel-title").html(data.code)
            setTimeout(function () {
              $("#qr-panel-opened").animate({
                'left': '-=' + get_width("#qr-panel-opened") ,
                'top': '-=' + (get_height("#qr-panel-opened") * 0.6)
              });

              close_menu()
            },200)
          })
           
      })

      $("#proxy-setting-btn").click(function(){
          JsonPost("/asyncremoteapi",{
            'req':{
              'op':'set-proxy',
              'proxy':$("#proxy-setting-content>input").val()
            }
          }, function(data){
            $("#register-server-content").text(data.res)
            $("#register-server-content").modal()
          })
      })

      $("#get-status").click(function(){
          console.log("Post !!!")
          JsonPost("/asyncremoteapi", {
            'req':{
              'op':'status',
              'ip':cursor_fearture.properties.name
            }
          }, function(data){
              setTimeout(function(){
                sao_table("#get-status", data)  
              }, 500)
              
             
          })
      })

      $("#destroy-server").click(function(){
        console.log("Destroy !!!")
        destroy_server()
      })

      $("#get-check").click(function(){
        JsonPost("/asyncremoteapi",{
          'req':{
            'op':'check',
            'ip':cursor_fearture.properties.name
          }
        }, function(data){
          sao_table('#get-check', data)
        })
      })

      $("#link-start").click(function(){
          JsonPost("/asyncremoteapi", {
              "req":{
                  "op":"link",
                  'use-minute': $("#use-minute").val(),
                  'ip':cursor_fearture.properties.name ,
                  'target': second_cursor_feature.properties.name
              }
          }, function(data){
              close_in("#panel-input")
              $("#register-server-content").text(data.res)
              if(data.status != 0){
                line_layer.clearLayers()
              }
              $("#register-server").modal()
          })
      })

      $("input#cmd_mode").keyup(function(evt){
          console.log(evt);
          if(evt.keyCode == 13){
            set_mode();
          }
      })

      $("input#set_label").keyup(function(evt){
          console.log(evt);
          if(evt.keyCode == 13){
            set_label();
          }
      })
      
      function search(datas){
          var table = "<table class=\"table\" ><thead><tr>"
          var head = Object.keys(datas[0])
          for(i=0; i < head.length; i++){
              table += "<th>"+head[i] + "</th>"
          }
          table += "</tr></thead><tbody>"
          for(i = 0; i< datas.length; i ++){
              item = datas[i]
              ii = '<tr onclick="go_to(\'' + item['host'] + '\')">'
              for(i2 = 0; i2 < head.length ; i2 ++){
                ii += '<td>' + item[head[i2]] + '</td>'
                

              }
              ii += '</tr>'
              table += ii
          // console.log(item)
          }
          table += '</tbody></table>'
          // $("input#cmd_mode").popover("hide");
          $("input#cmd_mode").popover({
              "title":'result',
              "html":true,
              "content": table
          }).popover("show")

          $("input#cmd_mode")[0].value = '';
      }
      function set_mode(){
        // $("input#cmd_mode").popover("hide");
        $("input#cmd_mode").popover("destroy")
        tmp = $("input#cmd_mode").val();
        hs = []
        HOST_INFO.forEach(function(data){
              if(data.host.indexOf(tmp) != -1){
                  hs.push(data)
              }else if( data.createTime.indexOf(tmp) != -1){
                  hs.push(data)
              }else if( data.location.indexOf(tmp) != -1){
                  hs.push(data)
              }else if( data.os.indexOf(tmp) != -1){
                  hs.push(data)
              }
        })
        // console.log(tmp)
        // console.log(hs)
        search(hs)
      }

      function set_label(){
        tmp = $("input#cmd_mode").val();
        if (tmp.indexOf(":") == -1){
          alert("Must 'x.x.x.x:label' ")
        }
        s = tmp.split(":")
        ip = s[0]
        label = s[1]
        JsonPost("/asyncremoteapi", {
          "req":{
            "op":'mark',
            'ip':ip,
            'label':label
          }
        }, function(data){
          alert("set ok")
          wait_ok()
        })
        wait()
      }
      // lmap.on("click", function(){
      //   close_menu();
      // })

      feature_layer.on("click", function (e) {
          console.log(e)
          if  (from_point_loc == null){
              if ( e.layer.hasOwnProperty("_latlng") ){
                // close_menu();
                show_menu(relX, relY);  
                console.log(e)
                cursor_fearture = e.layer.feature

              } 
              from_loc = e.latlng
              
              
              // lmap.on("mousemove", onmousemoveF)
              // drawline(from_loc);
              load_sao();


              
              get_links(cursor_fearture.properties.name, e.latlng)
              // close_menu()

          }else{
              end_loc = e.layer._latlng
              second_cursor_feature = e.layer.feature
              lay = line_layer._layers[dylamic_line_id]
              lay.setLatLngs([from_loc, end_loc])
              lmap.off("mousemove", onmousemoveF)
              from_point_loc = null;
              from_loc = null
              dylamic_line_id = null;
              console.log("Here")
              show_in("#panel-input", relX, relY)
              setTimeout(function () {
                $("#panel-input-opened").animate({
                  'left': '-=' + get_width("#panel-input-opened") ,
                  'top': '-=' + (get_height("#panel-input-opened") * 0.6)
                });
              },500)

              // lmap.on('click', function(e){ 
                // console.log(e.latlng)
                
              // });
          }
      })
      ondraging = function(change){
        change_in("#handle-menu-opened", change.x,change.y)
      }
      // onmousedown = function(e){

      // }
      
      cities_layer.addLayer(feature_layer)
    // cities_layer.addLayer(tor_exit_layer);

    // console.log(data);
    // $.each(data, function(i, item){
    //     p = item['geo']
    //     l = item['desc']
    //     console.log(l)
    //     if (!IP_GEO_DATA.hasOwnProperty(l)){
    //         L.marker(p).addTo(lmap).bindPopup(l).openPopup();
    //         IP_GEO_DATA[l] = p
    //     }

    // })
    
    $(".token-dialog").modal("show")

  });
}


function wait(){
  $("body").css("filter","blur(15px)")
}

function wait_ok(){
  $("body").css("filter","blur(0px)")
}

function show_menu(x,y){
    $("#handle-menu").css({
        "left": x,
        "top":y
    })
    $("#handle-menu").collapse("show");
    $("#handle-menu").attr("id","handle-menu-opened");
    load_sao();
}


var relX = null;
var relY = null;
$("body").mousemove(function(e){
   var parentOffset = $(this).offset();
   relX = e.pageX - parentOffset.left;
   relY = e.pageY - parentOffset.top;
   

});

function search_geo(geo_name, callback){
  $.ajax({
    type: "POST",
    url: "/search_geo",
    data: {
    name:geo_name
    },
    success: function( data ) {
        var items = [];

        console.log(data);
        if (callback != null){
            callback(data);
        }
    },
    dataType: 'json'
  });
}


function JsonPost(url, data, callback){
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        success: function( data ) {
            console.log(data);
            if (callback != null){
                callback(data);
            }
        },
        dataType: 'json'
    });
}

function JsonGet(url, callback){
    $.getJSON(url, callback);
}

function go_to(ip){
    IP_GEO_DATA.forEach(function(d){
        if (ip.indexOf(d.properties.name) != -1 ){
            l = d.geometry.coordinates
            lmap.zoomOut(2)
            lmap.flyTo([l[1],l[0]],4)
            
            w = cities_layer.getLayers()[0]
            ks = Object.keys(w._layers)
            m = null
            ks.forEach(function(k){
                ipp = w._layers[k].feature.properties.name
                if (ipp == ip){
                    m = w._layers[k]
                }
            })

            if (m){
                m.openPopup()
            }
            
        }
        
    })
    $(".popover").popover("destroy");
}

