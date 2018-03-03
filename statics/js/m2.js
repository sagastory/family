var myfamily = new Vue({
    el: "#myfamily",
    delimiters: ['${', '}'],
    data: {
        familyid: $('#familyid').val(),
        mesgs: {},
        events: {},
        ablums: {}
    },
    methods: {
        init: function () {
            //alert(this.familyid);
            //get familydata
            $.post('/family', {
                    fid: this.familyid,
                    cmd: "getmesgs"
                },
                function (data, status) {
                    //alert("Data: " + data + "\nStatus: " + status);

                    myfamily.mesgs = JSON.parse(data);

                }
            );
        },
        getevents: function () {
            $.post('/family', {
                    fid: this.familyid,
                    cmd: "getevents"
                },
                function (data, status) {
                    //alert("Data: " + data + "\nStatus: " + status);

                    myfamily.events = JSON.parse(data);

                }
            );
        },
        getpics: function () {
            $.post('/family', {
                    fid: this.familyid,
                    cmd: "getpics"
                },
                function (data, status) {
                    //alert("Data: " + data + "\nStatus: " + status);
                    //alert(data);
                    myfamily.ablums = JSON.parse(data);
                    //myfamily.ablums.sort();
                    //load_image();
                }
            );
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

                    myfamily.mesgs.forEach(function (msg) {
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
        },
        hidecomment: function (id1) {
            // alert(id1);
            $('#' + id1).toggle();
        }

    }
})

var plistVue = new Vue({
    el: ".user-friends",
    delimiters: ['${', '}'],
    data: {
        familyid: $('#familyid').val(),
        plist:[]
    },
    methods: {
        getpersons: function () {
            $.post('/family', {
                fid: this.familyid,
                cmd: "getpersons"
            },
            function (data, status) {
                //alert("Data: " + data + "\nStatus: " + status);
                //alert(data);
                plistVue.plist = JSON.parse(data);
                //myfamily.ablums.sort();
                //load_image();
            }
        );
        }
    }
})

myfamily.init();
plistVue.getpersons();

var tabhead = new Vue({
    el: "#tabmenu",
    methods: {
        init: function () {
            myfamily.init();
        },
        getevents: function () {
            myfamily.getevents()
        },
        getpics: function () {
            myfamily.getpics();

        }
    }
})


var eventid = "";

function guid() {
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}

$('#writeMesg').on('shown.bs.modal', function () {
    eventid = guid();
})
/*   
$('#myModal').on('shown.bs.modal', function () {
    eventid = guid();
}) */

$('#myFam').on('shown.bs.modal', function () {
    //alert(1);
    personVue.getfperson();
})

$('#myFam2').on('shown.bs.modal', function () {
    //alert(1);
    $('.datetimepicker').datetimepicker(
        {
        format: 'yyyy-mm-dd',
        autoclose: true,
        minView: 2,
        language: 'zh-CN'
    });
})

//var Dropzone = require("dropzone");



addDropzone.on("sending", function (file, xhr, data) {
    data.append("cmd", "add");
    //data.append("evid", eventid);
    data.append("fid", $('#familyid').val());
})

var myDropzone = new Dropzone("#myDropzone", {
    url: "/writemsg",
    method: 'post',
    maxFilesize: 2, // MB
    maxFiles: 6,
    autoProcessQueue: true,
    previewsContainer: "#preview",
    addRemoveLinks: true,
    dictRemoveFile: "移除",
    dictMaxFilesExceeded: "一次最大上传6个文件",
    dictCancelUpload: "/removeimg",
    success: function (file, response, e) {
        /*var res = JSON.parse(response);
        if (res.error) {
            $(file.previewTemplate).children('.dz-error-mark').css('opacity', '1')
        }*/
    }
});


myDropzone.on("sending", function (file, xhr, data) {
    data.append("evid", eventid);
    data.append("fid", $('#familyid').val());
})

myDropzone.on("maxfilesexceeded", function (file) {
    //document.getElementById("addpic").display="none";
    myDropzone.removeFile(file);
    document.getElementById("wmsg").innerHTML = "<i>已达到最大张数</i>";
    //myDropzone.disable();
})


function doupload() {
    $.post('/writetxt', {
            txt: $('#textarea').val(),
            mid: eventid,
            fid: $('#familyid').val()
        },
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
            //alert(data);

            eventid = "";
            $('#writeMesg').modal('hide');
            myfamily.init();
            //success_prompt("!");
            toastr.success("上传成功!");

        }
    );
}

function addmemberfinish(event) {
    event.preventDefault();
    $.ajax({
        cache: true,
        type: "POST",
        url: "/addfinish",
        data: $('#memberinfo').serialize(), // 你的formid
        error: function (request) {
            //fail_prompt("");
            toastr.error("网络错误!");
        },
        success: function (data) {
            //alert(data);

            $('#myFam2').modal('hide');
            myfamily.init();
            plistVue.getpersons();
            //success_prompt("成功!");
            toastr.success("添加成员成功!");
            //alert('1');
        }
    });
}

// init Masonry
/* var msnry = new Masonry('.grid', {
    // options
    itemSelector: '.grid-item',

    animate: true,

}); */

/* function load_image() {
    var cparent = document.getElementById("container");
    for (var i = 0; i < myfamily.ablums.length; i++) {
        var ccontent = document.createElement('div');
        ccontent.className = 'grid-item';
        cparent.appendChild(ccontent);

        var img = document.createElement("img");
        //img.style.cssText = 'opacity: 0; transform:scale(0)';
        img.src = "/static/pic/" + myfamily.ablums[i][1] + "/ablum/"+myfamily.ablums[i][2];
        ccontent.appendChild(img);
        
    }

    console.log(cparent.children);

    imagesLoaded(document.querySelector('.grid'), function (instance) {
        console.log('all images are loaded');

        //msnry.layout();
        console.log("ok");
    });
} */