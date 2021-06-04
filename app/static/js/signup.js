var app = new Vue({    
    el: "#app",   
    data:{     
        firstName: '', 
        lastName: '', 
        userName: '', 
        email: '', 
        pass: '', 
        reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
     },    
    methods:{  
        signup(){
            if(this.firstName == ''){
                $( "#firstName" ).focus();
                lastName
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'First Name required',
                  })
                  
                  return false

            }
            if(this.lastName == ''){
                $( "#lastName" ).focus();
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Last Name required',
                  })
                  return false
            }
           
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
            if(this.userName == ''){
                $( "#username" ).focus();
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'User Name required',
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
            url: $SCRIPT_ROOT + '/_registrar_user',
            data: {"firstName": this.firstName, "lastName": this.lastName, "email": this.email, "userName":this.userName,
            "pass": this.pass
            },
            success: function(response)
            {
              if(response.status != 0){
                $.LoadingOverlay("hide");
               location.href = '/dashboard'
              }else{
                $.LoadingOverlay("hide");
              }
            }
            });
        }
       },
       mounted() {
        $( "#firstName" ).focus();
       },      
   
    });
