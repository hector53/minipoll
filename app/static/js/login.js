var app = new Vue({    
    el: "#app",   
    data:{     
        email: '', 
        pass: '', 
        reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
     },    
    methods:{  
        Login(){
            if(this.email == ''){
                $( "#email" ).focus();
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Email required',
                  })
                  return false
            }
            if(!this.reg.test(this.email)){
                $( "#email" ).focus();
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Email incorrecto',
                  })
                  return false
            }
            if(this.pass == ''){
                $( "#pass" ).focus();
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Pass required',
                  })
                  return false
            }
            $.LoadingOverlay("show");
            $.ajax({
            type: "POST",
            url: $SCRIPT_ROOT + '/_login_user',
            data: { "email": this.email,  "pass": this.pass
            },
            success: function(response)
            {
              if(response.status == 1){
                $.LoadingOverlay("hide");
               location.href = '/dashboard'
              }else{
                  if(response.status == 2){
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'email or password incorrect',
                      })
                    $.LoadingOverlay("hide");
                  }else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'data incorrect',
                      })
                  }
                
              }
            }
            });
            }
       },
       mounted() {
        $( "#email" ).focus();
       },      
   
    });
