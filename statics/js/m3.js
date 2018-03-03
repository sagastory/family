function sendinvote(event, fid, targetpid, invotepid, invotename) {
    event.preventDefault()
    var phone = $('#mobile').val();
    if (phone == '') {
        return;
    }
    //alert(phone);
    $.post('/invote', {
            fid: fid,
            phone: phone,
            targetpid: targetpid,
            invotepid: invotepid,
            invotename: invotename
        },
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
            //alert(data);
            $('#invode').modal('hide');
            //success_prompt("邀请成功!");
            toastr.success("邀请成功!");

        });

}


