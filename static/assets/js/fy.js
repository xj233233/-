let script =
    $(function () {
        //获取上一页html传递过来的id信息
        var search = location.search;
        var cid = search.split("=")[1];

        //调用异步交互方法
        load();
    });

//创建异步交互方法,currentPage:当前第几页；pageSize：每页展示的数据记录数（10条记录）
function load(currentPage, pageSize) {
    $.post("category/findByPage",{currentPage:currentPage,pageSize:pageSize},function (pb) {
        var str="";
        //添加每页要展示的信息
        for(var x=0;x<pb.pageSize;x++){
            var s="<li style='height: 200px'>\n" +
                "<div class=\"img\"><img style='width: 300px;height: 200px' src=\" "+pb.list[x].rimage+"\" alt=\"\"></div>\n" +
                "<div class=\"text1\">\n" +
                "<p>"+pb.list[x].rname+"</p>\n" +
                "<br/>\n" +
                "<p>"+pb.list[x].routeIntroduce+"</p>\n" +
                "</div>\n" +
                "<div class=\"price\">\n" +
                "<p class=\"price_num\">\n" +
                "<span>&yen;</span>\n" +
                "<span>"+pb.list[x].price+"</span>\n" +
                "<span>起</span>\n" +
                "</p>\n" +
                "<p><a href=\"route_detail.html\">查看详情</a></p>\n" +
                "</div>\n" +
                "</li>";

            str +=s;

        }

        //添加分页功能
        var lis="";
        lis += "<li><a href=\"route_list.html?currentPage=1&pageSize="+pb.pageSize+"\">首页</a></li>";
        lis += '<li style="width: 60px"><a href="javascript:load('+(pb.currentPage-1)+','+pb.pageSize+')">上一页</a></li>';
        //前5后4共10个
        var begin;
        var end;
        //每次展示10个分页，前5后4，不够就补
        for(var x=0;x<pb.pageSize;x++){
            if(pb.currentPage<7){
                var li="<li><a href=\"javascript:load("+(x+1)+","+pb.pageSize+")\">"+(x+1)+"</a></li>";
            }else if(pb.currentPage >= 7 && pb.currentPage <= (pb.toalPage-4)){
                var li="<li><a href=\"javascript:load("+(pb.currentPage-5+x)+","+pb.pageSize+")\">"+(pb.currentPage-5+x)+"</a></li>";
            }else{
                var li="<li><a href=\"javascript:load("+(pb.toalPage-9+x)+","+pb.pageSize+")\">"+(pb.toalPage-9+x)+"</a></li>";
            }

            lis +=li;
        }

        lis += '<li style="width: 60px"><a href="javascript:load('+(pb.currentPage+1)+','+pb.pageSize+')">下一页</a></li>';
        lis += '<li style="width: 60px"><a href="javascript:load('+pb.toalPage+','+pb.pageSize+')">末页</a></li>';

        //把str,lis写进HTML
        $("#ul").html(str);
        $("#pageNum").html(lis);
        $("#toalPage").html(pb.toalPage);
        $("#totalCurrent").html(pb.totalCurrent);
    });
}
;
