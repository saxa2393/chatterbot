
      //create a message wrapper to connect easily every QA with a button
      function createMessageWrapper() {
        var wrapper = document.createElement('div');
        wrapper.className = 'wrapper'
        return wrapper;
      }

      //create a <span> element inside a <p> element and apende the given text(response)
      function createText(rawText, className) {
        var text = document.createElement('p');
        text.className = className;

        var textSpan = document.createElement('span');
        textSpan.innerText = rawText;

        $(text).append(textSpan);
        return text;
      }
      
      //A function to detect and return a link "http:...." inside a text 
      //To do this we use regular expresion      
      function urlify(text) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        var url = text.match(urlRegex);
        return url;
      }


      // What to do when the user evaluate the answer with 1 or 2 stars . Take userText and botText and send them to python           
      function onBadBtnClick() {
        var parent1 = $(this).parent('.rating');
        var parent = $(parent1).parent('.wrapper');
        var userText = parent.find('.userText').text();
        var botText = parent.find('.botText').text();

        $.get("/badResponse", {userText: userText,botText: botText}).done(function (data) {

        });
      }
      /* a function that get the feedback from the user(star evaluation 3 stars) and send data to python in order to create the json file */
      function changeClassName1() {
        var parent1 = $(this).parent('.rating');
        var parent = $(parent1).parent('.wrapper');
        var userText = parent.find('.userText').text();
        var botText = parent.find('.botText').text();

        var t3 = $(parent1).find('span[data-star="3"]');
        var t2 = $(parent1).find('span[data-star="2"]');
        var t1 = $(parent1).find('span[data-star="1"]');
        $(t1).toggleClass('checked')
        $(t2).toggleClass('checked')
        $(t3).toggleClass('checked')
        $(t3).attr('id','star checked')
        $(t2).attr('id','star checked')
        $(t1).attr('id','star checked')

        $(t1).unbind("click");
        $(t2).unbind("click");
        $(t3).unbind("click");
        var x =$(parent1).find('span[class="fa fa-star checked"]');
        $(x).attr('data-star', '0');

        $.get("/userFeedback", {userText: userText,botText: botText,userFeed: '3',}).done(function (data) {

        });            

      }
      /* a function that get the feedback from the user(star evaluation 2 stars) and send data to python in order to create the json file */

      function changeClassName2() {
        var parent1 = $(this).parent('.rating');
        var parent = $(parent1).parent('.wrapper');
        var userText = parent.find('.userText').text();
        var botText = parent.find('.botText').text();

        var t3 = $(parent1).find('span[data-star="3"]');
        var t2 = $(parent1).find('span[data-star="2"]');
        var t1 = $(parent1).find('span[data-star="1"]');
        
        $(t1).toggleClass('checked')
        $(t2).toggleClass('checked')
        $(t3).attr('id','star checked')
        $(t2).attr('id','star checked')
        $(t1).attr('id','star checked')
        $(t1).unbind("click");
        $(t2).unbind("click");
        $(t3).unbind("click");
        var x =$(parent1).find('span[class="fa fa-star checked"]');
        $(x).attr('data-star', '0');
        var y =$(parent1).find('span[class="fa fa-star"]');
        $(y).attr('data-star', '0');
        $.get("/userFeedback", {userText: userText,botText: botText,userFeed: '2',}).done(function (data) {

        });
      }

      /* a function that get the feedback from the user(star evaluation 1 star) and send data to python in order to create the json file */
      function changeClassName3() {
        var parent1 = $(this).parent('.rating');
        var parent = $(parent1).parent('.wrapper');
        var userText = parent.find('.userText').text();
        var botText = parent.find('.botText').text();

        var t3 = $(parent1).find('span[data-star="3"]');
        var t2 = $(parent1).find('span[data-star="2"]');
        var t1 = $(parent1).find('span[data-star="1"]');

        $(t1).toggleClass('checked')
        $(t3).attr('id','star checked')
        $(t2).attr('id','star checked')
        $(t1).attr('id','star checked')
        $(t1).unbind("click");
        $(t2).unbind("click");
        $(t3).unbind("click");
        var x =$(parent1).find('span[class="fa fa-star checked"]');
        $(x).attr('data-star', '0');
        var y =$(parent1).find('span[class="fa fa-star"]');
        $(y).attr('data-star', '0');
        $.get("/userFeedback", {userText: userText,botText: botText,userFeed: '1',}).done(function (data) {

        });
      }
      // After user input , it creates a  div element to append the input as well as the response
      // the respone is taken from $.get("/get", { msg: rawText }).done(function (data) through python
      function getBotResponse() {
        //takes input from the user      
        var rawText1 = $("#textInput").val();
        if (rawText1 == "") {
          alert("Πρέπει να κάνεις μία ερώτηση");
          return false;
        }
        // Remove accents/diacritics in the string in JavaScript
        var rawText = rawText1.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
        var wrapper = createMessageWrapper();

        var userText = createText(rawText, 'userText')

        $(wrapper).append($(userText));

        $("#textInput").val("");
        $("#chatbox").append($(wrapper));

        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });

        $.get("/getResponse", { msg: rawText }).done(function (data) {
          var myLink = urlify(String(data));
          var botText = createText(data, 'botText');
          
          if (myLink!=null) {
            var myText = $(botText).find('span').text();
            var res = myText.replace(String(myLink), " ");
            $(botText).html("<span>"+ res +"<a href='" + myLink + "' class='link' target='_blank'>"+"ΕΔΩ"+"</a></span>");
          }

          $(wrapper).append($(botText));
          var sky = document.createElement('div');
          $(sky).addClass('rating');
          $(sky).attr('id', 'sky');



          var star = document.createElement('span');
          var star1 = document.createElement('span');
          var star2 = document.createElement('span');


          $(star).addClass('fa fa-star');
          $(star1).addClass('fa fa-star');
          $(star2).addClass('fa fa-star');
          $(star2).attr('id','star');
          $(star1).attr('id','star');
          $(star).attr('id','star');
          star.setAttribute('data-star', '3');
          star1.setAttribute('data-star', '2');
          star2.setAttribute('data-star', '1');

          $(star).click(changeClassName1)
          $(star1).click(onBadBtnClick)
          $(star1).click(changeClassName2)
          $(star2).click(onBadBtnClick)
          $(star2).click(changeClassName3)

          $(sky).append($(star));
          $(sky).append($(star1));
          $(sky).append($(star2));

          $(wrapper).append($(sky));

          document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
        });

      }
      $("#textInput").keypress(function (e) {
        if (e.which == 13) {
          getBotResponse();
        }
      });
      $("#buttonInput").click(function () {
        getBotResponse();
      });

