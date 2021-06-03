
var app = new Vue({    
    el: "#app",   
    delimiters: ['{$', '$}'],
    data:{     
        misEncuestas: [], 
        cantVotos: 0, 
        cantEncuestas: 0
     },    
    methods:{  
      
        eliminarEncuesta(id){
            Swal.fire({
                title: '¿Estas seguro que quieres borrar esta encuesta ? ',
                html: 'Se perderan todas las votaciones realizadas en ella',
                showCancelButton: true,
                confirmButtonText: `Si borrar`,
                denyButtonText: `No Cancelar`,
              }).then((result) => {
                if (result.isConfirmed) {
                  //borrar
                  $.LoadingOverlay("show");
                  axios.get($SCRIPT_ROOT + '/_delete_encuesta',  {
                    params: {
                        id:id
                    }
                  }).then((response) => {
                    console.log(response)
                    $.LoadingOverlay("hide");
                    if(response.data.status != 0){
                        var encuestas = response.data.encuestas
                        if(encuestas.length == 0){
                            $("#seccionPanel").hide();
                            $("#sinEncuestas").show();
                        }
                        this.misEncuestas = response.data.encuestas
                      Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: 'Borrado con exito',
                        showConfirmButton: false,
                        timer: 1500
                      })
                    }else{
                      Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: 'Error al borrar la encuesta',
                        showConfirmButton: false,
                        timer: 1500
                      })
                    }
                        
                  });


                   
                } 
              })

            
        },

        
          async getEncuesta(){
            await axios.get($SCRIPT_ROOT + '/_get_panel').then((response) => {
              console.log(response)
                if(response.data.status != 0){
                    this.misEncuestas = response.data.encuestas
                    this.cantVotos = response.data.cantVotos
                    this.cantEncuestas = response.data.cantEncuestas
                    $("#loader").hide();
                    $(".section-hero").show();
                }else{
                  $("#loader").hide();
                    $("#sinEncuestas").show();
                }
            
            });
          }
       },      
    mounted: function(){   
        this.getEncuesta()
    },    
    computed:{

    }    
    });
