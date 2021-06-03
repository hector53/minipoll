
var app = new Vue({    
    el: "#app",   
    data:{     
        opcionEncuesta: ['', ''],
        cantidadOpciones: 0,
        preguntaEncuesta: "",   
        codigoEncuesta: "", 
        opcionEncuestaNuevo: []
     },    
    methods:{  
        crearEncuesta(){
            if(this.preguntaEncuesta==''){
              Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Debes realizar una pregunta',
              })
              return false
            }

            for(i=0; i<this.opcionEncuesta.length; i++){
              if(this.opcionEncuestaNuevo[i] == ''){
                Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Opción '+(i+1)+' vacía',
                })
                return false
              }

            }
            //aqui si enviar a guardar la encuesta 
            $.LoadingOverlay("show");
              $.ajax({
              type: "POST",
              url: $SCRIPT_ROOT + '/_guardar_encuesta_editar',
              data: {"pregunta":this.preguntaEncuesta, "codigo": this.codigoEncuesta,
               "opciones": JSON.stringify(this.opcionEncuesta), "opcionesNuevas": JSON.stringify(this.opcionEncuestaNuevo)
              },
              success: function(response)
              {
                if(response.status != 0){
                  $.LoadingOverlay("hide");
                  Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Actualizado con exito',
                    showConfirmButton: false,
                    timer: 1500
                  })
                    }else{
                  $.LoadingOverlay("hide");
                }
              }
              });
          }, 
          reducirOpcionesNuevo(index){
            this.opcionEncuestaNuevo.splice(index,1)
          },
       reducirOpciones(index) {
              Swal.fire({
                title: '¿Estas seguro que quieres borrar esta opción ? ',
                html: 'Se perderan todas las votaciones realizadas en ella',
                showCancelButton: true,
                confirmButtonText: `Si borrar`,
                denyButtonText: `No Cancelar`,
              }).then((result) => {
                /* Read more about isConfirmed, isDenied below */
                if (result.isConfirmed) {
                  $.LoadingOverlay("show");
                  //borrar
                   axios.get($SCRIPT_ROOT + '/_delete_option_encuesta',  {
                    params: {
                      id_opcion: this.opcionEncuesta[index]["id"], 
                      cod_encuesta: this.codigoEncuesta
                    }
                  }).then((response) => {
                    console.log(response)
                    $.LoadingOverlay("hide");
                    if(response.data.status != 0){
                      this.opcionEncuesta = response.data.opciones
                      
                    }else{
                      Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: 'Error',
                        showConfirmButton: false,
                        timer: 1500
                      })
                    }
                        
                  });
                } 
              })
          },
          addOpcion() {
            this.opcionEncuestaNuevo.push('')
          },
        async getEncuesta(id){
            await axios.get($SCRIPT_ROOT + '/_get_encuesta_editar',  {
              params: {
                codigo: id
              }
            }).then((response) => {
              console.log(response)
                  this.opcionEncuesta = response.data.opciones
                  this.preguntaEncuesta = response.data.encuesta[1]
                  $("#seccionEncuesta").show();
            });
          }
       },      
    mounted: function(){    
 var pathname = window.location.pathname; 
      if(pathname != '/'){
          var param = pathname.substr(1,5)
          this.codigoEncuesta = param
          this.getEncuesta(param)
      }
    },    
    computed:{

    }    
    });
