var mesgshow = new Vue({
    el: '#msglist',
    delimiters: ['${', '}'],
    data: {
        mesgs: {}
    },
    methods: {
        init: function () {
            $.ajax({
                url: '/',
                type: 'PUT',
                success: function (data) {
                    // Do something with the result
                    //alert(1);
                    mesgshow.mesgs = JSON.parse(data);
                }
            });
        },
        hidecomment: function (id1) {
            // alert(id1);
            $('#' + id1).toggle();
        },
        writecomment: function (id1, id2) {
            var nodevalue = document.getElementById(id1).value;
            if (!nodevalue) return;
            $.post('/writecomment', {
                    con: nodevalue,
                    mid: id1,
                    fid: id2
                },
                function (data, status) {
                    //alert("Data: " + data + "\nStatus: " + status);
                    //alert(data);
                    var revalue = JSON.parse(data);

                    mesgshow.mesgs.forEach(function (msg) {
                        if (msg[0][0] == id1) {
                            msg[2].push(revalue);

                            msg[2].sort(function (a, b) {
                                // Turn your strings into dates, and then subtract them
                                // to get a value that is either negative, positive, or zero.
                                return new Date(b[3]) - new Date(a[3]);
                            });
                        }
                        document.getElementById(id1).value = "";
                    });


                }
            );
        }
    }
})

mesgshow.init();


addDropzone.on("sending", function (file, xhr, data) {
    data.append("cmd", "create");
    //data.append("evid", eventid);
    //data.append("fid",$('#familyid').val());
})

$('#myFam2').on('shown.bs.modal', function () {
    //alert(1);
    var p = document.getElementById("createfid");
    p.setAttribute("value", headVue.fid);
    //alert(p.getAttribute("value"));
    var q = document.getElementById("createfphoto");
    q.setAttribute("value", headVue.fphoto);

    $('.datetimepicker').datetimepicker(
        {
        format: 'yyyy-mm-dd',
        autoclose: true,
        minView: 2,
        language: 'zh-CN'
    });
})

function createfinish(event) {
    event.preventDefault();
    $.ajax({
        cache: true,
        type: "POST",
        url: "/create",
        data: $('#memberinfo').serialize(), // 你的formid
        error: function (request) {
            //fail_prompt("Connection error");
            toastr.error("网络错误!");
        },
        success: function (data) {
            //alert(data);

            $('#myFam2').modal('hide');
            window.location.href = "/family/" + headVue.fid;
            //alert('1');
        }
    });
}



/* function create2(event) {
    event.preventDefault();
    $.ajax({
        cache: true,
        type: "POST",
        url:"/createf",
        data:$('#createf').serialize(),// 你的formid
        error: function(request) {
            alert("Connection error");
        },
        success: function (data) {
            //alert(data);
            app4.personlist = (JSON.parse(data))[1];
            app4.value1 = (JSON.parse(data))[0];
            $('#myFam').modal('hide');
            $('#myFam2').modal('show');           
            //alert('1');
        }
    });
} */

/* var app4 = new Vue({
    el: "#familyinfo",
    delimiters: ['${', '}'],
    data: {
        personlist: {},
        value1:{}
    },
    set: function (value) {
        this.personlist = value
    }
}) */


/* 
var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data() {
        return {
            imageUrl: '',
            loading: '',
            op: {
                tmpf:Math.random()
            }
           
        };
    },
    methods: {
        handleAvatarSuccess(res, file) {
            //this.imageUrl = URL.createObjectURL(file.raw);
            $.post('/', {
                cmd: 'create',
                tmpf: this.op.tmpf
            },
            function (data, status) {
                //alert("Data: " + data + "\nStatus: " + status);
                headVue.piclist = JSON.parse(data);
                //alert(app3.piclist);
                $('#myFam').modal('show');
                $('#myModal').modal('hide');
                loading.close();
            }
            );
     
            
        },
        handleUploadSuccess(res, file) {
            //this.imageUrl = URL.createObjectURL(file.raw);
            var r=document.getElementById("app");
            var familyid = r.getAttribute("name");
            alert(2);
            $.post('/', {
                cmd: 'Add',
                tmpf: this.op.tmpf,
                family: familyid
            },
            function (data, status) {
                
                //alert("Data: " + data + "\nStatus: " + status);
                //alert(data);
                headVue.piclist = (JSON.parse(data))['pic'];
                //alert(app3.piclist);
                $('#myFam').modal('show');
                $('#myModal').modal('hide');
                loading.close();
            }
            );
     
            
        },
        beforeAvatarUpload(file) {
            //var r=document.getElementById("app");
            //this.of.tmpf = r.getAttribute("name");
            //const isJPG = file.type === 'image/jpeg';
            const isLt2M = file.size / 1024 / 1024 < 2;
            
            if (!isJPG) {
              this.$message.error('上传头像图片只能是 JPG/png 格式!');
            }
            
            if (!isLt2M) {
              this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            
            loading = this.$loading({
                lock: true,
                text: 'uploading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            return isLt2M;
        },
        handleError(err){
            console.log(err);
            loading.close();
            alert("fail");
        },
        imageProc: function (event) {   
            
            
        }
    }

})  */