var app = new Vue({    
    el: "#app",   
    data:{     
        participantes: "" , 
        premios: 1, 
        ganadores: false, 
        arrayGanadores: []
     },    
    methods:{  
        borrarNombres(){
            $("#participantes").val('')
        },
      async  Sortear(){
          if(this.participantes == ''){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Debes agregar participantes',
              })
              return false
          }
            var lines = [];
            $.each($('#participantes').val().split(/\n/), function(i, line){
                if(line){
                    lines.push(line);
                } else {
                    lines.push("");
                }
            });

            if(lines.length <=1){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Debes agregar al menos 2 participantes',
                  })
                  return false
              }

              if(this.premios > lines.length){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'El numero de premios no puede ser mayor que los participantes',
                  })
                  return false
              }

        await axios.get($SCRIPT_ROOT + '/_sortear1', {
            params: {
                participantes: JSON.stringify(lines),
            premios: this.premios
              }
            }).then(response => {
                console.log(response)
                    this.ganadores = true
                    this.arrayGanadores = response.data.ganadores
            })

        }
       },      
   
    });
