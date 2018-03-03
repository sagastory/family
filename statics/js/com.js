var personVue = new Vue({
    el: '#personlist',
    delimiters: ['${', '}'],
    data: {
        member: [
            [0,'我','/static/pic/man.png','',''],
            [1, '爱人','/static/pic/man.png','',''],
            [2, '儿子','/static/pic/man.png','',''],
            [3, '女儿','/static/pic/man.png','',''],
            [4, '爸爸','/static/pic/man.png','',''],
            [5, '妈妈','/static/pic/man.png','','']
        ]
    },
    methods: {
        getfperson: function () {
            //alert(2);
            $.post('/family', {
                cmd:"getpersons",
                fid:$('#familyid').val()
            },
            function (data, status) {
                //alert("Data: " + data + "\nStatus: " + status);
                //alert(data);
                var revalue = JSON.parse(data);

                personVue.member = revalue;
                //personVue.num = revalue.length;


            }
            );
        }
    },
    components: {
        'person-list': {
            props: ['layer'],
            template: '<ul class="slide-box"><li v-for="(value,index) in layer" class="slide-item"><img :src="value[2]" :oldsrc="value[2]" class="img-circle" :pid="value[0]" :id="index" :name="value[1]" :pname="value[3]" :birthday="value[4]" style="height:60px;width:60px;margin-bottom: 5px;" ondragstart="dostart(event,false)" ondragover="event.preventDefault()" ondrop="dodrop(event)"><span style="position:relative; top:-20px;left:-5px">{{value[1]}}</span></li><li class="slide-item" onclick="additem()"><i class="fa fa-plus fa-3x"></i></li></ul>'
        }
        
    }
})

var memberVue = new Vue({
    el: '#myFam2',
    delimiters: ['${', '}'],
    data: { 
        memberlist: []
    }
})

function additem() {
    var name = prompt("请输入家庭关系", "");
    if (name) {
        //personVue.newitem = name;
        personVue.member.push([ '0', name,'/static/pic/man.png','' ]);
    }
    
}

function dostart(event,beremove) {
    event.dataTransfer.setData("iID", event.target.id);
    event.dataTransfer.setData("src", event.target.getAttribute("src"));
    event.dataTransfer.setData("removeself", beremove);
    //event.target.setAttribute("src","static/pic/man.png")
}

function dodrop(event) {
    //event.preventDefault();
    var id = event.dataTransfer.getData("iID");
    var src = event.dataTransfer.getData("src");
    var removeself = event.dataTransfer.getData("removeself");

    event.target.setAttribute("src", src);

    var pid = event.target.getAttribute("pid");
    var relationname = event.target.getAttribute("name");
    var pname = event.target.getAttribute("pname");
    var birthday = event.target.getAttribute("birthday");
    memberVue.memberlist.push([pid, relationname, src,pname,birthday]);

    var p = document.getElementById(id); //根据id值找到相关的元素  
    //var f = document.getElementById("createf"); //提交表单

    if (removeself == "true") {
        p.parentNode.removeChild(p);  //从父元素中删除子节点
    }
    else {
        var oldsrc = p.getAttribute("oldsrc");
        p.setAttribute("src", oldsrc);

        var name = p.getAttribute("name");

        for (var i = 0; i < memberVue.memberlist.length; i++){
            if (memberVue.memberlist[i][1] == name) {
                memberVue.memberlist.splice(i, 1);
            }
        }

        /* if (memberVue.memberlist[id]) {
            //alert(1);
            delete memberVue.memberlist[id];

        } */  

    }


}

Dropzone.autoDiscover = false;
var addDropzone = new Dropzone("#addmember", {
    url: "/addmember",
    method: 'post',
    maxFilesize: 5, // MB
    maxFiles: 1,
    autoProcessQueue: true,
    success: function (file, data, e) {
        //addDropzone.disable();
        //eventid = "";
        //alert(data);
        unloading();
        var revalue = JSON.parse(data);
        if (revalue['status'] == 'success') {
            headVue.piclist = revalue['pic'];
            headVue.fid = revalue['fid'];
            headVue.fphoto=revalue['fphoto'];
            $('#myModal').modal('hide');
            $('#myFam').modal('show');
        }
        else {
            alert('网络异常，请稍后再试');
            $('#myModal').modal('hide');
        } 
        addDropzone.removeFiles();
        //$('#myModal').modal('hide');
        //myfamily.init();
        
    }
});

addDropzone.on("maxfilesexceeded", function (file) {
    //document.getElementById("addpic").display="none";
    addDropzone.removeFile(file);
    document.getElementById("emsg").innerHTML = "<i>只能上传单张</i>";
    //myDropzone.disable();
})

addDropzone.on("sending", function (file) {
    //document.getElementById("addpic").display="none";
    loading();
    //myDropzone.disable();
})

var headVue = new Vue({
    el: "#headlist",
    delimiters: ['${', '}'],
    data: {
        piclist: '',
        fid: '',
        fphoto:''
    },
    set: function (value) {
        this.piclist = value
    }
})

function addmembernextstep() {
    $('#myFam').modal('hide');
    $('#myFam2').modal('show');   
}


