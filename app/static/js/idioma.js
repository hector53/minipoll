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
