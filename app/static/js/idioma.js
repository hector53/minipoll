function setCookie(cname, cvalue, exdays) {
   var d = new Date();
   d.setTime(d.getTime() + (exdays*24*60*60*1000));
   var expires = "expires="+ d.toUTCString();
   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
 }

 function getCookie(cname) {
   var name = cname + "=";
   var decodedCookie = decodeURIComponent(document.cookie);
   var ca = decodedCookie.split(';');
   for(var i = 0; i <ca.length; i++) {
     var c = ca[i];
     while (c.charAt(0) == ' ') {
       c = c.substring(1);
     }
     if (c.indexOf(name) == 0) {
       return c.substring(name.length, c.length);
     }
   }
   return "";
 }
 var cookieIdioma = getCookie('resultAppLang')
 if(cookieIdioma){
      console.log("hola")
 }else{
    //crear
    setCookie('resultAppLang', '0', 1000)
 }

var app = new Vue({    
    el: "#appLang",   
    data:{     
     },    
    methods:{  
          cambiarIdioma(lang){
         
           $.ajax({
             type: "POST",
             url: $SCRIPT_ROOT + '/_cambiar_idioma',
             data: {
                lang: lang
             },
             success: function(response)
             {
                location.reload();
             }
             });
           },
       },      
   
    });
