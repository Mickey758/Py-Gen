const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function genaccount(){
    var name = document.getElementById("gen").value;
    var genbtn = document.getElementById("genbtn");
    if (name === "disabled"){
        genbtn.disabled = true;
        Toast.fire({
            icon: 'info',
            text: 'Select a gen from the dropdown menu'
        })
    }
    else{
        r = new XMLHttpRequest();
        r.open("GET","/gen?name="+name,"True")
        r.send();
        r.onload = function (){
            if (r.status === 200){
                Swal.fire({
                    title:"Account Info",
                    icon:"success",
                    confirmButtonColor:"#4f4f4f",
                    text:r.response
                })
            }
            else if (r.status === 202){
                genbtn.disabled = true;
                Toast.fire({
                    icon: 'warning',
                    text: 'That gen type is out of stock'
                })
            }
            else if (r.status === 404){
                genbtn.disabled = true;
                Toast.fire({
                    icon: 'error',
                    text: 'That gen type does not exist'
                })
            }
            else if (r.status === 429 || r.response === "Generating too fast"){
                Toast.fire({
                    icon: 'error',
                    text: 'Wait at least 5 seconds before generating another account!'
                })
            }
            else{
                Toast.fire({
                    icon: 'error',
                    text: 'An error occured'
                })
            }
        }
    }
}
$(document).ready(function() { 
    var genbtn = document.getElementById("genbtn");
    var info = document.getElementById("gen");
    if (info.value === "disabled"){
        genbtn.disabled = true
    }
    $('#gen').change(function() {
        if ($(this).val() === 'disabled') {
            genbtn.disabled = true
            Toast.fire({
                icon: 'info',
                text: 'Select a gen from the dropdown menu'
            })
        }
        else{
            genbtn.disabled = false
            var name = $(this).val();
            var r = new XMLHttpRequest();
            r.open("GET","/stock?name="+name,true);
            r.send();
            r.onload = function (){
                if (r.status === 200){
                    Toast.fire({
                        icon: 'info',
                        text: 'That gen type has '+r.response+' accounts in stock'
                    })
                }
                else if (r.response === "0" || r.status === 202){
                    genbtn.disabled = true
                    Toast.fire({
                        icon: 'warning',
                        text: 'That gen type is out of stock'
                    })
                }
                else if (r.status === 404){
                    genbtn.disabled = true
                    Toast.fire({
                        icon: 'error',
                        text: 'That gen type does not exist'
                    })
                }
                else{
                    Toast.fire({
                        icon: 'error',
                        text: 'An error occured'
                    })
                }
            }
        }
    });
});