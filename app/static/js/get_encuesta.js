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

var user = getCookie('uPoll')
var pathname = window.location.pathname; 
var cod = pathname.substr(1)
console.log(user)
var socket = io();
socket.on('connect', function() {
  socket.emit('conectar', {
    username: user,
    room: cod
  });



});

socket.on('join_room_announcement', function (data) {
  console.log(data);
  if (data.username !== user) {
    console.log(`<b>${data.username}</b> has joined the room`)
}
  //aqui podemos decir si el usuario es diferente entonces anunciarlo
});

socket.on('respuestaDelVoto', function (data) {
console.log("llego respuesta")
    if (data.username !== user) {
    console.log("respuesta del voto de alguien mas");
    app.getEncuesta(cod)
    }
 
});





var app = new Vue({    
    el: "#app",   
    delimiters: ['{$', '$}'],
    data:{     
        opciones: [], 
        preguntaGetEncuesta: "", 
        id_encuesta: "", 
        totalVotos: "",
        codigoEncuesta: "",
        qrCode: false, 
        yaVote: false, 
        capturar: 0, 
        resultados: false, 
        actualizaVoto: false, 
        colores: [
          '#ffaf59', 
          '#59b1ff', 
          '#59ffbf', 
          '#FF5252', 
          '#FF96E0', 
          '#BDC3C7', 
          '#F53B86', 
          '#E3500D',
          '#C287E8',
          '#8AD3A0', 
          'transparent'
        ], 
        miVoto: 0, 
        miVotoViejo: 0
     },    
    methods:{  
      
      copyLink(Url, tipo){
        const el = document.createElement('textarea');
        el.value = Url;
        el.setAttribute('readonly', '');
        el.style.position = 'absolute';
        el.style.left = '-9999px';
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        var copia; 
        if(tipo == 1){
          copia = "Link"
        }else{
          copia = "#"+this.codigoEncuesta
        }
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: copia+' copiado con exito',
          showConfirmButton: false,
          timer: 1500
        })
      },
     async cancelarVoto(){
        await axios.get($SCRIPT_ROOT + '/_cancelar_voto',  {
          params: {
            id_encuesta: this.id_encuesta
          }
        }).then((response) => {
         //   console.log(response)
            if(response.data.status == 1){
              
              this.actualizaVoto = false
              this.miVoto = 0
              this.getEncuesta(this.codigoEncuesta)
            }else{
              Swal.fire({
                position: 'center',
                icon: 'error',
                title: 'Error al cancelar el voto',
                showConfirmButton: false,
                timer: 1500
              })
            }
          
        });
      },
      mostrarQr(){
        this.qrCode = !this.qrCode
        $("#seccionEncuesta").show();
      },
     async votar(id){
      $.LoadingOverlay("show");
        await axios.get($SCRIPT_ROOT + '/_votar_',  {
            params: {
              id_opcion: id, 
              id_encuesta: this.id_encuesta
            }
          }).then((response) => {
            $.LoadingOverlay("hide");
            if(response.data.result ==  1){
               
                  this.resultados = true
                  this.actualizaVoto = true
                 
            }

            if(response.data.result ==  2){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Ya has realizado tu voto',
                  })
                  this.actualizaVoto = false
            }

            if(response.data.result ==  3){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Error desconocido',
                  })
                  this.actualizaVoto = false
            }
            if(response.data.result ==  0){
              Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Ya tienes un usuario registrado en este dispositivo debes iniciar sesion',
                confirmButtonText: `OK`,
              }).then((result) => {
                if (result.isConfirmed) {
                  location.href = '/login'
                }
              })
          }
            
          });

          if(this.actualizaVoto){
            console.log("votare")
            await this.getEncuesta(this.codigoEncuesta)
            this.capture(2)
            Swal.fire({
              position: 'center',
              icon: 'success',
              title: 'Votación exitosa',
              showConfirmButton: false,
              timer: 1500
            })
          }


      },
        
          async getEncuesta(id){
            await axios.get($SCRIPT_ROOT + '/_get_encuesta',  {
              params: {
                codigo: id
              }
            }).then((response) => {
                console.log(response)
              if(response.data != 0){
               //   console.log("estoy")
                  this.opciones = response.data.opciones
                  this.preguntaGetEncuesta = response.data.encuesta[1]
                  this.id_encuesta = response.data.encuesta[0]
                  this.totalVotos = response.data.totalVotos
                  if(response.data.siVote == 1){
                    this.yaVote = true
                    this.resultados = true
                  }else{
                    this.yaVote = false
                    this.resultados = false
                  }
                  if(response.data.miVoto != 0){
                      this.miVoto = response.data.miVoto
                  }

                  
                  $(".cubreEncuesta").show();
                  $(".cubreLoader").hide();

                  if(response.data.encuesta[5]==0){
                    this.capturar = 1
                  }
                  if(response.data.resultado == 1){
                    this.resultados = true

                    if(response.data.encuesta[6]==0){
                      this.capturar = 2
                    }

                  }
              }
            });
          }, 
          detectaTecla(event){
            console.log(event.keyCode)
            console.log(event.ctrlKey)
            if(event.ctrlKey == false && this.yaVote){
            if(event.keyCode === 67){
              //cancelar voto tecla C
              this.cancelarVoto()
            }
          }

          if(event.keyCode === 85){
            //copiar url 
            this.copyLink(window.location.href, 1)
          }

          if(event.keyCode === 72){
            //copiar url 
            this.copyLink(this.codigoEncuesta, 2)
          }
            var tecladoArriba = 49
            var tecladoDerecho = 97
            
            for(i=0; i<9; i++){
            
                if(event.keyCode === (tecladoArriba+i) || event.keyCode === (tecladoDerecho+i)){
                  //presiono la tecla 1
                  if(this.opciones.length >= (i+1)){
                      //si tengo esta cantidad de opciones por lo tanto puedo votar
                      this.votar(this.opciones[i]["id"])
                  }else{
                    Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'No existe esa opción',
                    })
                  }
              }
              
                  
            }
          

          }, 
         async capture(tipo){
            
            $(".text-block-8").hide();
            $(".div-block-11").hide();
            $(".submit-button-3").hide();
            $(".link-2").hide();
            $(".radio-button-field ").css("width", "98%");
            this.miVotoViejo = this.miVoto
            this.miVoto = 0
            
            html2canvas(document.querySelector(".section-hero")).then(canvas => {
           // document.body.appendChild(canvas)
              var capture = canvas.toDataURL("image/png")
            //  console.log(capture)
              //ahora enviarla por post y guardarla 
              $.ajax({
                type: "POST",
                url: $SCRIPT_ROOT + '/_guardar_capture',
                data: {capture: capture, codigo: this.codigoEncuesta, tipo:tipo
                },
                success: function(response)
                {
                  
                  console.log(response)
                }
                });
          });
          

          $(".text-block-8").show();
          $(".div-block-11").show();
          $(".submit-button-3").show();
          $(".link-2").show();
          $(".radio-button-field ").css("width", "100%");
          this.miVoto = this.miVotoViejo
          this.miVotoViejo = 0
        
          
          }
          
       },      
  async  mounted(){   
      window.addEventListener('keyup', this.detectaTecla)  
      var pathname = window.location.pathname; 
      if(pathname != '/'){
          var param = pathname.substr(3)
          this.codigoEncuesta = param
         await this.getEncuesta(param)
          if(this.capturar == 1){
            this.capture(1)
          }
          if(this.capturar == 2){
            this.capture(2)
          }
      }
   
    },    
    computed:{

    }    , 
    destroyed() {
      window.removeEventListener('keyup', this.solteTecla)
    },
    });
