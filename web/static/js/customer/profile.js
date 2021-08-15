$(document).ready(()=>{

    var url_update = $("#profile-script").attr("data-url-form")
    var question_sent_title = $('#profile-script').attr('data-question-sent-title')
    var question_error_title = $('#profile-script').attr('data-question-error-title')
    var question_sent_body = $('#profile-script').attr('data-question-sent-body')
    var csrf_token = $('#profile-script').attr('data-csrf-token')

    $("#btn-update").click(()=>{

        var form = document.getElementById("form")
        // We prevent the form from being sent
        event.preventDefault();

        // If the form isn't valid
        if (!form.checkValidity()) {
            return false
        }
        $(".lu").removeClass("sr-only")
        $("#btn-update").prop("disabled",true)

        var first_name = $("#id_first_name").val()
        var last_name = $("#id_last_name").val()
        var request = $.ajax({
            "type": "POST",
            "url": url_update,
            "data":{
                "csrfmiddlewaretoken":csrf_token,
                "first_name":first_name,
                "last_name":last_name,
            }
        });
        request.done((response)=>{
            if(response.success){
                swal({
                    title: question_sent_title+first_name+"!",
                    text: question_sent_body
                })
                $("#id_first_name").val(first_name)
                $("#id_last_name").val(last_name)
                $(".first-name").html(first_name)
                $(".full-name").html(first_name+" "+last_name)
            }else{
                swal({
                    title: question_error_title,
                    text: response.response
                })
            }
            $("#btn-update").prop("disabled",false)
            $(".lu").addClass("sr-only")
        })
    })

    var url_delete= $("#profile-script").attr("data-url-delete-form")
    $("#btn-delete").click(()=>{
        $(".ld").removeClass("sr-only")
        $("#btn-delete").prop("disabled",true)

        var name = $("#id_name").val()
        console.log(name)
        var request = $.ajax({
            "type": "POST",
            "url": url_delete,
            "data":{
                "csrfmiddlewaretoken":csrf_token,
                "name":name,
            }
        });
        request.done((response)=>{
            console.log(response)
            if(response.success){
                window.location.href = $("#profile-script").attr("data-site-root")
            }else{
                swal({
                    title: question_error_title,
                    text: response.response
                })
            }
            $("#btn-delete").prop("disabled",false)
            $(".ld").addClass("sr-only")
        })
    })
})
