$.getJSON("_getmemos", {}, 
          function(data) {
            rsl = data.result.memos;
            var now = moment()
            var memo;
            var human;

            for(i = 0; i < rsl.length; i++) {
              //human = rsl[i].human;
              title = rsl[i].title;
              date = moment.unix(rsl[i].date).local();
              human = now.diff(date, 'days')
              date = date.format()
              // console.log("Got a day! It's " + human);
              var a_html_code = "";
              if (typeof has_login != "undefined" && has_login) {
                a_html_code += "<input type=\"checkbox\" name=\"memo_selected\">";
              }
              a_html_code += "<label hidden>" + title + "</label>";
              a_html_code += "<label hidden>" + date + "</label>";
              a_html_code += "<button name=\"details_view\" onclick=\"show_details(this)\" class=\"link\"><label>" + title + "</label></button>";
              a_html_code += "<label>" + date + "</label><br>";
              a_html_code = "<div class=\"col-md-4\">" +  "<div class=\"fh5co-blog animate-box\">" + a_html_code + "</div></div>"
              if (human == 0){
                $("#today").append(a_html_code);
              } else if (human < 0) { 
                $("#incoming").append(a_html_code);
              } else{
                $("#past").append(a_html_code);
              }
            }
          }
  );

function load_date_time(yyyy, mm, dd, hh, min, secs) {
  $("#setting_date").append("<label>Memo Date</label>");
  $("#setting_date").append("<input type=number name=\"memo_year\" id=\"memo_year\" value=" + yyyy +   " min=\"1970\" max=\"2032\"  />");
  $("#setting_date").append("<input type=number name=\"memo_month\" id=\"memo_month\" value=" + mm +   " min=\"1\" max=\"12\" />");
  $("#setting_date").append("<input type=number name=\"memo_day\" id=\"memo_day\" value=" + dd +   " min=\"1\" max=\"31\" />");
  $("#setting_date").append("<input type=number name=\"memo_hour\" id=\"memo_hour\" value=" + hh + " min=\"0\" max=\"23\"  />");
  $("#setting_date").append("<input type=number name=\"memo_min\" id=\"memo_min\" value=" + min + " min=\"0\" max=\"59\"  />");
  $("#setting_date").append("<input type=number name=\"memo_sec\" id=\"memo_sec\" value=" + secs + " min=\"0\" max=\"59\"  />");
}

function load_text_area() {
  $("#main_input").append("<input type=\"text\" name=\"memo_title\" id=\"memo_title\" placeholder=\"title\" autofocus /><br>");
  $("#main_input").append("<textarea rows=\"4\" style=\"height:400px;width:600px;\" name=\"input_memo\" id=\"input_memo\" placeholder=\"body\"/>");
}


function show_details(btn){
    var memo_title = $(btn).text()
    var date_time = $(btn).next('label').text()
    console.log(memo_title, date_time)
          
    $.getJSON("_getDetailedMemo", {date_time : date_time, memo_title : memo_title}, 
        function(data) {
          rsl = data.result.memos;
          $("#temp_window").html("<div class=\"row\"><p id=\"main_input\"></p></p></div>")
          $("#main_input").append("<input type=\"text\" name=\"memo_title\" id=\"memo_title\"><br><div id=\"Body_article\"></div>")
          
          $("#memo_title").val(rsl.title)
          if('text' in rsl){
          	var converter = new showdown.Converter({extensions: ['table']})
          	var html = converter.makeHtml(rsl.text)
            $("#Body_article").html(html)
          }

          
          $("#dialog").dialog({
            resizable: true,
            autoResize:true,
            height: "auto",
            width: "auto",
            title: "Details",
            buttons:{}
          })
                
        })
  }

$(document).ready(function(){
  $("#Delete_selected_memos").click(
      function(){
        var all_selected_text = {};
        $('input[name="memo_selected"]:checked').each(
            function(){
              var title = $(this).next('label').text(); // memo_text
              $(this).next('label').remove();
              var date = $(this).next('label').text(); // memo_date
              date = moment(date, "YYYY-MM-DD HH:mm:ss").unix()
              
              
              all_selected_text[date] = title;
            }
        ).promise().done($.ajax({
                          type: 'POST',
                          contentType: 'application/json',
                          url: '_delmemos', 
                          dataType: 'json',
                          data: JSON.stringify(all_selected_text),
                          error: function(result) {console.log(result)},
                          success: function(result) {location.reload()}
                          }))
      }
  )

  $("#check_all").click(
      function(){
        if($('input[name="memo_selected"]').length == $('input[name="memo_selected"]:checked').length) {
          $('input[name="memo_selected"]').prop('checked', false);  
        } else {
          $('input[name="memo_selected"]').prop('checked', true);
        }
        
      }
  )

  $("#Add_memo").click(
    function(){
      var today = new Date();
     
      var yyyy = today.getFullYear();
      var mm = today.getMonth()+1; //January is 0!
      var dd = today.getDate();
      var hh = today.getHours();
      var min = today.getMinutes();
      var secs = today.getSeconds();

      if(dd<10){
        dd='0'+dd;
      } 
      if(mm<10){
        mm='0'+mm;
      } 
      if(hh<10){
        hh='0'+hh;
      }
      if(min<10){
        min='0'+min;
      }
      $("#temp_window").html("<div class=\"row\"><p id=\"setting_date\" /></div>")
      $("#temp_window").append("<div class=\"row\"><p id=\"main_input\" /></div>")
      $("#temp_window").append("<div id=\"result\" name=\"result\" />");

      load_date_time(yyyy, mm, dd, hh, min, secs);
      load_text_area();

      $("#dialog").dialog({
        resizable: true,
        autoResize:true,
        height: "auto",
        width: "auto",
        title: "Add a memo",
        cache: false,
        buttons: {
          "Preview": function(){
            console.log("Rendering!")
            var text = $("#input_memo").val();
            var converter = new showdown.Converter({extensions: ['table']});
            var html = converter.makeHtml(text);
            $("#result").html(html);
          },
          "Submit": function(){ // "2017-11-01 10:30:30"
            var date_time = $("#memo_year").val() +'-'+ $("#memo_month").val() +'-'+ $("#memo_day").val() + ' ' + $("#memo_hour").val() +':'+$("#memo_min").val() +':'+ $("#memo_sec").val();
            date_time = moment(date_time, "YYYY-MM-DD HH:mm:ss").unix()
            $.getJSON("_sendmemo", {date_time : date_time, title : $("#memo_title").val(), memo : $("#input_memo").val()}, function(data) {window.location.reload(true);});}
        }
      })

    });

});