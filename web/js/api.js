function randomColors(total) {
    var colors = [];
    for(var i = 0; i < total; i++) {
        let r = Math.floor(Math.random() * 255),
            g = Math.floor(Math.random() * 255),
            b = Math.floor(Math.random() * 255)
        colors.push(`rgba(${r}, ${g}, ${b}, 1.0)`);
    }
    return colors;
}

var MyItems = {
    start: function() {
        let container = $('#ItemsContainer');
        for(let j = 0; j < Data.count; j++) {
            container.append($(`<div class="item-header" style="padding: 5px 10px; border: 2px solid ${Data.colors[j]}; border-radius: 10px"><span>Cluster-${j}<span></div>`));
            for(let i = 0; i < Data.xyDots.length; i++) {
                if (Data.another[i] == j) {
                    let item = $(`<div class="item"><span>${Data.unique[i]}<span></div>`);
                    container.append(item);
                }
            }
            
        }
    }
}

var API = {
    baseDataAnalyze: function() {
        var fileData = $("#SourceFileInput").prop('files')[0];   
        var uploadingData = new FormData();
        uploadingData.append('data_file', fileData);
        $.ajax({
            url: '/api/base_data_analyze',
            dataType: 'text',
            cache: false,
            contentType: false,
            processData: false,
            data: uploadingData,                         
            type: 'post',
            success: function(data){
                console.log(data);
                try {
                    data = JSON.parse(data);
                    console.log(data);
                    Data.xyDots = data[0];
                    Data.another = data[1];
                    Data.count = data[2];
                    Data.unique = data[3];
                    Data.colors = randomColors(Data.count);
                    MyChart.draw();
                    MyItems.start()
                    Index.switchBlock("AnalyzeSystemResult");
                } catch(err) {
                    console.log(err);
                    Index.switchBlock("AnalyzeError");
                }
            }
        });
    }
}