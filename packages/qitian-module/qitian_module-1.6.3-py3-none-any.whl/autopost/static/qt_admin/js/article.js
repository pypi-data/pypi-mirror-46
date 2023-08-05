layui.use('upload', function () {
    var $ = layui.jquery
        , upload = layui.upload;

    //拖拽上传
    upload.render({
        elem: '#upload_docx'
        , url: '/autopost/convert_docx/'
        , accept: 'file'
        , exts: 'docx' //只允许上传docx
        , done: function (res) {
            if(res.code == 200){
                let ue = UE.getEditor("content",{zIndex: 100});
                ue.setContent(res.data);
            }
        }
    });

});