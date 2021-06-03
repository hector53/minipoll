const  generateRandomString = (num) => {
  const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result1= '';
  const charactersLength = characters.length;
  for ( let i = 0; i < num; i++ ) {
      result1 += characters.charAt(Math.floor(Math.random() * charactersLength));
  }

  return result1;
}
var app = new Vue({    
  el: "#app",   
  data:{     
      opcionEncuesta: ['', ''],
      cantidadOpciones: 2,
      preguntaEncuesta: "",  
      codigoBuscador: ""  
   },    
  methods:{  
  
    votar(id){
      alert("votar por la "+id)
    },
      reducirOpciones(index) {
          this.opcionEncuesta.splice(index,1)
        },
        addOpcion() {
          this.opcionEncuesta.push('')
        },
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
            if(this.opcionEncuesta[i] == ''){
              Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Opcion '+(i+1)+' vacia',
              })
              return false
            }

          }
          //aqui si enviar a guardar la encuesta 
          $.LoadingOverlay("show");
            $.ajax({
            type: "POST",
            url: $SCRIPT_ROOT + '/_guardar_encuesta',
            data: {"pregunta":this.preguntaEncuesta, "opciones": JSON.stringify(this.opcionEncuesta), miCodigo: generateRandomString(5)
            },
            success: function(response)
            {
              if(response.status != 0){
                $.LoadingOverlay("hide");
               location.href = '/'+response.codigo
              }else{
                $.LoadingOverlay("hide");
              }
            }
            });
        }, 
     },      
  mounted: function(){    

  },    
  computed:{

  }    
  });
