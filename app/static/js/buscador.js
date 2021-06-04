var app = new Vue({    
    el: "#appB",   
    data:{     
        codigoBuscador: ""  
     },    
    methods:{  
        async  buscarEncuesta(){
            if(this.codigoBuscador == ''){
             Swal.fire({
               icon: 'error',
               title: 'Oops...',
               text: 'Debes insertar un codigo',
             })
             return false
            }
           $.LoadingOverlay("show");
           $.ajax({
             type: "POST",
             url: $SCRIPT_ROOT + '/_buscar_encuesta_codigo',
             data: {
               codigo: this.codigoBuscador
             },
             success: function(response)
             {
               console.log(response)
               $.LoadingOverlay("hide");
               if(response.status != 0){
                location.href = '/p/'+response.codigo
               }else{
                 Swal.fire({
                   icon: 'error',
                   title: 'Oops...',
                   text: 'Codigo no existe',
                 })
               }
             }
             });
           },
       },      
   
    });
