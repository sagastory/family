function loading() {
    $('.black_overlay').show();
};

function unloading() {
    $('.black_overlay').hide();
};

function showrela() {
    $.get('/getrela',
        function (data, status) {
            //alert("Data: " + data + "\nStatus: " + status);
            //alert(data);
            var revalue = JSON.parse(data);
            var nodes = revalue[0];
            var edges = revalue[1];

            var container = document.getElementById('family-rela');
            var data = {
                nodes: nodes,
                edges: edges
            };
            var options = {};


            var network = new vis.Network(container, data, options);

            network.on("click", function (params) {
                //alert(params.nodes);
                params.event = "[original event]";
                window.location.href = '/person/' + params.nodes;
                console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
            });

        }
    );

}

var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data() {
        return {
            e3: 0,
            e31: true,
            drawer: null,
            snackbar: false,
            color: 'info',
            infotext: '',
            dialog: false,
            dialog2: false,
            dialog3: false,
            dialog4: false,
            stepone: false,
            steptwo: false,
            timeout: 2000,
            tab: "tab-2",
            dates: [],
            menus: [],
            membername: '',
            addDropzone: '',
            piclist: [],
            memberlist: [],
            mesgs: {},
            radios: '',
            fid: '',
            fphoto: '',
            member: [
                [0, '我', 'teal', '', ''],
                [1, '爱人', 'purple', '', ''],
                [2, '儿子', 'teal', '', ''],
                [3, '女儿', 'purple', '', '']
            ],
            items: [{
                    title: 'Home',
                    icon: 'dashboard'
                },
                {
                    title: 'About',
                    icon: 'question_answer'
                }
            ]
        }
    },
    methods: {
        init: function () {
            $.ajax({
                url: '/',
                type: 'PUT',
                success: function (data) {
                    // Do something with the result
                    //alert(1);
                    app.mesgs = JSON.parse(data);
                }
            });
        },
        createfinish: function () {
            this.dialog4 = false;
            $.ajax({
                cache: true,
                type: "POST",
                url: "/create",
                data: $('#memberinfo').serialize(), // 你的formid
                error: function (request) {
                    //fail_prompt("Connection error");
                    app.infotext = "网络错误!";
                    app.color = "error";
                    app.snackbar = true;
                },
                success: function (data) {
                    //alert(data);
                    app.infotext = "创建成功!";
                    app.color = "success";
                    app.snackbar = true;
                    //$('#myFam2').modal('hide');
                    window.location.href = "/family/" + app.fid;
                    //alert('1');
                }
            });


        },
        save: function (index, date) {
            //console.log('save');
            //console.log(index);
            //console.log(this.$refs.menu);
            this.$refs.menu[index].save(date);
            //console.log(this.$el.querySelector(selector));
            //var selector = '[name=date-'+index+']';
            //this.$el.querySelector(selector).save(date);

        },
        addmember: function () {
            if (!this.membername) {
                return;
            }
            this.dialog3 = false;
            this.member.push(['0', this.membername, '', '', '']);
        },
        showthis: function () {
            this.dialog = true;
            this.stepone = false;

            if (!this.addDropzone) {
                Dropzone.autoDiscover = false;
                this.addDropzone = new Dropzone("#addmember", {
                    url: "/addmember",
                    method: 'post',
                    maxFilesize: 10, // MB
                    timeout: 50000,
                    maxFiles: 1,
                    autoProcessQueue: true,
                    clickable: ".fileinput-button",
                    previewTemplate: '<div class="dz-preview dz-file-preview"><span class="preview"><img data-dz-thumbnail /></span></div>',
                    success: function (file, data, e) {
                        //addDropzone.disable();
                        //eventid = "";

                        unloading();
                        //alert(data);

                        //addDropzone.disable();
                        var revalue = JSON.parse(data);
                        if (revalue['status'] == 'success') {
                            app.piclist = revalue['pic'];
                            app.fid = revalue['fid'];
                            app.fphoto = revalue['fphoto'];
                            // toastr.success("上传成功!");
                            app.infotext = "上传成功!";
                            app.color = "success";
                            app.snackbar = true;
                            app.stepone = true;
                            app.addDropzone.disable();

                            //setTimeout(app.showdialog2(), 2000);
                            //enabletouch();
                            //app.showdialog2();
                        } else {
                            //toastr.error("网络异常!");
                            app.infotext = "网络异常!";
                            app.color = "error";
                            app.snackbar = true;
                            app.addDropzone.removeFile(file);
                        }

                        //$('#myModal').modal('hide');
                        //myfamily.init();


                    },
                    transformFile: function (file, done) {

                        loading();

                        var reader = new FileReader();

                        reader.onload = function () {
                            var img = new Image();

                            img.onload = function () {
                                console.log("begin compress and rotate");
                                var cvs = document.createElement('canvas');
                                var width = img.naturalWidth;
                                var height = img.naturalHeight;
                                cvs.width = width;
                                cvs.height = height;
                                var ctx = cvs.getContext("2d");

                                //console.log(zipImg);
                                EXIF.getData(img, function () {
                                    var orientation = EXIF.getTag(this,
                                        'Orientation');
                                    // orientation = 6;//测试数据
                                    console.log('orientation:' +
                                        orientation);
                                    switch (orientation) {
                                        //正常状态
                                        case 1:
                                            console.log('旋转0°');
                                            // canvas.height = height;
                                            // canvas.width = width;
                                            break;
                                            //旋转90度
                                        case 6:
                                            console.log('旋转90°');
                                            cvs.height = width;
                                            cvs.width = height;
                                            ctx.rotate(Math.PI / 2);
                                            ctx.translate(0, -height);

                                            break;
                                            //旋转180°
                                        case 3:
                                            console.log('旋转180°');
                                            cvs.height = height;
                                            cvs.width = width;
                                            ctx.rotate(Math.PI);
                                            ctx.translate(-width, -
                                                height);

                                            break;
                                            //旋转270°
                                        case 8:
                                            console.log('旋转270°');
                                            cvs.height = width;
                                            cvs.width = height;
                                            ctx.rotate(-Math.PI / 2);
                                            ctx.translate(-height, 0);

                                            break;
                                            //undefined时不旋转
                                        case undefined:
                                            console.log(
                                                'undefined  不旋转');
                                            break;
                                    }
                                });

                                ctx.drawImage(img, 0, 0);

                                var zipImg;

                                if (file.size < 2048 * 1000) {
                                    console.log("<2M");
                                    zipImg = cvs.toDataURL("image/jpeg", 1);
                                } else {
                                    console.log("bigen compress");
                                    zipImg = cvs.toDataURL("image/jpeg", 70 /
                                        100);
                                }


                                return done(Dropzone.dataURItoBlob(zipImg));

                            }
                            img.src = reader.result;

                        }

                        reader.readAsDataURL(file);
                    }
                });
                this.addDropzone.on("sending", function (file, xhr, data) {
                    //loading();
                    data.append("cmd", "create");
                    //data.append("evid", eventid);
                    //data.append("fid",$('#familyid').val());
                })

                this.addDropzone.on("error", function (file, errorMessage) {
                    //document.getElementById("addpic").display="none";
                    app.addDropzone.removeFile(file);
                    //toastr.error(errorMessage);
                    app.infotext = errorMessage;
                    app.color = "error";
                    app.snackbar = true;
                    unloading();
                    //myDropzone.disable();
                });
            } else {
                this.addDropzone.enable();
                this.addDropzone.removeAllFiles();
            }

            //
        },
        showdialog2: function () {

            console.log("showdialog2...");
            this.dialog = false;
            this.dialog2 = true;
            this.steptwo = false;
            var $wrapper = $('.dragable');
            //alert(1);
            console.log($wrapper);

            $wrapper
                .touch({

                    // Turn on document tracking for smoother dragging.
                    trackDocument: true,

                    // Set drag threshold to zero for maximum drag sensitivity.
                    dragThreshold: 0,

                    // Set drag delay to zero for fastest drag response.
                    dragDelay: 0,

                    // Turn on drop filter (true = limit to siblings of item being dragged).
                    dropFilter: false,

                    // Delegate touch events to items.
                    delegateSelector: '.img-circle',

                    // Lower tap and hold delay.
                    tapAndHoldDelay: 250,

                    useMouse: true,

                    // Prevent default events for drag events. Ordinarily this takes a boolean value, but in the case
                    // of this demo we're doing the following to prevent:
                    //
                    // - If we're *not* on a mobile device, always prevent default drag events.
                    // - If we *are* on a mobile device, only prevent default drag events when we're in a "tap and hold" gesture.
                    preventDefault: {
                        drag: true,
                        swipe: true
                    }

                })
                .on('dragStart', function (e, o) {
                    // Stop propagation.
                    e.stopPropagation();
                    console.log('dragStart');

                    var $this = $(this);


                    $this
                        .css('width', $this.outerWidth())
                        .css('height', $this.outerHeight())
                        .addClass('is-dragging')
                        .css('position', 'fixed')
                        .css('top', (o.y - o.event.target.offsetHeight / 2) + 'px')
                        .css('left', (o.x - o.event.target.offsetWeight / 2) + 'px');

                    //$placeholder
                    //   .insertBefore($this);
                })
                .on('drag', function (e, o) {
                    console.log('drag');
                    //console.log(e);
                    var $this = $(this);

                    $this
                        .css('top', (o.y - e.target.offsetHeight / 2) + 'px')
                        .css('left', (o.x - e.target.offsetHeight / 2) + 'px');

                })
                .on('dragEnd', function (e, o) {

                    // Stop propagation.
                    e.stopPropagation();

                    // Vars.
                    var $this = $(this);

                    // Reset drag element.
                    $this
                        .removeClass('is-dragging')
                        .css('width', '')
                        .css('height', '')
                        .css('position', '')
                        .css('top', '')
                        .css('left', '');

                })
                .on('drop', function (e, o) {

                    console.log('drop');
                    //console.log(e);
                    //console.log(o);

                    if (!$(o.element).attr("droptarget")) {
                        //console.log("out");
                        return;
                    }

                    e.stopPropagation();

                    // Vars.
                    var $this = $(this);

                    // Unmark as drop target.
                    var id = e.target.id;
                    var src = $(e.target).attr("src");

                    $(o.element).attr("src", src);

                    $(e.target).detach();

                    app.steptwo = true;

                    var pid = $(o.element).attr("pid");
                    var relationname = $(o.element).attr("name");
                    var pname = $(o.element).attr("pname");
                    var birthday = $(o.element).attr("birthday");

                    app.memberlist.push([pid, relationname, src, pname, birthday]);


                })
            console.log("show end");
        }
    }
});

app.init();